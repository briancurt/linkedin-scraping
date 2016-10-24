#!/bin/python3

import argparse
import requests
from robobrowser import RoboBrowser

def main():

        parser = argparse.ArgumentParser(description='Login to Pixelarity.')
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()

        browser = RoboBrowser()

        browser.open('https://pixelarity.com/login')

        login_form = browser.get_form(id='ajaxForm1')

        login_form['email'].value = args.email
        login_form['password'].value = args.password

        browser.submit_form(login_form)

        request = browser.session.get('{{{downloadUrl}}}', stream=True)
        with open('{{{zipFile}}}', "wb") as temp_zip:
                temp_zip.write(request.content)
        
if __name__ == "__main__":
    main()
