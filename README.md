# fflogsapi

fflogsapi is a lazy Python 3 client for [fflogs](https://www.fflogs.com/)' v2 API with query caching functionality.

[![Tests](https://github.com/halworsen/fflogsapi/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/halworsen/fflogsapi/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/halworsen/fflogsapi/branch/master/graph/badge.svg?token=YTEGMDJOGL)](https://codecov.io/gh/halworsen/fflogsapi)

---

## Features

* Retrieve information from fflogs' v2 GraphQL API
* Lazy evaluation
  * Queries for data are not executed until it is explicitly needed
* Query caching
  * Requesting the same data twice will instead fetch the result from cache
  * Customizable cache lifetime and options to ignore cached results

## Example usage

```python
from config import CLIENT_ID, CLIENT_SECRET

from fflogsapi.client import FFLogsClient

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
report = client.get_report('rGARYmQwTKbahXz9')

for fight in report:
    print(f'Fight #{fight.fight_id}:', fight.name(), f'- Kill: {fight.is_kill()}')
    pot_table = fight.fight_table(filters={'sourceAurasPresent': 'Medicated'})
    potted_damage = 0
    for damage in pot_table['damageDone']:
        potted_damage += damage['total']
    print(f'Damage done under pots: {potted_damage}')
    if not fight.is_kill():
        print(f'Percentage reached: {fight.percentage()}')

client.close()
client.save_cache()
```

```python
from config import CLIENT_ID, CLIENT_SECRET

from fflogsapi.client import FFLogsClient

client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
for page in client.report_pages(filters={ 'guildID': 80551 }):
    print(f'Reports in page: {page.count()}')
    for report in page:
        print(report.title(), f'Duration: {report.duration()}')

client.close()
client.save_cache()
```
