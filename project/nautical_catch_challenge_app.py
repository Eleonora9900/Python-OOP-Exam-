from typing import List

from project.divers.base_diver import BaseDiver
from project.divers.free_diver import FreeDiver
from project.divers.scuba_diver import ScubaDiver
from project.fish.deep_sea_fish import DeepSeaFish
from project.fish.predatory_fish import PredatoryFish


class NauticalCatchChallengeApp:
    VALID_DIVERS = {"FreeDiver": FreeDiver, "ScubaDiver": ScubaDiver}
    VALID_FISHES = {"PredatoryFish": PredatoryFish, "DeepSeaFish": DeepSeaFish}

    def __init__(self):
        self.divers: List[BaseDiver] = []
        self.fish_list: List = []

    @staticmethod
    def find_obj(obj_name, collection):
        return next((o for o in collection if o.name == obj_name), None)

    def dive_into_competition(self, diver_type: str, diver_name: str):
        if diver_type not in self.VALID_DIVERS:
            return f"{diver_type} is not allowed in our competition."
        diver = self.find_obj(diver_name, self.divers)
        if diver:
            return f"{diver_name} is already a participant."
        new_diver = self.VALID_DIVERS[diver_type](diver_name)
        self.divers.append(new_diver)
        return f"{diver_name} is successfully registered for the competition as a {diver_type}."

    def swim_into_competition(self, fish_type: str, fish_name: str, points: float):
        if fish_type not in self.VALID_FISHES:
            return f"{fish_type} is forbidden for chasing in our competition."
        fish = self.find_obj(fish_name, self.fish_list)
        if fish:
            return f"{fish_name} is already permitted."
        new_fish = self.VALID_FISHES[fish_type](fish_name, points)
        self.fish_list.append(new_fish)
        return f"{fish_name} is allowed for chasing as a {fish_type}."

    def chase_fish(self, diver_name: str, fish_name: str, is_lucky: bool):
        diver = self.find_obj(diver_name, self.divers)
        if diver is None:
            return f"{diver_name} is not registered for the competition."
        fish = self.find_obj(fish_name, self.fish_list)
        if fish is None:
            return f"The {fish_name} is not allowed to be caught in this competition."
        if diver.has_health_issue:
            return f"{diver_name} will not be allowed to dive, due to health issues."
        if diver.oxygen_level < fish.time_to_catch:
            diver.miss(fish.time_to_catch)
            if diver.oxygen_level == 0:
                diver.has_health_issue = True
            return f"{diver_name} missed a good {fish_name}."
        elif diver.oxygen_level == fish.time_to_catch:
            if is_lucky:
                diver.hit(fish)
                if diver.oxygen_level == 0:
                    diver.has_health_issue = True
                return f"{diver_name} hits a {fish.points}pt. {fish_name}."
            diver.miss(fish.time_to_catch)
            if diver.oxygen_level == 0:
                diver.has_health_issue = True
            return f"{diver_name} missed a good {fish_name}."
        else:
            diver.hit(fish)
            if diver.oxygen_level == 0:
                diver.has_health_issue = True
            return f"{diver_name} hits a {fish.points}pt. {fish_name}."

    def health_recovery(self):
        count = 0
        for diver in self.divers:
            if diver.has_health_issue:
                diver.update_health_status()
                diver.renew_oxy()
                count += 1
        return f"Divers recovered: {count}"

    def diver_catch_report(self, diver_name: str):
        diver = self.find_obj(diver_name, self.divers)
        result = [f"**{diver_name} Catch Report**"]
        for f in diver.catch:
            info = f.fish_details()
            result.append(info)
        return "\n".join(result)

    def competition_statistics(self):
        new_divers = [d for d in self.divers if not d.has_health_issue]
        result = ["**Nautical Catch Challenge Statistics**"]
        for d in sorted(new_divers, key=lambda x: (-x.competition_points, -len(x.catch), x.name)):
            result.append(d.__str__())
        return "\n".join(result)


