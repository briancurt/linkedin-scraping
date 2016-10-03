#!/bin/python3

from bs4 import BeautifulSoup
import sys
import urllib3

profile = str(sys.argv[1])		# LinkedIn profile URL
company = str(sys.argv[2]).lower()	# Company name

http = urllib3.PoolManager()
headers = urllib3.util.make_headers(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36')	# By pass LinkedIn's 999 response code, also force desktop site version

r = http.request('GET', profile, headers=headers)	# Get the HTML

soup = BeautifulSoup(r.data, 'html.parser')	# Parse beautifully and make it more readable

job_history = soup.find("ul", {"class": "positions"}).find_all("h5", {"class": "item-subtitle"})	# Get his/her job history

# Consider above: Using header tag instead of li - only shows company - for time range add span class experience-date-locale

if company in str(job_history).lower():
	for i in range(len(job_history)):
		if company in job_history[i].string.lower():
			isworking = job_history[i].parent.parent
			if isworking.attrs['data-section'] == 'currentPositionsDetails':
				print("Currently works at", job_history[i].string.upper())
			else:
				print("Previously worked at", job_history[i].string.upper())
else:
	print("Never worked at", company.upper())
