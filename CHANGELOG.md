# Changelog

Backwards compatibility is not guaranteed in versions <1.0.0.

## v2.1.0

* Added support for the new phase data exposed by the API. See
  [the official v2 API docs](https://www.fflogs.com/v2-api-docs/ff/encounterphases.doc.html)
  for more information
  * Phase information is exposed at the fight level in this client (`FFLogsFight.phases`),
    *not* at the report level
* Fix quotes not being properly escaped in query filters

## v2.0.2

* [fix zone_rankings giving up on exception (#1)](https://github.com/halworsen/fflogsapi/commit/b428f992f623d2a313da078409a3f1d9960afe3a)

## v2.0.1

* Stricter pinning of dependencies
  * urllib3 has been pinned to ~=1.26.14 to prevent breaking interop between requests >=2.29.0 and urllib3 >=2.0.0
* Fix docs dependencies

## v2.0.0

* Improved docstrings, including docstrings for many subpackages
* Added generated documentation pages. They are available at [fflogsapi.readthedocs.io](https://fflogsapi.readthedocs.io)
* Improved package API. It's now possible to import most objects of interest without digging into specific modules
* Fixed some flaky character tests
* Added the `clean_cache` param to the client, which deletes expired caches on client instantiation.
  * Cache cleaning is enabled by default

Breaking changes:

* Replaced most `fflogsapi.constants` with enums for things like fight difficulty and event types
  * To migrate to v2, replace all `fflogsapi.constants` imports with the new enums
* Moved all dataclasses into the `data` package
  * To migrate to v2, import dataclasses from `fflogsapi.data`
* Certain client extension method names have been changed.
* Internal `_id` fields and corresponding `id()` functions have been replaced with just `id` as a property.
  * `FFLogsReport.code()` has been removed. If you need the report code, access the `FFLogsReport.code` property.

## v1.1.0

* Add dataclass return for zone partitions
  * A deprecation warning for dict returns has been added to FFLogsZone.partitions
* Add dataclass returns for character ranking information
  * Deprecation warnings for dict returns have been added to
    FFLogsCharacter.encounter_rankings and FFLogsCharacter.zone_rankings
* Add support for phase-related queries to fights

## v1.0.1

* Fix missing client for characters retrieved through fight rankings

## v1.0.0

* Extended support for report/fight data to cover the vast majority of interesting API endpoints
* Added `compare` and `timeframe` filtering for fight rankings
* Add ability to specify the directory in which query caches should be stored
  * The new default directory for cached queries is `./fflogs-querycache`
* Added more event type constants
* Added `constants.TIMESTAMP_PRECISION`, which can be used to convert timestamps to seconds
* Improved docstrings, including references to the API documentation where relevant

## v0.6.0

* Add support for game data
* Remove `character_pages` from the client in favor of `FFLogsGuild.characters`
  as they are functionally the same, but character pagination through characterData queries is
  less stable.
* Report master data is no longer fetched in batch.

## v0.5.0

* Add support for rate limit data
* Add support for prog race data
* Add support for guild data
* Extend support for characters, reports and users to include guild, user and report tag data

## v0.4.0

* Add support for the authorization code flow by specifying `mode='user'` when instantiating client
* Add support for most user data exposed by the API
