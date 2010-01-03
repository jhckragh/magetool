import unittest

from lxml import etree

from magetool.libraries.util import find_or_create

class UtilTest(unittest.TestCase):

    def test_find_or_create(self):
        root = etree.Element("root")
        find_or_create(root, "child")
        self.failIf(root.find("child") is None)

if __name__ == "__main__":
    unittest.main()
