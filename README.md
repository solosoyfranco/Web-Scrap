# Web Portal Scraper Project

## Overview
This project includes a Scrapy spider integrated with Selenium for scraping and interacting with dynamic web pages. The purpose is to navigate a web portal, retrieve specific documents, and perform actions like clicking and printing using automated browser interactions.

## Prerequisites
Ensure you have Python installed on your system. This project requires setting up a virtual environment and installing several dependencies.

### Required Libraries
- Scrapy
- scrapy-selenium
- selenium
- pyperclip
- beautifulsoup4
- bs4

## Installation

1. **Set up a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. **Install the required libraries:**
    ```bash
    pip install Scrapy scrapy-selenium selenium pyperclip beautifulsoup4 bs4

3. **Clone the project:**
   ```bash
   git clone https://your-github-repo-link.git
    cd your-project-directory


### Configuration

Run Chrome in debugging mode to allow Selenium to control it:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
```


### Usage

Start the Scrapy project (if not already created):

```bash

scrapy startproject webportal_scraper  
```
List available spiders (to verify setup):

```bash

scrapy list
```
Run the spider:

```bash

scrapy runspider portal_spider.py
```
