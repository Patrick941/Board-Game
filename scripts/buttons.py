from scripts import army, holds, menu
from typing import Tuple, List, Optional

class UnitTrainer:
    def __init__(self):
        pass
    
    def train_unit(self, selected_hold: dict, player_house: str, cost: List[int], 
                     unit_type: army.UnitType, file_name: str) -> bool:
        get_resources = holds.get_total_resources(player_house)
        get_resources_list = list(get_resources)

        for i in range(len(cost)):
            if get_resources_list[i] < cost[i]:
                menu.draw_hover_text("Not enough resources!", 1000, 200)
                return False

        for i in range(len(cost)):
            get_resources_list[i] -= cost[i]

        holds.set_total_resources(player_house, tuple(get_resources_list))
        unit = army.ArmyUnit(unit_type, experience=1, file_name=file_name)
        selected_hold["army"].append(unit)
        return True

    def upgrade_unit(self, selected_hold: dict, player_house: str, cost: List[int], 
                       from_type: army.UnitType, to_type: army.UnitType, new_file_name: str) -> bool:
        get_resources = holds.get_total_resources(player_house)
        get_resources_list = list(get_resources)

        for i in range(len(cost)):
            if get_resources_list[i] < cost[i]:
                menu.draw_hover_text("Not enough resources!", 1000, 200)
                return False

        unit_to_upgrade = None
        for unit in selected_hold["army"]:
            if unit.unit_type == from_type:
                unit_to_upgrade = unit
                break

        if not unit_to_upgrade:
            menu.draw_hover_text(f"No {from_type.name.lower()} available to upgrade!", 1000, 200)
            return False

        for i in range(len(cost)):
            get_resources_list[i] -= cost[i]

        holds.set_total_resources(player_house, tuple(get_resources_list))

        unit_to_upgrade.unit_type = to_type
        unit_to_upgrade.file_name = new_file_name
        return True

    def train_archer(self, selected_hold: dict, player_house: str) -> bool:
        cost = [10, 10, 3, 0]
        return self.train_unit(selected_hold, player_house, cost, army.UnitType.ARCHER, "_archer")

    def train_soldier(self, selected_hold: dict, player_house: str) -> bool:
        cost = [15, 15, 5, 0]
        return self.train_unit(selected_hold, player_house, cost, army.UnitType.SOLDIER, "_soldier")

    def train_knight(self, selected_hold: dict, player_house: str) -> bool:
        cost = [15, 20, 10, 1]
        return self.upgrade_unit(selected_hold, player_house, cost, 
                                 army.UnitType.SOLDIER, army.UnitType.KNIGHT, "_knight")

    def appoint_kingsguard(self, selected_hold: dict, player_house: str) -> bool:
        cost = [20, 25, 15, 10]
        return self.upgrade_unit(selected_hold, player_house, cost,
                                 army.UnitType.KNIGHT, army.UnitType.KINGSGUARD, "_kingsguard")


class ResourceManager:
    def __init__(self):
        pass
    
    def improve_resource(self, selected_hold: dict, player_house: str, cost: List[int], 
                           resource_index: int, no_resource_msg: str, maxed_msg: str) -> bool:
        resources = holds.get_output(selected_hold)
        current_value = resources[resource_index]
        max_resources = holds.get_max_output(selected_hold)
        max_value = max_resources[resource_index]

        if current_value == 0:
            menu.draw_hover_text(no_resource_msg, 1000, 200)
            return False
        elif current_value >= max_value:
            menu.draw_hover_text(maxed_msg, 1000, 200)
            return False

        get_resources = holds.get_total_resources(player_house)
        get_resources_list = list(get_resources)

        for i in range(len(cost)):
            if get_resources_list[i] < cost[i]:
                menu.draw_hover_text("Not enough resources!", 1000, 200)
                return False

        for i in range(len(cost)):
            get_resources_list[i] -= cost[i]

        if selected_hold["size"] == "Large":
            improvement = 3
        elif selected_hold["size"] == "Medium":
            improvement = 2
        else:
            improvement = 1

        holds.set_total_resources(player_house, tuple(get_resources_list))
        new_value = min(current_value + improvement, max_value)

        new_output = list(resources)
        new_output[resource_index] = new_value
        holds.set_output(selected_hold, tuple(new_output))
        return True

    def improve_farms(self, selected_hold: dict, player_house: str) -> bool:
        cost = [30, 10, 5, 0]
        return self.improve_resource(
            selected_hold, player_house, cost, 0,
            "Hold has no farms",
            "Farms already at maximum efficiency"
        )

    def plant_forests(self, selected_hold: dict, player_house: str) -> bool:
        cost = [10, 30, 5, 0]
        return self.improve_resource(
            selected_hold, player_house, cost, 1,
            "Hold has no forests",
            "Forests already at maximum efficiency"
        )

    def improve_iron_mines(self, selected_hold: dict, player_house: str) -> bool:
        cost = [5, 10, 30, 0]
        return self.improve_resource(
            selected_hold, player_house, cost, 2,
            "Hold has no iron mines",
            "Iron mines already at maximum efficiency"
        )

    def improve_gold_mines(self, selected_hold: dict, player_house: str) -> bool:
        cost = [5, 5, 10, 30]
        return self.improve_resource(
            selected_hold, player_house, cost, 3,
            "Hold has no gold mines",
            "Gold mines already at maximum efficiency"
        )


class KingdomManager:
    def __init__(self):
        pass
    
    def call_banners(self, selected_hold: dict, player_house: str) -> None:
        for hold in holds.holds:
            if hold["house"] == player_house and hold != selected_hold:
                for unit in hold["army"]:
                    selected_hold["army"].append(unit)
                hold["army"].clear()

    def declare_kingdom(self, selected_hold: dict, player_house: str) -> bool:
        if holds.houses[player_house]["kingdom"] is True:
            menu.draw_hover_text("You are already a kingdom!", 1000, 200)
            return False
        
        cost = [0, 0, 0, 0]
        resources = holds.get_total_resources(player_house)
        
        if (resources[0] > 200) and (resources[1] > 200) and (resources[2] > 200) and (resources[3] > 200):
            for _ in range(7):
                unit_trainer = UnitTrainer()
                unit_trainer.train_unit(selected_hold, player_house, cost, army.UnitType.KINGSGUARD, "_kingsguard")
            
            holds.set_total_resources(player_house, (resources[0] - 200, resources[1] - 200, resources[2] - 200, resources[3] - 200))
            holds.houses[player_house]["kingdom"] = True
            return True
        else:
            menu.draw_hover_text("Not enough resources to declare a kingdom!", 1000, 200)
            return False