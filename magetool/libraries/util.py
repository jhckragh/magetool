import os.path, sys
from lxml import etree

def get_prog():
    return os.path.basename(sys.argv[0])

def find_or_create(parent, elem):
    """Search parent for sub element elem. Create this sub element if
    it does not exist.

    """
    res = parent.find(elem)
    if res is None:
        res = etree.SubElement(parent, elem)
    return res
