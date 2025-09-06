import os
import pyglet
import math
from enum import Enum

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
army_dir = os.path.join(current_dir, "Images", "army")

images_dir = os.path.join(current_dir,'Images')
star_image = pyglet.image.load(os.path.join(images_dir, 'star.png'))


from dataclasses import dataclass
from enum import Enum

class UnitType(Enum):
    SOLDIER = 1
    ARCHER = 2
    KNIGHT = 3
    KINGSGUARD = 4

@dataclass
class ArmyUnit:
    unit_type: UnitType
    experience: int
    file_name: str = ""

army_images = {}


def army_init():
    for filename in os.listdir(army_dir):
        if filename.endswith(".png"):
            image_name = filename.replace(".png", "")
            path = os.path.join(army_dir, filename)
            army_images[image_name] = pyglet.image.load(path)

convert_type = {
    UnitType.SOLDIER: 0,
    UnitType.ARCHER: 1,
    UnitType.KNIGHT: 2,
    UnitType.KINGSGUARD: 3
}

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
