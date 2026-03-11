from unittest import mock
from unittest.mock import Mock

from django.test import SimpleTestCase, TestCase
from wagtail.blocks import StreamBlockValidationError, StructBlockValidationError
from wagtail.documents.models import Document
from wagtail.models import Page

from wagtail_link_block.blocks import LinkBlock, URLValue


class URLValueGetURLTestCase(SimpleTestCase):
    """Tests for URLValue.get_url() across all link types."""

    def _make_value(self, data):
        """Helper to create a URLValue with the given data."""
        block = LinkBlock()
        return URLValue(block, data)

    def test_page_with_object(self):
        page = Mock()
        page.url = "/about-us/"
        value = self._make_value({"link_to": "page", "page": page})
        self.assertEqual(value.get_url(), "/about-us/")

    def test_page_with_none(self):
        value = self._make_value({"link_to": "page", "page": None})
        self.assertIsNone(value.get_url())

    def test_file_with_object(self):
        doc = Mock()
        doc.url = "/documents/report.pdf"
        value = self._make_value({"link_to": "file", "file": doc})
        self.assertEqual(value.get_url(), "/documents/report.pdf")

    def test_file_with_none(self):
        value = self._make_value({"link_to": "file", "file": None})
        self.assertIsNone(value.get_url())

    def test_custom_url(self):
        value = self._make_value({"link_to": "custom_url", "custom_url": "https://example.com"})
        self.assertEqual(value.get_url(), "https://example.com")

    def test_custom_url_path(self):
        value = self._make_value({"link_to": "custom_url", "custom_url": "/some/path"})
        self.assertEqual(value.get_url(), "/some/path")

    def test_custom_url_empty(self):
        value = self._make_value({"link_to": "custom_url", "custom_url": ""})
        self.assertEqual(value.get_url(), "")

    def test_anchor(self):
        value = self._make_value({"link_to": "anchor", "anchor": "section-1"})
        self.assertEqual(value.get_url(), "#section-1")

    def test_email(self):
        value = self._make_value({"link_to": "email", "email": "hello@example.com"})
        self.assertEqual(value.get_url(), "mailto:hello@example.com")

    def test_phone(self):
        value = self._make_value({"link_to": "phone", "phone": "+44123456789"})
        self.assertEqual(value.get_url(), "tel:+44123456789")

    def test_relative_url(self):
        value = self._make_value({"link_to": "relative_url", "relative_url": "/features/"})
        self.assertEqual(value.get_url(), "/features/")

    def test_relative_url_empty(self):
        value = self._make_value({"link_to": "relative_url", "relative_url": ""})
        self.assertIsNone(value.get_url())

    def test_relative_url_none(self):
        value = self._make_value({"link_to": "relative_url", "relative_url": None})
        self.assertIsNone(value.get_url())

    def test_no_link_to(self):
        value = self._make_value({"link_to": None})
        self.assertIsNone(value.get_url())

    def test_empty_link_to(self):
        value = self._make_value({"link_to": ""})
        self.assertIsNone(value.get_url())

    def test_missing_link_to_key(self):
        value = self._make_value({})
        self.assertIsNone(value.get_url())

    def test_get_url_dispatches_to_helper(self):
        """get_url() calls the per-type helper method."""
        value = self._make_value({"link_to": "page", "page": Mock(url="/test/")})
        with mock.patch.object(URLValue, "get_page_url", return_value="/mocked/") as m:
            result = value.get_url()
        m.assert_called_once()
        self.assertEqual(result, "/mocked/")

    def test_get_url_unknown_type_returns_none(self):
        """get_url() returns None for an unrecognized link_to value."""
        value = self._make_value({"link_to": "unknown_type"})
        self.assertIsNone(value.get_url())


class URLValueGetLinkToTestCase(SimpleTestCase):
    """Tests for URLValue.get_link_to()."""

    def _make_value(self, data):
        block = LinkBlock()
        return URLValue(block, data)

    def test_returns_link_to_value(self):
        value = self._make_value({"link_to": "page"})
        self.assertEqual(value.get_link_to(), "page")

    def test_returns_none_when_missing(self):
        value = self._make_value({})
        self.assertIsNone(value.get_link_to())


class LinkBlockCleanTestCase(TestCase):
    """Tests for LinkBlock.clean() validation and field clearing."""

    def _make_block_value(self, link_to="", **kwargs):
        """Helper to build the raw value dict that clean() expects."""
        defaults = {
            "link_to": link_to,
            "page": None,
            "file": None,
            "custom_url": "",
            "relative_url": "",
            "anchor": "",
            "email": "",
            "phone": "",
            "new_window": False,
        }
        defaults.update(kwargs)
        return defaults

    def test_clean_custom_url_valid(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="custom_url", custom_url="https://example.com")
        result = block.clean(value)
        self.assertEqual(result["custom_url"], "https://example.com")
        self.assertEqual(result["link_to"], "custom_url")
        # Other link fields should be cleared
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_custom_url_missing_raises(self):
        block = LinkBlock()

        value_empty_string = self._make_block_value(link_to="custom_url", custom_url="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value_empty_string)
        self.assertIn("custom_url", ctx.exception.block_errors)

        value_none = self._make_block_value(link_to="custom_url", custom_url=None)
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value_none)
        self.assertIn("custom_url", ctx.exception.block_errors)

    def test_clean_email_valid(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="email", email="hello@example.com")
        result = block.clean(value)
        self.assertEqual(result["email"], "hello@example.com")
        # Other link fields should be cleared
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_email_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="email", email="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("email", ctx.exception.block_errors)

    def test_clean_anchor_valid(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="anchor", anchor="my-section")
        result = block.clean(value)
        self.assertEqual(result["anchor"], "my-section")
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_anchor_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="anchor", anchor="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("anchor", ctx.exception.block_errors)

    def test_clean_phone_valid(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="phone", phone="+44123456789")
        result = block.clean(value)
        self.assertEqual(result["phone"], "+44123456789")
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")

    def test_clean_phone_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="phone", phone="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("phone", ctx.exception.block_errors)

    def test_clean_page_valid(self):
        block = LinkBlock()
        page = Page.objects.first()
        value = self._make_block_value(link_to="page", page=page.pk)
        result = block.clean(value)
        self.assertEqual(result["page"], page)
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_page_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="page", page=None)
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("page", ctx.exception.block_errors)

    def test_clean_file_valid(self):
        block = LinkBlock()
        doc = Document.objects.create(title="Test Document")
        value = self._make_block_value(link_to="file", file=doc.pk)
        result = block.clean(value)
        self.assertEqual(result["file"], doc)
        self.assertIsNone(result["page"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_file_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="file", file=None)
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("file", ctx.exception.block_errors)

    def test_clean_relative_url_valid(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="relative_url", relative_url="/features/")
        result = block.clean(value)
        self.assertEqual(result["relative_url"], "/features/")
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_relative_url_missing_raises(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="relative_url", relative_url="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("relative_url", ctx.exception.block_errors)

    def test_clean_relative_url_invalid_raises(self):
        block = LinkBlock()
        value = self._make_block_value(
            link_to="relative_url", relative_url="doesnotstartwithaslash"
        )
        with self.assertRaises(StructBlockValidationError) as ctx:
            block.clean(value)
        self.assertIn("relative_url", ctx.exception.block_errors)

    def test_clean_empty_link_to_passes(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="")
        result = block.clean(value)
        # All link fields should be reset to defaults
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["anchor"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_clean_clears_unselected_fields(self):
        """When selecting one link type, other fields with stale data get cleared."""
        block = LinkBlock()
        value = self._make_block_value(
            link_to="anchor",
            anchor="top",
            custom_url="https://stale.com",
            email="stale@example.com",
            phone="+000",
        )
        result = block.clean(value)
        self.assertEqual(result["anchor"], "top")
        self.assertEqual(result["custom_url"], "")
        self.assertEqual(result["relative_url"], "")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")
        self.assertIsNone(result["page"])
        self.assertIsNone(result["file"])

    def test_clean_error_message_format(self):
        block = LinkBlock()
        value = self._make_block_value(link_to="custom_url", custom_url="")
        with self.assertRaises(StreamBlockValidationError) as ctx:
            block.clean(value)
        error_list = ctx.exception.block_errors["custom_url"]
        self.assertIn("You need to add a custom url link", [str(e) for e in error_list])

    def test_get_url_field_default_values_contains_all_types(self):
        block = LinkBlock()
        defaults = block.get_url_field_default_values()
        self.assertEqual(
            set(defaults.keys()),
            {"page", "file", "custom_url", "relative_url", "anchor", "email", "phone"},
        )

    def test_clean_link_type_returns_empty_dict_for_valid_value(self):
        block = LinkBlock()
        result = block.clean_link_type("custom_url", {"custom_url": "https://example.com"})
        self.assertEqual(result, {})

    def test_clean_link_type_returns_error_for_empty_value(self):
        block = LinkBlock()
        result = block.clean_link_type("custom_url", {"custom_url": ""})
        self.assertIn("custom_url", result)

    def test_clean_link_type_dispatches_to_per_type_method(self):
        """clean_link_type() calls clean_<url_type>() when defined."""
        block = LinkBlock()
        with mock.patch.object(LinkBlock, "clean_page", create=True, return_value={}) as m:
            block.clean_link_type("page", {"page": Mock()})
        m.assert_called_once()


class LinkBlockInitTestCase(SimpleTestCase):
    """Tests for LinkBlock.__init__() required propagation."""

    def test_default_not_required(self):
        block = LinkBlock()
        self.assertFalse(block.child_blocks["link_to"].field.required)

    def test_required_true_propagates(self):
        block = LinkBlock(required=True)
        self.assertTrue(block.child_blocks["link_to"].field.required)

    def test_required_does_not_leak_between_instances(self):
        block_required = LinkBlock(required=True)
        block_optional = LinkBlock(required=False)
        self.assertTrue(block_required.child_blocks["link_to"].field.required)
        self.assertFalse(block_optional.child_blocks["link_to"].field.required)


class LinkBlockSetNameTestCase(SimpleTestCase):
    """Tests for LinkBlock.set_name() label override."""

    def test_set_name_sets_name_without_label(self):
        block = LinkBlock()
        block.set_name("my_link")
        self.assertEqual(block.name, "my_link")
        # Label should remain None (not auto-set from name)
        self.assertIsNone(block.meta.label)
