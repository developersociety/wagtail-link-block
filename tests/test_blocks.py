from wagtail_link_block.blocks import LinkBlock



from django.test import SimpleTestCase, TestCase


class LinkBlockTestCase(SimpleTestCase):
    def test_block(self):
        block = LinkBlock()

        self.assertIsNotNone(block.render({}))
