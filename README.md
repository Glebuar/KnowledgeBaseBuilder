# Knowledge Base Builder

This project scrapes specific web pages and converts the content into HTML files, organizing them into a knowledge base. The project uses Selenium for web scraping and BeautifulSoup for HTML parsing.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Google Chrome browser
- ChromeDriver

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Glebuar/KnowledgeBaseBuilder.git
    cd knowledge-base-builder
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Download ChromeDriver**:

    - Download the correct version of ChromeDriver that matches your Chrome browser from [here](https://developer.chrome.com/docs/chromedriver/downloads).
    - Place the `chromedriver` executable in a known location.

5. **Update `config.json`**:

    - Make sure the `config.json` file is present in the root directory with the correct structure and update the `chrome_driver_path` to the path where you placed the `chromedriver` executable.

    Example `config.json`:
    ```json
    {
        "chrome_driver_path": "path/to/chromedriver",
        "urls": [
            {
                "url": "https://example.com/page1",
                "children": []
            },
            {
                "url": "https://example.com/page2",
                "children": [
                    {
                        "url": "https://example.com/page2-1",
                        "children": []
                    }
                ]
            }
        ]
    }
    ```

## Running the Script

```bash
python main.py