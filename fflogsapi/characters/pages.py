from ..data.page import FFLogsPage, FFLogsPaginationIterator
from .character import FFLogsCharacter
from .queries import Q_CHARACTER_PAGINATION


class FFLogsCharacterPage(FFLogsPage):
    '''
    Represents a page of characters on FFLogs.
    '''

    PAGINATION_QUERY = Q_CHARACTER_PAGINATION
    PAGE_INDICES = ['characterData', 'characters']
    OBJECT_ID_FIELD = 'id'

    def init_object(self, id: int) -> FFLogsCharacter:
        '''
        Initializes a character with the given ID.
        '''
        return FFLogsCharacter(id=id, client=self._client)


class FFLogsCharacterPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple character pages
    '''

    PAGE_CLASS = FFLogsCharacterPage
