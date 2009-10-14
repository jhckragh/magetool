from magetool.libraries.globalclass import GlobalClass

class Helper(GlobalClass):
    """Class which represents Mage helpers, i.e., PHP classes which go in
    a module's Helper/ directory.

    """
    @staticmethod
    def help():
        print """Usage: magetool [OPTION]... (create|register) helper [NAME]

Options:
  -s, --superclass=SUPERCLASS  Make the helper extend SUPERCLASS.
                               Default: Mage_Core_Helper_Abstract.

  -o, --override               Tell Mage that the helper overrides
                               its superclass (use in conjunction
                               with --superclass=SUPERCLASS.)

Examples:
  magetool create helper Data
        Define a PHP class in Helper/Data.php and update the module's
        configuration accordingly.

  magetool -s Mage_Checkout_Helper_Data create helper Data
        Define a PHP class in Helper/Data.php which extends the class
        Mage_Checkout_Helper_Data and update the module's configuration
        file accordingly.

  magetool -os Mage_Checkout_Helper_Data create helper Data
        Define a PHP class in Helper/Data.php which extends and overrides
        Mage_Checkout_Helper_Data.

  magetool register helper
        Update the module's configuration file to tell Mage that the module
        has one or more helper classes."""
