# TABGRAB3.PY
# is a code snippet I've "borrowed" from Tim Cowlishaw

import requests
from boilerpy3.extractors import CanolaExtractor

# BoilerPy3 is a library for extracting main textual content from web pages
# by removing boilerplate and extraneous content
# it promotes the idea of cleaning and simplifying web content for analysis
# CanolaExtractor is a specific extractor
# incorporating a particular understanding of content vs boilerplate based on its training data

def get_web_page_text(url):
    response = requests.get(url)
    extractor = CanolaExtractor()
    return extractor.get_content(response.text)