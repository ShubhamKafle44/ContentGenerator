import openai
import os

from dotenv import load_dotenv

from sqlalchemy.orm import Session

import crud, models

import threading

from concurrent.futures import ThreadPoolExecutor

load_dotenv()


OPENAI_API = os.getenv("OPENAI_API")


## Define a semaphore here

semaphore = threading.Semaphore(5)##we can adjust the number of semaphores as needed


def generate_content(db: Session, topic: str) -> str:
    with semaphore:
        search_term = crud.get_search_term(db, topic)
        if not search_term:
            search_term = crud.create_search_term(db, topic)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"Write a detailed article about {topic}"},
            ])
        generated_text = response.choices[0].message['cotent'].strip()
        crud.create_generated_content(db, generated_text, search_term.id)


def analyze_content(db:Session,content:str):
    with semaphore:
        search_term = crud.get_search_term(db, content)
        if not search_term:
            search_term = crud.create_search_term(db, content)

    readability = get_readability_score(content)
    sentiment = get_sentiment_anlaysis(content)
    crud.create_sentiment_analysis(db, readability, sentiment, search_term.id)
    return readability, sentiment


def get_readability_score(content: str)->str:
    return "REadability score: Good"#NEed to work on it

def get_sentiment_anlaysis(content:str)->str:
    response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"Analyze the sentiment of the following text:  {content}"},
            ], 
            max_tokens = 10
    )
    return response.choices[0].message['content'].strip()