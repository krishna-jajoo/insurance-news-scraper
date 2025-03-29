import json
import time
from typing import Dict, Any


def load_json(file_path: str) -> Any:
    """Loads JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


def calculate_kpis(raw_data: list, structured_data: list) -> Dict[str, Any]:
    """Calculates key performance metrics for the news processing pipeline."""
    total_articles_scraped = len(raw_data)
    total_articles_processed = len(structured_data)

    # Accuracy (Processed / Scraped)
    processing_accuracy = (
        (total_articles_processed / total_articles_scraped) * 100
        if total_articles_scraped > 0
        else 0
    )

    return {
        "Total Articles Scraped": total_articles_scraped,
        "Total Articles Processed": total_articles_processed,
        "Processing Accuracy (%)": round(processing_accuracy, 2),
    }


if __name__ == "__main__":
    start_time = time.time()

    # Load scraped (raw) and processed (structured) news
    raw_news = load_json("outputs/raw_news.json")
    structured_news = load_json("outputs/structured_news.json")

    if raw_news and structured_news:
        metrics = calculate_kpis(raw_news, structured_news)

        # Save metrics to file
        with open("outputs/performance_metrics.txt", "w", encoding="utf-8") as file:
            for key, value in metrics.items():
                file.write(f"{key}: {value}\n")

        print("Performance metrics calculated and saved.")

    execution_time = round(time.time() - start_time, 2)
    print(f"Execution Time: {execution_time} seconds")
