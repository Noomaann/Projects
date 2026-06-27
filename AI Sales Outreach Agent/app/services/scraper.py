from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def get_company_info(company_name: str) -> str:
    """কোম্পানির নাম দিয়ে ইন্টারনেট থেকে তথ্য খুঁজে আনবে"""
    try:
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
        search = DuckDuckGoSearchResults(api_wrapper=wrapper)
        
        query = f"{company_name} company what they do core business"
        results = search.run(query)
        
        return results
    except Exception as e:
        return f"Could not find information for {company_name} online."