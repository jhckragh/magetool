import os
import sys
from textwrap import fill

from lxml import etree

import magetool.settings as settings

def get_prog():
    return os.path.basename(sys.argv[0])

def find_or_create(parent, elem):
    res = parent.find(elem)
    if res is None:
        res = etree.SubElement(parent, elem)
    return res

def _err(msg, type):
    sys.stderr.write(fill("%s: %s: %s" % (get_prog(), type, msg)) + "\n")

def error(msg, status=2):
    _err(msg, "error")
    sys.exit(status)

def warn(msg):
    _err(msg, "warning")

def remove_module(namespace, name):
    """Remove a skeleton module and its activation file. (For use in tests.)"""
    os.remove(os.path.join("..", "..", "..", "etc",
                           "modules", "%s_%s.xml" % (namespace, name)))
    os.remove(os.path.join(name, "etc", "config.xml"))
    for directory in settings.directories:
        os.rmdir(os.path.join(name, directory))
    os.rmdir(name)
