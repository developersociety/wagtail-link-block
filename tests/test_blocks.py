from django.test import SimpleTestCase

from wagtail_link_block.blocks import LinkBlock


class LinkBlockTestCase(SimpleTestCase):
    def test_block(self):
        block = LinkBlock()

        self.assertIsNotNone(block.render({}))
