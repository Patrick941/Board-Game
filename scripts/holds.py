import pyglet
import csv
import os
from scripts import army
from pyglet import shapes

current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, '..', 'Images')
data_dir = os.path.join(current_dir, '..', 'data')
menu_bg_color = (228, 213, 183)

icons = {
    "food": pyglet.image.load(os.path.join(images_dir, 'Food.png')),
    "wood": pyglet.image.load(os.path.join(images_dir, 'Wood.png')),
    "iron": pyglet.image.load(os.path.join(images_dir, 'Iron.png')),
    "gold": pyglet.image.load(os.path.join(images_dir, 'Gold.png'))
}

# Consolidated house data into a single dictionary
houses = {
    "Tyrell": {
        "region": "The Reach",
        "colours": [(150, 255, 150), (150, 255, 150)],
        "resources": (0, 0, 0, 0)
    },
    "Stark": {
        "region": "The North",
        "colours": [(200, 200, 200), (240, 240, 240)],
        "resources": (0, 0, 0, 0)
    },
    "Arryn": {
        "region": "The Vale",
        "colours": [(173, 150, 255), (173, 216, 255)],
        "resources": (0, 0, 0, 0)
    },
    "Tully": {
        "region": "The Riverlands",
        "colours": [(170, 85, 230), (230, 85, 170)],
        "resources": (0, 0, 0, 0)
    },
    "Baratheon": {
        "region": "The Stormlands",
        "colours": [(255, 255, 100), (255, 255, 100)],
        "resources": (0, 0, 0, 0)
    },
    "Martell": {
        "region": "Dorne",
        "colours": [(255, 165, 50), (255, 165, 50)],
        "resources": (0, 0, 0, 0)
    },
    "Lannister": {
        "region": "The Westerlands",
        "colours": [(255, 70, 70), (255, 70, 70)],
        "resources": (0, 0, 0, 0)
    },
    "Greyjoy": {
        "region": "The Iron Islands",
        "colours": [(50, 160, 160), (50, 160, 160)],
        "resources": (0, 0, 0, 0)
    },
    "Targaryen": {
        "region": "The Crownlands",
        "colours": [(100, 100, 100), (0, 0, 0)],
        "resources": (0, 0, 0, 0)
    }
}

holds = []
hold_markers = []

# Load castle images with proper path handling
small_castle_image = pyglet.image.load(os.path.join(images_dir, 'Small_Castle_Icon.png'))
medium_castle_image = pyglet.image.load(os.path.join(images_dir, 'Medium_Castle_Icon.png'))
large_castle_image = pyglet.image.load(os.path.join(images_dir, 'Large_Castle_Icon.png'))

def reset_resources():
    for house_name in houses:
        houses[house_name]["resources"] = (0, 0, 0, 0)
        
def get_output(hold):
    food = int(hold.get("food", "0"))
    wood = int(hold.get("wood", "0"))
    iron = int(hold.get("iron", "0"))
    gold = int(hold.get("gold", "0"))
    
    return (food, wood, iron, gold)

def get_max_output(hold):
    food = int(hold.get("food", "0")) * 2
    wood = int(hold.get("wood", "0")) * 2
    iron = int(hold.get("iron", "0")) * 2
    gold = int(hold.get("gold", "0")) * 2
    
    return (food, wood, iron, gold)

def set_output(hold, new_output):
    hold["food"] = str(int(new_output[0]))
    hold["wood"] = str(int(new_output[1]))
    hold["iron"] = str(int(new_output[2]))
    hold["gold"] = str(int(new_output[3]))
    
def get_total_increase(player_house):
    increase_list = [0, 0, 0, 0]
    for hold in holds:
        if hold.get("house") == player_house:
            resources = get_output(hold)
            for i in range(4):
                increase_list[i] += int(resources[i])
    return tuple(increase_list)
    
def get_total_resources(player_house):
    return houses[player_house]["resources"]

def set_total_resources(player_house, new_resources):
    houses[player_house]["resources"] = new_resources

def load_holds(turn_counter):
    unit_types = ["_archer", "_soldier", "_knight", "_kingsguard"]
    global holds, hold_markers
    hold_markers = []

    csv_path = os.path.join(data_dir, 'holds.csv')
    if turn_counter[0] == 1:
        holds = []
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                region_name = row.get("region", "")
                # Find house by region
                house_name = next((name for name, data in houses.items() if data["region"] == region_name), "NA")
                
                resources_string = row.get("resources")
                resources = resources_string.split("|")
                size = row.get("size", "Small")
                if size == "Small":
                    multiplier = 1
                elif size == "Medium":
                    multiplier = 2
                elif size == "Large":
                    multiplier = 4
                else:
                    print("ERROR invalid castle size, exiting")
                    exit(2)
                    
                for i, resource in enumerate(resources):
                    resources[i] = str(int(resources[i]) * multiplier)
                    
                convert_type = {
                    0: army.UnitType.ARCHER,
                    1: army.UnitType.SOLDIER,
                    2: army.UnitType.KNIGHT,
                    3: army.UnitType.KINGSGUARD
                }
                    
                army_string = row.get("army")
                army_values = army_string.split("|")
                army_struct_array = []
                for i, unit_type in enumerate(army_values):
                    for _ in range(int(unit_type)):
                        unit = army.ArmyUnit(convert_type[i], experience=1, file_name=unit_types[i])
                        army_struct_array.append(unit)
                        

                h = {
                    "name": row.get("name", ""),
                    "region": region_name,
                    "x_cord": row.get("x_cord", "0"),
                    "y_cord": row.get("y_cord", "0"),
                    "defense_rating": row.get("defense_rating", "0"),
                    "size": size,
                    "house": house_name,
                    "borders": row.get("borders", ".."),
                    "food": resources[0],
                    "wood": resources[1],
                    "iron":resources[2],
                    "gold": resources[3],
                    "army": army_struct_array
                }
                holds.append(h)
                
    for house_name in houses:
        total_resources = get_total_resources(house_name)
        total_increase = get_total_increase(house_name)
        total_resources = tuple(total_resources[i] + total_increase[i] for i in range(len(total_resources)))
        set_total_resources(house_name, total_resources)

    for h in holds:
        if all(h.get(k, "NA") != "NA" for k in ("name", "region", "x_cord", "y_cord")):
            try:
                wx = float(h["x_cord"])
                wy = float(h["y_cord"])
            except ValueError:
                continue
            size = h.get("size", "Small").lower()
            if size == "large":
                castle_img = large_castle_image
            elif size == "medium":
                castle_img = medium_castle_image
            else:
                castle_img = small_castle_image
            sprite = pyglet.sprite.Sprite(castle_img, x=0, y=0)
            sprite.scale = 0.5
            house = h.get("house", "")
            sprite.color = houses[house]["colours"][0]
            hold_markers.append({
                "world": (wx, wy),
                "sprite": sprite,
                "data": h,
                "size": size
            })

def show_titles(holds, world_to_screen, zoom, font_name):
    for hold in holds:
        name = hold["name"]
        size = hold.get("size", "Small").lower()
        house = hold.get("house", "NA")

        try:
            wx = float(hold["x_cord"])
            wy = float(hold["y_cord"])
        except ValueError:
            continue

        sx, sy = world_to_screen(wx, wy)
        x_offset = 0
        if size == "large":
            y_offset = 65
            x_offset = 15
        elif size == "medium":
            y_offset = 35
        else:
            y_offset = 30

        colour = houses[house]["colours"][1]

        label = pyglet.text.Label(
            name,
            font_name=font_name,
            font_size=int(30 * zoom),
            x=sx + x_offset,
            y=sy + y_offset,
            anchor_x='center',
            anchor_y='bottom',
            color=colour
        )
        label.draw()
        
def highlight_hold(window_width, window_height, camera_x, camera_y, zoom, mouse_x, mouse_y, tolerance, font_name):
    for hold in holds:
        x = (int(hold["x_cord"]) - camera_x) * zoom
        y = (int(hold["y_cord"]) - camera_y) * zoom
        dx = mouse_x - x
        dy = mouse_y - y
        distance = (dx**2 + dy**2)**0.5
        if (distance < tolerance):
            army.show_units(houses, hold, window_width, window_height, camera_x, camera_y, zoom)
            
            
            icon_size = 40
            icons_width = icon_size * 8
            bg_width = icons_width + (icon_size / 2)
            bg_height = 50
            bg_x = x - (bg_width / 2)
            bg_y = y - (bg_height) - 5

            background_rect = shapes.RoundedRectangle(
                x=bg_x - (icon_size / 2), 
                y=bg_y, 
                width=bg_width, 
                height=bg_height, 
                color=menu_bg_color,
                radius=20
            )
            background_rect.draw()

            for i, (name, sprite_image) in enumerate(icons.items()):
                icon_x = x - (icons_width / 2) + (icons_width / (2 * len(icons))) + (i * (icons_width / len(icons))) - (icon_size / 2)
                text_x = icon_x - icon_size
                text_string = hold[name]
                
                sprite = pyglet.sprite.Sprite(sprite_image)
                scale = icon_size / max(sprite.image.width, sprite.image.height)
                sprite.scale = scale
                sprite.x = icon_x
                sprite.y = y - 50
                sprite.draw()
                
                pyglet.text.Label(
                    text_string,
                    font_name=font_name,
                    font_size=30,
                    x=text_x,
                    y=y - 50,
                    anchor_x="left",
                    anchor_y="bottom",
                    color=houses[hold["house"]]["colours"][1]
                ).draw()