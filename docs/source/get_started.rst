Getting started
===============

Installation
------------

fflogsapi is available as a `PyPi package <https://pypi.org/project/fflogsapi/>`_. You can install it with pip:

.. code-block:: sh

    # install the latest version of fflogsapi
    python3 -m pip install fflogsapi
    # install fflogsapi with development and test tools
    python3 -m pip install fflogsapi[dev,test]

If you'd like to install from source, it is available on `GitHub <https://github.com/halworsen/fflogsapi>`_.

Getting API credentials
-----------------------

fflogsapi requires you to create an API client before use. For information on how to get a client ID and client secret,
read `the official FF Logs API documentation <https://articles.fflogs.com/help/api-documentation>`_.

.. note::
    If you're looking to access private information, you must use fflogsapi in user mode,
    which may require special setup when creating the API client. For more information, see :doc:`user_flow`.

Using the client
----------------

You can start using the client by importing ``FFLogsClient`` from the ``fflogsapi`` package.

.. code-block:: python

    from fflogsapi import FFLogsClient
    client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)

For select examples on how the client can be used, see :doc:`examples`.
