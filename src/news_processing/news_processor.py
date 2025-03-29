# import openai
import json

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from src.model.model import get_llm_model
from src.prompt.prompt import get_prompt
from src.utils import extract_and_parse_json

load_dotenv()


def load_config(config_path="config/config.json"):
    with open(config_path, "r") as file:
        return json.load(file)


def process_news(news_articles, model_name="gpt-4o"):
    PROMPT_PATH = os.path.join("src/prompt/news_article_prompt.md")
    llm = get_llm_model(
        vendor="openai", model_name=model_name
    )  # Initialize LLM model "gpt-4o"
    prompt_template = get_prompt(PROMPT_PATH)

    prompt = PromptTemplate(
        input_variables=["title", "content", "source"], template=prompt_template
    )
    # name_chain = LLMChain(llm=llm, prompt=prompt)  # Create LLM chain
    name_chain = prompt | llm

    structured_data = []

    for article in news_articles:
        inputs = {
            "title": article.get("title", "Unknown"),
            "content": article.get("content", "No content available"),
            "source": article.get("url", "Unknown"),
        }

        ai_message = name_chain.invoke(inputs)
        response = ai_message.content
        parsed_data = extract_and_parse_json(response)
        if parsed_data:
            structured_data.append(parsed_data)

    return structured_data


def init():
    config = load_config()
    raw_news_path = config.get("raw_news_path", "outputs/raw_news.json")
    structured_news_path = config.get(
        "structured_news_path", "outputs/structured_news.json"
    )
    with open(raw_news_path, "r", encoding="utf-8") as f:
        raw_news = json.load(f)

    structured_news = process_news(raw_news)
    with open(structured_news_path, "w", encoding="utf-8") as f:
        json.dump(structured_news, f, indent=4)

    print("News processed and saved!")


if __name__ == "__main__":
    init()
