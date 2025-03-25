# import openai
import json

import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from scripts.azure.azure import get_llm_model
from src.prompt.prompt import get_prompt
from src.utils import extract_and_parse_json

# Load API Key
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def process_news(news_articles):
#     """
#     Processes and summarizes news articles using GPT-4o.
#     """
#     structured_data = []

#     for article in news_articles:
#         prompt = f"""
#         Summarize this news article and categorize it into relevant insurance
#         topics (Climate Risk, InsureTech, Policies, Re-insurance).

#         Title: {article.get('title', 'Unknown')}
#         Content: {article.get('content', 'No content available')}

#         Expected JSON output:
#         {{
#           "title": "...",
#           "summary": "...",
#           "category": "...",
#           "source": "...",
#           "date": "...",
#           "tags": ["..."]
#         }}
#         """
#         response = openai.ChatCompletion.create(
#             model="gpt-4o", messages=[{"role": "user", "content": prompt}]
#         )
#         structured_data.append(json.loads(response["choices"][0]["message"]["content"]))

#     return structured_data


def process_news(news_articles, model_name="gpt-4o"):
    PROMPT_PATH = os.path.join("src/prompt/news_article_prompt.md")
    llm = get_llm_model(model_name=model_name)  # Initialize LLM model
    prompt_template = get_prompt(PROMPT_PATH)

    prompt = PromptTemplate(
        input_variables=["title", "content"], template=prompt_template
    )
    name_chain = LLMChain(llm=llm, prompt=prompt)  # Create LLM chain

    structured_data = []

    for article in news_articles:
        inputs = {
            "title": article.get("title", "Unknown"),
            "content": article.get("content", "No content available"),
        }

        response = name_chain.run(inputs)  # Execute chain and get response
        parsed_data = extract_and_parse_json(response)

        if parsed_data:
            structured_data.append(parsed_data)

    return structured_data


if __name__ == "__main__":
    # Load raw news
    with open("outputs/raw_news.json", "r") as f:
        raw_news = json.load(f)

    structured_news = process_news(raw_news)

    # Save processed news
    with open("outputs/structured_news.json", "w") as f:
        json.dump(structured_news, f, indent=4)

    print("News processed and saved!")
