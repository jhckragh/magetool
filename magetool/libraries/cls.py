import os

from magetool.libraries.command import Command
from string import Template

class Class(Command):
    """Base class for Mage classes, e.g., blocks, controllers, and models."""

    def _fill_template(self, name, superclass):
        """Fill out the template file for a class.

        Args:
            name: The part of the class name which follows
                  the base name, e.g., "Abstract" or
                  "Customer_Recent".
            superclass: The full name of the superclass, e.g.,
                        "Mage_Core_Block_Template".

        Return:
            A string.

        """
        template = Template(self.template)
        template = template.substitute(namespace=self.module.namespace,
                                       module_name=self.module.name,
                                       name=name,
                                       superclass=superclass)
        return template


    def _create_class(self, name, superclass):
        """Create a skeleton PHP class."""
        dest = self._prepare_path_to(name)
        if os.path.isfile(dest):
            raise OSError("File exists: " + dest)
        dest = open(dest, "w")
        dest.write(self._fill_template(name, superclass))
        dest.close()

    def _prepare_path_to(self, name):
        """Return the path to where on the file system name should reside."""
        directory = ("controllers" if self.type == "controller" else
                     self.type.capitalize())
        base = os.path.join(self.module.path, directory)
        dirname = self._words_to_dirs(base, name)
        self._create_missing_dirs(dirname)
        return os.path.join(dirname, name.split("_")[-1] + ".php")

    def _words_to_dirs(self, path, name):
        """Convert underscore-delimited string to a path."""
        words = name.split("_")
        if len(words) > 1:
            path = os.path.join(path, *words[:-1])
        return path

    def _create_missing_dirs(self, path):
        try:
            os.makedirs(path)
        except OSError:
            pass # The directories already exist
