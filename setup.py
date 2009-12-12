#!/usr/bin/env python

from distutils.core import setup

setup(name="magetool",
      version="0.1.6",
      description="CLI tool to automate repetitive tasks in Mage development.",
      author="Jacob Kragh",
      author_email="jhckragh@gmail.com",
      url="http://jhckragh.github.com/magetool/",
      license="BSD",
      packages=["magetool", "magetool.commands", "magetool.libraries",
                "magetool.templates"],
      scripts=["magetool/magetool"],
      classifiers=["Programming Language :: Python",
                   "Programming Language :: Python :: 2.6",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Topic :: Software Development",
                   "Topic :: Software Development :: Code Generators"],
      long_description="""\
CLI utility for automating common tasks in Mage module development
------------------------------------------------------------------

Supports
 - Creating and activating modules
 - Creating and registering controllers, blocks, helpers, and models
 - Creating block/helper/model overrides

This program requires lxml.
"""
      )
