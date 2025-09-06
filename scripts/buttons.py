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

def improve_resource(selected_hold, player_house, cost, resource_index, no_resource_msg, maxed_msg):
    resources = holds.get_output(selected_hold)
    current_value = resources[resource_index]
    max_resources = holds.get_max_output(selected_hold)
    max_value = max_resources[resource_index]

    if current_value == 0:
        menu.draw_hover_text(no_resource_msg, 1000, 200)
        return
    elif current_value >= max_value:
        menu.draw_hover_text(maxed_msg, 1000, 200)
        return
    else:
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


def improve_farms(selected_hold, player_house):
    cost = [30, 10, 5, 0]
    return improve_resource(
        selected_hold, player_house, cost, 0,
        "Hold has no farms",
        "Farms already at maximum efficiency"
    )


def plant_forests(selected_hold, player_house):
    cost = [10, 30, 5, 0]
    return improve_resource(
        selected_hold, player_house, cost, 1,
        "Hold has no forests",
        "Forests already at maximum efficiency"
    )


def improve_iron_mines(selected_hold, player_house):
    cost = [5, 10, 30, 0]
    return improve_resource(
        selected_hold, player_house, cost, 2,
        "Hold has no iron mines",
        "Iron mines already at maximum efficiency"
    )


def improve_gold_mines(selected_hold, player_house):
    cost = [5, 5, 10, 30]
    return improve_resource(
        selected_hold, player_house, cost, 3,
        "Hold has no gold mines",
        "Gold mines already at maximum efficiency"
    )


def call_banners(selected_hold, player_house):
    pass

def declare_kingdom(selected_hold, player_house):
    pass