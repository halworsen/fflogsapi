from ..data import FFAbility, FFItem, FFMap
from ..data.page import FFLogsPage, FFLogsPaginationIterator
from .queries import Q_ABILITY_PAGINATION, Q_ITEM_PAGINATION, Q_MAP_PAGINATION


class FFLogsAbilityPage(FFLogsPage):
    '''
    Representation of a page of Abilitys on FFLogs.
    '''

    PAGINATION_QUERY = Q_ABILITY_PAGINATION
    PAGE_INDICES = ['gameData', 'abilities']
    DATA_FIELDS = ['id', 'name', 'description', 'icon']

    def init_object(self, data: dict) -> FFAbility:
        '''
        Initializes an ability with the given code.
        '''
        return FFAbility(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            icon=data['icon'],
        )


class FFLogsAbilityPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple ability pages
    '''

    PAGE_CLASS = FFLogsAbilityPage


class FFLogsItemPage(FFLogsPage):
    '''
    Representation of a page of items on FFLogs.
    '''

    PAGINATION_QUERY = Q_ITEM_PAGINATION
    PAGE_INDICES = ['gameData', 'items']
    DATA_FIELDS = ['id', 'name', 'icon']

    def init_object(self, data: dict) -> FFItem:
        '''
        Initializes an item with the given code.
        '''
        return FFItem(
            id=data['id'],
            name=data['name'],
            icon=data['icon']
        )


class FFLogsItemPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple ability pages
    '''

    PAGE_CLASS = FFLogsItemPage


class FFLogsMapPage(FFLogsPage):
    '''
    Representation of a page of maps on FFLogs.
    '''

    PAGINATION_QUERY = Q_MAP_PAGINATION
    PAGE_INDICES = ['gameData', 'maps']
    DATA_FIELDS = ['id', 'name', 'filename', 'offsetX', 'offsetY', 'sizeFactor']

    def init_object(self, data: dict) -> FFMap:
        '''
        Initializes an map with the given code.
        '''
        return FFMap(
            id=data['id'],
            name=data['name'],
            filename=data['filename'],
            offset_x=data['offsetX'],
            offset_y=data['offsetY'],
            size_factor=data['sizeFactor'],
        )


class FFLogsMapPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple ability pages
    '''

    PAGE_CLASS = FFLogsMapPage
