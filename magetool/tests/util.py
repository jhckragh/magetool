import os

import magetool.settings as settings

TEST_DIR = os.path.abspath(os.path.join("..", "app", "code", "local", "Foo"))

def remove_module(namespace, name):
    """Remove a skeleton module and its activation file."""
    os.remove(os.path.join("..", "..", "..", "etc",
                           "modules", "%s_%s.xml" % (namespace, name)))
    os.remove(os.path.join(name, "etc", "config.xml"))
    for directory in settings.directories:
        os.rmdir(os.path.join(name, directory))
    os.rmdir(name)
