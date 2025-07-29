from parsers.base_parser import BaseParser

class ReliefWebParser(BaseParser):
    SOURCE = "relief_web_"
    URL = "https://reliefweb.int/disasters?search=&sl=environment-disaster_listing"
