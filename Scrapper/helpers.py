import requests
import csv

def download_page_content(url, target):
    page = requests.get(url)

    if page.status_code == 200:
        return page.text

    return None


def download_csv_content(url, target):
    pageContent = download_page_content(url, target)

    if pageContent == None:
        return None

    cr = csv.reader(pageContent.splitlines(), delimiter=',')

    return list(cr)
    