import os
import unittest

from magetool.commands.model import Model
from magetool.commands.module import Module
from magetool.tests.util import remove_module, TEST_DIR

reference_reg_config = """<?xml version="1.0"?>
<config>
  <modules>
    <Foo_Quux>
      <version>0.1.0</version>
    </Foo_Quux>
  </modules>
  <global>
    <models>
      <quux>
        <class>Foo_Quux_Model</class>
      </quux>
    </models>
  </global>
</config>
"""

reference_config = """<?xml version="1.0"?>
<config>
  <modules>
    <Foo_Quux>
      <version>0.1.0</version>
    </Foo_Quux>
  </modules>
  <global>
    <models>
      <quux>
        <class>Foo_Quux_Model</class>
        <resourceModel>quux_mysql4</resourceModel>
      </quux>
      <quux_mysql4>
        <class>Foo_Quux_Model_Mysql4</class>
        <entities>
          <tag>
            <table>quux_tag</table>
          </tag>
        </entities>
      </quux_mysql4>
    </models>
  </global>
</config>
"""

reference_model = """<?php

class Foo_Quux_Model_Tag extends Mage_Core_Model_Abstract
{
    protected function _construct()
    {
        $this->_init('quux/tag');
    }
}
"""

reference_resource = """<?php

class Foo_Quux_Model_Mysql4_Tag extends Mage_Core_Model_Mysql4_Abstract
{
    protected function _construct()
    {
        $this->_init('quux/tag', 'tag_id');
    }
}
"""

class ModelTest(unittest.TestCase):

    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir(TEST_DIR)
        Module().create("Quux")
        os.chdir("Quux")
        self.model = Model()

    def tearDown(self):
        os.chdir("..")
        remove_module("Foo", "Quux")
        os.chdir(self.old_cwd)
        del self.model

    def test_register(self):
        self.model.register()
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_reg_config, config.read())

    def test_create(self):
        self.model.create("Tag")
        with open(os.path.join("etc", "config.xml")) as config:
            self.assertEqual(reference_config, config.read())
        with open(os.path.join("Model", "Tag.php")) as model:
            self.assertEqual(reference_model, model.read())
        with open(os.path.join("Model", "Mysql4", "Tag.php")) as resource:
            self.assertEqual(reference_resource, resource.read())
        os.remove(os.path.join("Model", "Mysql4", "Tag.php"))
        os.rmdir(os.path.join("Model", "Mysql4"))
        os.remove(os.path.join("Model", "Tag.php"))

if __name__ == "__main__":
    unittest.main()
