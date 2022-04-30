import os
import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("./chromedriver")

def read_csv(filename):
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            data = [i for i in reader]
        return data
    except Exception as e:
        print(f"Error while reading {filename}: {e}")

def save_article(stock, headline, url):
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error while loading '{headling}': {e}")

    try:
        article = driver.execute_script(
            """
            article = {date: "", body: []};
            let date = document.getElementsByClassName('timestamp')[0].children[1].dateTime;
            let article_blocks = document.getElementsByClassName('body__content')[0].getElementsByTagName('p');
            for (let i = 0; i < article_blocks.length; i++) {
                article.body[i] = article_blocks[i].innerText;
            }
            article.date = date;
            return article;
            """
        )
    except Exception as e:
        print(f"Error while parsing {headline}: {e}")

    article["headline"] = headline
    article["url"] = url

    try:
        if not os.path.isdir(f"articles/{stock}"):
            os.mkdir(f"articles/{stock}")
        with open(f"articles/{stock}/{article['date']}.json", "w") as f:
            json.dump(article, f)
    except Exception as e:
        print(f"Error while saving {headline}: {e}")

# Read headlines
headlines = read_csv("headlines/aapl.csv")

# Save articles into json format
for i in range(10):
    print(headlines[i][0])
    save_article("aapl", headlines[i][0], headlines[i][1])
    print("Waiting for 5 seconds...")
    time.sleep(5)


