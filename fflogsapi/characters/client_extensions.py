from typing import Optional

from .character import FFLogsCharacter


class CharactersMixin:
    '''
    Client extensions to support character data exposed by the FF Logs API.
    '''

    def get_character(self, filters: dict = {}, id: Optional[int] = -1) -> FFLogsCharacter:
        '''
        Retrieves character data from FFLogs.
        Note that it is possible to use only the `filters` argument,
        the id parameter is there for ease of use.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/characterdata.doc.html

        Args:
            filters: Optional filters to find the character by.
            id: The ID of the character to retrieve.
        Returns:
            A FFLogsCharacter representing the requested character.
        '''
        return FFLogsCharacter(filters=filters, id=id, client=self)
