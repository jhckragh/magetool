from lxml import etree

from magetool.libraries.cls import Class

class Controller(Class):
    """Class representing Mage controllers, i.e., PHP classes which go
    in a module's controllers/ directory and whose names end with
    'Controller'.

    """
    def __init__(self, front_name=None, override=False, superclass=None,
                 router=None):
        """Initialize the controller, e.g., by storing run-time arguments.

        Args:
            front_name: The string to use as the module's
                        frontName. By convention this string
                        is the module's name, lower-cased.
            override: Whether the module's controller(s) should
                      override the controller(s) of the module
                      to which its superclass belongs.
            superclass: Full name of the controller's superclass,
                        e.g., "Mage_Adminhtml_Controller_Action".
            router: Name of the front controller router to use.
                    Available routers are "standard", "admin", and
                    "default".

        """
        Class.__init__(self)
        self.front_name = front_name or self.module.name.lower()
        self.override = override
        self.superclass = superclass or "Mage_Core_Controller_Front_Action"
        self.router = router or "standard"

    def _format_name(self, name):
        """Format a name according to the naming convention for controllers.

        Args:
            name: The name of the controller, with or without the
                  'Controller' suffix, e.g., 'IndexController' or
                  'Tracking'.

        """
        suffix = "controller"
        if name.lower().endswith(suffix):
            name = name[:-len(suffix)]
        substrings = name.split("_")
        substrings[-1] = substrings[-1].capitalize() + "Controller"
        name = "_".join(substrings)
        return name

    def _add_route(self, elem):
        """Add a <routers> element with associated sub elements to elem.

        Args:
            elem: An lxml.etree._Element object mapping to a <frontend>
                  element.

        Return:
            An lxml.etree._Element object.

        """
        xpath = "/config/%s/routers/%s"
        route = elem.xpath(xpath % (elem.tag, self.module.name.lower()))
        if route:
            return # Bail (assume that a route already exists).

        routers = elem.find("routers")
        if routers is None:
            routers = etree.SubElement(elem, "routers")
        group = etree.SubElement(routers, self.module.name.lower())
        use = etree.SubElement(group, "use")
        use.text = self.router
        args = etree.SubElement(group, "args")
        module = etree.SubElement(args, "module")
        module.text = "%s_%s" % (self.module.namespace, self.module.name)
        front_name = etree.SubElement(args, "frontName")
        front_name.text = self.front_name
        return elem

    def _add_override(self, elem):
        """Make the module's controller override another module's controllers.

        Given a <frontend> element, create the sub elements necessary to
        make the module's controller(s) override the controller(s) of the
        module to which self.superclass belongs.

        Args:
            elem: An lxml.etree._Element object mapping to a <frontend>
                  element.

        Return:
            An lxml.etree._Element object.

        """
        substrings = self.superclass.split("_")
        super_module = substrings[1].lower()
        super_prefix = "_".join(substrings[:2])

        routers = elem.find("routers")
        if routers is None:
            routers = etree.SubElement(elem, "routers")

        if routers.find(super_module) is not None:
            return # Bail (assume that an override already exists).

        super_module = etree.SubElement(routers, super_module)
        args = etree.SubElement(super_module, "args")
        modules = etree.SubElement(args, "modules")
        group = etree.SubElement(modules, self.module.name.lower())
        group.set("before", super_prefix)
        group.text = "_".join((self.module.namespace, self.module.name))
        return elem

    def create(self, name):
        """Create the controller.

        Dispatch requests to create an empty controller class and
        update the module's configuration file.

        """
        name = self._format_name(name)
        self._create_class(name, self.superclass)
        self.register()

    def register(self):
        """Make Mage aware that this module has controllers to dispatch to.
        
        Update the module's configuration file to configure a route,
        which will allow Mage to dispatch requests to the module's
        controller(s).

        """
        config = self.get_config()
        frontend = config.find("frontend")
        if frontend is None:
            frontend = etree.SubElement(config, "frontend")
        # Now we're sure frontend exists, so we can add sub elements to it.
        if self.override:
            frontend = self._add_override(frontend)
        else:
            frontend = self._add_route(frontend)
        self.put_config(config)

    @staticmethod
    def help():
        print """Usage: magetool [OPTION]... (create|register) controller NAME

Options:
  -f, --frontname=FRONTNAME    Use FRONTNAME as the module's frontName.
                               Default: The module's name, lower-cased.

  -o, --override               Tell Mage that the controller overrides
                               the controllers of the module to which
                               its superclass belongs (use with
                               --superclass=SUPERCLASS.)

  -s, --superclass=SUPERCLASS  Make the controller extend SUPERCLASS.
                               Default: Mage_Core_Controller_Front_Action.

  -r, --router=ROUTER          Use internal router ROUTER to route
                               requests to this module. Available
                               routers are: standard, admin, and
                               default. Default: standard.

Examples:
  magetool create controller index
        Create a file called IndexController.php in controllers/ and configure
        a route in etc/config.xml so Mage can dispatch requests to the module's
        controller(s).

  magetool -s Mage_Adminhtml_Controller_Action create controller OrderController
        Define a PHP class in controllers/OrderController.php which extends
        the class Mage_Adminhtml_Controller_Action.

  magetool -os Mage_Downloadable_DownloadController create controller Over
        Define a PHP class in controllers/OverController.php which extends
        and overrides the class Mage_Downloadable_DownloadController.

  magetool -r admin create controller order
        Define a PHP class in controllers/OrderController.php and configure
        a route in etc/config.xml using the 'admin' router.

  magetool -r admin -s Mage_Adminhtml_IndexController create controller order
        Define a PHP class in controllers/OrderController.php which extends
        the class Mage_Adminhtml_IndexController and configure a route in
        etc/config.xml using the 'admin' router.

  magetool register controller
        Configure a route in etc/config.xml so Mage can dispatch
        requests to the module's controller(s)."""
