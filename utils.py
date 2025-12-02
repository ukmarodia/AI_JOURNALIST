from urllib.parse import quote_plus
import os
import requests
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
def generate_valid_news_url(keyword: str)->str:

    """
    Generate a Google News search URL for a keyword
    Args:
        keyword: Search term to use in the news search
    returns:
        str: constructed Google news search url
    """
    q = quote_plus(keyword)
    return f"https://news.google.com/search?q={q}&tbs=sbd:1"

def scrape_with_brightdata(url: str) -> str:
    #scrape a url using brightdata
    headers = {
        "Authorization": f"Bearer{os.getenv('BRIGHT_API_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload ={
        "zone": os.getenv('WEB_UNLOCKER_ZONE'),
        "url":url,
        "format":"raw"
    }

    try:
        response = requests.post("https://api.brightdata.com/request",json = payload, headers = headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code = 500, detail = f"BrightData error:{str(e)}")


def clean_html_to_text(html_content: str) ->str:
    """Clean Html content to plain text"""
    soup = BeautifulSoup(html_content, "html.parse")
    text = soup.get_text(separator="\n")
    return text.strip()