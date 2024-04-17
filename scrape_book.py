import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json
import os

class ScrapeBook:
    def __init__(self):
        self.url = 'https://www.gutenberg.org/browse/languages/zh'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.data_folder = '/Users/kevinhsu/Documents/GitHub/Book_Scraping/data'
        self.num = 201
    def extract_book_url(self):
        for i in range(1,self.num):
            print(i)
            self.driver.get(self.url)
            book = self.driver.find_element(By.XPATH, f"(//li[@class='pgdbetext']/a)[{i}]")
            href = book.get_attribute('href')
            self.extract_book_info(href)


    def extract_book_info(self, url):
        self.driver.get(str(url))

        self.author = self.driver.find_element(By.XPATH, "//table[@class='bibrec']/tbody//td[1]/a").text
        self.title = self.driver.find_element(By.XPATH, "//td[@itemprop='headline']").text.replace('/','-')
        self.date = self.driver.find_element(By.XPATH, "//td[@itemprop='datePublished']").text
        try:
            content_url = self.driver.find_element(By.XPATH, "//a[@type='text/plain; charset=us-ascii']").get_attribute('href')
            self.extract_book_content(content_url)
        except selenium.common.exceptions.NoSuchElementException:
            self.num += 1
            print("Can't watch on website")
            print(self.title)
            print(url)
            

    def extract_book_content(self, url):
        self.driver.get(str(url))
        text = self.driver.find_element(By.XPATH, "(//pre)[1]").text.replace('\n', '')
        self.book_content = text
        self.write_to_file()

    def write_to_file(self):
        filename = f"{self.title}.json"
        book_data = {
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "content": self.book_content
        }
        full_path = os.path.join(self.data_folder, filename)
        with open(full_path, "w", encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=4)
        
    def close_browser(self):
        self.driver.quit()

scraper = ScrapeBook()
scraper.extract_book_url()
scraper.close_browser()

