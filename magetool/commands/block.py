from magetool.libraries.globalclass import GlobalClass

class Block(GlobalClass):
    """Class representing Mage blocks, i.e., PHP classes which go in
    a module's Block/ directory.

    """
    @staticmethod
    def help():
        """Print a help message describing this command."""
        print """Usage: magetool [OPTION]... (create|register) block [NAME]

Options:
  -s, --superclass=SUPERCLASS  Make the block extend SUPERCLASS.
                               Default: Mage_Core_Block_Template.

  -o, --override               Tell Mage that the block overrides
                               its superclass (use in conjunction
                               with --superclass=SUPERCLASS.)

Examples:
  magetool create block Product
        Define a PHP class in Block/Product.php and update the module's
        configuration accordingly.

  magetool -s Mage_Catalog_Block_Product_View_Type_Simple create block Simple
        Define a PHP class in Block/Simple.php which extends the class
        Mage_Catalog_Block_Product_View_Type_Simple and update the module's
        configuration file accordingly.

  magetool -os Mage_Catalog_Block_Product_View_Type_Simple create block Simple
        Define a PHP class in Block/Simple.php which extends and overrides
        Mage_Catalog_Block_Product_View_Type_Simple.

  magetool register block
        Update the module's configuration file to tell Mage that the module
        has one or more block classes."""
