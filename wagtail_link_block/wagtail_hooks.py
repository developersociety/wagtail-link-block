from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import __version__ as wagtail_version

if int(wagtail_version[0]) >= 3:
    from wagtail import hooks
else:
    from wagtail.core import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("link_block/link_block.css"))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("link_block/link_block.js"))
