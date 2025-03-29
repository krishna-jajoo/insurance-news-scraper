import streamlit as st
import json
# import datetime
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain


def load_news_data(file_path="outputs/validated_news.json"):
    """Load validated news from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def extract_filters(news_data):
    """Extract unique filters from news data."""
    categories = list(set(news["category"] for news in news_data if news["category"]))
    tags = list(set(chain.from_iterable(news.get("tags", []) for news in news_data)))
    risk_factors = list(
        set(chain.from_iterable(news.get("risk_factors", []) for news in news_data))
    )
    regions = list(
        set(
            news["geographical_region"]
            for news in news_data
            if news["geographical_region"]
        )
    )
    sentiments = ["Positive", "Neutral", "Negative"]
    return categories, tags, risk_factors, regions, sentiments


def filter_news(
    news_data,
    selected_category,
    selected_tag,
    selected_risk,
    selected_region,
    selected_sentiment,
    search_query,
):
    """Filter news based on multiple criteria."""
    return [
        news
        for news in news_data
        if (selected_category == "All" or news["category"] == selected_category)
        and (selected_tag == "All" or selected_tag in news.get("tags", []))
        and (selected_risk == "All" or selected_risk in news.get("risk_factors", []))
        and (selected_region == "All" or news["geographical_region"] == selected_region)
        and (selected_sentiment == "All" or news["sentiment"] == selected_sentiment)
        and (
            search_query.lower() in news["title"].lower()
            or search_query.lower() in news["summary"].lower()
        )
    ]


def display_news(news_articles):
    """Display filtered news articles."""
    for article in news_articles:
        st.subheader(article["title"])
        st.caption(f"Source: {article['source']} | Date: {article['date']}")
        st.write(article["summary"])

        if "tags" in article:
            st.write("**Tags:** " + ", ".join(article["tags"]))
        if "risk_factors" in article:
            st.write("**Risk Factors:** " + ", ".join(article["risk_factors"]))
        if "economic_impact" in article:
            st.write(f"**Economic Impact:** {article['economic_impact']}")
        if "geographical_region" in article:
            st.write(f"**Region:** {article['geographical_region']}")

        if article["validated"]:
            st.success(f"Verified with: {article['matched_research']}")
        else:
            st.warning("No matching research found")

        st.markdown("---")


def plot_sentiment_distribution(news_articles):
    """Display a sentiment distribution chart."""
    sentiment_counts = pd.Series(
        [news["sentiment"] for news in news_articles]
    ).value_counts()
    st.subheader("Sentiment Distribution")
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind="bar", ax=ax, color=["green", "gray", "red"])
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    st.pyplot(fig)


def main():
    """Main function to run the Streamlit app."""
    st.title("Insurance & Climate Risk News Dashboard")
    st.markdown("---")

    news_data = load_news_data()
    categories, tags, risk_factors, regions, sentiments = extract_filters(news_data)

    selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)
    selected_tag = st.sidebar.selectbox("Filter by Tag", ["All"] + tags)
    selected_risk = st.sidebar.selectbox(
        "Filter by Risk Factor", ["All"] + risk_factors
    )
    selected_region = st.sidebar.selectbox("Filter by Region", ["All"] + regions)
    selected_sentiment = st.sidebar.selectbox(
        "Filter by Sentiment", ["All"] + sentiments
    )
    search_query = st.sidebar.text_input("Search", "")

    filtered_news = filter_news(
        news_data,
        selected_category,
        selected_tag,
        selected_risk,
        selected_region,
        selected_sentiment,
        search_query,
    )
    display_news(filtered_news)

    if filtered_news:
        plot_sentiment_distribution(filtered_news)
    else:
        st.warning("No news articles match the selected criteria.")


if __name__ == "__main__":
    main()
