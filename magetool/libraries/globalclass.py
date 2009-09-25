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

from lxml import etree
from magetool.libraries.cls import Class
from magetool.libraries.core import get_config, put_config

class GlobalClass(Class):
    """Superclass for 'global classes'.

    (Global classes are classes whose presence must be registered within
    the <global> element of a module's configuration file to be loaded by
    Mage.)

    """
    def __init__(self, superclass=None, override=False):
        """Initialize the global class by storing run-time arguments.

        Args:
            superclass: Full name of the global class's superclass,
                        e.g., "Mage_Rss_Block_Abstract".
            override: Whether this global class should override its
                      superclass.

        """
        Class.__init__(self)
        self.superclass = self._infer_super(superclass)
        self.override = override

    def _infer_super(self, superclass):
        """Infer the global class's superclass if none is supplied."""
        if superclass is None:
            end = "Template" if self.type == "block" else "Abstract"
            superclass = "Mage_Core_%s_%s" % (self.type.capitalize(), end)
        return superclass

    def create(self, name):
        """Create the global class.

        Dispatch requests to create an empty global class and update
        the module's configuration file.

        Args:
            name: Name of the global class, e.g., "Product" or
                  "ActivePoll".

        """
        self.name = name
        self._create_class(name, self.superclass)
        self.register()

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
                                        self.module["name"],
                                        self.type.capitalize())
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
                                        self.type.capitalize(),
                                        self.name)
