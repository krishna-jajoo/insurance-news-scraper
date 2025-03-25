# Project Overview

## Insurance News Scraper 🚀

A Python-based tool that scrapes **insurance and reinsurance news**, processes them using **GPT-4o**, validates insights with research papers, and presents findings in an **interactive dashboard**.

## Features

✅ Fetches real-time news from **Tavily API**
✅ Summarizes & categorizes using **GPT-4o**
✅ Validates credibility with **research papers**
✅ Generates structured reports (JSON & CSV)
✅ Interactive dashboard with **Streamlit**

# Installation Guide

## Clone the Repository:

```env
git clone https://github.com/yourusername/insurance-news-scraper.git  
cd insurance-news-scraper
```

## Create a Virtual Environment & Install Dependencies

✅ **Windows**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

✅ **Mac/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  
```

# **How to Run**

## Set API keys:

Create a `.env` file inside the directory and add your API keys.

```env
OPENAI_API_KEY="your_openai_key"  
TAVILY_API_KEY="your_tavily_key"
```

## Run news processing:

```md
python main.py 
```

## Launch the dashboard:

```md
streamlit run ui/dashboard.py  
```

# About Me

Krishna Jajoo
