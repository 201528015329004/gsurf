#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 20:51:19 2017

@author: MacBook
"""

from pyvirtualdisplay import Display
from selenium import webdriver

usingChrome = True

def get(url):
    global usingChrome
    with Display():
        # we can now start Firefox and it will run inside the virtual display
        try:
            if usingChrome:
                browser = webdriver.Chrome()
        except:
            browser = webdriver.Firefox()
            usingChrome = False
            
        if usingChrome is False:
            browser = webdriver.Firefox()

        # put the rest of our selenium code in a try/finally
        # to make sure we always clean up at the end
        try:
            browser.get(url)
            source = browser.page_source.encode('utf-8')
            title = browser.title #this should print "Google"
            return title,source

        finally:
            browser.quit()
            
            
if __name__ == '__main__':
    print get('http://www.google.com')