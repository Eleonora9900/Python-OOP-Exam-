from project.divers.base_diver import BaseDiver


class FreeDiver(BaseDiver):
    def __init__(self, name: str):
        super().__init__(name, 120.0)

    def miss(self, time_to_catch: int):
        value = time_to_catch - time_to_catch * 0.6
        if isinstance(value, float):
            round(value)
        if self.oxygen_level - value < 0:
            self.oxygen_level = 0
        else:
            self.oxygen_level -= value

    def renew_oxy(self):
        self.oxygen_level = 120
