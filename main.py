# # import os
# import json
# from scripts.news_scraper import fetch_insurance_news
# from scripts.news_processor import process_news
# from scripts.news_validation import validate_news_with_research

# # Step 1: Fetch news
# print("Fetching news...")
# news_data = fetch_insurance_news("Climate risk insurance impact")

# # Step 2: Process news
# print("Processing news...")
# structured_news = process_news(news_data)

# # Step 3: Validate news credibility
# print("Validating news with research...")
# validated_news = validate_news_with_research(structured_news)

# # Step 4: Save processed news
# with open("outputs/validated_news.json", "w") as f:
#     json.dump(validated_news, f, indent=4)

# print(
#     "✅ News processing complete! Run 'streamlit run ui/dashboard.py' to view "
#     "results."
# )

import json
import os
from news_processing.news_scraper import fetch_insurance_news
from news_processing.news_processor import process_news
from news_processing.news_validation import validate_news_with_research


def load_config(config_path="config.json"):
    with open(config_path, "r") as file:
        return json.load(file)


def main():
    config = load_config()

    input_query = config.get("input_query", "Climate risk insurance impact")
    output_path = config.get("output_validated_news_path", "outputs/validated_news.json")

    # Step 1: Fetch news
    print("Fetching news...")
    news_data = fetch_insurance_news(input_query)

    # Step 2: Process news
    print("Processing news...")
    structured_news = process_news(news_data)

    # Step 3: Validate news credibility
    print("Validating news with research...")
    validated_news = validate_news_with_research(structured_news)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Step 4: Save processed news
    with open(output_path, "w") as f:
        json.dump(validated_news, f, indent=4)

    print(
        "✅ News processing complete! Run 'streamlit run ui/dashboard.py' to view results."
    )


if __name__ == "__main__":
    main()
