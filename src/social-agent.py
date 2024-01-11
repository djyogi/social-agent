#!/usr/bin/env python

from ContentGenerator import GenContent
from IGPost import IGPost
import argparse
import configparser

if __name__ == "__main__":

    #Load config
    settings = configparser.ConfigParser()
    settings.read('settings.cfg')
    openai_key = settings.get('OPENAI_API', 'openai_key')
    
    #Setup CLI
    argparser = argparse.ArgumentParser(
    prog='Social Agent AI',
    description='Social content generator and publisher using AI')

    argparser.add_argument('post_type')
    argparser.add_argument('-u', '--url')
    
    args = argparser.parse_args()

    if args.post_type == 'ig-post':
        
        post_content = GenContent(args.url, 'article-url', openai_key)
        new_post = IGPost(post_content)

        new_post.gen_caption()
        new_post.gen_headline()
        new_post.gen_src_image()
        new_post.apply_style('text-overlay-1')

        publish_ans = input(f"IG Post created: (" + new_post.post_image + "), OK to publish? [Y/n]\n")

        if publish_ans == '':
            #Get IG login from settings
            ig_username = settings.get('IG_ACCOUNT', 'ig_username')
            ig_password = settings.get('IG_ACCOUNT', 'ig_password')
            ig_login = [ig_username, ig_password]

            new_post.publish_post(ig_login)
        else:
            exit()

    
    


