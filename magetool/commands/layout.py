import os.path
from lxml import etree
from magetool.libraries.command import Command

class Layout(Command):
    """Class representing a Mage layout."""

    def _format_name(self, name):
        if not name.endswith(".xml"):
            name = name + ".xml"
        return name

    def create(self, name):
        """Create the layout XML file and update the module's configuration
        file accordingly.

        """
        name = self._format_name(name)
        path = os.path.normpath(self.module.path + (".." + os.sep) * 5 +
                                "design/frontend/default/default/layout")
        dest = path + os.sep + name
        dest = open(dest, "w")
        dest.write(self.template)
        dest.close()
        self.register(name)

    def register(self, name):
        """Make Mage aware that the module supplies a layout file."""
        name = self._format_name(name)
        config = self.get_config()
        # Make sure a <frontend> element exists.
        frontend = config.find("frontend")
        if frontend is None:
            frontend = etree.SubElement(config, "frontend")
        # Make sure an <updates> element exists.
        updates = frontend.find("updates")
        if updates is None:
            updates = etree.SubElement(frontend, "updates")
        # Only update the file if the following element doesn't exist.
        # This way we avoid inadvertently creating duplicate layout
        # updates.
        module_lower = updates.find(self.module.name.lower())
        if module_lower is None:
            module_lower = etree.SubElement(updates, self.module.name.lower())
            file_ = etree.SubElement(module_lower, "file")
            file_.text = name
            self.put_config(config)

    @staticmethod
    def help():
        print """Usage: magetool (create|register) layout NAME

Examples:
  magetool create layout newproduct
        Create a bare-bones layout file called newproduct.xml in
        app/design/frontend/default/default/ and update the module's
        configuration file accordingly.

  magetool register layout newproduct
        Update the module's configuration file to tell Mage that the module
        supplies a layout file called newproduct.xml."""
