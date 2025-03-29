import json


def load_config(config_path="config/config.json"):
    with open(config_path, "r") as file:
        return json.load(file)


def extract_research_papers(raw_json):
    """Extracts research papers dynamically from raw JSON data."""
    research_papers = []

    for paper in raw_json:
        research_papers.append(
            {
                "title": paper.get("title", "Unknown Title"),
                "content": paper.get("content", ""),
            }
        )

    return research_papers


def validate_news_with_research(news_data, raw_json):
    """Cross-checks news articles with research papers."""
    research_papers = extract_research_papers(raw_json)
    validated_news = []
    for article in news_data:
        for paper in research_papers:
            if any(tag.lower() in paper["content"].lower() for tag in article["tags"]):
                article["validated"] = True
                article["matched_research"] = paper["title"]
                break
        else:
            article["validated"] = False
            article["matched_research"] = "No matching research found"

        validated_news.append(article)

    return validated_news


def init():
    config = load_config()
    validated_news_path = config.get(
        "validated_news_path", "outputs/validated_news.json"
    )
    raw_news_path = config.get("raw_news_path", "outputs/raw_news.json")
    structured_news_path = config.get(
        "structured_news_path", "outputs/structured_news.json"
    )
    with open(structured_news_path, "r", encoding="utf-8") as f:
        news_data = json.load(f)

    with open(raw_news_path, "r", encoding="utf-8") as f:
        raw_json = json.load(f)
    validated_news = validate_news_with_research(news_data, raw_json)
    with open(validated_news_path, "w", encoding="utf-8") as f:
        json.dump(validated_news, f, indent=4)

    print("News validated and saved!")
    print(
        "✅ News processing complete! Run 'streamlit run ui/dashboard.py' to view results."
    )


if __name__ == "__main__":
    init()
