

from .guild import FFLogsGuild
from .pages import FFLogsGuildPaginationIterator


class GuildsMixin:
    '''
    Client extensions to support guild data exposed by the FF Logs API.
    '''

    def guilds(self, filters: dict = {}) -> FFLogsGuildPaginationIterator:
        '''
        Iterate over pages of guilds on FF Logs.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/guilddata.doc.html

        Args:
            filters: Filters to find guilds by.
        Returns:
            An iterator over the pages of guilds that match the given filters.
        '''
        return FFLogsGuildPaginationIterator(filters=filters, client=self)

    def get_guild(self, filters: dict = {}, id: int = -1) -> FFLogsGuild:
        '''
        Retrieves the given guild data from FFLogs.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/guilddata.doc.html

        Args:
            filters: Filters to find the guild by.
            id: The guild ID.
        Returns:
            A FFLogsGuild object representing the guild.
        '''
        return FFLogsGuild(filters=filters, id=id, client=self)
