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
from string import Template

def get_config():
    """Read and parse a module configuration file, returning the root element
    of the file.

    """
    parser = etree.XMLParser(remove_blank_text=True)
    source = open("etc/config.xml")
    config = etree.parse(source, parser).getroot()
    source.close()
    return config

def put_config(element):
    """Write a formatted serialisation of element to a module configuration
    file.

    """
    dest = open("etc/config.xml", "w")
    dest.write(etree.tostring(element, pretty_print=True))
    dest.close()

def fill_tmplt(tmplt, module, name, superclass):
    """Fill out the template file for the global class.

    Args:
        template: A Template string.
        module: A dictionary containing the keys "namespace" and "name".
        name: The name of the global class, e.g., "Product".
        superclass: The full name of the superclass, e.g.,
                    "Mage_Core_Block_Template".

    Return:
        A string.

    """
    tmplt = Template(tmplt)
    tmplt = tmplt.substitute(namespace=module["namespace"],
                             module_name=module["name"],
                             name=name,
                             superclass=superclass)
    return tmplt
