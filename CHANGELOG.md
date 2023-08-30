# Changelog

Backwards compatibility is not guaranteed in versions <1.0.0.

## v1.2.0

* Improved docstrings, including docstrings for many subpackages

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
