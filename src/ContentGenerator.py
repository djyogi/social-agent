#!/usr/bin/env python

from llama_index import VectorStoreIndex, Document
from llama_index.llms import OpenAI
import openai
from pathlib import Path
from newspaper import Article
import base64

class GenContent:
    def __init__(self, src, src_type, openai_key):

        openai.api_key = openai_key
        
        #Get an article by url, return a parsed article object
        if src_type == 'article-url':
            
            print(f"\nDownloading and parsing article url: " + src + "\n")
            article = Article(src)
            article.download()
            article.parse()
            
            self.src_type = src_type
            self.src_content = article

            #Initialize the llama-index vector DB with data sources
            print(f"Indexing article: " + article.title + "\n")
            docs = [Document(text=article.title), Document(text=article.text)]
            index = VectorStoreIndex.from_documents(docs)
            query_engine = index.as_query_engine()

            self.query_engine = query_engine

    #Query w/ llama-index vector db, embeddings
    def gen_query(self, prompt):
        query_completion = self.query_engine.query(prompt)
        return query_completion.response
    
    #Generate text w/ llama-index from chatgpt 3.5
    def gen_text(self, prompt):
        text_completion = OpenAI().complete(prompt)
        return text_completion.text

    #Genereate image w/ dalle-3
    def gen_image(self, prompt, output_path):
        client = openai.OpenAI(api_key=openai.api_key)
        generate_image = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json"
        )
        
        image_b64 = generate_image.data[0].b64_json

        with open(output_path, "wb") as dalle_file:
            dalle_file.write(base64.b64decode(image_b64))
            return output_path
        
    #Generate audio
    def gen_audio(prompt=None, speech_file_path='content/speech.mp3'):
        speech_file_path = Path(__file__).parent / "content/speech.mp3"
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            speed=1.1,
            input=prompt)
        response.stream_to_file(speech_file_path)