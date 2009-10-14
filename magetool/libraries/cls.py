import os
from magetool.libraries.command import Command
from string import Template

class Class(Command):
    """Base class for Mage classes, e.g., blocks, controllers, and models."""

    def _fill_template(self, name, superclass):
        """Fill out the template file for a class.

        Args:
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
        template = self._fill_template(name, superclass)
        directory = ("controllers" if self.type == "controller" else
                     self.type.capitalize())

        path = self.module.path + os.sep + directory + os.sep
        # Check if the class name contains underscores. If it does, interpret
        # them as directory separators.
        if not name.find("_") == -1:
            substrings = name.split("_")
            path += os.path.join(*substrings[:-1]) + os.sep
            try:
                os.makedirs(path)
            except OSError:
                pass # The directories already exist
            name = substrings[-1]
        dest = path + name + ".php"
        if not os.path.isfile(dest):
            dest = open(dest, "w")
            dest.write(template)
            dest.close()
        else:
            raise OSError("File exists: " + dest)
