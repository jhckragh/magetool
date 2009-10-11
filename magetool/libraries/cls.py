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

import os
from magetool.libraries.command import Command
from string import Template

class Class(Command):
    """Base class for Mage classes, e.g., blocks, controllers, and models."""
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
