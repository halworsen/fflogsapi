

from .guild import FFLogsGuild
from .pages import FFLogsGuildPaginationIterator


class GuildsMixin:
    '''
    Client extensions to support guild data exposed by the FF Logs API.
    '''

    def guild_pages(self, filters: dict = {}) -> FFLogsGuildPaginationIterator:
        '''
        Iterate over pages of guilds on FF Logs.

        Args:
            filters: A dictionary containing filters to use when finding guilds.
        Returns:
            An iterator over the pages of guilds that match the given filters.
        '''
        return FFLogsGuildPaginationIterator(filters=filters, client=self)

    def get_guild(self, id: int) -> FFLogsGuild:
        '''
        Retrieves the given guild data from FFLogs.

        Args:
            id: The guild ID.
        Returns:
            A FFLogsGuild object representing the guild.
        '''
        return FFLogsGuild(id=id, client=self)
