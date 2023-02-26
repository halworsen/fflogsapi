from dataclasses import dataclass


@dataclass
class FFLogsAbility:
    '''
    Represents an ability in a report
    '''
    game_id: int
    name: str
    type: str


@dataclass
class FFLogsActor:
    '''
    Represents an actor in a report
    '''
    id: int
    name: str
    type: str
    sub_type: str
    server: str
    game_id: int
    pet_owner: int = None

    def job(self):
        return self.sub_type
