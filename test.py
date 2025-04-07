from html import escape

import jinja2
import json
import pathlib

import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree


ROOT = pathlib.Path(__file__).parent
JSON_FILE = ROOT / 'upd2.local.json'

with open(JSON_FILE, 'r', encoding='utf-8') as file:
    raw = json.load(file)


template_loader = jinja2.FileSystemLoader(searchpath="./template")  # Template folder
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("upd.xml")

# Render the template with data
xml_string = template.render(data=raw)
xml_string = xml_string.replace('&', '&amp;')
root = ET.fromstring(xml_string)
cleaned_xml = ET.tostring(root, encoding='unicode', method='xml')

# Pretty print XML with proper indentation
pretty_xml = minidom.parseString(cleaned_xml).toprettyxml(indent="  ")

# Remove empty lines from the pretty XML
cleaned_pretty_xml = '\n'.join([line for line in pretty_xml.splitlines() if line.strip()])

# Write the cleaned and pretty XML back to a file with windows-1251 encoding
with open('output.xml', 'w', encoding='windows-1251') as file:
    file.write(cleaned_pretty_xml)

