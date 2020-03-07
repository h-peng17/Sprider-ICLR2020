from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import trange 
import argparse
import json 
import os 
EXECUTABLE_PATH = 'C:\WebDriver\chromedriver.exe' 


def parserICLR(driver, url, path, name):
    """Parser ICLR html
        @Args:
            driver: web driver
            url: must be an iclr website url
            path: path to save data
            name: name of saved data
        @Return:
            No Return. 
            Save path + name.json  
    """
    driver.get(url)
    driver.find_element_by_class_name("note ")

    # html src
    html_doc = driver.page_source.encode("UTF8", "ignore")
    soup = BeautifulSoup(html_doc, features="lxml")

    print("parsing " + url) 
    papers = soup.find_all("li", class_="note")
    results = []
    iter = trange(len(papers))
    for i in iter:
        paper = papers[i]
        result = {}
        result["title"] = paper.h4.a.string.strip()
        result["href"] = "https://openreview.net/" + paper.h4.a["href"]
        result["authors"] = []
        for author in paper.find("div", class_="note-authors").find_all("a"):
            result["authors"].append(author.text)
        keys = paper.find_all("strong", class_="note-content-field")
        values = paper.find_all("span", class_="note-content-value")
        for i in range(len(keys)):
            result[keys[i].string[:-1].lower()] = values[i].get_text().strip()
        results.append(result)
    
    json.dump(results, open(os.path.join(path, name+".json"), 'w'))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default="https://openreview.net/group?id=ICLR.cc/2020/Conference#accept-poster",
                        help="url to download")
    parser.add_argument("--save_dir", dest="save_dir", default=".",
                        help="save path")
    parser.add_argument("--filename", dest="filename", default="iclr",
                        help="dumped file name")
    args = parser.parse_args()

    # don't show the broswer window
    options = Options() 
    options.add_argument("--headless")

    # set driver
    driver = webdriver.Chrome(options=options, executable_path=EXECUTABLE_PATH)  

    # wait for async loading
    driver.implicitly_wait(20)

    
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)

    # 
    parserICLR(driver, args.url, args.save_dir, args.filename)








