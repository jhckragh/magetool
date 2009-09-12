from lxml import etree

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
