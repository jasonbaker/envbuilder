Command-line Reference
========================

.. program:: envb

Global command-line options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -h, --help

    Print out help and exit.

.. cmdoption:: -p <parcels>, --parcels=<parcels>

    Select the parcels to run the selected command over.

.. cmdoption:: -v, --verbose

    Verbose output.

.. cmdoption:: -N, --no-deps

    If a command has dependencies, do not install them automatically.

.. cmdoption:: -U, --upgrade

    Upgrade a command's dependencies whether or not they need to be updated.
    Note that dependencies may be updated anyway if a command requires a newer
    version of a dependency you already have installed.

Checkout
~~~~~~~~~~~~~~

Check all parcels out from VCS.

Required Parcel Options
++++++++++++++++++++++++++

**checkout** - The command-line commands to run that will check this parcel out.

Extra Dependencies
+++++++++++++++++++++

None

Extra Command-line Options
+++++++++++++++++++++++++++

None

Setup
~~~~~~~~~~

Run setup on all parcels.

Required Parcel Options
++++++++++++++++++++++++

**setup** - The command-line commands to run that will set this parcel up.

Extra Dependencies
++++++++++++++++++++

None

Extra Command-line Options
++++++++++++++++++++++++++++

None


