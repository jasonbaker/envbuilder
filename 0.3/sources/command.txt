command
===============

Writing your own envbuilder commands in Python
-------------------------------------------------

Hello world
~~~~~~~~~~~~~~~

Here is the command to write a hello world command using envbuilder::

    from envbuilder.command import Command
    from envbuilder.sh import notify

    class hello(Command):
        """
        Print hello world.
        """
        name = 'hello'
        def run(self, args, config):
            notify('Hello, world!')

This command is actually stored in the `envb-site-commands <http://github.com/jasonbaker/envb-site-commands>`_
package.  To try it out, you simply need to use the following .env file:

.. code-block:: ini

    [project]
    parcels = 'site-commands'
    
        [[site-commands]]
        checkout = 'git clone git@github.com:jasonbaker/envb-site-commands.git'

To access non-builtin commands, envbuilder uses a dot notation.  The hello
command in site-commands is stored in hello.py.  If we wanted to use this
in Python code, we would do something like the following::

    import hello
    hello_cmd = hello.hello()

The important part is the "hello.hello".  This is the name that Python uses
once a module has been imported.  Envbuilder will allow the same syntax.
Thus, to call the hello command, you would do the following:

.. code-block:: bash

    envb hello.hello
    > Hello, world!

You are even provided a basic help command (though it only shows the default
arguments that envbuilder takes).

Using a shell command
~~~~~~~~~~~~~~~~~~~~~~~

Envbuilder will allow you to run any arbitrary shell command easily.  Let's
modify the hello command to echo hello from the shell instead of using the
notify function.  This depends on the :func:`~envbuilder.sh.sh` function.

.. code-block:: python

    from envbuilder.command import Command
    from envbuilder.sh import sh

    class hellosh(Command):
        """
        Print hello world.
        """
        name = 'hello'
        def run(self, args, config):
            sh("echo 'Hello, world!'")

If we run this, we get the following output:

.. code-block:: bash

    envb hello.hellosh
    > echo 'Hello, world!'
    -> (From: /home/jason/src/interface_dev)
    Hello, world!

That was easy, wasn't it?

Running a webserver
~~~~~~~~~~~~~~~~~~~~~~~

You can even run a webserver under envbuilder::


    class helloweb(Command):
        """
        Run a webserver that prints hello world
        """
        name='helloweb'
        def run(self, args, config):
            import cherrypy
            class HelloWorld(object):
                def index(self):
                    return 'Hello, world!'
                index.exposed=True
            cherrypy.quickstart(HelloWorld())
    
There's just one problem:

.. code-block:: bash

    envb hello.helloweb
    Traceback (most recent call last):
      File "/home/jason/.virtualenvs/main/bin/envb", line 8, in <module>
        load_entry_point('envbuilder==0.3.0c2.dev', 'console_scripts', 'envb')()
      File "/home/jason/src/envbuilder/envbuilder/run.py", line 34, in main
        command.main(config.args, config)
      File "/home/jason/src/envbuilder/envbuilder/command.py", line 130, in main
        self.run(args, config)
      File "./envb-site-commands/hello.py", line 26, in run
        import cherrypy
    ImportError: No module named cherrypy

We don't know if the user has cherrypy installed or not!

Dependency management
~~~~~~~~~~~~~~~~~~~~~~~~

Believe it or not, python dependencies aren't terribly difficult to deal with.  In
this case, we just need to change the above command to this::

    class helloweb(Command):
        """
        Run a webserver that prints hello world
        """
        name='helloweb'
        py_dependencies=['cherrypy']
        def run(self, args, config):
            import cherrypy
            class HelloWorld(object):
                def index(self):
                    return 'Hello, world!'
                index.exposed=True
            cherrypy.quickstart(HelloWorld())

The py_dependencies attribute is a list of dependencies that must be installed for
a command to run.  If you run the command again:

.. code-block:: bash

     envb hello.helloweb

You should get a cherrypy webserver running and serving on `<http://127.0.0.1:8080>`_.

Reference
---------------

.. automodule:: envbuilder.command
    :members:
