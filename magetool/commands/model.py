from string import Template

from lxml import etree

from magetool.libraries.globalclass import GlobalClass
from magetool.libraries.util import find_or_create
from magetool.templates.resource import string as resource_template

class Model(GlobalClass):
    """Class which represents Mage models, i.e., PHP classes which go in
    a module's Model/ directory.

    """
    def __init__(self, superclass=None, override=False, table=None,
                 id_field_name=None):
        GlobalClass.__init__(self, superclass, override)
        self.table = table
        self.id_field_name = id_field_name

    def _fill_template(self, name, superclass):
        """See _fill_template in magetool.libraries.cls."""
        end = name.lower().split("_")[-1]
        id_field_name = self.id_field_name or end + "_id"
        template = Template(self.template)
        template = template.substitute(namespace=self.module.namespace,
                                       module_name=self.module.name,
                                       name=name,
                                       superclass=superclass,
                                       group=self.module.name.lower(),
                                       name_lower=name.lower(),
                                       end=end,
                                       id_field_name=id_field_name)
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
        table.text = self.table or group.tag + "_" + name_lower.tag

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
  -i, --id-field-name=NAME     Make the model's resource use NAME
                               as the column which uniquely identifies
                               rows in the model's table. Default:
                               Concatenation of the end of the model's
                               name and the string "_id" (a convention
                               many core module's follow).

  -o, --override               Tell Mage that the model overrides
                               its superclass (use in conjunction
                               with --superclass=SUPERCLASS).

  -s, --superclass=SUPERCLASS  Make the model extend SUPERCLASS.
                               Default: Mage_Core_Model_Abstract.

  -t, --table=TABLENAME        Tell Mage that the model's entity
                               corresponds to the table named
                               TABLENAME. Default: Concatenation
                               of the module name and the model's
                               name (a convention many core
                               module's follow).

Examples:
  magetool create model Data
        Define a PHP clas in Model/Data.php. Also, create a resource
        model at Model/Mysql4/Data.php and update the module's
        configuration file accordingly.

  magetool -t blog_meta create model Data
        Define a PHP clas in Model/Data.php. Also, create a resource
        model at Model/Mysql4/Data.php. Finally, update the module's
        configuration file to tell Mage that the model's entity
        corresponds to a table named blog_meta.

  magetool -i id create model Data
        Define a PHP clas in Model/Data.php. Also, create a resource
        model at Model/Mysql4/Data.php which uses the column named
        'id' to identify table rows uniquely. Finally, update the
        module's configuration file accordingly.

  magetool -s Mage_Customer_Model_Address_Abstract create model Address
        Define a PHP class in Model/Address.php which extends
        Mage_Customer_Model_Address_Abstract. Also, create a resource
        for the model at Model/Mysql4/Address.php and update the
        module's configuration file accordingly.

  magetool -os Mage_Customer_Model_Customer create model Customer
        Define a PHP class in Model/Customer.php which extends and
        overrides Mage_Customer_Model_Customer. Also, create a
        resource for the model at Model/Mysql4/Customer.php and update
        the module's configuration file accordingly.

  magetool register model
        Update the module's configuration file to tell Mage that the module
        has one or more model classes."""
