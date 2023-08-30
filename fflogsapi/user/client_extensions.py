from typing import Optional

from .queries import Q_CURRENT_USER
from .user import FFLogsUser


class UserMixin:
    '''
    Client extensions to support the user data exposed by the FF Logs API.
    '''

    def get_current_user(self) -> Optional[FFLogsUser]:
        '''
        Get the current user. This requires the client to be in user mode!

        Raises:
            PermissionError if the client is not in user mode
        '''
        if self.mode != 'user':
            error = 'The client must be in user mode to get the current user.'
            error += '\nSee the documentation for setup required to use user mode.'
            raise PermissionError(error)

        user_id = self.q(Q_CURRENT_USER.format(
            innerQuery='id'
        ))['userData']['currentUser']['id']
        return FFLogsUser(id=user_id, client=self)

    def get_user(self, id: int) -> FFLogsUser:
        '''
        Get the user with the given ID.

        Args:
            id: The ID of the user to retrieve.
        '''
        return FFLogsUser(id=id, client=self)
