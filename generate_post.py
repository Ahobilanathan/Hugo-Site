import os
import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def load_keywords():
    """Load keywords from keywords.txt file."""
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except FileNotFoundError:
        print("keywords.txt not found. Creating with sample keywords.")
        sample_keywords = [
            "AI Tools for Developers",
            "Machine Learning Basics",
            "Natural Language Processing",
            "Computer Vision Applications",
            "Deep Learning Frameworks"
        ]
        with open('keywords.txt', 'w') as f:
            f.write('\n'.join(sample_keywords))
        return sample_keywords

def mark_keyword_used(keyword):
    """Mark a keyword as used by moving it to used_keywords.txt."""
    with open('keywords.txt', 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]
    
    keywords.remove(keyword)
    
    with open('keywords.txt', 'w') as f:
        f.write('\n'.join(keywords))
    
    with open('used_keywords.txt', 'a') as f:
        f.write(f"{keyword}\n")

def generate_post(keyword):
    """Generate a blog post using OpenAI."""
    if not OPENAI_API_KEY:
        print("Error: OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        return None

    prompt = f"""Write a detailed blog post about {keyword}. 
    The post should be informative and valuable for readers.
    
    Include:
    1. An engaging introduction
    2. Main sections with clear explanations
    3. Practical examples and use cases
    4. Best practices and tips
    5. A conclusion with key takeaways
    
    Format the response in Markdown with proper headings and formatting.
    Keep the content focused and well-structured."""
    
    try:
        print(f"Generating post about {keyword} using OpenAI...")
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a technical writer specializing in AI and technology topics. Write clear, informative content that provides value to readers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # Set to 2000 tokens as requested
        )
        print(f"Successfully generated post about {keyword}!")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating post: {str(e)}")
        return None

def save_post(keyword, content):
    """Save the generated post as a Markdown file."""
    today = datetime.datetime.now()
    filename = f"content/posts/{today.strftime('%Y-%m-%d')}-{keyword.lower().replace(' ', '-')}.md"
    
    # Create posts directory if it doesn't exist
    Path("content/posts").mkdir(parents=True, exist_ok=True)
    
    frontmatter = f"""---
title: "{keyword}"
date: {today.strftime('%Y-%m-%dT%H:%M:%S%z')}
draft: false
description: "A detailed guide to {keyword}"
tags: ["AI", "Technology", "Tools"]
---

"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    return filename

def main():
    """Main function to generate and save a new post."""
    keywords = load_keywords()
    if not keywords:
        print("No keywords available. Please add keywords to keywords.txt")
        return
    
    # Generate one post per run
    keyword = keywords[0]  # Get the first unused keyword
    content = generate_post(keyword)
    
    if content:
        filename = save_post(keyword, content)
        mark_keyword_used(keyword)
        print(f"Successfully generated post: {filename}")
    else:
        print(f"Failed to generate post for keyword: {keyword}")

if __name__ == "__main__":
    main() 