from magetool.libraries.globalclass import GlobalClass
from string import Template

class Model(GlobalClass):
    """Class which represents Mage models, i.e., PHP classes which go in
    a module's Model/ directory.

    """
    def _fill_template(self, name, superclass):
        """See _fill_template in magetool.libraries.cls."""
        template = Template(self.template)
        template = template.substitute(namespace=self.module.namespace,
                                       module_name=self.module.name,
                                       name=name,
                                       superclass=superclass,
                                       group=self.module.name.lower(),
                                       name_lower=name.lower())
        return template

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
