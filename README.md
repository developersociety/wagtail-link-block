# Wagtail Link Block

A link block to use as part of other StructBlocks which lets the user choose a link either to a
Page (with an optional anchor), Document, external URL, Email, telephone or anchor within the
current page and whether or not they want the link to open in a new window.

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
{% if self.link.get_url %}
    <a href="{{ self.link.get_url }}" {% if self.link.new_window %}target="_blank" rel="noopener noreferrer"{% endif %}>
        {{ self.text }}
    </a>
{% endif %}
```

`get_url` returns `None` when there's no link to render (no link type chosen, or the chosen page
or document has been deleted), so wrap the link in `{% if %}` to avoid `href="None"`.

Using `{% include_block self.link %}` renders a plain link with the default
`blocks/link_block.html` template, which outputs nothing when there's no URL.

## Extending

`LinkBlock` can be subclassed to add your own link types, or change how an existing type is
built or validated, without copying `get_url()` or `clean()`.

For a link type called `<type>`:

- `URLValue.get_<type>_url()` returns the URL for that type, or `None` if there isn't one.
  `get_url()` calls it for the selected type.
- `LinkBlock.clean_<type>(clean_values)` validates that type, and returns a dict of
  `{field_name: ErrorList([...])}` (empty if valid). Without it, `clean()` only checks that the
  selected type has a value.
- `LinkBlock.get_url_field_default_values()` returns the empty value for each link type's field.
  `clean()` uses it to clear the fields of the types that weren't selected.

To add a new type, you also need to add its field, and redefine the `link_to` choices to include
it. For example, a relative URL type:

```python
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, ChoiceBlock
from wagtail_link_block.blocks import LinkBlock, URLValue


class MyURLValue(URLValue):
    def get_relative_url_url(self):
        return self.get("relative_url") or None


class MyLinkBlock(LinkBlock):
    link_to = ChoiceBlock(
        choices=[
            ("page", _("Page")),
            ("file", _("File")),
            ("custom_url", _("Custom URL")),
            ("relative_url", _("Relative URL")),
            ("email", _("Email")),
            ("anchor", _("Anchor")),
            ("phone", _("Phone")),
        ],
        required=False,
        classname="link_choice_type_selector",
        label=_("Link to"),
    )
    relative_url = CharBlock(max_length=300, required=False, label=_("Relative URL"))

    class Meta:
        value_class = MyURLValue

    def get_url_field_default_values(self):
        defaults = super().get_url_field_default_values()
        defaults["relative_url"] = ""
        return defaults
```

The admin only shows and hides the fields of the built-in link types, so a field added by a
subclass is always shown.
