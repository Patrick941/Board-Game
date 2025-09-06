from scripts import army, holds, menu

def train_soldiers(selected_hold, player_house):
    cost = [10, 10, 3, 0]  # wood, food, iron, gold, stone
    get_resources = holds.get_total_resources(player_house)
    get_resources_list = list(get_resources)
    for i in range(len(cost)):
        if get_resources_list[i] < cost[i]:
            menu.draw_hover_text("Not enough resources!", 1000, 200)
            return
        get_resources_list[i] -= cost[i]
    holds.set_total_resources(player_house, tuple(get_resources_list))
    unit = army.ArmyUnit(army.UnitType.ARCHER, experience=1, file_name="_archer")
    selected_hold["army"].append(unit)
    return

def upgrade_units(selected_hold, player_house):
    pass

def improve_farms(selected_hold, player_house):
    pass

def plant_forests(selected_hold, player_house):
    pass

def improve_iron_mines(selected_hold, player_house):
    pass

def improve_gold_mines(selected_hold, player_house):
    pass

def call_banners(selected_hold, player_house):
    pass

def declare_kingdom(selected_hold, player_house):
    pass