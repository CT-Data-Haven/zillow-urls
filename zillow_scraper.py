# crawl zillow research site to get all urls for download since they change periodically
# data is updated on 16th of every month, so set cron job to run every 17th
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

from crawler import crawler

def scrape_container(div: webdriver.remote.webelement.WebElement) -> str | None:
    try:
        hdr = div.find_element(By.TAG_NAME, 'h2').text
        selects = div.find_elements(By.TAG_NAME, 'select')
        links = {}
        datasets_el = Select(selects[0])
        geos_el = Select(selects[1])
        for idx, dataset in enumerate(datasets_el.options):
            datasets_el.select_by_index(idx)
            geos = geos_el.options
            geo_lvls = [geo.text for geo in geos]
            urls = [geo.get_dom_attribute('value') for geo in geos]
            links[dataset.text] = {
                'geo': geo_lvls,
                'url': urls
            }
        return (hdr, links)

    except NoSuchElementException:
        return None

def container_to_df(scrape: dict) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(scrape, orient='index').explode(['geo', 'url'])
    # drop "choose one..." options
    df = df.loc[df['url'] != '']
    return df

def main():
    base_url = "https://www.zillow.com/research/data/"
    path_out = 'urls.csv'
    docker_url = crawler.start_selenium(fetch_dir=None, port='4444')
    driver = crawler.setup_driver(docker_url)
    crawler.navigate(driver, base_url)

    # get div.container { h2, selects }
    container_els = driver.find_elements(By.CSS_SELECTOR, 'div.container')
    # iterate over select 1 to get options in select 2
    containers = list(filter(None, [scrape_container(el) for el in container_els]))
    dfs = {}
    for hdr, cont in containers:
        dfs[hdr] = container_to_df(cont)
    all_urls = pd.concat(dfs, names = ['section', 'dataset'])
    print(f'Writing out {all_urls.shape[0]} URLs to {path_out}')
    
if __name__ == '__main__':
    main()