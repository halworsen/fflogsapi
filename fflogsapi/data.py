class Report:

    def __init__(self, code, title='Untitled Report', owner={}, start=0, end=0):
        self.code = code
        self.title = title
        self.owner = owner
        self.start = start
        self.end = end

        self.fights = []

        self._iter_idx = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        result = None
        try:
            result = self.fights[self._iter_idx]
        except IndexError:
            self._iter_idx = 0
            raise StopIteration
        self._iter_idx += 1
        return result
    
    def add_fight(self, fight):
        self.fights.append(fight)
    
    def duration(self):
        return self.end - self.start


class Fight:

    def __init__(
        self,
        id=-1,
        difficulty=-1,
        name='Unknown Fight',
        kill=None,
        fightPercentage=-1,
        start=0,
        end=0,
    ):
        self.id = id
        self.difficulty = difficulty
        self.name = name
        self.kill = kill
        self.fightPercentage = fightPercentage
        self.start = start
        self.end = end
    
    def duration(self):
        return self.end - self.start
