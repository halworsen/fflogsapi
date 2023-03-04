from typing import Optional

from .character import FFLogsCharacter


class CharactersMixin:
    '''
    Client extensions to support character data exposed by the FF Logs API.
    '''

    def get_character(self, filters: dict = {}, id: Optional[int] = -1) -> FFLogsCharacter:
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
        return FFLogsCharacter(filters=filters, id=id, client=self)
