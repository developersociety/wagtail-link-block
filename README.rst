Wagtail LinkBlock
=================

.. image:: https://github.com/developersociety/wagtail-link-block/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/developersociety/wagtail-link-block/actions/
   :alt: Build Status

.. |PyPI version fury.io| image:: https://badge.fury.io/py/wagtail-link-block.svg
   :target: https://pypi.python.org/pypi/wagtail-link-block/

.. |Licence| image:: https://img.shields.io/github/license/developersociety/wagtail-link-block.svg
   :alt: BSD Licenced

A link block to use as part of other StructBlocks which
lets the user choose a link either to a Page, Document,
external URL, Email, telephone or anchor within the current page
and whether or not they want the link to open in a new window.

It hides the unused fields, making the admin clearer and less cluttered.

Usage
-----

To install:

.. code-block:: console

    $ pip install wagtail-link-block

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "wagtail_link_block",
        # ...
    ]

To use in a block

.. code-block:: python

    from wagtail_link_block.blocks import LinkBlock

    class MyButton(StructBlock):
        text = CharBlock()
        link = LinkBlock()

        class Meta:
            template = "blocks/my_button_block.html"

And the blocks/my_button_block.html

.. code-block:: HTML

    <a href="{{ self.link.get_url }}" {% if self.link.new_window %}target="_blank"{% endif %}>{{ self.text }}</a>

Developing
----------

We're using ``black``, ``isort`` & ``flake8`` for formatting & linting, and there are ``poetry``
commands in the ``Makefile`` for building, etc.
