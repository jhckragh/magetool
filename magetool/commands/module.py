# Copyright (c) 2009, Jacob Kragh
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials
#    provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os, re
import magetool.settings as settings
from magetool.templates.config_xml import config_xml
from magetool.templates.regfile import regfile
from string import Template
from xml.dom.minidom import parseString

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
        except AttributeError:
            raise EnvironmentError("Wrong execution directory.")

    def identify(self):
        """Return information about the module which other classes can use."""
        return {"name": self.name,
                "namespace": self.namespace,
                "code_pool": self.code_pool,
                "path": self.path}

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

    @staticmethod
    def help():
        """Print a help message describing this command."""
        print """Usage: magetool create module NAME

Example:
  magetool create module NewProduct
        Create a module skeleton in NewProduct/ and register the module in
        app/etc/modules/Namespace_NewProduct.xml."""
