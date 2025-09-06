from scripts import army, holds, menu

def train_unit(selected_hold, player_house, cost, unit_type, file_name):
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


def upgrade_unit(selected_hold, player_house, cost, from_type, to_type, new_file_name):
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


def train_archer(selected_hold, player_house):
    cost = [10, 10, 3, 0]
    train_unit(selected_hold, player_house, cost, army.UnitType.ARCHER, "_archer")


def train_soldier(selected_hold, player_house):
    cost = [15, 15, 5, 0]
    train_unit(selected_hold, player_house, cost, army.UnitType.SOLDIER, "_soldier")


def train_knight(selected_hold, player_house):
    cost = [15, 20, 10, 1]
    upgrade_unit(selected_hold, player_house, cost, army.UnitType.SOLDIER, army.UnitType.KNIGHT, "_knight")

def appoint_kingsguard(selected_hold, player_house):
    cost = [20, 25, 15, 10]
    upgrade_unit(selected_hold, player_house, cost, army.UnitType.KNIGHT, army.UnitType.KINGSGUARD, "_kingsguard")

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