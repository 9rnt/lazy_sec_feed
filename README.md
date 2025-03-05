# Lazy Security Feed Reader

A Python-based RSS feed reader that aggregates security-related feeds and provides AI-powered summaries using Google's Gemini API. This tool helps security professionals stay updated with the latest security news and vulnerabilities by automatically collecting and summarizing content from various security-focused RSS feeds.

## Features

- Aggregates security feeds from multiple trusted sources:
  - AWS Security Bulletins and Blogs
  - SANS ISC Storm Center
  - Graham Cluley's Security Blog
  - Krebs on Security
  - Bruce Schneier's Blog
  - Kaspersky's Securelist
  - The Hacker News
- Filters entries by date
- Generates concise AI-powered summaries of security updates
- Configurable feed sources through YAML configuration
- Easy to add new feed sources

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lazy_sec_feed.git
cd lazy_sec_feed
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

## Configuration

The `feeds.config` file contains the configuration for all RSS feeds. You can add, remove, or modify feeds as needed:

```yaml
rss:
    aws:
        blogs:
            feed: 'https://aws.amazon.com/blogs/security/feed/'
            enabled: true
            read_content: true
        bulletins:
            feed: 'https://aws.amazon.com/security/security-bulletins/rss/feed/'
            enabled: true
            read_content: true
    sans:
        storm_center:
            feed: 'https://isc.sans.edu/rssfeed.xml'
            enabled: true
    # ... other feeds ...
```

Each feed configuration can have the following options:
- `feed`: The RSS feed URL
- `enabled`: Whether to include this feed (true/false)
- `read_content`: Whether to include the full content in summaries (true/false)

## Usage

Run the script to fetch and summarize security updates:

```bash
python main.py
```

By default, the script will:
1. Fetch entries from all enabled feeds
2. Filter entries for the current date
3. Generate a concise summary using Gemini AI
4. Display both individual entries and the AI summary

To fetch entries for a specific date, modify the date in the `main.py` file:
```python
entries = read_rss_feed(feed_url, '2025-03-04')  # Change the date as needed
```

## Output

The script provides two types of output:
1. Individual entries from each feed, showing:
   - Title
   - Link
   - Publication date
   - Summary
   - Content (if enabled)

2. An AI-generated summary that:
   - Focuses on high-risk vulnerabilities
   - Highlights important security updates
   - Provides concise, actionable information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for providing the AI summarization capabilities
- All the security feed providers for their valuable content