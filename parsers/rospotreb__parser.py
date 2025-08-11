from parsers.base_parser import BaseParser


class RospotrebParser(BaseParser):
    SOURCE = "rospotreb_"
    URL = "https://www.rospotrebnadzor.ru/"
    SEARCH_INPUT = None
    SEARCH_BUTTON = None
