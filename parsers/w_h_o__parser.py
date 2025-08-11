from parsers.base_parser import BaseParser


class WHOParser(BaseParser):
    SOURCE = "w_h_o_"
    URL = "https://www.who.int/"
    SEARCH_INPUT = None
    SEARCH_BUTTON = None
