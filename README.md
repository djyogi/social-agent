<img src="readme/sa-logo.jpeg?raw=true"/>

# Social Agent AI

> **Social Agent** is a LLM-based AI agent that allows you to transform any source content into many other forms of social media content. You can take a news or blog article and ask this agent to generate Instagram posts, reels, TikTok videos, YouTube shorts, LinkedIn posts, and more.

## Getting Started

### Requirements
- Python 3
- OpenAI API
- Instagram

### How to install
1. Download ZIP

    <img src="readme/sa-download-zip.png?raw=true"/>

    Or clone this repo:

        `$ git clone https://github.com/djyogi/social-agent.git`

2. Install dependencies

    `$ cd social-agent`

    `$ pip install -r requirements.txt`

### How to use

**1. Configure your settings in `settings.cfg`:**

`$ cd src/`

`$ cp settings.cfg.example settings.cfg`

Open `settings.cfg`
    
- Add your OpenAI API key
- Add your Instagram username and password

**2. Run the agent on your command line by specifying:**
- Content type to generate:
    - `ig-post` (Instagram post)
- URL with your source content

`$ python -m social-agent <content-type> -u <article-url>`

Example:

#### 1. Choose an article.

<img src="readme/sa-input.png?raw=true"/>

#### 2. Run social-agent and provide the article.

<img src="readme/sa-demo.gif?raw=true"/>

#### 3. Review your post in this folder: `content/ig_post.png` and press `<Enter>` to publish it.

<img src="readme/sa-example.png?raw=true"/>

## How it works (for 'ig-post')

Social Agent will:
1. Download and index your source content.
2. Generate a caption from the content for a new post.
3. Generate a headline for the new post.
4. Generate an image based on the headline.
5. Create a post with the headline overlayed on the image.
6. Publish the post (by hitting `<Enter>`)

You can review the post before publishing, it's saved to `content/ig_post.png`

## Version 0.1.0
Added support for generating Instagram posts
