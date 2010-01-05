import os.path
import sys
from textwrap import fill

from lxml import etree

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
