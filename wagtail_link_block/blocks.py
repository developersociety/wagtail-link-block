"""
The LinkBlock is not designed to be used on it's own - but as part of other blocks.
"""
from django.forms.utils import ErrorList

from wagtail.core.blocks import (
    BooleanBlock,
    ChoiceBlock,
    PageChooserBlock,
    StreamBlockValidationError,
    StructBlock,
    StructValue,
    CharBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.forms.choosers import URLOrAbsolutePathValidator

##############################################################################
# Component Parts - should not be used on their own - but as parts of other
# blocks:


class URLValue(StructValue):
    """
    Get active link used in LinkBlock or CustomLinkBlock if there is one
    """

    def get_url(self):
        link_to = self.get("link_to")

        if link_to == "page" or link_to == "file":
            # If file or page check obj is not None
            if self.get(link_to):
                return self.get(link_to).url
        elif link_to == "custom_url":
            return self.get(link_to)
        return None


class LinkBlock(StructBlock):
    """
        A Link which can either be to a (off-site) URL, to a page in the site,
        or to a document. Use this instead of URLBlock.
    """

    link_to = ChoiceBlock(
        choices=[("page", "Page"), ("file", "File"), ("custom_url", "Custom URL")],
        required=False,
        classname="link_choice_type_selector",
    )
    page = PageChooserBlock(required=False, classname="page_link")
    file = DocumentChooserBlock(required=False, classname="file_link")
    custom_url = CharBlock(
        max_length=300,
        required=False,
        classname="custom_url_link url_field",
        validators=[URLOrAbsolutePathValidator()],
    )
    new_window = BooleanBlock(
        label="Open in new window", required=False, classname="new_window_toggle"
    )

    class Meta:
        label = None
        value_class = URLValue
        icon = "fa-share-square"
        form_classname = "link_block"
        form_template = "wagtailadmin/block_forms/link_block.html"
        template = "blocks/link_block.html"

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
        }
        url_type = clean_values.get("link_to")

        # Check that a value has been uploaded for the chosen link type
        if url_type != "" and clean_values.get(url_type) in [None, ""]:
            errors[url_type] = ErrorList(
                ["You need to add a {} link".format(url_type.replace("_", " "))]
            )
        else:
            try:
                # Remove values added for link types not selected
                url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
            except KeyError:
                errors[url_type] = ErrorList(["Enter a valid link type"])

        if errors:
            raise StreamBlockValidationError(block_errors=errors)

        return clean_values
