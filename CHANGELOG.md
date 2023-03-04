# Changelog

Backwards compatibility is not guaranteed in versions <1.0.0.

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
