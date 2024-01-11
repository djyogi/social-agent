#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client as igclient
import os

class IGPost:
    def __init__(self, content):
        self.content = content
        self.caption = ''
        self.headline = ''
        self.src_image = ''
        self.post_image = ''
    
    def gen_caption(self, prompt=''):
        if prompt == '':
            prompt = """Summarize this article in a concise, but informative way to produce 
            a detailed caption for a tiktok or instagram post and include relevant emoji's 
            and hashtags with the intention of reaching a wide audience."""
        
        self.caption = self.content.gen_query(prompt=prompt)
        print(f"Generated caption: " + self.caption + "\n")
    
    def gen_headline(self, prompt=''):
        if prompt == '':
            prompt = "Rephrase this article's title to captivate a social media audience in a professional way: " + self.content.src_content.title

        self.headline = self.content.gen_text(prompt=prompt)
        print(f"Generated headline: " + self.headline + "\n")

    def resize_image(self, input_path, output_path, size=(1080, 1080)):
        with Image.open(input_path) as image:
            # Resizing the image to the specified size
            resized_image = image.resize(size, Image.LANCZOS)
            # Saving the resized image to the specified output path
            resized_image.save(output_path)

    def gen_src_image(self, prompt='', output_path=''):
        #Use headline to generate a good dall-e prompt
        if prompt == '':
            prompt = f"Give me a good dall-e prompt to create a hero image with no text for an instagram or tiktok post that represents this headline: " + self.headline

        image_prompt = self.content.gen_text(prompt=prompt)

        if output_path == '':
            output_path = 'content/gen_image.png'

        self.src_image = self.content.gen_image(prompt=image_prompt, output_path=output_path)

        #Resize the image for instagram
        self.resize_image(input_path=self.src_image, output_path=self.src_image, size=(1080,1080))

        print("Generated image: " + self.src_image + "\n")

    #Wraps text to fit an image
    def wrap_text(self, text, max_width, font):
        lines = []
        words = text.split(' ')
        
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            line_width = font.getlength(test_line)
            if line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line[:-1])
                current_line = word + ' '
    
        lines.append(current_line[:-1])
        return lines

    def add_text_to_image_1(self, image, full_text, output_path):
        font_size = 72
        font = ImageFont.truetype('fonts/TitilliumWeb-BoldItalic.ttf', font_size)
        
        max_width = int(image.width * 0.9)
        wrapped_text = self.wrap_text(full_text, max_width, font)
        
        draw = ImageDraw.Draw(image)
        line_spacing = 1.3 
        x = (image.width - max_width) // 2
        y = (image.height - int(font_size * len(wrapped_text) * line_spacing)) // 1.1
        
        for line in wrapped_text:
            line_width = font.getlength(line)

            left, top, right, bottom = draw.textbbox(((image.width - line_width) // 2, y), line, font=font)
            draw.rectangle((left-10, top-10, right+10, bottom+10), fill="yellow")

            draw.text(((image.width - line_width) // 2, y), line, "black", font=font)

            y += int(font_size * line_spacing)
    
        # save image to disk
        image.save(output_path)
        print(f"Generated IG post: " + output_path + "\n")
        return output_path
    
    def apply_style(self, style='', output_path=''):
        if output_path == '':
            output_path = 'content/ig_post.png'

        if style == 'text-overlay-1':
            image = Image.open(self.src_image)
            #Sanitize any quotes in headline
            self.post_image = self.add_text_to_image_1(image, self.headline.replace('"',''), output_path=output_path)

    def publish_post(self, login=[]):
        new_igclient = igclient()
        new_igclient.login(login[0], login[1])

        #Convert image to jpeg for IG
        img_png = Image.open(self.post_image)
        img_png.save('content/ig_post_jpeg.jpg')

        #Post to instagram
        ig_post = new_igclient.photo_upload(
            path='content/ig_post_jpeg.jpg', 
            caption=self.caption)
        
        os.remove('content/ig_post_jpeg.jpg')