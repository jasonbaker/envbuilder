Command
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

.. code-block:: sh

    envb hello.hello

You are even provided a basic help command (though it only shows the default
arguments that envbuilder takes).

Reference
---------------

.. automodule:: envbuilder.command
    :members:
