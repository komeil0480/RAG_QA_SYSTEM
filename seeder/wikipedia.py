import requests
import wikipediaapi
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
import sys
import os
from datetime import datetime
import time
# Append the root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from mongo_db import mongo_db


documents_collection = mongo_db.get_document_collection() 


# Make a GET request to a service that returns your User-Agent
response = requests.get('https://httpbin.org/user-agent')
# Parse the JSON response
user_agent = response.json()['user-agent']
wiki_wiki = wikipediaapi.Wikipedia(user_agent)

def fetch_wikipedia_page(page_title):
    page = wiki_wiki.page(page_title)
    if page.exists():
        return page.text
    else:
        print(f"Page '{page_title}' does not exist.")
        return None

def chunk_text(text):
    documents = [Document(text=text)] 
    base_splitter = SentenceSplitter(chunk_size=512)
    # If 'text' is a single string, wrap it in a list
    nodes = base_splitter.get_nodes_from_documents(documents)
    print(len(nodes))
    return nodes

def insert_chunks(page_title, chunks):
    start_time = time.time()
    for chunk in chunks:
        document ={
                "text": chunk.get_content(),
                "embedding": {},
                "timestamp": datetime.utcnow(),
                "timestamp": datetime.utcnow(),
                "duration": time.time() - start_time,
            }
        documents_collection.insert_one(document)
    print(f'Inserted {len(chunks)} chunks into the database.')

def process_wikipedia_page(page_titles):
    for page_title in page_titles:
        text = fetch_wikipedia_page(page_title)
        if text:
            chunks = chunk_text(text)
            insert_chunks(page_title, chunks)

if __name__ == "__main__":
    page_titles = [
    "ChatGPT",
    "Deaths in 2023",
    "2023 Cricket World Cup",
    # "Indian Premier League",
    # "Oppenheimer (film)",
    # "J. Robert Oppenheimer",
    # "Cricket World Cup",
    # "Jawan (film)",
    # "Taylor Swift",
    # "The Last of Us (TV series)",
    # "2023 Indian Premier League",
    # "Pathaan (film)",
    # "Premier League",
    # "Barbie (film)",
    # "Lionel Messi",
    # "Cristiano Ronaldo",
    # "Donald Trump",
    # "Elon Musk",
    # "Kamala Harris",
    # "Joe Biden",
    # "Vladimir Putin",
    # "Xi Jinping",
    # "Narendra Modi",
    # "Boris Johnson",
    # "Angela Merkel",
    # "Emmanuel Macron",
    # "Justin Trudeau",
    # "Jacinda Ardern",
    # "Sanna Marin",
    # "Volodymyr Zelenskyy",
    # "Greta Thunberg",
    # "Malala Yousafzai",
    # "Bill Gates",
    # "Jeff Bezos",
    # "Mark Zuckerberg",
    # "Warren Buffett",
    # "Bernard Arnault",
    # "Larry Page",
    # "Sergey Brin",
    # "Steve Jobs",
    # "Tim Cook",
    # "Sundar Pichai",
    # "Satya Nadella",
    # "Sheryl Sandberg",
    # "Susan Wojcicki",
    # "Marissa Mayer",
    # "Meg Whitman",
    # "Ginni Rometty",
    # "Indra Nooyi",
    # "Oprah Winfrey"
    ]
    process_wikipedia_page(page_titles)

