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
package.  To try it out, you simply need to use the following .env file::

    [project]
    parcels = 'site-commands'
    
        [[site-commands]]
        checkout = 'git clone git@github.com:jasonbaker/envb-site-commands.git'


Reference
---------------

.. automodule:: envbuilder.command
    :members:
