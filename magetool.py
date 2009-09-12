#!/usr/bin/env python

__version__ = "0.1.0"

from optparse import OptionParser

def main():
    usage = "usage: %prog COMMAND [ARGS] [OPTION]"
    version = "%prog version " + __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-o", action="store_true", dest="override", default=None,
                      help="in conjunction with 'magetool -s SUPERCLASS " +
                      "create [block|model|helper]', tell Mage that the " +
                      "created class overrides SUPERCLASS.")
    parser.add_option("-s", dest="superclass",
                      help="extend SUPERCLASS.", metavar="SUPERCLASS")
    parser.add_option("-r", dest="router",
                      help="when creating a route for the module " +
                      "use ROUTER (standard, admin, or default).",
                      metavar="ROUTER")

    options, args = parser.parse_args()
    if not len(args) > 1:
        parser.error("incorrect number of arguments")
    kwargs = dict([(k, v) for k, v in options.__dict__.items()
                  if not k.startswith("__") and v != None])

    method, module = [arg.lower() for arg in args[:2]]
    cls = module.capitalize()
    module_import = "from commands.%s import %s as cls" % (module, cls)
    try:
        exec module_import
        cls = cls(**kwargs)
    except ImportError:
        parser.error("command %s not implemented" % module)
    getattr(cls, method)(*args[2:])

if __name__ == "__main__":
    main()
