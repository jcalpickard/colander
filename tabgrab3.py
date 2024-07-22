# TABGRAB3.PY
# is a code snippet I've "borrowed" from Tim Cowlishaw

import requests
from boilerpy3.extractors import CanolaExtractor

def get_web_page_text(url):
    response = requests.get(url)
    extractor = CanolaExtractor()
    return extractor.get_content(response.text)