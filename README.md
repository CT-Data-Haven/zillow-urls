# zillow URL scraper

I needed to download a couple files from Zillow's [research hub](https://www.zillow.com/research/data/), but got annoyed by how to retrieve URLs, which also change periodically. So this is a scraper to just get the URLs of every dataset listed there out of dropdowns. It runs [Selenium in a docker container](https://hub.docker.com/r/selenium/standalone-firefox), crawls the dataset listings to get every available combination of dataset and geography, extracts the URLs for each file, and writes them to a CSV file ([`./urls.csv`](./urls.csv)). That's it.

Since they say they update their data on the 16th of every month, might be worth it to add a GitHub cron action to rerun this on the 17th.