import os
import unittest

from magetool.commands.module import Module

TEST_DIR = os.path.abspath(os.path.join("..", "app", "code", "local", "Foo"))

class ModuleTest(unittest.TestCase):

    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir(TEST_DIR)
        self.module = Module()

    def tearDown(self):
        os.chdir(self.old_cwd)
        del self.module

    def test_init_throws_exception(self):
        os.chdir("..")
        try:
            Module()
        except EnvironmentError:
            pass
        else:
            self.fail("Did not see EnvironmentError")

    def test_init_works_in_block(self):
        os.chdir(os.path.join("Bar", "Block"))
        try:
            Module()
        except EnvironmentError:
            self.fail("__init__() threw EnvironmentError on valid path.")

    def test_init_works_in_etc(self):
        os.chdir(os.path.join("Bar", "etc"))
        try:
            Module()
        except EnvironmentError:
            self.fail("__init__() threw EnvironmentError on valid path.")

    def test_create(self):
        reference_reg_file = """<?xml version="1.0"?>
<config>
    <modules>
        <Foo_Baz>
            <active>true</active>
            <codePool>local</codePool>
        </Foo_Baz>
    </modules>
</config>
"""
        reference_config = """<?xml version="1.0"?>
<config>
    <modules>
        <Foo_Baz>
            <version>0.1.0</version>
        </Foo_Baz>
    </modules>
</config>
"""
        paths = {"reg_file": os.path.join("..", "..", "..", "etc", "modules",
                                          "Foo_Baz.xml"),
                 "config": os.path.join("Baz", "etc", "config.xml")}

        self.module.create("Baz")

        with open(paths["reg_file"]) as actual_reg_file:
            self.assertEqual(reference_reg_file, actual_reg_file.read())
        with open(paths["config"]) as actual_config:
            self.assertEqual(reference_config, actual_config.read())

        os.remove(paths["config"])
        dirs = ["Block", "controllers", "etc", "Helper", "Model", "sql"]
        for directory in dirs:
            os.rmdir(os.path.join("Baz", directory))
        os.rmdir("Baz")
        os.remove(paths["reg_file"])

if __name__ == "__main__":
    unittest.main()