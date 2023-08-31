from typing import TYPE_CHECKING

from ..characters.character import FFLogsCharacter
from ..data import FFLogsAttendanceReport
from ..data.page import FFLogsPage, FFLogsPaginationIterator
from ..world.zone import FFLogsZone
from .queries import Q_GUILD_ATTENDANCE_PAGINATION, Q_GUILD_CHARACTER_PAGINATION, Q_GUILD_PAGINATION

if TYPE_CHECKING:
    from .guild import FFLogsGuild


class FFLogsGuildPage(FFLogsPage):
    '''
    A page of guilds on FF Logs.
    '''

    PAGINATION_QUERY = Q_GUILD_PAGINATION
    PAGE_INDICES = ['guildData', 'guilds']
    DATA_FIELDS = ['id']

    def init_object(self, data: dict) -> 'FFLogsGuild':
        '''
        Creates a guild from the given data
        '''
        from .guild import FFLogsGuild
        return FFLogsGuild(id=data['id'])


class FFLogsGuildPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of guilds.
    '''

    PAGE_CLASS = FFLogsGuildPage


class FFLogsGuildAttendancePage(FFLogsPage):
    '''
    Represents a page of guild attendance reports on FF Logs.
    '''

    PAGINATION_QUERY = Q_GUILD_ATTENDANCE_PAGINATION
    PAGE_INDICES = ['guildData', 'guild', 'attendance']
    DATA_FIELDS = ['code', 'players{ name, presence, type }', 'startTime', 'zone{ id }']

    def init_object(self, data: dict) -> FFLogsAttendanceReport:
        '''
        Creates an attendance report from the given data
        '''
        from ..reports.report import FFLogsReport
        return FFLogsAttendanceReport(
            report=FFLogsReport(data['code']),
            players=[(p['name'], p['presence'], p['type']) for p in data['players']],
            start=data['startTime'],
            zone=FFLogsZone(id=data['zone']['id'])
        )


class FFLogsGuildAttendancePaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of guild attendance reports
    '''

    PAGE_CLASS = FFLogsGuildAttendancePage


class FFLogsCharacterPage(FFLogsPage):
    '''
    Represents a page of a guild's characters on FF Logs.
    '''

    PAGINATION_QUERY = Q_GUILD_CHARACTER_PAGINATION
    PAGE_INDICES = ['guildData', 'guild', 'members']
    DATA_FIELDS = ['id']

    def init_object(self, data: dict) -> FFLogsCharacter:
        '''
        Initializes a character with the given ID.
        '''
        return FFLogsCharacter(id=data['id'], client=self._client)


class FFLogsCharacterPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple character pages
    '''

    PAGE_CLASS = FFLogsCharacterPage
