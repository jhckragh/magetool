import os
import unittest

from magetool.commands.block import Block
from magetool.commands.module import Module

TEST_DIR = os.path.abspath(os.path.join("..", "app", "code", "local", "Foo"))

reference_config = """<?xml version="1.0"?>
<config>
  <modules>
    <Foo_Quux>
      <version>0.1.0</version>
    </Foo_Quux>
  </modules>
  <global>
    <blocks>
      <quux>
        <class>Foo_Quux_Block</class>
      </quux>
    </blocks>
  </global>
</config>
"""

reference_override_config = """<?xml version="1.0"?>
<config>
  <modules>
    <Foo_Quux>
      <version>0.1.0</version>
    </Foo_Quux>
  </modules>
  <global>
    <blocks>
      <tag>
        <rewrite>
          <product_list>Foo_Quux_Block_List</product_list>
        </rewrite>
      </tag>
    </blocks>
  </global>
</config>
"""

class BlockTest(unittest.TestCase):

    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir(TEST_DIR)
        Module().create("Quux")
        os.chdir("Quux")
        self.block = Block()

    def tearDown(self):
        os.chdir("..")
        self._remove_module("Quux")
        os.chdir(self.old_cwd)
        del self.block

    def _remove_module(self, name):        
        os.remove(os.path.join("..", "..", "..", "etc",
                               "modules", "Foo_Quux.xml"))
        os.remove(os.path.join(name, "etc", "config.xml"))
        for dir_ in ["Block", "controllers", "etc", "Helper", "Model", "sql"]:
            os.rmdir(os.path.join(name, dir_))
        os.rmdir(name)

    def test_create(self):
        self.block.create("Product")
        with open(os.path.join("Block", "Product.php")) as block_file:
            self.assertEqual(self._get_reference_class("Product"),
                             block_file.read())
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_config, config.read())
        os.remove(os.path.join("Block", "Product.php"))

    def test_create_works_in_depth(self):
        os.chdir("Block")
        self.block.create("Product")
        os.chdir("..")
        with open(os.path.join("Block", "Product.php")) as block_file:
            self.assertEqual(self._get_reference_class("Product"),
                             block_file.read())
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_config, config.read())
        os.remove(os.path.join("Block", "Product.php"))

    def test_create_works_with_underscores(self):
        self.block.create("Product_List")
        with open(os.path.join("Block", "Product", "List.php")) as block_file:
            self.assertEqual(self._get_reference_class("Product_List"),
                             block_file.read())
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_config, config.read())
        os.remove(os.path.join("Block", "Product", "List.php"))
        os.rmdir(os.path.join("Block", "Product"))

    def test_overriding_works(self):
        superclass = "Mage_Tag_Block_Product_List"
        Block(superclass, True).create("List")
        with open(os.path.join("Block", "List.php")) as block_file:
            self.assertEqual(self._get_reference_class("List", superclass),
                             block_file.read())
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_override_config, config.read())
        os.remove(os.path.join("Block", "List.php"))

    def _get_reference_class(self, name, superclass="Mage_Core_Block_Template"):
        return """<?php

class Foo_Quux_Block_%s extends %s
{

}
""" % (name, superclass)

if __name__ == "__main__":
    unittest.main()
