import os
import unittest

from magetool.libraries.cls import Class

MODULE_DIR = os.path.abspath("../app/code/local/Foo/Bar")

class ClsTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(MODULE_DIR)
        os.mkdir("Class")
        self.cls = Class()

    def tearDown(self):
        os.rmdir("Class")
        os.chdir(self.cwd)
        del self.cls

    def test__fill_template(self):
        self.failUnlessEqual(self.cls._fill_template("Hello", "World"),
                             "Foo|Bar|Hello|World")

    def test__create_class1(self):
        class_string = ""
        name = "Baz"
        target = os.path.join("Class", name + ".php")
        self.cls._create_class(name, "World")
        with open(target) as class_file:
            for line in class_file:
                class_string += line
        self.failUnlessEqual(class_string, "Foo|Bar|" + name + "|World")
        os.remove(target)

    def test__create_class2(self):
        class_string = ""
        name = "Quux_Qux"
        target = os.path.join("Class", "Quux", "Qux.php")
        self.cls._create_class(name, "World")
        with open(target) as class_file:
            for line in class_file:
                class_string += line
        self.failUnlessEqual(class_string, "Foo|Bar|Quux_Qux|World")
        os.remove(target)
        os.rmdir(target[:target.rfind(os.sep)])

    def test__words_to_dirs1(self):
        self.failUnlessEqual(self.cls._words_to_dirs(MODULE_DIR, "Product"),
                             MODULE_DIR)

    def test__words_to_dirs2(self):
        self.failUnlessEqual(self.cls._words_to_dirs(MODULE_DIR, "Abc_Def"),
                             os.path.join(MODULE_DIR, "Abc"))

    def test__words_to_dirs3(self):
        self.failUnlessEqual(self.cls._words_to_dirs(MODULE_DIR, "Abc_Def_Ghi"),
                             os.path.join(MODULE_DIR, "Abc", "Def"))

    def test__create_missing_dirs1(self):
        self.cls._create_missing_dirs(os.path.join("abc", "def", "ghi"))
        os.rmdir(os.path.join("abc", "def", "ghi"))
        os.rmdir(os.path.join("abc", "def"))
        os.rmdir("abc")

    def test__create_missing_dirs2(self):
        self.cls._create_missing_dirs(os.path.join(os.path.abspath(os.getcwd()),
                                                   "abc", "def", "ghi"))
        os.rmdir(os.path.join("abc", "def", "ghi"))
        os.rmdir(os.path.join("abc", "def"))
        os.rmdir("abc")

    def test__prepare_path_to(self):
        self.failUnlessEqual(self.cls._prepare_path_to("Product"),
                             os.path.join(MODULE_DIR, "Class", "Product.php"))

if __name__ == "__main__":
    unittest.main()
