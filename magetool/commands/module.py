import os
import re
from string import Template
from xml.dom.minidom import parseString

import magetool.settings as settings
from magetool.libraries.util import abbreviate, error, warn
from magetool.templates.config_xml import config_xml
from magetool.templates.regfile import regfile

class Module:

    NAME_CASE_WARNING = ("Internal Mage methods expect namespaces " +
                         "and module names to be capitalized. " +
                         "Violating this convention will prevent " +
                         "Mage from loading the module.")

    CODE_DIR_INDEX = -3 # Expected position of the `code/' directory,
                        # assuming a path such as the following:
                        # `/path/to/mage/app/code/<code_pool>/<namespace>'

    def __init__(self):
        """Initialize the module."""
        self._configure()
        self._check_case_convention()
        self._files_created = []

    def _configure(self):
        """Configure the module by guessing its code pool, namespace, and
        name.

        """
        self.path = self._guess_module_path(os.getcwd())
        dirs = self.path.split(os.sep)
        self.name = dirs.pop() if dirs[self.CODE_DIR_INDEX] != "code" else None
        self.code_pool, self.namespace = dirs[-2:]
        self.app_path = os.sep.join(dirs[:self.CODE_DIR_INDEX])
        self.cfg_path = os.path.join(self.path, "etc", "config.xml")

    def _guess_module_path(self, path):
        sep = "/" if os.sep == "/" else "\\\\"
        pat = "/app/code/(%s)/([A-Za-z]+)/?([A-Za-z]+)?".replace("/", sep) % (
            "|".join(settings.code_pools))
        match = re.search(pat, path)
        if match is None:
            error("Found neither module nor namespace on path `%s'" % (path,))
        return path[:match.end()]

    def _check_case_convention(self):
        if not self.namespace[0].isupper():
            warn(self.NAME_CASE_WARNING)
        if not self.name is None and not self.name[0].isupper():
            warn(self.NAME_CASE_WARNING)

    def create(self, name):
        """Create a directory structure, a configuration file, and an
        activation file for the module, using the name parameter as the
        module's name.

        """
        if not name[0].isupper():
            warn(self.NAME_CASE_WARNING)
        self.name = name
        self._mkdir(self.name)
        for directory in settings.directories:
            self._mkdir(os.path.join(self.name, directory))
        self._create_config()
        self._create_regfile()
        self._print_feedback()

    def _mkdir(self, path):
        os.mkdir(path)
        self._files_created.append(os.path.abspath(path))

    def _create_config(self):
        template = Template(config_xml).substitute(namespace=self.namespace,
                                                   module_name=self.name)
        parseString(template) # Syntax check
        self._write(os.path.join(self.name, "etc", "config.xml"), template)

    def _create_regfile(self):
        """Create a file to register the module with Mage. This file makes
        Mage scan the module's etc/ directory.

        """
        template = Template(regfile).substitute(namespace=self.namespace,
                                                module_name=self.name,
                                                code_pool=self.code_pool)
        parseString(template) # Syntax check
        self._write(os.path.join(self.app_path, "etc", "modules",
                                "%s_%s.xml" % (self.namespace, self.name)),
                   template)

    def _write(self, path, str):
        dest = open(path, "w")
        dest.write(str)
        dest.close()
        self._files_created.append(os.path.abspath(path))

    def _print_feedback(self):
        print "Created %d files:" % (len(self._files_created),)
        for f in self._files_created:
            print abbreviate(f)

    @staticmethod
    def help():
        print """Usage: magetool create module NAME

Example:
  magetool create module NewProduct
        Create a module skeleton in NewProduct/ and register the module in
        app/etc/modules/Namespace_NewProduct.xml."""
