from typing import Optional

from .character import FFLogsCharacter
from .pages import FFLogsCharacterPaginationIterator


class CharactersMixin:
    def character_pages(self, guild_id: int) -> FFLogsCharacterPaginationIterator:
        '''
        Iterate over pages of FFLogs characters in a specific guild.

        Args:
            guild_id: The ID of the guild to retrieve characters from.
        Returns:
            An iterator over the pages of characters that are in the given guild.
        '''
        return FFLogsCharacterPaginationIterator(filters={'guildID': guild_id}, client=self)

    def get_character(self, filters: dict = {}, id: Optional[int] = None) -> FFLogsCharacter:
        '''
        Retrieves character data from FFLogs.
        Note that it is possible to use only the filters argument.
        The id argument is implemented for ease of use.

        Args:
            filters: Optional filters to find the character by.
                     Valid filter fields are: id, name, serverSlug and serverRegion.
            id: The ID of the character to retrieve.
        Returns:
            A FFLogsCharacter representing the requested character.
        '''
        if 'id' not in filters and id is not None:
            filters['id'] = id
        return FFLogsCharacter(filters=filters, client=self)
