import os
import json
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

# Load API keys
load_dotenv()


def load_config(config_path="config/config.json"):
    with open(config_path, "r") as file:
        return json.load(file)


def load_api_keys():
    """
    Load API keys from environment variables.
    """
    return os.getenv("TAVILY_API_KEY")


def initialize_tavily_search(api_key):
    """
    Initialize the Tavily search tool with the API key.
    """
    return TavilySearchResults(
        tavily_api_key=api_key,
        max_results=10,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
    )


def fetch_insurance_news(tool, query):
    """
    Fetch latest insurance-related news using Tavily API.
    """
    response = tool.invoke({"query": query})
    return response


def init():
    config = load_config()
    raw_news_path = config.get("raw_news_path", "outputs/raw_news.json")
    api_key = load_api_keys()
    if not api_key:
        raise ValueError("TAVILY_KEY is missing from environment variables.")

    tool = initialize_tavily_search(api_key)
    news = fetch_insurance_news(tool, "Climate risk insurance impact")
    os.makedirs("outputs", exist_ok=True)  # Ensure the 'outputs' directory exists
    with open(raw_news_path, "w", encoding="utf-8") as f:
        json.dump(news, f, indent=4)
    print("News fetched and saved!")


if __name__ == "__main__":
    init()
