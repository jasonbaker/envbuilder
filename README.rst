
**NOTE**:  These are the docs for the version of envbuilder in git.  For
documentation on the last release, see the `pypi_page <http://pypi.python.org/pypi/envbuilder/>`_.

.. split here

Envbuilder is a system for automatically building virtualenvs in Python.
To do this, it uses a .env config file to define *parcels*, which are
individual pieces of software to be checked out and installed into
the virtualenv.

It is mainly tested under Linux, but it should work under any platform that
supports unix-y commands (including cygwin).  In fact, you might even be
able to make one config file work on both Windows and \*nix if you're
careful.

Envbuilder has a few goals:

 * **Transparency** - You should understand what your build is doing and
   how it works.
 * **Developer-friendly** - Although envbuilder is perfectly fine for production
   deployment, it is primarily intended to make work environments for developers.
 * **Dynamic** - Envbuilder should be able to work with a variety of technologies,
   languages, and frameworks.  Developers shouldn't be limited to a narrowly defined
   set of technologies.  And neither should their tools!
 * **VCS-neutral** - Envbuilder will work with your shiny new DVCS out of the box.
   In fact, it will work with any VCS that has a command-line interface.  Use it
   with hg, git, bzr, SVN, or CVS (if you're a masochist).

For more information, see the `envbuilder documentation <http://jasonbaker.github.com/envbuilder/0.3>`_.

Installing
---------------

For the latest stable version, the easiest way to install envbuilder is
through easy_intall::

    easy_install envbuilder

You may also install the current development version using easy_install::

    easy_install envbuilder==dev

Or you may `download it directly <http://github.com/jasonbaker/envbuilder/zipball/master>`_.

Support
------------------

If you have any issues using envbuilder, feel free to open an issue on the
`issue tracker <http://github.com/jasonbaker/envbuilder/issues>`_ or stop
by the `support mailing list <http://groups.google.com/group/envbuilder>`_.


Release Notes
------------------

0.3.0
~~~~~~~~~~~~~~~~~~

Compatibility issues:

* Most commands have been moved to envb-site-commands.

Other improvements:
* Command handling has been revamped to allow for more plugability
* Support for envb-site-commands
* Dependency handling for commands
* Lots of other miscellaneous fixes.

0.2.2
~~~~~~~~~~~~~~~~~~

* Requiring configobj 4.7.2 as it fixes some important bugs.

0.2.1
~~~~~~~~~~~~~~~~~~

* Adding a fix so that clean_pyc doesn't delete files in the python2.6
  directory.

0.2.0
~~~~~~~~~~~~~~~~~~

 * Added a couple of examples.  If you already have a working envbuilder
   installation, there is no requirement to upgrade.

0.2.0b2
~~~~~~~~~~~~~~~~~~

 * Required the correct version of ConfigObj.  This update is not necessary
   if you already have a working envbuilder installation.

0.2.0b1
~~~~~~~~~~~~~~~~~~

 * Readded the envbuilder entry point as renaming it caused some strange
   issues.

0.2.0b
~~~~~~~~~~~~~~~~~~

 * The name option on parcels is now set automatically from the subsection
   name.
 * Added percent (command) variables.
 * Added the CWD built-in variable.
 * Added a dir option for parcels that defaults to the name.
 * Removed the test command.  This can now be done with custom commands.
 * The envbuilder entry point is now envb.

