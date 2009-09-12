import os
import settings
from string import Template
from templates.config_xml import config_xml
from templates.regfile import regfile
from xml.dom.minidom import parseString

class Module:
    def __init__(self):
        """Initialize the module by retrieving its code pool, namespace, and
        name.

        """
        self._configure()

    def _configure(self):
        """Retrieve and store the module's code pool, namespace, and name."""
        path = os.getcwd().split(os.sep)
        grandparent, parent, cwd = path[-3:]
        if grandparent in settings.code_pools:
            self.code_pool = grandparent
            self.namespace = parent
            self.name = cwd
        elif parent in settings.code_pools:
            self.code_pool = parent
            self.namespace = cwd
        else:
            raise Exception("Wrong execution directory.")

    def identify(self):
        """Return information about the module which other classes can use."""
        return {"name": self.name,
                "namespace": self.namespace,
                "code_pool": self.code_pool}

    def create(self, name):
        """Create a directory structure and a configuration file for the
        module, using the name parameter as the module's name.

        """
        self.name = name
        self._create_directories()
        self._create_config()
        self._create_regfile()

    def _create_directories(self):
        """Create a directory structure for the module."""
        os.mkdir(self.name)
        for directory in settings.directories:
            os.mkdir("%s/%s" % (self.name, directory))

    def _create_config(self):
        """Create a configuration file for the module."""
        template = Template(config_xml)
        template = template.substitute(namespace=self.namespace,
                                       module_name=self.name)
        parseString(template) # Syntax check
        dest = open("%s/etc/config.xml" % self.name, "w")
        dest.write(template)
        dest.close()

    def _create_regfile(self):
        """Create a file to register the module with Mage. This file makes
        Mage scan the module's etc/ directory.

        """
        template = Template(regfile)
        template = template.substitute(namespace=self.namespace,
                                       module_name=self.name,
                                       code_pool=self.code_pool)
        parseString(template) # Syntax check
        dest = open("../../../etc/modules/%s_%s.xml" % (self.namespace,
                                                        self.name), "w")
        dest.write(template)
        dest.close()
