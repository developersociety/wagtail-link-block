# Wagtail Link Block

A link block to use as part of other StructBlocks which lets the user choose a link either to a
Page, Document, external URL, Email, telephone or anchor within the current page and whether or
not they want the link to open in a new window.

It hides the unused fields, making the admin clearer and less cluttered.

## Installation

Using [pip](https://pip.pypa.io/):

```console
$ pip install wagtail-link-block
```

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_link_block",
    # ...
]
```

## Usage

To use in a block

```python
from wagtail_link_block.blocks import LinkBlock

class MyButton(StructBlock):
    text = CharBlock()
    link = LinkBlock()

    class Meta:
        template = "blocks/my_button_block.html"
```

And create the template `blocks/my_button_block.html`:

```html
<a href="{{ self.link.get_url }}" {% if self.link.new_window %}target="_blank"{% endif %}>
    {{ self.text }}
</a>
```
