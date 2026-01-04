import pytest
from main import scrape_web, count_words


def test_scrape_web():
    """Test the scrape_web MCP tool with a GitHub repository URL."""

    url = "https://github.com/alexeygrigorev/minsearch"
    
    content = scrape_web.fn(url)
    
    assert content is not None
    assert isinstance(content, str)
    
    content_length = len(content)
    assert content_length > 100, f"Content should have more than 100 characters, got {content_length}"


def test_count_words():
    """Test the count_words MCP tool."""

    content = "data data Data Data"
    
    count = count_words.fn(content, "data")
    
    assert count == 4

    url = "https://datatalks.club/"
    
    content = scrape_web.fn(url)
    
    count = count_words.fn(content, "data")
    
    assert count == 61