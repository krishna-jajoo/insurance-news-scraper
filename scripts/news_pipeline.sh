#!/bin/bash
python -m src.news_processing.news_scraper
python -m src.news_processing.news_processor
python -m src.news_processing.news_validation