from fastmcp import FastMCP
import requests


mcp = FastMCP("Demo")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def scrape_web(url: str) -> str:
    """
    Scrape content from any web page using Jina reader.
    
    Args:
        url: The URL of the web page to scrape
        
    Returns:
        The content of the web page in markdown format
    """
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

@mcp.tool
def count_words(text: str, word: str) -> int:
    """
    Count the number of times the word appears in the text. Case-insensitive.
    
    Args:
        text: The text to count a word in
        word: The word to count
        
    Returns:
        The number of times the word appears in the text
    """
    return text.lower().count(word.lower())

if __name__ == "__main__":
    mcp.run()