import os
import json
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

# Load API keys
load_dotenv()
TAVILY_KEY = os.getenv("TAVILY_KEY")

# Initialize Tavily Search with the API key
tool = TavilySearchResults(
    tavily_api_key=TAVILY_KEY,  # Pass the API key here
    max_results=10,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
)


def fetch_insurance_news(query):
    """
    Fetch latest insurance-related news using Tavily API.
    """
    response = tool.invoke({"query": query})
    print(response)
    return response


if __name__ == "__main__":
    news = fetch_insurance_news("Climate risk insurance impact")
    os.makedirs("outputs", exist_ok=True)  # Ensure the 'outputs' directory exists
    with open("outputs/raw_news.json", "w") as f:
        json.dump(news, f, indent=4)
    print("News fetched and saved!")
