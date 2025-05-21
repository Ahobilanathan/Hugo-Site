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

    prompt = f"""Write a concise but informative blog post about {keyword}. 
    Keep it focused and practical. Include:
    - Brief introduction
    - 3-4 main points with examples
    - Short conclusion
    Format in Markdown with clear headings."""
    
    try:
        print("Generating post using OpenAI...")
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # Using the new nano model
            messages=[
                {"role": "system", "content": "You are a technical writer who creates concise, practical content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        print("Successfully generated post!")
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
description: "A practical guide to {keyword}"
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
    
    # Generate posts for the first 3 keywords
    for keyword in keywords[:3]:
        content = generate_post(keyword)
        if content:
            filename = save_post(keyword, content)
            mark_keyword_used(keyword)
            print(f"Successfully generated post: {filename}")
        else:
            print(f"Failed to generate post for keyword: {keyword}")

if __name__ == "__main__":
    main() 