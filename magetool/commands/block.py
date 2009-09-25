# Copyright (c) 2009, Jacob Kragh
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials
#    provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from magetool.libraries.globalclass import GlobalClass

class Block(GlobalClass):
    """Class representing Mage blocks, i.e., PHP classes which go in
    a module's Block/ directory.

    """
    @staticmethod
    def help():
        """Print a help message describing this command."""
        print """Usage: magetool [OPTION]... [create|register] block [NAME]

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
