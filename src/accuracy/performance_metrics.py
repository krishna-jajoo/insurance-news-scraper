import json
import time


def load_config(config_path="config/config.json"):
    with open(config_path, "r") as file:
        return json.load(file)


def load_json(file_path):
    """Loads JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print(
                    f"Warning: {file_path} does not contain a list. Defaulting to an empty list."
                )
                return []
            return data
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Defaulting to an empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON. Defaulting to an empty list.")
        return []


def extract_titles(news_data):
    """Extracts titles from news data."""
    return {
        news["title"]
        for news in news_data
        if "title" in news and isinstance(news["title"], str)
    }


def calculate_kpis(raw_data, structured_data, validated_data):
    """Calculates key performance metrics for the news processing pipeline."""

    total_articles_scraped = len(raw_data)
    total_articles_processed = len(structured_data)
    total_articles_validated = len(validated_data)

    # Avoid division by zero
    processing_accuracy = (
        (total_articles_processed / total_articles_scraped * 100)
        if total_articles_scraped
        else 0
    )

    # Extract titles for comparison
    structured_titles = extract_titles(structured_data)
    validated_titles = extract_titles(validated_data)

    # Precision, Recall, and F1-score calculations
    correct_matches = structured_titles & validated_titles
    false_positives = structured_titles - validated_titles
    false_negatives = validated_titles - structured_titles

    precision = (
        (len(correct_matches) / (len(correct_matches) + len(false_positives)) * 100)
        if (len(correct_matches) + len(false_positives))
        else 0
    )
    recall = (
        (len(correct_matches) / (len(correct_matches) + len(false_negatives)) * 100)
        if (len(correct_matches) + len(false_negatives))
        else 0
    )
    f1_score = (
        (2 * precision * recall / (precision + recall)) if (precision + recall) else 0
    )

    return {
        "Total Articles Scraped": total_articles_scraped,
        "Total Articles Processed": total_articles_processed,
        "Total Articles Validated": total_articles_validated,
        "Processing Accuracy (%)": round(processing_accuracy, 2),
        "Precision (%)": round(precision, 2),
        "Recall (%)": round(recall, 2),
        "F1 Score (%)": round(f1_score, 2),
        "Correct Matches": len(correct_matches),
        "False Positives (Irrelevant)": len(false_positives),
        "False Negatives (Missed)": len(false_negatives),
    }


if __name__ == "__main__":
    start_time = time.time()

    # Load news data
    config = load_config()
    raw_news_path = config.get("raw_news_path", "outputs/raw_news.json")
    structured_news_path = config.get(
        "structured_news_path", "outputs/structured_news.json"
    )
    validated_news_path = config.get(
        "validated_news_path", "outputs/validated_news.json"
    )
    raw_news = load_json(raw_news_path)
    structured_news = load_json(structured_news_path)
    validated_news = load_json(validated_news_path)
    accuracy_metrics_path = config.get(
        "accuracy_metrics_path", "outputs/accuracy_metrics.json"
    )
    if raw_news or structured_news or validated_news:
        metrics = calculate_kpis(raw_news, structured_news, validated_news)
        with open(accuracy_metrics_path, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        print(f"Performance metrics calculated and saved in {accuracy_metrics_path}")

    execution_time = round(time.time() - start_time, 2)
    print(f"Execution Time: {execution_time} seconds")
