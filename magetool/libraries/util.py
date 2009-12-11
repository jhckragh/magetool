import os.path
import sys

from lxml import etree

def get_prog():
    return os.path.basename(sys.argv[0])

def find_or_create(parent, elem):
    res = parent.find(elem)
    if res is None:
        res = etree.SubElement(parent, elem)
    return res

def error(msg, status=2):
    sys.stderr.write("%s: error: %s\n" % (get_prog(), msg))
    sys.exit(status)
