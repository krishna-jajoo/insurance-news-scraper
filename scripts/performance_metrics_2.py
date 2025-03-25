import json
import time
from typing import Dict, Any, List, Set


def load_json(file_path: str) -> Any:
    """Loads JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


def extract_titles(news_data: List[Dict[str, Any]]) -> Set[str]:
    """Extracts titles from news data."""
    return {news["title"] for news in news_data if "title" in news}


def calculate_kpis(raw_data: list, structured_data: list, validated_data: list) -> Dict[str, Any]:
    """Calculates key performance metrics for the news processing pipeline."""

    total_articles_scraped = len(raw_data)
    total_articles_processed = len(structured_data)
    total_articles_validated = len(validated_data)

    # Accuracy (Processed / Scraped)
    processing_accuracy = (
        (total_articles_processed / total_articles_scraped) * 100 if total_articles_scraped > 0 else 0
    )

    # Extract titles for comparison
    structured_titles = extract_titles(structured_data)
    validated_titles = extract_titles(validated_data)

    # Precision, Recall, and F1-score calculations
    correct_matches = structured_titles & validated_titles
    false_positives = structured_titles - validated_titles
    false_negatives = validated_titles - structured_titles

    precision = (
        len(correct_matches) / (len(correct_matches) + len(false_positives)) * 100
        if len(correct_matches) + len(false_positives) > 0
        else 0
    )
    recall = (
        len(correct_matches) / (len(correct_matches) + len(false_negatives)) * 100
        if len(correct_matches) + len(false_negatives) > 0
        else 0
    )
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
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
    raw_news = load_json("outputs/raw_news.json")
    structured_news = load_json("outputs/structured_news.json")
    validated_news = load_json("outputs/validated_news.json")

    if raw_news and structured_news and validated_news:
        metrics = calculate_kpis(raw_news, structured_news, validated_news)

        # Save metrics as JSON
        with open("outputs/performance_metrics_2.json", "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        print("Performance metrics calculated and saved.")

    execution_time = round(time.time() - start_time, 2)
    print(f"Execution Time: {execution_time} seconds")
