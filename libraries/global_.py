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

"""Superclass for 'global classes'.

(Global classes are classes whose presence must be registered within
the <global> element of a module's configuration file to be loaded by
Mage.)

"""

import os
from commands.module import Module
from libraries.core import get_config, put_config
from lxml import etree
from string import Template

class Global:
    def __init__(self, superclass=None, override=False):
        """Initialize the global class by storing run-time
        arguments and calling the configure method.

        Args:
            superclass: Full name of the global class's superclass,
                        e.g., "Mage_Rss_Block_Abstract".
            override: Whether this global class should override its
                      superclass.

        """
        self.superclass = superclass
        self.reg = True
        self.override = override
        self._configure()

    def _configure(self):
        """Configure the global class and retrieve information about the
        module to which it belongs.

        """
        self.module = Module().identify()
        self._get_type()
        self._get_template()

    def _get_type(self):
        """Get the name of the global class's type.

        At the time of writing there are three types of global
        classes: block, helper, and model.

        """
        self.type = self.__class__.__name__.lower()
        self.type_name = self.type.capitalize()

    def _get_template(self):
        """Import the template file for the global class."""
        template_import = "from templates.%(type)s import %(type)s as template"
        exec template_import % {"type": self.type}
        self.template = template

    def create(self, name):
        """Create the global class.

        Dispatch requests to create an empty global class and update
        the module's configuration file.

        Args:
            name: Name of the global class, e.g., "Product" or
                  "ActivePoll".

        """
        self.name = name
        if self.superclass is None:
            superclass = "Mage_Core_%s_%s"
            end = "Template" if self.type == "block" else "Abstract"
            self.superclass = superclass % (self.type_name, end)
        self._create_class()
        self.register()

    def _create_class(self):
        """Create an empty global class."""
        template = Template(self.template)
        template = template.substitute(namespace=self.module["namespace"],
                                       module_name=self.module["name"],
                                       name=self.name,
                                       superclass=self.superclass)
        name = self.name
        path = self.type_name + os.sep
        # Check if the class name contains underscores. If it does, interpret
        # them as directory separators.
        if not self.name.find("_") == -1:
            substrings = self.name.split("_")
            path += os.path.join(*substrings[:-1]) + os.sep
            try:
                os.makedirs(path)
            except OSError:
                pass # The directories already exist
            name = substrings[-1]
        dest = open(path + name + ".php", "w")
        dest.write(template)
        dest.close()

    def register(self):
        """Tell Mage that the module has one or more self.type global classes.

        Update the module's configuration file to register that the
        module has one or more global classes of type self.type.

        """
        type_tag = self.type + "s"
        module = self.module["name"].lower()

        config = get_config()
        if config.xpath("/config/global"):
            xpath = "/config/global/%s/%s"
            tags = (type_tag, module)
            # Check if global classes of type self.type are already registered
            if config.xpath(xpath % tags):
                self.reg = False
            # Check if a rewrite directive already exists
            if self.override:
                tags = (type_tag, self.superclass.split("_")[1].lower())
                if config.xpath(xpath % tags):
                    self.override = False

        # Make sure global_ and type_ exist
        global_ = config.xpath("/config/global")
        global_ = global_[0] if global_ else etree.SubElement(config, "global")
        type_ = config.xpath("/config/global/%s" % type_tag)
        type_ = type_[0] if type_ else etree.SubElement(global_, type_tag)

        if self.reg and not self.override:
            module = etree.SubElement(type_, module)
            class_ = etree.SubElement(module, "class")
            class_.text = "%s_%s_%s" % (self.module["namespace"],
                                        self.module["name"], self.type_name)
        if self.override:
            self._add_rewrite(type_)
        put_config(config)

    def _add_rewrite(self, elem):
        """Add a rewrite directive to the <elem> element.

        Args:
            elem: The lxml.etree._Element object which the <rewrite>
                  element should be added to. This should be a type_
                  element, e.g., <blocks> or <models>.

        """
        sc_substrings = self.superclass.split("_")
        sc_module = sc_substrings[1].lower()
        sc_name = "_".join(sc_substrings[3:]).lower() # e.g., "product_view"

        sc_module = etree.SubElement(elem, sc_module)
        rewrite = etree.SubElement(sc_module, "rewrite")
        sc_name = etree.SubElement(rewrite, sc_name)
        sc_name.text = "%s_%s_%s_%s" % (self.module["namespace"],
                                        self.module["name"],
                                        self.type_name,
                                        self.name)

