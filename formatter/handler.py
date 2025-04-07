from functools import cached_property

import jinja2
import xml.etree.ElementTree as ET
from xml.dom import minidom

from formatter.logger.mix_in import LoggerMixIn
from formatter.utils.singleton import SingletonMixin


class UPDToXmlHandler(LoggerMixIn, SingletonMixin):
    TEMPLATES_PATH = "./template"
    MAIN_TEMPLATE_FILE = 'upd.xml'

    @cached_property
    def xml_template(self):
        template_loader = jinja2.FileSystemLoader(searchpath=self.TEMPLATES_PATH)  # Template folder
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.MAIN_TEMPLATE_FILE)

        return template

    def process_data(self, raw):
        self.logger.info("Receive raw data")

        xml_string = self.xml_template.render(data=raw)

        self.logger.info("Render template")

        xml_string = xml_string.replace('&', '&amp;')
        root = ET.fromstring(xml_string)
        cleaned_xml = ET.tostring(root, encoding='windows-1251', method='xml')

        pretty_xml = (
            minidom
            .parseString(cleaned_xml)
            .toprettyxml(indent="  ", encoding='windows-1251')
            .decode(encoding='windows-1251')
        )

        # pretty_xml.replace('<?xml version=\"1.0\" ?>', '<?xml version=\"1.0\" encoding=\"windows-1251\"?>')

        cleaned_pretty_xml = '\n'.join([line for line in pretty_xml.splitlines() if line.strip()])

        self.logger.info("Finish cleanup")

        return cleaned_pretty_xml
