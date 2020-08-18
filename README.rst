Wagail LinkBlock
================

A link block to use as part of other StructBlocks which
lets the user choose a link either to a Page, Document,
or external URL, and whether or not they want the link
to open in a new window.

It hides the unused fields, making the admin clearer and less cluttered.

Usage
-----

To install ::

    pip install wagtail-link-block

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


