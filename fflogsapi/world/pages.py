from ..characters.pages import FFLogsCharacterPage
from ..data.page import FFLogsPaginationIterator
from .queries import Q_SERVER_CHARACTER_PAGINATION


class FFLogsServerCharacterPage(FFLogsCharacterPage):
    '''
    Represents a page of a server's characters on FFLogs.
    '''

    PAGINATION_QUERY = Q_SERVER_CHARACTER_PAGINATION
    PAGE_INDICES = ['worldData', 'server', 'characters']


class FFLogsServerCharacterPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of a server's characters.
    '''

    PAGE_CLASS = FFLogsServerCharacterPage
