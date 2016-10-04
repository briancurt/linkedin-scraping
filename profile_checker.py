#!/bin/python3

from bs4 import BeautifulSoup
import sys
import urllib3
import re

def tomonths(a):
    # Receives the full STRING within the TIME/SPAN tags for a given position. Then the parsed variable
    # will get only what is within parenthesis, that is, the actual duration. The resulting string can
    # only have 2 or 4 words: if 2, it's either number of months or number of years. If 4, it's years with months.
    parsed = re.search('\((.*)\)', a).group(1)
    if len(parsed.split()) == 2:
        if "year" in parsed or "año" in parsed:
            return int(parsed.split()[0]) * 12
        else:
            return int(parsed.split()[0])
    elif len(parsed.split()) == 4:
        return int(parsed.split()[0]) * 12 + int(parsed.split()[2])
    else:
        print("Error getting duration in months. Check duration span tag")
        quit()

def main():
    profile = str(sys.argv[1])          # LinkedIn profile URL
    company = str(sys.argv[2]).lower()  # Company name

    http = urllib3.PoolManager()
    # Bypass LinkedIn's 999 response code, also force desktop site version.
    headers = urllib3.util.make_headers(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36')
	
    # Get the HTML.
    r = http.request('GET', profile, headers=headers)

    # Parse beautifully and make it more readable.
    soup = BeautifulSoup(r.data, 'html.parser')

    # Get job history in a list called job_history.
    job_history = soup.find("ul", {"class": "positions"}).find_all("h5", {"class": "item-subtitle"})

    # I compare company to the whole job_history list converted to a string.
    # This may not be the best way, but for now it kinda works.
    if company in str(job_history).lower():
        for i in range(len(job_history)):
            if company in job_history[i].string.lower():
                isworking = job_history[i].parent.parent
                months = tomonths(job_history[i].parent.next_sibling.get_text())
                if isworking.attrs['data-section'] == 'currentPositionsDetails':
                    print("Has been workoing at {} for {} months".format(job_history[i].string.upper(),months))
                else:
                    print("Previously worked at {} for {} months".format(job_history[i].string.upper(),months))
    else:
        print("Never worked at", company.upper())
		
if __name__ == "__main__":
    main()
