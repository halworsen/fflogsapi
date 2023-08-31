# fflogsapi

fflogsapi is a lazy Python 3 client for [FF Logs](https://www.fflogs.com/)' v2 API with query caching functionality.

[![Tests](https://github.com/halworsen/fflogsapi/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/halworsen/fflogsapi/actions/workflows/test.yml)
[![Linting](https://github.com/halworsen/fflogsapi/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/halworsen/fflogsapi/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/halworsen/fflogsapi/branch/master/graph/badge.svg?token=YTEGMDJOGL)](https://codecov.io/gh/halworsen/fflogsapi)
[![Documentation Status](https://readthedocs.org/projects/fflogsapi/badge/?version=latest)](https://fflogsapi.readthedocs.io/en/latest/?badge=latest)
[![pypi](https://shields.io/pypi/v/fflogsapi)](https://pypi.org/project/fflogsapi/)

---

## Features

* Retrieve information from FF Logs' v2 GraphQL API
  * Including private information only accessible through the user API
* Lazy evaluation
  * Queries for data are not executed until the result is explicitly needed
* Query caching
  * Requesting the same data twice will instead fetch the result from cache
  * Customizable cache lifetime and options to ignore cached results

## Installation

fflogsapi is available as a [PyPI package](https://pypi.org/project/fflogsapi/) and
can be installed with pip:

```shell
pip install fflogsapi
```

If you want to contribute, you can install fflogsapi with the following to
additionally install development and test tools:

```shell
pip install fflogsapi[dev,test]
```

## Example usage

Calculating damage done under pots:

```python
from config import CLIENT_ID, CLIENT_SECRET

from fflogsapi import FFLogsClient

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
report = client.get_report('rGARYmQwTKbahXz9')

for fight in report:
    print(f'Fight #{fight.fight_id}:', fight.name(), f'- Kill: {fight.is_kill()}')
    pot_table = fight.table(filters={'sourceAurasPresent': 'Medicated'})
    potted_damage = 0
    for damage in pot_table['damageDone']:
        potted_damage += damage['total']
    print(f'Damage done under pots: {potted_damage}')
    if not fight.is_kill():
        print(f'Percentage reached: {fight.percentage()}')

client.close()
client.save_cache()
```

Listing reports and durations for a specific guild:

```python
from config import CLIENT_ID, CLIENT_SECRET

from fflogsapi import FFLogsClient

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
for page in client.reports(filters={ 'guildID': 80551 }):
    print(f'Reports in page: {page.count()}')
    for report in page:
        print(report.title(), f'Duration: {report.duration()}')

client.close()
client.save_cache()
```

Listing a character's RDPS & All stars rank for Abyssos Savage in 6.28:

```python
from config import CLIENT_ID, CLIENT_SECRET

from fflogsapi import FFLogsClient, GQLEnum, FightDifficulty

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
character = fapi.get_character(id=19181640)

abyssos = fapi.get_zone(id=49)
partition_628 = next(filter(
    lambda p: '6.28' in p.name,
    abyssos.partitions()
))

rankings = character.zone_rankings(filters={
    'specName': 'Reaper',
    'metric': GQLEnum('rdps'),
    'zoneID': abyssos.id,
    'difficulty': FightDifficulty.SAVAGE.value,
    'partition': partition_628.id,
})

print('6.28 All Star points: '
      f'{rankings.all_stars[0].points} (rank {rankings.all_stars[0].rank})')

for rank in rankings.encounter_ranks:
    print(f'{rank.encounter.name()}: {rank.best_amount}rdps (rank {rank.all_stars.rank})')

client.close()
client.save_cache()
```

## User mode

The default mode of the client is 'client' mode, which uses the public API. This is by far the most
convenient method to use the client, and usually provides enough functionality for the majority of
use cases.

If you need access to private information, however, it is possible to use the client in user mode,
granting access to extra information such as private reports provided by the user API.

To use user mode, you must first specify `https://localhost:4433` as the redirect URL in your API
client on FF Logs. Then, provide the `mode='user'` kwarg to the client when instantiating it:

```python
client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, mode='user')
```

This will have the client popup a browser window for the user for login, after which the client has
access to the user API. Note that the client will generate a self-signed certificate to serve
the redirect. Your browser will likely produce a warning about this, although it is safe to ignore.

If you wish to handle the user authentication flow yourself, you can still use the API client in
user mode by calling `set_auth_response` on the client **before using it**:

```python
# Your implementation of the user authentication flow here
...

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, mode='user')
client.set_auth_response(response)

# Start using the client
...
```
