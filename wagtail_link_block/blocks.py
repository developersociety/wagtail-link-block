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

        if link_to in ("page", "file"):
            # If file or page check obj is not None
            if self.get(link_to):
                return self.get(link_to).url
        elif link_to == "page_anchor":
            return self.get("page").url + "#" + self.get("anchor")
        elif link_to == "custom_url":
            return self.get(link_to)
        elif link_to == "anchor":
            return "#" + self.get(link_to)
        elif link_to == "email":
            return f"mailto:{self.get(link_to)}"
        elif link_to == "phone":
            return f"tel:{self.get(link_to)}"
        return None

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
            ("page_anchor", _("Page + Anchor")),
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

    def clean(self, value):
        clean_values = super().clean(value)
        errors = {}

        url_default_values = {
            "page": None,
            "file": None,
            "custom_url": "",
            "anchor": "",
            "email": "",
            "phone": "",
        }
        url_type = clean_values.get("link_to")

        # Check that a value has been uploaded for the chosen link type
        if url_type not in ["", "page_anchor"] and clean_values.get(url_type) in [None, ""]:
            errors[url_type] = ErrorList(
                ["You need to add a {} link".format(url_type.replace("_", " "))]
            )
        elif url_type == "page_anchor" and (
            clean_values.get("page") in [None, ""] or clean_values.get("anchor") in [None, ""]
        ):
            if clean_values.get("page") in [None, ""]:
                errors["page"] = ErrorList(["You need to add a page link"])
            if clean_values.get("anchor") in [None, ""]:
                errors["anchor"] = ErrorList(["You need to add an anchor link"])
        else:
            try:
                if url_type == "page_anchor":
                    url_default_values.pop("page", None)
                    url_default_values.pop("anchor", None)
                else:
                    # Remove values added for link types not selected
                    url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
            except KeyError:
                errors[url_type] = ErrorList(["Enter a valid link type"])

        if errors:
            raise StreamBlockValidationError(block_errors=errors, non_block_errors=ErrorList([]))

        return clean_values
