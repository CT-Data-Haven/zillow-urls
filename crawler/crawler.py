from selenium import webdriver
import subprocess
import time
from pathlib import Path

# start docker
def start_selenium(fetch_dir, port = '4444'):
    if fetch_dir is not None:
        fetch_dir = Path(fetch_dir)
        fetch_dir = fetch_dir.resolve()
        print(fetch_dir)
    # -v {fetch_dir}:/home/seluser/Downloads \
    subprocess.run(
        f'docker run --rm -d \
            -p {port}:4444 -p 7900:7900 \
            --shm-size="2g" \
            --name selenium \
            -e SE_SESSION_REQUEST_TIMEOUT=1200 \
            selenium/standalone-firefox:latest',
        shell=True
    )
    time.sleep(5)
    return f'http://localhost:{port}'

def stop_selenium():
    subprocess.run('docker stop selenium', shell = True)
    return True

def setup_driver(local_url):
    ff_opts = webdriver.FirefoxOptions()
    driver = webdriver.Remote(
        command_executor=local_url,
        options=ff_opts
    )
    # time.sleep(5)
    return driver

def navigate(dr, url):
    dr.get(url)
    time.sleep(3)
    return dr

def get_href(el):
    return el.get_attribute('href')