from lxml import etree

from magetool.libraries.cls import Class
from magetool.libraries.util import find_or_create

class GlobalClass(Class):
    """Base class for 'global classes'.

    (Global classes are classes whose presence must be registered
    within the <global> element of a module's configuration file in
    order to be loaded by Mage.)

    """
    def __init__(self, superclass=None, override=False):
        """Initialize the global class, e.g., by storing run-time
        arguments and by retrieving and preparing the module's
        configuration file.

        Args:
            superclass: Full name of the global class's superclass,
                        e.g., "Mage_Rss_Block_Abstract".
            override: Whether this global class should override its
                      superclass.

        """
        Class.__init__(self)
        self.superclass = self._infer_super(superclass)
        self.override = override
        self.type_tag = self.type + "s"
        self.config = self.get_config()
        self._prepare_config()
        self.xpath = "/config/global/" + self.type_tag
        self.type_elem = self.config.xpath(self.xpath)[0]

    def _infer_super(self, superclass):
        """Infer the global class's superclass if none is supplied."""
        if superclass is None:
            end = "Template" if self.type == "block" else "Abstract"
            superclass = "Mage_Core_%s_%s" % (self.type.capitalize(), end)
        return superclass

    def _prepare_config(self):
        """Prepare the module's configuration file for class registration.

        To make Mage aware that the module has one or more global
        classes of type self.type, the module's configuration file
        must have a <global> element. Furthermore, this <global>
        element must have a sub element whose tag matches the type of
        the global class. If these elements don't exist, we create
        them.

        """
        global_ = find_or_create(self.config, "global")
        type_ = find_or_create(global_, self.type_tag)

    def create(self, name):
        """Create the global class.

        Dispatch requests to create an empty global class and update
        the module's configuration file.

        Args:
            name: Name of the global class, e.g., "Product" or
                  "ActivePoll".

        """
        self.name = name
        self._create_class(name, self.superclass)
        if self.override:
            self._override()
        else:
            self.register()
        self.put_config(self.config)

    def register(self):
        """Tell Mage that the module has one or more self.type global
        classes.

        """
        tag = self.module.name.lower()
        if not self.config.xpath(self.xpath + "/" + tag):
            group = etree.SubElement(self.type_elem, self.module.name.lower())
            class_ = etree.SubElement(group, "class")
            class_.text = "%s_%s_%s" % (self.module.namespace,
                                        self.module.name,
                                        self.type.capitalize())

    def _override(self):
        """Tell Mage that this global class overrides self.superclass."""
        substrings = self.superclass.split("_")
        tags = {"module": substrings[1].lower(),
                "name": "_".join(substrings[3:]).lower()} # e.g., product_view
        elems = "/rewrite/".join((tags["module"], tags["name"]))
        if not self.config.xpath(self.xpath + "/" + elems):
            module = find_or_create(self.type_elem, tags["module"])
            rewrite = find_or_create(module, "rewrite")
            name = etree.SubElement(rewrite, tags["name"])
            name.text = "%s_%s_%s_%s" % (self.module.namespace,
                                         self.module.name,
                                         self.type.capitalize(),
                                         self.name)
