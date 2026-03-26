"""
The LinkBlock is not designed to be used on it's own - but as part of other blocks.
"""

from copy import deepcopy

from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms.choosers import URLOrAbsolutePathValidator
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    EmailBlock,
    PageChooserBlock,
    StreamBlockValidationError,
    StructBlock,
    StructValue,
)
from wagtail.documents.blocks import DocumentChooserBlock

##############################################################################
# Component Parts - should not be used on their own - but as parts of other
# blocks:


class URLValue(StructValue):
    """
    Get active link used in LinkBlock or CustomLinkBlock if there is one
    """

    def get_url(self):
        link_to = self.get("link_to")
        method = getattr(self, f"get_{link_to}_url", None)
        if method:
            return method()
        return None

    def get_page_url(self):
        page = self.get("page")
        return page.url if page else None

    def get_file_url(self):
        file = self.get("file")
        return file.url if file else None

    def get_custom_url_url(self):
        return self.get("custom_url")

    def get_anchor_url(self):
        anchor = self.get("anchor")
        return "#" + anchor if anchor else None

    def get_email_url(self):
        email = self.get("email")
        return f"mailto:{email}" if email else None

    def get_phone_url(self):
        phone = self.get("phone")
        return f"tel:{phone}" if phone else None

    def get_link_to(self):
        """
        Return link type for accessing in templates
        """
        return self.get("link_to")


class LinkBlock(StructBlock):
    """
    A Link which can either be to a (off-site) URL, to a page in the site,
    or to a document. Use this instead of URLBlock.
    """

    link_to = ChoiceBlock(
        choices=[
            ("page", _("Page")),
            ("file", _("File")),
            ("custom_url", _("Custom URL")),
            ("email", _("Email")),
            ("anchor", _("Anchor")),
            ("phone", _("Phone")),
        ],
        required=False,
        classname="link_choice_type_selector",
        label=_("Link to"),
    )
    page = PageChooserBlock(required=False, classname="page_link", label=_("Page"))
    file = DocumentChooserBlock(required=False, classname="file_link", label=_("File"))
    custom_url = CharBlock(
        max_length=300,
        required=False,
        classname="custom_url_link url_field",
        validators=[URLOrAbsolutePathValidator()],
        label=_("Custom URL"),
    )
    anchor = CharBlock(
        max_length=300,
        required=False,
        classname="anchor_link",
        label=_("#"),
    )
    email = EmailBlock(required=False)
    phone = CharBlock(max_length=30, required=False, classname="phone_link", label=_("Phone"))

    new_window = BooleanBlock(
        label=_("Open in new window"), required=False, classname="new_window_toggle"
    )

    class Meta:
        label = None
        value_class = URLValue
        icon = "fa-share-square"
        form_classname = "link_block"
        form_template = "wagtailadmin/block_forms/link_block.html"
        template = "blocks/link_block.html"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Make a deep copy of the link-to, as we need to pass the
        # 'required' option down to it, and don't want to pollute
        # the other LinkBlocks that are defined on other parent blocks.
        self.child_blocks["link_to"] = deepcopy(self.child_blocks["link_to"])
        self.child_blocks["link_to"].field.required = kwargs.get("required", False)

    def set_name(self, name):
        """
        Over ride StructBlock set_name so label can remain empty in streamblocks
        """
        self.name = name

    def get_url_field_default_values(self):
        """Return a dict mapping each URL-type field name to its empty/default value.

        Subclasses should override this to add new link types, e.g.:
            def get_url_field_default_values(self):
                defaults = super().get_url_field_default_values()
                defaults["relative_url"] = ""
                return defaults
        """
        return {
            "page": None,
            "file": None,
            "custom_url": "",
            "anchor": "",
            "email": "",
            "phone": "",
        }

    def clean_link_type(self, url_type, clean_values):
        """Validate the selected link type's value. Called by clean().

        Dispatches to ``clean_<url_type>(clean_values)`` if such a method
        exists on the class. Otherwise performs the default check that the
        selected type's value is not empty.

        Subclasses can add per-type validation by defining a method, e.g.::

            def clean_relative_url(self, clean_values):
                # custom validation ...
                return {}  # or {field_name: ErrorList([...])}
        """
        method = getattr(self, f"clean_{url_type}", None)
        if method:
            return method(clean_values)
        # Default: check that the selected type has a non-empty value
        if clean_values.get(url_type) in [None, ""]:
            return {
                url_type: ErrorList(
                    ["You need to add a {} link".format(url_type.replace("_", " "))]
                )
            }
        return {}

    def clean(self, value):
        clean_values = super().clean(value)
        errors = {}
        url_default_values = self.get_url_field_default_values()
        url_type = clean_values.get("link_to")

        if url_type != "":
            errors.update(self.clean_link_type(url_type, clean_values))

        if not errors:
            # Remove values added for link types not selected
            url_default_values.pop(url_type, None)
            for field in url_default_values:
                clean_values[field] = url_default_values[field]

        if errors:
            raise StreamBlockValidationError(block_errors=errors, non_block_errors=ErrorList([]))

        return clean_values
