from typing import Any

from ..util.filters import construct_filter_string
from .queries import Q_PROG_RACE


class ProgressRaceMixin:
    '''
    Client extensions to support progress race data exposed by the FF Logs API.
    '''

    def get_progress_race(self, filters: dict = {}) -> dict[str, Any]:
        '''
        Retrieve progress race information from the FF Logs API. This includes information such as
        best fight percentages, pull counts and stream information for different guilds.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/progressracedata.doc.html

        Args:
            filters: Filters to use when finding progress races data.
        Returns:
            Progress race data made available by the FF Logs API.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        race_data = self.q(Q_PROG_RACE.format(
            innerQuery=f'progressRace{filters}'
        ))['progressRaceData']['progressRace']
        return race_data

    # def get_composition_data(self, filters: dict = {}) -> dict[str, Any]:
    #     '''
    #     Retrieve composition data for a given guild and encounter. `guildID` must be specified
    #     in the filters.

    #     Does not seem to work currently.

    #     Returns:
    #         Progress race data made available by the FF Logs API.
    #     '''
    #     filters = construct_filter_string(filters)
    #     if filters:
    #         filters = f'({filters})'

    #     comp_data = self.q(Q_PROG_RACE.format(
    #         innerQuery=f'detailedComposition{filters}'
    #     ))['progressRaceData']['detailedComposition']
    #     return comp_data
