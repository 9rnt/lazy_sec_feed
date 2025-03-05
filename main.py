import feedparser
from datetime import datetime
import yaml
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def read_rss_feed(feed_url, date=None):
    """
    Read and parse an RSS feed from the given URL.
    Returns a list of feed entries with their details.
    """
    # Parse the feed
    feed = feedparser.parse(feed_url)
    
    # Get date
    if date:
        today = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
    # Filter entries from today
    today_entries = []
    for entry in feed.entries:
        # Convert entry published date to datetime
        if hasattr(entry, 'published_parsed'):
            entry_date = datetime(*entry.published_parsed[:6]).date()
            if entry_date == today:
                today_entries.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', 'No link'),
                    'published': entry.get('published', 'No date'),
                    'summary': entry.get('summary', 'No summary'),
                    'content': entry.get('content', 'No content')
                })
    
    return today_entries

def get_config():
    """
    Read and parse the feeds.config YAML file.
    Returns a dictionary containing the feed configurations.
    """
    try:
        with open('feeds.config', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: feeds.config file not found")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {str(e)}")
        return {}

def summarize_entries(entries, api_key):
    """
    Summarize the entries using LLAMA 3.
    """
    if not entries:
        return "No entries to summarize."
    
    # Initialize LLAMA model
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {str(e)}")
        return "Error initializing Gemini client."

    # Prepare the text to summarize
    text_to_summarize = "Today's Security Updates:\n\n"
    for entry in entries:
        text_to_summarize += f"Title: {entry['title']}\n"
        text_to_summarize += f"Summary: {entry['summary']}\n"
        if entry.get('content'):
            text_to_summarize += f"Content: {entry['content']}\n"
        text_to_summarize += "-" * 80 + "\n"

    # Generate summary using LLAMA
    prompt = f"""As a security expert, please provide a concise summary under 40 per entry of these security updates, focusing on the most important points and high risks and vulnerabilities. If no provided summary or content skip the entry:

{text_to_summarize}

Summary:"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Failed to generate summary."

def main():
    # Get API key from environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please set the GEMINI_API_KEY environment variable."
        )
    # Get feed configurations
    config = get_config()
    
    # Collect all entries for summarization
    all_entries = []
    
    # Process each feed in the configuration
    for provider, feeds in config.get('rss', {}).items():
        print(f"\nProcessing {provider} feeds:")
        for feed_type, feed_config in feeds.items():
            if feed_config.get('enabled', False):
                feed_url = feed_config.get('feed')
                if feed_url:
                    try:
                        entries = read_rss_feed(feed_url)
                        
                        if not entries:
                            print(f"No entries found for {feed_type} feed.")
                            continue
                            
                        print(f"\nFound {len(entries)} entries for {feed_type}:")
                        
                        # Add entries to the collection for summarization
                        all_entries.extend(entries)
                            
                    except Exception as e:
                        print(f"Error reading {feed_type} feed: {str(e)}")
    
    # Generate summary of all entries
    if all_entries:
        print("\nGenerating summary of all entries using GEMINI...")
        summary = summarize_entries(all_entries, api_key)
        print("\nSummary:")
        print("=" * 80)
        print(summary)
        print("=" * 80)
            
if __name__ == "__main__":
    main()
