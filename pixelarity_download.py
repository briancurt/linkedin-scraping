#!/bin/python3

from bs4 import BeautifulSoup
import sys
import urllib3
import re
import requests

def main():

	http = urllib3.PoolManager()

	r = http.request('GET', 'https://pixelarity.com/')

	soup = BeautifulSoup(r.data, 'html.parser')

	templates = soup.find("section").find_all("article")

	for index in range(len(templates)):
		print(templates[index].h2.string)

if __name__ == "__main__":
    main()
