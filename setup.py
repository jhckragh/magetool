#!/usr/bin/env python

from distutils.core import setup

setup(name="Magetool",
      version="0.1.0",
      description="CLI tool to automate repetitive tasks in Mage development.",
      author="Jacob Kragh",
      author_email="jhckragh@gmail.com",
      license="BSD",
      packages=["magetool", "magetool.commands", "magetool.libraries",
                "magetool.templates"],
      package_dir={"magetool": "src/magetool"},
      scripts=["src/magetool/magetool"],
      )
