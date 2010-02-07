import os
import re
from string import Template
from xml.dom.minidom import parseString

import magetool.settings as settings
from magetool.libraries.util import warn
from magetool.templates.config_xml import config_xml
from magetool.templates.regfile import regfile

NAME_CASE_WARNING = ("Internal Mage methods expect namespaces " +
                     "and module names to be capitalized. " +
                     "Violating this convention will prevent " +
                     "Mage from loading the module.")

class Module:
    def __init__(self):
        """Initialize the module by retrieving its code pool, namespace, and
        name.

        """
        cwd = os.getcwd()
        code_pools = "(%s)" % ("|".join(settings.code_pools),)
        pattern = os.path.join("", "(app)", "code", code_pools,
                               "([A-Za-z]+)", "?([A-Za-z]+)?")
        match = re.search(pattern, cwd)
        try:
            self.code_pool = match.group(2)
            self.namespace = match.group(3)
            self.name = match.group(4)
            self.path = cwd[:match.end()]
            self.app_path = cwd[:match.end(1)]
            self.cfg_path = os.path.join(self.path, "etc", "config.xml")

            if not self.namespace[0].isupper():
                warn(NAME_CASE_WARNING)
            if not self.name is None and not self.name[0].isupper():
                warn(NAME_CASE_WARNING)
        except AttributeError:
            raise EnvironmentError("Wrong execution directory.")

    def create(self, name):
        """Create a directory structure, a configuration file, and an
        activation file for the module, using the name parameter as the
        module's name.

        """
        if not name[0].isupper():
            warn(NAME_CASE_WARNING)
        self.name = name
        os.mkdir(self.name)
        for directory in settings.directories:
            os.mkdir(os.path.join(self.name, directory))
        self._create_config()
        self._create_regfile()

    def _create_config(self):
        template = Template(config_xml).substitute(namespace=self.namespace,
                                                   module_name=self.name)
        parseString(template) # Syntax check
        dest = open(os.path.join(self.name, "etc", "config.xml"), "w")
        dest.write(template)
        dest.close()

    def _create_regfile(self):
        """Create a file to register the module with Mage. This file makes
        Mage scan the module's etc/ directory.

        """
        template = Template(regfile).substitute(namespace=self.namespace,
                                                module_name=self.name,
                                                code_pool=self.code_pool)
        parseString(template) # Syntax check
        path = os.path.join(self.app_path, "etc", "modules",
                            "%s_%s.xml" % (self.namespace, self.name))
        dest = open(path, "w")
        dest.write(template)
        dest.close()

    @staticmethod
    def help():
        print """Usage: magetool create module NAME

Example:
  magetool create module NewProduct
        Create a module skeleton in NewProduct/ and register the module in
        app/etc/modules/Namespace_NewProduct.xml."""
