import os

# Название класса -> URL
sites = {
    "WHOParser": "https://www.who.int/",
    "OutbreakNewsParser": "https://outbreaknewstoday.substack.com/",
    "WHOWeeklyRecordParser": (
        "https://www.who.int/publications/journals/weekly-"
        "epidemiological-record"
    ),
    "RospotrebParser": "https://www.rospotrebnadzor.ru/",
    "FSVPSParser": "https://fsvps.gov.ru/",
    "MCXParser": "https://mcx.gov.ru/",
    "ProMEDParser": "http://www.promedmail.org/",
    "ECDCParser": "http://www.ecdc.europa.eu/en",
    "SEAROParser": "http://www.searo.who.int/",
    "WPROParser": "http://www.wpro.who.int/",
    "AFROParser": "http://www.afro.who.int/",
    "EUROParser": "http://www.euro.who.int/",
    "EMROParser": "http://www.emro.who.int/",
    "MMWRParser": "https://www.cdc.gov/mmwr",
    "CDCParser": "https://www.cdc.gov/",
    "ECDCAtlasParser": (
        "https://www.ecdc.europa.eu/en/data-tools/atlas/"
        "Pages/atlas"
    ),
    "EIOSParser": "https://www.who.int/initiatives/eios",
    "GOARNParser": "https://goarn.who.int/",
    "CISIDParser": "https://cisid.euro.who.int/CISID/",
    "EWARSParser": (
        "https://www.who.int/emergencies/surveillance/"
        "early-warning-alert-and-response-system-ewars"
    ),
    "CIDRAPParser": "http://www.cidrap.umn.edu",
    "HealthMapParser": "http://www.healthmap.org/en",
    "EpiSouthParser": "https://www.episouthnetwork.org/",
    "WOAHParser": "https://www.woah.org/en/home",
    "WAHISParser": "https://wahis.woah.org/#/home",
    "AfricaCDCParser": "https://africacdc.org/",
    "EDPLNParser": "https://www.who.int/groups/edpln",
    "PandemicHubParser": "https://pandemichub.who.int/",
    "ReliefWebParser": (
        "https://reliefweb.int/disasters?search=&sl="
        "environment-disaster_listing"
    ),
    "MelioidosisParser": "https://www.melioidosis.info/infobox.aspx"
}

parser_template = '''from parsers.base_parser import BaseParser

class {classname}(BaseParser):
    SOURCE = "{source}"
    URL = "{url}"
'''


def camel_to_snake(name):
    parts = ['_' + c.lower() if c.isupper() else c for c in name]
    return ''.join(parts).lstrip('_').replace("parser", "")


def generate_parsers():
    os.makedirs("parsers", exist_ok=True)
    imports = []
    registrations = []

    for classname, url in sites.items():
        filename_prefix = camel_to_snake(classname)
        filename = f"{filename_prefix}_parser.py"
        source = filename_prefix

        content = parser_template.format(
            classname=classname,
            source=source,
            url=url
        )

        filepath = os.path.join("parsers", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Created: {filepath}")

        import_line = (
            f"from parsers.{filename_prefix}_parser import {classname}"
        )
        site_entry = f'    "{source}": {classname},'
        imports.append(import_line)
        registrations.append(site_entry)

    return imports, registrations


def write_base_sites(imports, registrations):
    filepath = "parsers/base_sites.py"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Автоматически сгенерировано\n\n")
        f.write("\n".join(imports))
        f.write("\n\nSITES = {\n")
        f.write("\n".join(registrations))
        f.write("\n}\n")
    print(f"✓ Updated: {filepath}")


if __name__ == "__main__":
    imports, registrations = generate_parsers()
    write_base_sites(imports, registrations)
