"""
Search implementation for fastmcp documentation using minsearch.
This module indexes documentation files and provides search functionality.
"""

import zipfile
from pathlib import Path
from minsearch import Index


def load_documents_from_zip(zip_path: str) -> list[dict]:
    """
    Load markdown documents from zip file.
    
    Args:
        zip_path: Path to the zip file
        
    Returns:
        List of documents with 'content' and 'filename' fields
    """
    documents = []
    
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Get all file names in the zip
        file_list = zip_file.namelist()
        
        for file_path in file_list:
            # Only process .md and .mdx files
            if file_path.endswith(('.md', '.mdx')):
                # Read the file content
                with zip_file.open(file_path) as f:
                    content = f.read().decode('utf-8')
                
                # Remove the first part of the path (e.g., "fastmcp-main/")
                # Split by '/' and skip the first part
                path_parts = file_path.split('/', 1)
                if len(path_parts) > 1:
                    cleaned_filename = path_parts[1]
                else:
                    cleaned_filename = file_path
                
                documents.append({
                    'content': content,
                    'filename': cleaned_filename
                })
    
    return documents


def create_search_index(documents: list[dict]) -> Index:
    """
    Create and fit a minsearch index with the documents.
    
    Args:
        documents: List of documents to index
        
    Returns:
        Fitted Index object
    """
    # Create index with text fields and keyword fields
    index = Index(
        text_fields=['content', 'filename'],
        keyword_fields=[]
    )
    
    # Fit the index with documents
    index.fit(documents)
    
    return index


def search(index: Index, query: str, num_results: int = 5) -> list[dict]:
    """
    Search for documents matching the query.
    
    Args:
        index: The minsearch Index object
        query: Search query string
        num_results: Number of results to return (default: 5)
        
    Returns:
        List of matching documents
    """
    # Boost filename slightly higher than content for better matches
    boost_dict = {
        'filename': 2.0,
        'content': 1.0
    }
    
    results = index.search(
        query,
        boost_dict=boost_dict,
        num_results=num_results
    )
    
    return results


def main():
    """Main function to test the search implementation."""
    print("Loading documents from zip file...")
    # Use pathlib to get the zip file path relative to this script
    zip_path = Path(__file__).parent / "fastmcp-main.zip"
    documents = load_documents_from_zip(str(zip_path))
    
    print(f"Loaded {len(documents)} documents")
    
    # Show some sample filenames
    print("\nSample filenames:")
    for doc in documents[:5]:
        print(f"  - {doc['filename']}")
    
    print("\nCreating search index...")
    index = create_search_index(documents)
    
    # Test searches
    test_queries = [
        "getting started",
        "installation",
        "fastmcp server",
        "context",
        "demo"
    ]
    
    print("\nTesting search functionality:\n")
    for query in test_queries:
        print(f"Query: '{query}'")
        results = search(index, query, num_results=5)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['filename']}")
        print()


if __name__ == "__main__":
    main()
