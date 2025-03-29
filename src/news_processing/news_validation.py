import json


def extract_research_papers(raw_json):
    """Extracts research papers dynamically from raw JSON data."""
    research_papers = []

    # research_papers = [
    #     {
    #         "title": "Managing Basis Risks in Parametric Insurance",
    #         "keywords": ["parametric insurance", "basis risk"],
    #     },
    #     {
    #         "title": "Data-driven Parametric Insurance Framework",
    #         "keywords": ["risk modeling", "climate insurance"],
    #     },
    # ]

    for paper in raw_json:
        research_papers.append(
            {
                "title": paper["title"],
                "content": paper["content"],
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


if __name__ == "__main__":
    with open("outputs/structured_news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)

    with open("outputs/raw_news.json", "r", encoding="utf-8") as f:
        raw_json = json.load(f)
    validated_news = validate_news_with_research(news_data, raw_json)
    with open("outputs/validated_news.json", "w", encoding="utf-8") as f:
        json.dump(validated_news, f, indent=4)

    print("News validated and saved!")
