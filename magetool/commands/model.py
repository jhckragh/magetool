from lxml import etree
from magetool.libraries.globalclass import GlobalClass
from magetool.libraries.util import find_or_create
from magetool.templates.resource import string as resource_template
from string import Template

class Model(GlobalClass):
    """Class which represents Mage models, i.e., PHP classes which go in
    a module's Model/ directory.

    """
    def __init__(self, superclass=None, override=False, table=None):
        GlobalClass.__init__(self, superclass, override)
        self.table = table

    def _fill_template(self, name, superclass):
        """See _fill_template in magetool.libraries.cls."""
        end = name.lower().split("_")[-1]
        template = Template(self.template)
        template = template.substitute(namespace=self.module.namespace,
                                       module_name=self.module.name,
                                       name=name,
                                       superclass=superclass,
                                       group=self.module.name.lower(),
                                       name_lower=name.lower(),
                                       end=end)
        return template

    def _register_resource(self, name):
        """Tell Mage that the module has one or more resource models."""
        GlobalClass.register(self)
        tag = self.module.name.lower()
        group = self.config.xpath(self.xpath + "/" + tag)[0]
        group_mysql4 = group.tag + "_mysql4"
        resource_model = find_or_create(group, "resourceModel")
        resource_model.text = group_mysql4
        group_mysql4 = find_or_create(group, group_mysql4)
        class_ = find_or_create(group_mysql4, "class")
        class_.text = "%s_%s_%s_Mysql4" % (self.module.namespace,
                                           self.module.name,
                                           self.type)
        entities = find_or_create(group_mysql4, "entities")
        name_lower = find_or_create(entities, name.lower())
        table = find_or_create(name_lower, "table")
        if self.table is None:
            table.text = self.module.name.lower() + "_" + name_lower.tag
        else:
            table.text = self.table

    def create(self, name):
        """Create the model and its resource."""
        self._register_resource(name)
        GlobalClass.create(self, name)
        self.template = resource_template
        name = "Mysql4_" + name # We prepend this string so _create_class()
                                # will create a directory called "Mysql4"
                                # in the Model/ directory.
        self._create_class(name, "Mage_Core_Model_Mysql4_Abstract")

    @staticmethod
    def help():
        print """Usage: magetool [OPTION]... (create|register) model [NAME]

Options:
  -s, --superclass=SUPERCLASS  Make the model extend SUPERCLASS.
                               Default: Mage_Core_Model_Abstract.

  -o, --override               Tell Mage that the model overrides
                               its superclass (use in conjunction
                               with --superclass=SUPERCLASS.)

Examples:
  magetool create model Data
        Define a PHP class in Model/Data.php and update the module's
        configuration accordingly.

  magetool -s Mage_Customer_Model_Address_Abstract create model Address
        Define a PHP class in Model/Address.php which extends the class
        Mage_Customer_Model_Address_Abstract and update the module's
        configuration file accordingly.

  magetool -os Mage_Customer_Model_Customer create model Customer
        Define a PHP class in Model/Customer.php which extends and overrides
        Mage_Customer_Model_Customer.

  magetool register model
        Update the module's configuration file to tell Mage that the module
        has one or more model classes."""
