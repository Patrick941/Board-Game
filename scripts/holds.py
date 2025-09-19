import pyglet
import csv
import os
from pyglet import shapes
from typing import Dict, Any, List, Tuple, Optional
from scripts.army import ArmyUnit, UnitType, army_manager

class HoldManager:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.current_dir, '..', 'Images')
        self.data_dir = os.path.join(self.current_dir, '..', 'data')
        self.menu_bg_color = (228, 213, 183)
        
        self.icons = self._load_icons()
        self.houses = self._create_houses_dict()
        self.holds: List[Dict[str, Any]] = []
        self.hold_markers: List[Dict[str, Any]] = []
        
        self.small_castle_image = pyglet.image.load(os.path.join(self.images_dir, 'Small_Castle_Icon.png'))
        self.medium_castle_image = pyglet.image.load(os.path.join(self.images_dir, 'Medium_Castle_Icon.png'))
        self.large_castle_image = pyglet.image.load(os.path.join(self.images_dir, 'Large_Castle_Icon.png'))
        
        self.wood_shield = pyglet.image.load(os.path.join(self.images_dir, 'wood_shield.png'))
        self.iron_shield = pyglet.image.load(os.path.join(self.images_dir, 'iron_shield.png'))
        self.gold_shield = pyglet.image.load(os.path.join(self.images_dir, 'gold_shield.png'))
        self.reinforced_shield = pyglet.image.load(os.path.join(self.images_dir, 'reinforced_shield.png'))
    
    def _load_icons(self) -> Dict[str, Any]:
        icon_files = {
            "food": 'Food.png',
            "wood": 'Wood.png',
            "iron": 'Iron.png',
            "gold": 'Gold.png'
        }
        
        icons = {}
        for name, filename in icon_files.items():
            try:
                path = os.path.join(self.images_dir, filename)
                icons[name] = pyglet.image.load(path)
            except FileNotFoundError:
                print(f"Warning: Could not load icon {filename}")
                icons[name] = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(32, 32)
        
        return icons
    
    def _create_houses_dict(self) -> Dict[str, Dict[str, Any]]:
        return {
            "Tyrell": {
                "region": "The Reach",
                "colours": [(150, 255, 150), (150, 255, 150)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Stark": {
                "region": "The North",
                "colours": [(200, 200, 200), (240, 240, 240)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Arryn": {
                "region": "The Vale",
                "colours": [(173, 150, 255), (173, 216, 255)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Tully": {
                "region": "The Riverlands",
                "colours": [(170, 85, 230), (230, 85, 170)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Baratheon": {
                "region": "The Stormlands",
                "colours": [(255, 255, 100), (255, 255, 100)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Martell": {
                "region": "Dorne",
                "colours": [(255, 165, 50), (255, 165, 50)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Lannister": {
                "region": "The Westerlands",
                "colours": [(255, 70, 70), (255, 70, 70)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Greyjoy": {
                "region": "The Iron Islands",
                "colours": [(50, 160, 160), (50, 160, 160)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            },
            "Targaryen": {
                "region": "The Crownlands",
                "colours": [(100, 100, 100), (0, 0, 0)],
                "resources": (0, 0, 0, 0),
                "kingdom": False
            }
        }
    
    def reset_resources(self) -> None:
        for house_name in self.houses:
            self.houses[house_name]["resources"] = (0, 0, 0, 0)
    
    def get_output(self, hold: Dict[str, Any]) -> Tuple[int, int, int, int]:
        food = int(hold.get("food", "0"))
        wood = int(hold.get("wood", "0"))
        iron = int(hold.get("iron", "0"))
        gold = int(hold.get("gold", "0"))
        
        return (food, wood, iron, gold)
    
    def get_max_output(self, hold: Dict[str, Any]) -> Tuple[int, int, int, int]:
        food = int(hold.get("food", "0")) * 2
        wood = int(hold.get("wood", "0")) * 2
        iron = int(hold.get("iron", "0")) * 2
        gold = int(hold.get("gold", "0")) * 2
        
        return (food, wood, iron, gold)
    
    def set_output(self, hold: Dict[str, Any], new_output: Tuple[int, int, int, int]) -> None:
        hold["food"] = str(int(new_output[0]))
        hold["wood"] = str(int(new_output[1]))
        hold["iron"] = str(int(new_output[2]))
        hold["gold"] = str(int(new_output[3]))
    
    def get_total_increase(self, player_house: str) -> Tuple[int, int, int, int]:
        increase_list = [0, 0, 0, 0]
        for hold in self.holds:
            if hold.get("house") == player_house:
                resources = self.get_output(hold)
                for i in range(4):
                    increase_list[i] += int(resources[i])
        return tuple(increase_list)
    
    def get_total_resources(self, player_house: str) -> Tuple[int, int, int, int]:
        return self.houses[player_house]["resources"]
    
    def set_total_resources(self, player_house: str, new_resources: Tuple[int, int, int, int]) -> None:
        self.houses[player_house]["resources"] = new_resources
    
    def load_holds(self, turn_counter: List[int]) -> None:
        unit_types = ["_archer", "_soldier", "_knight", "_kingsguard"]
        self.holds = []
        
        csv_path = os.path.join(self.data_dir, 'holds.csv')
        if turn_counter[0] == 1:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self._process_hold_row(row, unit_types)
        
        for house_name in self.houses:
            total_resources = self.get_total_resources(house_name)
            total_increase = self.get_total_increase(house_name)
            total_resources = tuple(total_resources[i] + total_increase[i] for i in range(len(total_resources)))
            self.set_total_resources(house_name, total_resources)
    
    def _process_hold_row(self, row: Dict[str, str], unit_types: List[str]) -> None:
        region_name = row.get("region", "")
        house_name = next((name for name, data in self.houses.items() if data["region"] == region_name), "NA")
        
        resources_string = row.get("resources", "")
        resources = resources_string.split("|") if resources_string else ["0", "0", "0", "0"]
        
        size = row.get("size", "Small")
        multiplier = self._get_size_multiplier(size)
        
        for i, resource in enumerate(resources):
            resources[i] = str(int(resource) * multiplier)
        
        army_struct_array = self._process_army_data(row.get("army", ""), unit_types)
        
        hold = {
            "name": row.get("name", ""),
            "region": region_name,
            "x_cord": row.get("x_cord", "0"),
            "y_cord": row.get("y_cord", "0"),
            "defense_rating": int(row.get("defense_rating", "0")),
            "size": size,
            "house": house_name,
            "borders": row.get("borders", ".."),
            "food": resources[0],
            "wood": resources[1],
            "iron": resources[2],
            "gold": resources[3],
            "army": army_struct_array,
            "capital": size == "Large"
        }
        self.holds.append(hold)
    
    def _get_size_multiplier(self, size: str) -> int:
        if size == "Small":
            return 1
        elif size == "Medium":
            return 2
        elif size == "Large":
            return 4
        else:
            print("ERROR invalid castle size, exiting")
            exit(2)
    
    def _process_army_data(self, army_string: str, unit_types: List[str]) -> List[ArmyUnit]:
        convert_type = {
            0: UnitType.ARCHER,
            1: UnitType.SOLDIER,
            2: UnitType.KNIGHT,
            3: UnitType.KINGSGUARD
        }
        
        army_values = army_string.split("|") if army_string else ["0", "0", "0", "0"]
        army_struct_array = []
        
        for i, unit_count in enumerate(army_values):
            for _ in range(int(unit_count)):
                unit = ArmyUnit(convert_type[i], experience=1, file_name=unit_types[i])
                army_struct_array.append(unit)
        
        return army_struct_array
    
    def reload_hold_markers(self) -> None:
        self.hold_markers = []
        
        for h in self.holds:
            if all(h.get(k, "NA") != "NA" for k in ("name", "region", "x_cord", "y_cord")):
                try:
                    wx = float(h["x_cord"])
                    wy = float(h["y_cord"])
                except ValueError:
                    continue
                
                castle_img = self._get_castle_image(h.get("size", "Small"))
                sprite = pyglet.sprite.Sprite(castle_img, x=0, y=0)
                sprite.scale = 0.5
                house = h.get("house", "")
                sprite.color = self.houses[house]["colours"][0]
                
                self.hold_markers.append({
                    "world": (wx, wy),
                    "sprite": sprite,
                    "data": h,
                    "size": h.get("size", "Small").lower()
                })
    
    def _get_castle_image(self, size: str) -> Any:
        if size.lower() == "large":
            return self.large_castle_image
        elif size.lower() == "medium":
            return self.medium_castle_image
        else:
            return self.small_castle_image
    
    def show_titles(self, world_to_screen, zoom: float, font_name: str) -> None:
        for hold in self.holds:
            name = hold["name"]
            size = hold.get("size", "Small").lower()
            house = hold.get("house", "NA")

            try:
                wx = float(hold["x_cord"])
                wy = float(hold["y_cord"])
            except ValueError:
                continue

            sx, sy = world_to_screen(wx, wy)
            x_offset, y_offset = self._get_title_offset(size)
            
            colour = self.houses[house]["colours"][1]

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
    
    def _get_title_offset(self, size: str) -> Tuple[int, int]:
        if size == "large":
            return (15, 65)
        elif size == "medium":
            return (0, 35)
        else:
            return (0, 30)
    
    def highlight_hold(self, window_width: int, window_height: int, camera_x: float, 
                      camera_y: float, zoom: float, mouse_x: float, mouse_y: float, 
                      tolerance: float, font_name: str) -> None:
        for hold in self.holds:
            x = (int(hold["x_cord"]) - camera_x) * zoom
            y = (int(hold["y_cord"]) - camera_y) * zoom
            dx = mouse_x - x
            dy = mouse_y - y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < tolerance:
                self._draw_hold_highlight(hold, x, y, zoom, font_name)
    
    def _draw_hold_highlight(self, hold: Dict[str, Any], x: float, y: float, 
                             zoom: float, font_name: str) -> None:
        army_manager.show_units(hold, 0, 0, 0, 0, zoom)
        
        defense_rating = hold.get("defense_rating", 0)
        shield_image = self._get_shield_image(defense_rating)
        
        icon_size = 40
        icons_width = icon_size * 8
        bg_width = icons_width + (icon_size / 2)
        bg_height = 50
        
        shield_sprite = pyglet.sprite.Sprite(shield_image)
        shield_sprite.scale = 0.1 * zoom
        shield_x = x + (bg_width / 2)
        shield_y = y - (3 * bg_height / 2)
        shield_sprite.x = shield_x
        shield_sprite.y = shield_y
        shield_sprite.draw()
        
        defense_label = pyglet.text.Label(
            str(defense_rating),
            font_name=font_name,
            font_size=50 * zoom,
            x=shield_x + shield_sprite.width / 2 - 10,
            y=shield_y + shield_sprite.height / 2 + 10,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 255)
        )
        defense_label.draw()
        
        bg_x = x - (bg_width / 2)
        bg_y = y - bg_height - 5

        background_rect = shapes.RoundedRectangle(
            x=bg_x - (icon_size / 2), 
            y=bg_y, 
            width=bg_width, 
            height=bg_height, 
            color=self.menu_bg_color,
            radius=20
        )
        background_rect.draw()

        for i, (name, sprite_image) in enumerate(self.icons.items()):
            self._draw_resource_highlight(hold, name, sprite_image, x, y, i, 
                                          icons_width, icon_size, font_name)
    
    def _get_shield_image(self, defense_rating: int) -> Any:
        if defense_rating <= 3:
            return self.wood_shield
        elif defense_rating <= 6:
            return self.iron_shield
        elif defense_rating <= 8:
            return self.gold_shield
        else:
            return self.reinforced_shield
    
    def _draw_resource_highlight(self, hold: Dict[str, Any], name: str, 
                                 sprite_image: Any, x: float, y: float, 
                                 index: int, icons_width: float, 
                                 icon_size: float, font_name: str) -> None:
        icon_x = x - (icons_width / 2) + (icons_width / (2 * len(self.icons))) + (index * (icons_width / len(self.icons))) - (icon_size / 2)
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
            color=self.houses[hold["house"]]["colours"][1]
        ).draw()
        
hold_manager = HoldManager()