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

class GlobalClass(Class):
    """Base class for 'global classes'.

    (Global classes are classes whose presence must be registered
    within the <global> element of a module's configuration file in
    order to be loaded by Mage.)

    """
    def __init__(self, superclass=None, override=False):
        """Initialize the global class, e.g., by storing run-time
        arguments and by retrieving and preparing the module's
        configuration file.

        Args:
            superclass: Full name of the global class's superclass,
                        e.g., "Mage_Rss_Block_Abstract".
            override: Whether this global class should override its
                      superclass.

        """
        Class.__init__(self)
        self.superclass = self._infer_super(superclass)
        self.override = override
        self.type_tag = self.type + "s"
        self.config = self.get_config()
        self._prepare_config()
        self.xpath = "/config/global/" + self.type_tag
        self.type_elem = self.config.xpath(self.xpath)[0]

    def _infer_super(self, superclass):
        """Infer the global class's superclass if none is supplied."""
        if superclass is None:
            end = "Template" if self.type == "block" else "Abstract"
            superclass = "Mage_Core_%s_%s" % (self.type.capitalize(), end)
        return superclass

    def _prepare_config(self):
        """Prepare the module's configuration file for class registration.

        To make Mage aware that the module has one or more global
        classes of type self.type, the module's configuration file
        must have a <global> element. Furthermore, this <global>
        element must have a sub element whose tag matches the type of
        the global class. If these elements don't exist, we create
        them.

        """
        global_ = self.config.xpath("/config/global")
        global_ = (global_[0] if global_ else
                   etree.SubElement(self.config, "global"))
        type_ = self.config.xpath("/config/global/" + self.type_tag)
        type_ = type_[0] if type_ else etree.SubElement(global_, self.type_tag)

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
        if self.override:
            self._override()
        else:
            self.register()
        self.put_config(self.config)

    def register(self):
        """Tell Mage that the module has one or more self.type global
        classes.

        """
        tag = self.module.name.lower()
        if not self.config.xpath(self.xpath + "/" + tag):
            module = etree.SubElement(self.type_elem, self.module.name.lower())
            class_ = etree.SubElement(module, "class")
            class_.text = "%s_%s_%s" % (self.module.namespace,
                                        self.module.name,
                                        self.type.capitalize())

    def _override(self):
        """Tell Mage that this global class overrides self.superclass."""
        tag = self.superclass.split("_")[1].lower()
        if not self.config.xpath(self.xpath + "/" + tag):
            substrings = self.superclass.split("_")
            module = substrings[1].lower()
            name = "_".join(substrings[3:]).lower()

            module = etree.SubElement(self.type_elem, module)
            rewrite = etree.SubElement(module, "rewrite")
            name = etree.SubElement(rewrite, name)
            name.text = "%s_%s_%s_%s" % (self.module.namespace,
                                         self.module.name,
                                         self.type.capitalize(),
                                         self.name)
