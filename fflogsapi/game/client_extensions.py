from ..data import FFAbility, FFGrandCompany, FFItem, FFJob, FFMap
from .pages import (FFLogsAbilityPaginationIterator, FFLogsItemPaginationIterator,
                    FFLogsMapPaginationIterator,)
from .queries import Q_ABILITY, Q_GRAND_COMPANIES, Q_ITEM, Q_JOBS, Q_MAP


class GameDataMixin:
    '''
    Client extensions to support game data exposed by the FF Logs API.
    '''

    def icon_url(self, icon: str) -> str:
        '''
        Get the full URL to a game object.

        Args:
            icons: The filename of the icon as given by the FF Logs API.
        Returns:
            The full URL to the icon.
        '''
        icon_type = 'maps' if icon[0] == 'm' else 'abilities'
        return f'https://assets.rpglogs.com/img/ff/{icon_type}/{icon}'

    def abilities(self) -> FFLogsAbilityPaginationIterator:
        '''
        Get a pagination of all game abilities.

        Returns:
            An iterator over all pages of game abilities.
        '''
        return FFLogsAbilityPaginationIterator(client=self)

    def items(self) -> FFLogsItemPaginationIterator:
        '''
        Get a pagination of all game items.

        Returns:
            An iterator over all pages of game items.
        '''
        return FFLogsItemPaginationIterator(client=self)

    def maps(self) -> FFLogsMapPaginationIterator:
        '''
        Get a pagination of all game maps.

        Returns:
            An iterator over all pages of game maps.
        '''
        return FFLogsMapPaginationIterator(client=self)

    def ability(self, id: int) -> FFAbility:
        '''
        Get ability data for the given ability `id`.

        Args:
            id: The ID of the game ability.
        Returns:
            The game ability.
        '''
        # this appears up in reports but the API will raise an error if queried for
        # as it isn't a real game ability
        if id == 0:
            return FFAbility(
                id=0,
                name='Unknown Ability',
                description='',
                icon='000000-000405.png',
                type=0,
            )

        ability = self.q(Q_ABILITY.format(abilityID=id))['gameData']['ability']
        return FFAbility(
            id=id,
            name=ability['name'],
            description=ability['description'],
            icon=ability['icon'],
        )

    def item(self, id: int) -> FFItem:
        '''
        Get item data for the given item `id`.

        Args:
            id: The ID of the game item.
        Returns:
            The game item.
        '''
        item = self.q(Q_ITEM.format(itemID=id))['gameData']['item']
        return FFItem(id=id, name=item['name'], icon=item['icon'])

    def map(self, id: int) -> FFMap:
        '''
        Get map data for the given map `id`.

        Args:
            id: The ID of the game map.
        Returns:
            The game map.
        '''
        map = self.q(Q_MAP.format(mapID=id))['gameData']['map']
        return FFMap(
            id=id,
            name=map['name'],
            filename=map['filename'],
            offset_x=map['offsetX'],
            offset_y=map['offsetY'],
            size_factor=map['sizeFactor'],
        )

    def jobs(self) -> list[FFJob]:
        '''
        Get a list of all game jobs supported by FF Logs.

        Returns:
            A list of all jobs.
        '''
        jobs = self.q(Q_JOBS)['gameData']['class']['specs']
        return [FFJob(
            id=job['id'],
            name=job['name'],
            slug=job['slug'],
        ) for job in jobs]

    def grand_companies(self) -> list[FFGrandCompany]:
        '''
        Get all grand companies (called factions by FF Logs) that guilds and characters can
        belong to.

        Returns:
            A list of all grand companies.
        '''
        gcs = self.q(Q_GRAND_COMPANIES)['gameData']['factions']
        return [FFGrandCompany(id=gc['id'], name=gc['name']) for gc in gcs]
