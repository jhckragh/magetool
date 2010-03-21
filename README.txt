# Magetool #

Magetool[1] is an open-source CLI utility designed to automate common
tasks in Magento[2] module development.

Often when you're developing a custom module you find yourself
performing certain tasks over and over again, e.g.,

 * Creating a directory structure for the module and activating it

 * Typing out long class names when creating a new controller, block,
   model, or helper

 * Editing the module's configuration file the first time you create a
   controller, block, model, or helper

Because these tasks are repetitive and error-prone, they should be
automated. Magetool does just that.


## Install ##

To install Magetool, type the following command at the terminal:

    python setup.py build

Then, as root, run

    python setup.py install


### Prerequisites ###

To run Magetool you need to have the following software installed:

 * Python 2.6
 * lxml[3]

On Ubuntu you can install these dependencies through apt:

    sudo apt-get install python2.6 python-lxml


## Example usage ##

Here's a sample Magetool workflow:

    cd ~/public_html/magento/app/code/local/Company
    magetool create module HelloWorld                 (1)
    cd HelloWorld
    magetool create controller index                  (2)

 1. This creates and activates a new module called HelloWorld.

 2. This defines a skeleton PHP class in controllers/IndexController.php
   and updates the module's configuration file accordingly.

See the file docs/usage.txt for more on what Magetool can do.


## Discussion and support ##

Found a bug? Let me know by creating a new issue on GitHub[4]. Feedback
is always welcome; drop me a line at jhckragh [at] gmail [dot] com.


## Bugs ##

Overriding abstract classes is unsupported. (For details on how to do
this manually, see the community forum[5].)


## Links ##

[1] <http://jhckragh.github.com/magetool/>
[2] <http://www.magentocommerce.com/>
[3] <http://codespeak.net/lxml/index.html#download>
[4] <http://github.com/jhckragh/magetool/issues>
[5] <http://www.magentocommerce.com/boards/viewthread/18494/#t151509>


## Legal ##

Magento is a trademark of Irubin Consulting Inc. Python is a trademark
or registered trademark of the Python Software Foundation. Ubuntu is a
registered trademark of Canonical Ltd.

Magetool is not in any way affiliated with or endorsed by any of these
trademark owners.
