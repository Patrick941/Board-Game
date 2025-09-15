import os
import pyglet
import math
import random
from enum import Enum

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
army_dir = os.path.join(current_dir, "Images", "army")

images_dir = os.path.join(current_dir,'Images')
star_image = pyglet.image.load(os.path.join(images_dir, 'star.png'))


from dataclasses import dataclass
from enum import Enum

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

lethality = 4
army_images = {}


def army_init():
    for filename in os.listdir(army_dir):
        if filename.endswith(".png"):
            image_name = filename.replace(".png", "")
            path = os.path.join(army_dir, filename)
            army_images[image_name] = pyglet.image.load(path)

convert_type = {
    UnitType.ARCHER: 0,
    UnitType.SOLDIER: 1,
    UnitType.KNIGHT: 2,
    UnitType.KINGSGUARD: 3
}

def move_units(source_hold, target_hold):
    units_to_move = source_hold["army"]
    target_hold["army"].extend(units_to_move)
    source_hold["army"] = []
    
def attack_hold(attacker_hold, defender_hold):
    attacker_units = attacker_hold["army"]
    defender_units = defender_hold["army"]
    
    # Create a combined list of unit dictionaries with roles
    combined_units = []
    for unit in attacker_units:
        combined_units.append({"unit": unit, "role": "attacker"})
    for unit in defender_units:
        combined_units.append({"unit": unit, "role": "defender"})

    random.shuffle(combined_units)

    attacker_strength = sum(unit.unit_type.value * unit.experience for unit in attacker_units)
    defender_strength = sum(unit.unit_type.value * unit.experience for unit in defender_units)

    units_to_remove = []
    units_to_promote = []

    for entry in combined_units:
        if attacker_strength <= 0 or defender_strength <= 0:
            break
        unit = entry["unit"]
        role = entry["role"]
        unit_power = unit.unit_type.value * unit.experience
        total_strength = attacker_strength + defender_strength
        if role == "attacker":
            survival_prob = (unit_power / total_strength) - (defender_strength / total_strength) * lethality
            rand_num = random.random()
            if rand_num > survival_prob:
                units_to_remove.append(unit)
                attacker_strength -= unit_power
            elif rand_num < survival_prob and unit.experience < 5:
                units_to_promote.append(unit)
        else:
            survival_prob = (unit_power / total_strength) - (attacker_strength / total_strength) * lethality
            rand_num = random.random()
            if rand_num > survival_prob:
                units_to_remove.append(unit)
                defender_strength -= unit_power
            elif rand_num < survival_prob and unit.experience < 5:
                units_to_promote.append(unit)

    for unit in units_to_remove:
        if unit in attacker_units:
            attacker_units.remove(unit)
        elif unit in defender_units:
            defender_units.remove(unit)

    for unit in units_to_promote:
        unit.experience += 1

    if len(attacker_units) > 0 and len(defender_units) == 0:
        move_units(attacker_hold, defender_hold)
    else:
        attacker_hold["army"] = attacker_units
    

def show_units(house_region, hold, window_width, window_height, camera_x, camera_y, zoom):
    house = hold["house"]
    units = hold["army"]
    total_army = len(units)
    icon_size = 150    
    compactor = 0.4

    unit_sprites = []
    
    total_unit_counts = {unit_type: 0 for unit_type in UnitType}
    unit_counts = {unit_type: 0 for unit_type in UnitType}
    for unit in units:
        total_unit_counts[unit.unit_type] += 1

    for unit in units:
        i = convert_type[unit.unit_type]
        image_name = house + unit.file_name
        
        y = (int(hold["y_cord"]) - camera_y) * zoom + (icon_size * i * 2.2 * compactor)
        x = ((int(hold["x_cord"]) - camera_x) * zoom) - (0.5 * compactor * total_unit_counts[unit.unit_type] * icon_size) - (icon_size * compactor) + (compactor * icon_size * unit_counts[unit.unit_type])
        unit_counts[unit.unit_type] += 1
        
        
        sprite_image = army_images[image_name.lower()]
        
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = icon_size / max(sprite.image.width, sprite.image.height)
        sprite.scale = scale
        sprite.x = x
        sprite.y = y
        sprite.scale *= zoom
        sprite.draw()
        unit_sprites.append(sprite)
    
    star_size = [60 ,30, 18, 12, 12]

    for i, sprite in enumerate(unit_sprites):
        star_count = units[i].experience
        icon_size = star_size[star_count - 1]
        scale = 0.02
        x_offset = 0
        y_offset = -15
        x_offset = -((star_count - 1) *icon_size) / 2
            
        
        for j in range(star_count):
            star_sprite = pyglet.sprite.Sprite(star_image)
            star_sprite.scale = scale * zoom
            if (star_count % 2) > 0:
                offset_num = abs(math.floor(star_count / 2) - j)
            else:
                offset_num = abs((star_count / 2 - 0.5) - j) + 0.5

            star_sprite.x = sprite.x + (sprite.width / 2) - (star_sprite.width / 2) + x_offset + (j * icon_size)
            star_sprite.y = sprite.y + sprite.height + (star_sprite.height / 2) + y_offset - (offset_num * (star_sprite.height / 3))

            star_sprite.draw()
