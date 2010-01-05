import os
import unittest

from magetool.commands.layout import Layout
from magetool.commands.module import Module
from magetool.libraries.util import remove_module

TEST_DIR = os.path.abspath(os.path.join("..", "app", "code", "local", "Foo"))

LAYOUT_DIR = os.path.join("..", "..", "..", "..", "design",
                          "frontend","default", "default", "layout")

XML = """<?xml version="1.0"?>
<layout version="0.1.0">

</layout>
"""

CONFIG = """<?xml version="1.0"?>
<config>
  <modules>
    <Foo_Quux>
      <version>0.1.0</version>
    </Foo_Quux>
  </modules>
  <frontend>
    <layout>
      <updates>
        <quux>
          <file>quux.xml</file>
        </quux>
      </updates>
    </layout>
  </frontend>
</config>
"""

class LayoutTest(unittest.TestCase):

    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir(TEST_DIR)
        Module().create("Quux")
        os.chdir("Quux")
        self.layout = Layout()

    def tearDown(self):
        os.chdir("..")
        remove_module("Foo", "Quux")
        os.chdir(self.old_cwd)
        del self.layout

    def test_create(self):
        file_name = "quux.xml"
        self.layout.create(file_name)
        try:
            with open(os.path.join(LAYOUT_DIR, file_name)) as layout_file:
                self.assertEqual(XML, layout_file.read())
        finally:
            os.remove(os.path.join(LAYOUT_DIR, file_name))
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(CONFIG, config.read())

    def test_create_without_file_extension(self):
        file_name = "quux"
        self.layout.create(file_name)
        try:
            with open(os.path.join(LAYOUT_DIR, file_name + ".xml")) as layout_file:
                self.assertEqual(XML, layout_file.read())
        finally:
            os.remove(os.path.join(LAYOUT_DIR, file_name + ".xml"))
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(CONFIG, config.read())

    def test_create_works_in_depth(self):
        file_name = "quux.xml"
        os.chdir("etc")
        self.layout.create(file_name)
        os.chdir("..")
        try:
            with open(os.path.join(LAYOUT_DIR, file_name)) as layout_file:
                self.assertEqual(XML, layout_file.read())
        finally:
            os.remove(os.path.join(LAYOUT_DIR, file_name))
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(CONFIG, config.read())


    def test_register(self):
        self.layout.register("quux")
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(CONFIG, config.read())

    def test_register_twice(self):
        self.layout.register("quux")
        self.layout.register("quux")
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(CONFIG, config.read())

if __name__ == "__main__":
    unittest.main()
