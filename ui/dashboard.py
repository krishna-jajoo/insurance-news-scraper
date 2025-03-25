'''
This code defines a Streamlit app that displays news articles based on selected categories and tags.
'''
import streamlit as st
import json
from itertools import chain


def load_news_data(file_path="outputs/validated_news.json"):
    """Load validated news from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def extract_categories_and_tags(news_data):
    """Extract unique categories and tags from news data."""
    categories = list(
        set(
            chain.from_iterable(
                (
                    [news["category"]]
                    if isinstance(news["category"], str)
                    else news["category"]
                )
                for news in news_data
            )
        )
    )

    tags = list(
        set(
            chain.from_iterable(
                news.get("tags", []) if isinstance(news.get("tags"), list) else []
                for news in news_data
            )
        )
    )
    return categories, tags


def filter_news(news_data, selected_category, selected_tag):
    """Filter news based on selected category and tag."""
    return [
        news
        for news in news_data
        if (
            selected_category == "All"
            or (
                selected_category in news["category"]
                if isinstance(news["category"], list)
                else news["category"] == selected_category
            )
        )
        and (selected_tag == "All" or selected_tag in news.get("tags", []))
    ]


def display_news(news_articles):
    """Display filtered news articles."""
    for article in news_articles:
        st.subheader(article["title"])
        st.caption(f"Source: {article['source']}")
        st.write(article["summary"])

        if "tags" in article:
            st.write("**Tags:** " + ", ".join(article["tags"]))

        if article["validated"]:
            st.success(f"Verified with: {article['matched_research']}")
        else:
            st.warning("No matching research found")

        st.markdown("---")


def main():
    """Main function to run the Streamlit app."""
    st.title("Insurance & Climate Risk News Dashboard")
    st.markdown("---")

    news_data = load_news_data()
    categories, tags = extract_categories_and_tags(news_data)

    selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)
    selected_tag = st.sidebar.selectbox("Filter by Tag", ["All"] + tags)

    filtered_news = filter_news(news_data, selected_category, selected_tag)
    display_news(filtered_news)


if __name__ == "__main__":
    main()
