import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scrape_headlines(stock="aapl", pages=20):
    driver = webdriver.Chrome("./chromedriver")
    driver.get(f"https://www.nasdaq.com/market-activity/stocks/{stock}/news-headlines")
    page_number = 0
    for i in range(pages):
        driver.execute_script(
            f"""
            let pagination = document.getElementsByClassName("pagination__pages")[0];
            pagination.children[{page_number}].click();
            """
        )
        if i < 6:
            page_number += 1
        else:
            page_number = 5
        time.sleep(1)
        urls = driver.execute_script(
            """
            let urls = [];
            let articles = [];
            let headlines = document.getElementsByClassName("quote-news-headlines__item");
            for(let i = 0; i < headlines.length; i++) {
                urls[i] = [headlines[i].children[0].children[1].textContent, headlines[i].children[0].href];
            }
            return urls;
            """
        )
        with open(f"headlines/{stock}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerows(urls)
        # Wait for 1 second
        time.sleep(1)

scrape_headlines(stock="aapl", pages=5)