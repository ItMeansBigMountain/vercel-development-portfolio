# News Webcrawler App

This project is a web crawler that gathers news articles from various sources and compiles them into a tailored morning newsletter. The application focuses on providing relevant news based on user preferences, including hyper-localized content.

## Features

- Crawls news from selected areas and sources.
- Provides news reports of top trending stories.
- Includes links to original articles.
- Offers hyper-localized news with 1-4 paragraphs of data for each selected town.
- Leverages existing services such as Reddit and Nextdoor.
- Aims to provide a balanced view of local and global news.
- Generates a morning newsletter for easy consumption.

## Project Structure

```
news-webcrawler-app
├── src
│   ├── crawler
│   │   └── index.py          # Main logic for the web crawler
│   ├── services
│   │   ├── reddit.py         # Functions to interact with the Reddit API
│   │   ├── nextdoor.py       # Functions to interact with the Nextdoor API
│   │   └── ...               # Additional services can be added here
│   ├── newsletter
│   │   └── generator.py      # Responsible for generating the morning newsletter
│   ├── main.py               # Entry point for the application
│   └── utils
│       └── helpers.py        # Utility functions for various tasks
├── requirements.txt           # Lists the dependencies required for the project
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd news-webcrawler-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Configure your preferences for news sources and areas in the `main.py` file.
- The application will fetch and compile news articles based on your settings.
- Check the generated newsletter for your tailored news updates.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.