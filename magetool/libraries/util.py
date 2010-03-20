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

def abbreviate(path, width=70):
    if len(path) <= width:
        return path
    mid = (width - 3) / 2
    left = path[:mid].rfind(os.sep) + 1
    right = path[len(path) - mid:].find(os.sep) + len(path) - mid
    return path[:left] + "..." + path[right:]
