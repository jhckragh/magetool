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
from magetool.commands.module import Module

class Command:
    """Base class for magetool commands."""

    def __init__(self):
        """Initialize the class by figuring out what kind of class it is
        and by retrieving the class's template as well as information about
        the module to which the class belongs.

        """
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
