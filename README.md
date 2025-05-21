# AI-Powered Content Generator

This is an automated content generation system that creates SEO-optimized blog posts using AI. The system runs daily using GitHub Actions and publishes content to a Hugo-based static site.

## Features

- Automated daily content generation using OpenAI GPT-4
- SEO-optimized blog posts
- GitHub Actions workflow for automated publishing
- Hugo static site generation
- GitHub Pages hosting

## Setup

1. Install Hugo:
   ```bash
   # Windows (using Chocolatey)
   choco install hugo-extended
   
   # macOS
   brew install hugo
   
   # Linux
   sudo apt-get install hugo
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-tools-hugo-site.git
   cd ai-tools-hugo-site
   ```

3. Install the Ananke theme:
   ```bash
   git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

5. Add your OpenAI API key to GitHub Secrets:
   - Go to your repository settings
   - Navigate to Secrets and Variables > Actions
   - Add a new secret named `OPENAI_API_KEY` with your API key

6. Add your keywords:
   - Edit `keywords.txt` to add your target keywords
   - One keyword per line

## Local Development

1. Start the Hugo server:
   ```bash
   hugo server -D
   ```

2. Test the post generator:
   ```bash
   python content/generate_post.py
   ```

## Deployment

The site is automatically deployed to GitHub Pages when new content is generated. The GitHub Actions workflow runs daily at 6:00 UTC.

## Customization

- Edit `config.toml` to modify site settings
- Modify the prompt in `generate_post.py` to change the content style
- Add or modify keywords in `keywords.txt`

## License

MIT License 