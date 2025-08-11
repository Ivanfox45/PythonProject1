from parsers.base_parser import BaseParser


class ECDCAtlasParser(BaseParser):
    SOURCE = "e_c_d_c_atlas_"
    URL = "https://atlas.ecdc.europa.eu/public/index.aspx"
    SEARCH_INPUT = None
    SEARCH_BUTTON = None
