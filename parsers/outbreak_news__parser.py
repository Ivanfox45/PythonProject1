from parsers.base_parser import BaseParser


class OutbreakNewsParser(BaseParser):
    SOURCE = "outbreak_news_"
    URL = "https://outbreaknewstoday.substack.com/"
    SEARCH_INPUT = None
    SEARCH_BUTTON = None
