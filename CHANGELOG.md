# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Support for Django 6.0 and Wagtail 7.3/7.4.
- Optional anchor for Page links, so a link can point to a section of another page (e.g.
  `/about-us/#team`) and still follow the page if it is moved or renamed (Thibaud Demay).

### Changed

- `LinkBlock` has a new `page_anchor` child block. This doesn't change the database, but
  `makemigrations` will create new migrations for every `StreamField` that uses `LinkBlock`, and
  `makemigrations --check` will fail until they are created.
- A leading `#` is now stripped from anchors when saving, so a bare `#` no longer passes
  validation.

### Fixed

- Anchor links saved with a leading `#` (e.g. `#foo`) now render as `#foo` instead of `##foo`.

### Removed

- Support for Wagtail 6.x. Wagtail 7.0 or newer is now required.
- Support for Django 5.1.

### Security

- Pin GitHub Actions to commit hashes and tighten publish workflow permissions.

## [1.2] - 2026-03-26

### Added

- Support for Wagtail 7 and Python 3.13/3.14 (Nick Moreton).
- Supported Django versions are now declared: 4.2, 5.1 and 5.2.
- "Open in new window" option for file links (Kyle Stevenson).
- Test suite (D Chukhin) and a tox/CI matrix covering the supported Python/Django/Wagtail
  versions.

### Changed

- README recommends `rel="noopener noreferrer"` on links that open in a new window.
- Packaging moved from Poetry to setuptools, and releases are published to PyPI with trusted
  publishing.
- Licence metadata uses the SPDX `BSD-3-Clause` identifier.

### Removed

- Support for Wagtail versions older than 6.3. Wagtail 6.3 or newer is now required.
- Support for Python versions older than 3.10.
- Fallback imports for Wagtail 2.x (`wagtail.core`).
- Example `blocks/link_block.html` template. `LinkBlock` still names this template in its
  `Meta`, so rendering a `LinkBlock` directly with `{% include_block %}` now raises
  `TemplateDoesNotExist`. To upgrade, either provide your own `blocks/link_block.html`, or render
  the link in the parent block's template with `{{ value.link.get_url }}`.

## [1.1.7] - 2023-10-04

The version number jumped from 0.1.6 to 1.1.7. There are no 0.2–1.1.6 releases.

### Fixed

- `LinkBlock(required=True)` now makes the "Link to" choice required, and the admin form shows
  it as required.

## [0.1.6] - 2023-03-14

### Added

- Support for Wagtail 3+ import paths (`wagtail.blocks` instead of `wagtail.core.blocks`)
  (Oliver Parker).

### Changed

- Dependencies are now declared: Wagtail 2.7 or newer, Python 3.8.1 or newer.
- Packaging moved to Poetry, with linting in GitHub Actions.

## [0.1.5] - 2022-06-22

### Added

- "Anchor" link type, for links to an anchor on the current page (Thomas Recouvreux).
- "Email" link type (`mailto:` links) (Oliver Parker).
- "Phone" link type (`tel:` links) (Hayley Kinnear).

## [0.1.4] - 2021-11-29

### Fixed

- Validation errors on Wagtail 2.15.

## [0.1.3] - 2021-08-25

### Added

- French translations (Thomas Recouvreux).

## [0.1.2] - 2021-05-21

### Added

- `get_link_to()` method, which returns the selected link type for use in templates (rokondo).

## [0.1.1] - 2021-03-31

### Fixed

- Compatibility with Django 3.0+ (the `staticfiles` template tag import was removed).

### Changed

- README includes instructions for adding the app to `INSTALLED_APPS`.

## [0.1] - 2021-01-25

### Added

- `LinkBlock`, which links to a page, document or custom URL, with an option to open in a new
  window. The admin hides the fields for link types that aren't selected.

[Unreleased]: https://github.com/developersociety/wagtail-link-block/compare/1.2...HEAD
[1.2]: https://github.com/developersociety/wagtail-link-block/compare/1.1.7...1.2
[1.1.7]: https://github.com/developersociety/wagtail-link-block/compare/0.1.6...1.1.7
[0.1.6]: https://github.com/developersociety/wagtail-link-block/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/developersociety/wagtail-link-block/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/developersociety/wagtail-link-block/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/developersociety/wagtail-link-block/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/developersociety/wagtail-link-block/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/developersociety/wagtail-link-block/compare/0.1...0.1.1
[0.1]: https://github.com/developersociety/wagtail-link-block/releases/tag/0.1
