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
    	python = '$PWD/bin/python'
    		
    	[[envbuilder]]
    	name = 'envbuilder'
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
  the virtualenv.

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

These are the shell commands that are run when you use ``envbuilder 
setup`` and ``envbuilder checkout`` (respectively).

String Interpolation
~~~~~~~~~~~~~~~~~~~~~~~~~

You'll notice that in this example, we use something called
*string interpolation*.  Every part that begins with a $ is defined
somewhere else in the config file.  The order that it uses to check is
the following:

   1. The current section.
   2. The DEFAULT subsection of the project section.
   3. The project section.
   4. The system's environment variables

To run this, copy the .env file to where you want to build the project and
run the following commands (the output only shows the shell commands, but the
output is left out for brevity's sake)::

    envbuilder co
    --> git clone git://github.com/jasonbaker/envbuilder.git

    envbuilder setup
    --> virtualenv --no-site-packages .
    --> /home/jason/src/envbuilder-src/bin/python setup.py develop
    (From: /home/jason/src/envbuilder-src/envbuilder)

As you can see, the setup command is executed from within the checked out
envbuilder directory (which is why the $cwd variable is required).  You can 
also see that the checkout command was translated in the following steps:

 1. $git_checkout
 2. git clone $url
 3. git clone git://github.com/jasonbaker/envbuilder.git

Questions
------------------

**Can't buildout do everything you're doing?**

Yes, it can (and more).  I'm of the opinion that that isn't necessarily a
good thing.  After all, C++ can do *much* more than Python.  And yet,
people still use Python because programming in it is much simpler.

**What revision control systems do you support?**

Envbuilder currently has support for svn (via an svn_checkout default
option).  However, you can theoretically use any revision control system
that has a command-line interface.

**Does envbuilder have to be used for Python?**

Envbuilder was designed to be flexible enough that it could *theoretically*
be used with other languages, but this has not yet been tried.  Any saps 
(aka "open source developers") willing to test this out are encouraged
to do so!
