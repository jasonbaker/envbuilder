
**NOTE**:  These are the docs for the version of envbuilder in git.  For
documentation on the last release, see the `pypi_page <http://pypi.python.org/pypi/envbuilder/>`_.

.. split here

.. contents:: Table of Contents
    :depth: 3

envbuilder
===============

Envbuilder is a system for automatically building virtualenvs in Python.
To do this, it uses a .env config file to define *parcels*, which are
individual pieces of Python software to be checked out and installed into
the virtualenv.

It is mainly tested under Linux, but it should work under any platform that
supports unix-y commands (including cygwin).  In fact, you might even be
able to make one config file work on both Windows and \*nix if you're
careful.

Installing
-------------

To install envbuilder, you have two options:  installing from git or installing
from pypi.  If you would like to install via git, use the following set of
commands::

    git clone git://github.com/jasonbaker/envbuilder.git
    cd envbuilder
    python setup.py install 
    # if you plan on making changes to envbuilder, use this command:
    python setup.py develop

If you would like to install from pypi, you should use `pip <http://pypi.python.org/pypi/pip/0.6.1>`_::

    pip install envbuilder

The .env file
------------------

The .env's file format is similar to the .ini file format, but there are
some major differences.  The best way to illustrate this is with an example.
The following will make a virtualenv with envbuilder installed.  There's
probably not any good reason to do this other than to provide an easy
example for the README::

    [project]
    parcels = 'envbuilder', # Note the comma

        [[DEFAULT]]
        git_checkout = 'git clone $url'
        python = '$CWD/bin/python'
		
        [[envbuilder]]
        dir = 'envbuilder'
        url = 'git://github.com/jasonbaker/envbuilder.git'
        setup = '$python setup.py develop'
        checkout = '$git_checkout'



The sections
~~~~~~~~~~~~~~~~~~

project
++++++++++++++++++++

This section is the top-level section.  It has two possible options:

* **parcels** - These are the parcels to be installed in the order they are
  to be installed.  This is a list delimited by commas.

* **requires** - This is a list of packages that will be easy_installed into
  the virtualenv when setup is run.  If the -U flag is passed in to setup,
  these will be upgraded.

DEFAULT
+++++++++++++++++++++

In this particular example, this particular section is probably
not very meaningful.  However, when using multiple parcels, it is useful to
define default values to be used in each section.  Note that these values
are currently only used in string interpolation.  There is no "inheritance"
concept.

envbuilder
+++++++++++++++++++++

Here's where we actually define a parcel.  There are 
currently only two options that need to be defined: setup and checkout.

These are the shell commands that are run when you use ``envb 
setup`` and ``envb checkout`` (respectively).

String Interpolation
~~~~~~~~~~~~~~~~~~~~~~~~~

You'll notice that in this example, we use something called
*string interpolation*.  Every part that begins with a $ is defined
elsewhere.  The order that it uses to check is the following:

   1. The current section.
   2. The DEFAULT subsection of the project section.
   3. The project section.
   4. The system's environment variables

To run this, copy the .env file to where you want to build the project and
run the following commands (the output only shows the shell commands, but the
output is left out for brevity's sake)::

    envb co
    --> git clone git://github.com/jasonbaker/envbuilder.git

    envb setup
    --> virtualenv --no-site-packages .
    --> /home/jason/src/envbuilder-src/bin/python setup.py develop
    (From: /home/jason/src/envbuilder-src/envbuilder)

As you can see, the setup command is executed from within the checked out
envbuilder directory (which is why the $CWD variable is required).  You can 
also see that the checkout command was translated in the following steps:

 1. $git_checkout
 2. git clone $url
 3. git clone git://github.com/jasonbaker/envbuilder.git

Custom Commands
---------------------

Now let's add a custom command to this.  Suppose we want to write a command
that can give us the current status of our checked-out git repository.  The
finished .env file will look like this::

    [project]
    parcels = 'envbuilder', # Note the comma
    
    	[[DEFAULT]]
    	git_checkout = 'git clone $url'
    	python = '$CWD/bin/python'
    		
    	[[envbuilder]]
    	dir = 'envbuilder'
    	url = 'git://github.com/jasonbaker/envbuilder.git'
    	setup = '$python setup.py develop'
    	checkout = '$git_checkout'
        
    [commands]
    	[[ status ]]
    	required = True
    	default = 'git status'
    	working_dir = '%dir'
    	help = 'Check the status of all checked-out parcels'

This works much like envbuilder's built in commands.  Each parcel can
override the default behavior by adding an option with the same name
as the command.  For instance, suppose we wanted to keep ``git status``
as the default behavior, but we wanted to make envbuilder's output use
the verbose flag.  We could change the above to this::

    [project]
    parcels = 'envbuilder', # Note the comma
    
    	[[DEFAULT]]
    	git_checkout = 'git clone $url'
    	python = '$CWD/bin/python'
    		
    	[[envbuilder]]
    	dir = 'envbuilder'
    	url = 'git://github.com/jasonbaker/envbuilder.git'
    	setup = '$python setup.py develop'
    	checkout = '$git_checkout'
	update = 'git status -v'
        
    [commands]
    	[[ status ]]
    	required = True
    	default = 'git status'
    	working_dir = '%dir'
    	help = 'Check the status of all checked-out parcels'

A command has the following options:

 * **required** - If this is True and no default is set, an error will
   be raised if a parcel has not defined its own way to run this command
 * **default** - If a parcel does not have its own way of running this
   command, use this instead.
 * **working_dir** - The directory to run this within.
 * **help** - The help text that will be given when ``envb -h`` is
   run.

Note that you may also access a parcel's options by prefixing the name with
a ``%`` instead of a ``$``.  In the above example, ``%dir`` is replaced
with the dir option of the parcel.

Questions
------------------

**Can't buildout do everything you're doing?**

Yes, it can (and more).  I'm of the opinion that that isn't necessarily a
good thing.  After all, C++ can do *much* more than Python.  And yet,
people still use Python because programming in it is much simpler.

**What revision control systems do you support?**

You can theoretically use any revision control system that has a 
command-line interface.  At its most core level, envbuilder is a
framework around the shell (with a focus around building virtualenvs).

**Does envbuilder have to be used for Python?**

Envbuilder was designed to be flexible enough that it could *theoretically*
be used with other languages, but this has not yet been tried.  Any saps 
(aka "open source developers") willing to test this out are encouraged
to do so!

Support
------------------

If you have any issues using envbuilder, feel free to open an issue on the
`issue tracker <http://github.com/jasonbaker/envbuilder/issues>`_ or stop
by the `support mailing list <http://groups.google.com/group/envbuilder>`_.


Release Notes
------------------

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

