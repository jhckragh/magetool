import os
import re
from string import Template
from xml.dom.minidom import parseString

import magetool.settings as settings
from magetool.templates.config_xml import config_xml
from magetool.templates.regfile import regfile

class Module:
    def __init__(self):
        """Initialize the module by retrieving its code pool, namespace, and
        name.

        """
        cwd = os.getcwd()
        code_pools = "|".join(settings.code_pools)
        pattern = "/app/code/(%s)/([A-Za-z]+)/?([A-Za-z]+)?" % code_pools
        match = re.search(pattern, cwd)
        try:
            self.code_pool = match.group(1)
            self.namespace = match.group(2)
            self.name = match.group(3)
            self.path = cwd[:match.end()]
            self.cfg_path = self.path + "/etc/config.xml".replace("/", os.sep)
        except AttributeError:
            raise EnvironmentError("Wrong execution directory.")

    def create(self, name):
        """Create a directory structure and a configuration file for the
        module, using the name parameter as the module's name.

        """
        self.name = name
        os.mkdir(self.name)
        for directory in settings.directories:
            os.mkdir("%s/%s" % (self.name, directory))
        self._create_config()
        self._create_regfile()

    def _create_config(self):
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

    @staticmethod
    def help():
        print """Usage: magetool create module NAME

Example:
  magetool create module NewProduct
        Create a module skeleton in NewProduct/ and register the module in
        app/etc/modules/Namespace_NewProduct.xml."""
