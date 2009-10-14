from lxml import etree
from magetool.commands.module import Module

class Command:
    """Base class for magetool commands."""

    def __init__(self):
        self.type = self.__class__.__name__.lower()
        self.template = self._get_template()
        self.module = Module()

    def get_config(self):
        """Read and parse a module configuration file, returning the root
        element of the file.

        """
        parser = etree.XMLParser(remove_blank_text=True)
        source = open(self.module.cfg_path)
        config = etree.parse(source, parser).getroot()
        source.close()
        return config

    def put_config(self, elem):
        """Write a formatted serialisation of elem to a module configuration
        file.

        """
        dest = open(self.module.cfg_path, "w")
        dest.write(etree.tostring(elem, pretty_print=True))
        dest.close()

    def _get_template(self):
        """Import the template file for the class. (We assume that the
        command's template file is named after the command's type.)

        """
        template = __import__("magetool.templates." + self.type,
                              globals(), locals(), ["magetool.templates"])
        return template.string
