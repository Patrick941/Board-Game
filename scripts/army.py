import os
import pyglet
import math
import random
from enum import Enum
from dataclasses import dataclass
from enum import Enum

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
army_dir = os.path.join(current_dir, "Images", "army")
images_dir = os.path.join(current_dir, 'Images')

class UnitType(Enum):
    ARCHER = 1
    SOLDIER = 2
    KNIGHT = 3
    KINGSGUARD = 4

@dataclass
class ArmyUnit:
    unit_type: UnitType
    experience: int
    file_name: str = ""
    stars: int = 1

class ArmyManager:
    def __init__(self):
        self.army_images = {}
        self.star_image = pyglet.image.load(os.path.join(images_dir, 'star.png'))
        self.convert_type = {
            UnitType.ARCHER: 0,
            UnitType.SOLDIER: 1,
            UnitType.KNIGHT: 2,
            UnitType.KINGSGUARD: 3
        }
        self.army_init()

    def army_init(self):
        for filename in os.listdir(army_dir):
            if filename.endswith(".png"):
                image_name = filename.replace(".png", "")
                path = os.path.join(army_dir, filename)
                self.army_images[image_name] = pyglet.image.load(path)

    def move_units(self, attacker_hold, defender_hold, hold_manager):
        defender_hold["army"].extend(attacker_hold["army"])
        attacker_hold["army"] = []
        defender_hold["house"] = attacker_hold["house"]
        hold_manager.reload_hold_markers()

    def attack_hold(self, attacker_hold, defender_hold, hold_manager, lethality=1.5, experience_gain_scale=3):
        attacker_units = attacker_hold["army"][:]
        defender_units = defender_hold["army"][:]

        attacker_strength = sum(unit.unit_type.value * unit.stars for unit in attacker_units)
        defender_strength = sum(unit.unit_type.value * unit.stars for unit in defender_units)

        combined_units = []
        for unit in attacker_units:
            combined_units.append({"unit": unit, "role": "attacker"})
        for unit in defender_units:
            combined_units.append({"unit": unit, "role": "defender"})

        random.shuffle(combined_units)
        units_to_remove = []

        for entry in combined_units:
            if attacker_strength <= 0 or defender_strength <= 0:
                break
            
            unit = entry["unit"]
            role = entry["role"]
            unit_power = unit.unit_type.value * unit.stars
            total_strength = attacker_strength + defender_strength

            if total_strength == 0:
                break

            if role == "attacker":
                death_prob = (defender_strength / total_strength) * lethality
            else:
                death_prob = (attacker_strength / total_strength) * lethality

            death_prob = max(0.1, min(0.9, death_prob))

            rand_num = random.random()
            if rand_num < death_prob:
                units_to_remove.append(unit)
                if role == "attacker":
                    attacker_strength -= unit_power
                else:
                    defender_strength -= unit_power
            else:
                xp_gain = (1 + (death_prob * 2)) * experience_gain_scale
                if death_prob > 0.7:
                    xp_gain += 1 * experience_gain_scale
                unit.experience += int(xp_gain)

        for unit in units_to_remove:
            if unit in attacker_units:
                attacker_units.remove(unit)
            if unit in defender_units:
                defender_units.remove(unit)

        for unit in combined_units:
            star_count = min(5, 1 + unit["unit"].experience // 10)
            unit["unit"].stars = star_count

        attacker_hold["army"] = attacker_units
        defender_hold["army"] = defender_units

        if len(defender_units) == 0 and len(attacker_units) > 0:
            defender_hold["army"].extend(attacker_hold["army"])
            attacker_hold["army"] = []
            defender_hold["house"] = attacker_hold["house"]
            hold_manager.reload_hold_markers()
            return "attacker_wins"
        elif len(attacker_units) == 0:
            return "defender_wins"
        else:
            return "stalemate"
        
    def show_units(self, hold, window_width, window_height, camera_x, camera_y, zoom):
        units = hold["army"]
        
        unit_sprites = self._draw_units(hold, camera_x, camera_y, zoom)
        
        self._draw_stars(units, unit_sprites, zoom)

    def show_units_ui_elements(self, hold, camera_x, camera_y, zoom):
        
        house = hold["house"]
        units = hold["army"]
        
        unit_sprites = self._draw_units(hold, camera_x, camera_y, zoom)
        
        self._draw_stars(units, unit_sprites, zoom)
        
    def update_costs(self, hold_manager):
        for hold in hold_manager.holds:
            for unit in hold["army"]:
                if unit.unit_type == UnitType.ARCHER:
                    cost = (1, 1, 0, 0)
                elif unit.unit_type == UnitType.SOLDIER:
                    cost = (1, 0, 1, 0)
                elif unit.unit_type == UnitType.KNIGHT:
                    cost = (1, 0, 2, 0)
                elif unit.unit_type == UnitType.KINGSGUARD:
                    cost = (1, 0, 2, 2)
                else:
                    cost = (0, 0, 0, 0)
                
                house = hold["house"]
                current_upkeep = hold_manager.houses_upkeep.get(house)
                new_upkeep = tuple(current_upkeep[i] + cost[i] for i in range(4))
                hold_manager.houses_upkeep[house] = new_upkeep

    def _draw_units(self, hold, camera_x, camera_y, zoom):
        
        house = hold["house"]
        units = hold["army"]
        icon_size = 150
        compactor = 0.4
        
        unit_sprites = []
        total_unit_counts = {unit_type: 0 for unit_type in UnitType}
        unit_counts = {unit_type: 0 for unit_type in UnitType}
        for unit in units:
            total_unit_counts[unit.unit_type] += 1
        
        for unit in units:
            i = self.convert_type[unit.unit_type]
            image_name = house + unit.file_name
            
            y = (int(hold["y_cord"]) - camera_y) + (icon_size * i * 2.2 * compactor)
            x = ((int(hold["x_cord"]) - camera_x)) - (0.5 * compactor * total_unit_counts[unit.unit_type] * icon_size) - (icon_size * compactor) + (compactor * icon_size * unit_counts[unit.unit_type])
            unit_counts[unit.unit_type] += 1
            
            sprite_image = self.army_images[image_name.lower()]
            
            sprite = pyglet.sprite.Sprite(sprite_image)
            scale = icon_size / max(sprite.image.width, sprite.image.height)
            sprite.scale = scale
            sprite.x = x
            sprite.y = y
            sprite.scale *= zoom
            sprite.draw()
            unit_sprites.append(sprite)
        
        return unit_sprites

    def _draw_stars(self, units, unit_sprites, zoom):
        
        star_size = [60, 30, 18, 12, 12]
        
        for i, sprite in enumerate(unit_sprites):
            star_count = units[i].stars
            icon_size = star_size[star_count - 1]
            scale = 0.02
            y_offset = -15
            
            x_offset = -((star_count - 1) * icon_size) / 2
                
            for j in range(star_count):
                star_sprite = pyglet.sprite.Sprite(self.star_image)
                star_sprite.scale = scale * zoom
                if (star_count % 2) > 0:
                    offset_num = abs(math.floor(star_count / 2) - j)
                else:
                    offset_num = abs((star_count / 2 - 0.5) - j) + 0.5
                
                star_sprite.x = sprite.x + (sprite.width / 2) - (star_sprite.width / 2) + x_offset + (j * icon_size)
                star_sprite.y = sprite.y + sprite.height + (star_sprite.height / 2) + y_offset - (offset_num * (star_sprite.height / 3))
                
                star_sprite.draw()
                
army_manager = ArmyManager()