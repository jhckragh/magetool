import os
from lxml import etree
from magetool.commands.module import Module
from string import Template

class Class(object):
    """Superclass for PHP classes, e.g., blocks, controllers, helpers,
    and models.

    """
    def __init__(self):
        """Initialize the class by figuring out what kind of class it is
        and by retrieving the class's template as well as information about
        the module to which the class belongs.

        """
        self.type = self.__class__.__name__.lower()
        self.template = self._get_template()
        self.module = Module()
        self.__config = self.module.path + "/etc/config.xml".replace("/",os.sep)

    def get_config(self):
        """Read and parse a module configuration file, returning the root
        element of the file.

        """
        parser = etree.XMLParser(remove_blank_text=True)
        source = open(self.__config)
        config = etree.parse(source, parser).getroot()
        source.close()
        return config

    def put_config(self, element):
        """Write a formatted serialisation of element to a module configuration
        file.

        """
        dest = open(self.__config, "w")
        dest.write(etree.tostring(element, pretty_print=True))
        dest.close()

    def _get_template(self):
        """Import the template file for the class. (We assume that the
        class's template file is named after the class's type.)

        """
        template = __import__("magetool.templates." + self.type,
                              globals(), locals(), ["magetool.templates"])
        return template.string

    def _fill_template(self, name, superclass):
        """Fill out the template file for a class.

        Args:
            superclass: The full name of the superclass, e.g.,
                        "Mage_Core_Block_Template".

        Return:
            A string.

        """
        template = Template(self.template)
        template = template.substitute(namespace=self.module.namespace,
                                       module_name=self.module.name,
                                       name=name,
                                       superclass=superclass)
        return template

    def _create_class(self, name, superclass):
        """Create a skeleton PHP class."""
        template = self._fill_template(name, superclass)
        directory = ("controllers" if self.type == "controller" else
                     self.type.capitalize())

        path = self.module.path + os.sep + directory + os.sep
        # Check if the class name contains underscores. If it does, interpret
        # them as directory separators.
        if not name.find("_") == -1:
            substrings = name.split("_")
            path += os.path.join(*substrings[:-1]) + os.sep
            try:
                os.makedirs(path)
            except OSError:
                pass # The directories already exist
            name = substrings[-1]
        dest = path + name + ".php"
        if not os.path.isfile(dest):
            dest = open(dest, "w")
            dest.write(template)
            dest.close()
        else:
            raise OSError("File exists: " + dest)
