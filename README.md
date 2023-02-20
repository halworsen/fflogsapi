# fflogsapi

fflogsapi is a lazy Python 3 client for the FFLogs API with query caching functionality.

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

client.save_cache()
```
