Example usage
=============

This page contains some select examples on how to use the fflogsapi client.

Calculating damage done under pots
----------------------------------

.. code-block:: python

    from config import CLIENT_ID, CLIENT_SECRET
    from fflogsapi import FFLogsClient

    client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
    report = client.get_report('rGARYmQwTKbahXz9')

    for fight in report:
        print(f'Fight #{fight.id}:', fight.name(), f'- Kill: {fight.is_kill()}')
        pot_table = fight.table(filters={'sourceAurasPresent': 'Medicated'})
        potted_damage = 0
        for damage in pot_table['damageDone']:
            potted_damage += damage['total']
        print(f'Damage done under pots: {potted_damage}')
        if not fight.is_kill():
            print(f'Percentage reached: {fight.percentage()}')

    client.close()
    client.save_cache()

Listing a guild's reports and their durations
---------------------------------------------

.. code-block:: python

    from config import CLIENT_ID, CLIENT_SECRET

    from fflogsapi import FFLogsClient

    client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
    for page in client.reports(filters={ 'guildID': 80551 }):
        print(f'Reports in page: {page.count()}')
        for report in page:
            print(report.title(), f'Duration: {report.duration()}')

    client.close()
    client.save_cache()

Listing a character's RPDS & All-stars rank for Abyssos Savage in 6.28
----------------------------------------------------------------------

.. code-block:: python

    from config import CLIENT_ID, CLIENT_SECRET
    from fflogsapi import FFLogsClient, GQLEnum, FightDifficulty

    client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
    character = client.get_character(id=19181640)

    abyssos = client.get_zone(id=49)
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
