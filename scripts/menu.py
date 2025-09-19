import pyglet
import os
from typing import Dict, Any, List, Tuple, Optional
from scripts.buttons import UnitTrainer, ResourceManager, KingdomManager

class MenuManager:
    def __init__(self):
        self.menu_bg_color = (228, 213, 183)
        self.menu_padding = 10
        self.icon_size = 50
        self.icon_padding = 10
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, '../Images')
        
        self.icons = self._load_icons(images_dir)
        
        self.unit_trainer = UnitTrainer()
        self.resource_manager = ResourceManager()
        self.kingdom_manager = KingdomManager()
        
        self.buttons_dict = self._create_buttons_dict()
    
    def _load_icons(self, images_dir: str) -> Dict[str, Any]:
        icon_files = {
            "food": 'Food.png',
            "wood": 'Wood.png',
            "iron": 'Iron.png',
            "gold": 'Gold.png'
        }
        
        icons = {}
        for name, filename in icon_files.items():
            try:
                path = os.path.join(images_dir, filename)
                icons[name] = pyglet.image.load(path)
            except FileNotFoundError:
                print(f"Warning: Could not load icon {filename}")
                icons[name] = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(32, 32)
        
        return icons
    
    def _create_buttons_dict(self) -> Dict[str, Dict[str, Any]]:
        return {
            "Train Archer": {
                "pressed": False,
                "hover_text": "Train new archers for your garrison.",
                "hovering": False,
                "function": self.unit_trainer.train_archer,
                "city_type": "all_city"
            },
            "Train Soldier": {
                "pressed": False,
                "hover_text": "Train new soldiers for your garrison.",
                "hovering": False,
                "function": self.unit_trainer.train_soldier,
                "city_type": "all_city"
            },
            "Train Knight": {
                "pressed": False,
                "hover_text": "Train new knights for your garrison.",
                "hovering": False,
                "function": self.unit_trainer.train_knight,
                "city_type": "all_city"
            },
            "Appoint Kingsguard": {
                "pressed": False,
                "hover_text": "Appoint a kingsguard to protect your king.",
                "hovering": False,
                "function": self.unit_trainer.appoint_kingsguard,
                "city_type": "all_city"
            },
            "Improve Farms": {
                "pressed": False,
                "hover_text": "Increase food production from farms.",
                "hovering": False,
                "function": self.resource_manager.improve_farms,
                "city_type": "all_city"
            },
            "Plant Forests": {
                "pressed": False,
                "hover_text": "Increase wood production and forestry capacity.",
                "hovering": False,
                "function": self.resource_manager.plant_forests,
                "city_type": "all_city"
            },
            "Improve Iron Mines": {
                "pressed": False,
                "hover_text": "Increase iron production from mines.",
                "hovering": False,
                "function": self.resource_manager.improve_iron_mines,
                "city_type": "all_city"
            },
            "Improve Gold Mines": {
                "pressed": False,
                "hover_text": "Increase gold production from mines.",
                "hovering": False,
                "function": self.resource_manager.improve_gold_mines,
                "city_type": "all_city"
            },
            "Call Banners": {
                "pressed": False,
                "hover_text": "Call your vassals to raise a larger army.",
                "hovering": False,
                "function": self.kingdom_manager.call_banners,
                "city_type": "capital"
            },
            "Declare Kingdom": {
                "pressed": False,
                "hover_text": "Declare independence and form a new kingdom.",
                "hovering": False,
                "function": self.kingdom_manager.declare_kingdom,
                "city_type": "capital"
            }
        }
    
    def is_point_inside(self, x: float, y: float, rect: Tuple[float, float, float, float]) -> bool:
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh
    
    def get_menu_rect(self, window_width: int, window_height: int, side: str) -> Tuple[int, int, int, int]:
        width = int(window_width * 0.2)
        height = int(window_height * 0.95)

        if side == "left":
            menu_x_base = 10
            menu_y_base = (window_height - height) // 2
        else:
            menu_x_base = window_width - width - 10
            menu_y_base = (window_height - height) // 2
            
        return (menu_x_base, menu_y_base, width, height)
    
    def draw_menu_button(self, text: str, x: float, y: float, height: float,
                         width: float, font_name: str, selected: bool) -> None:
        if not selected:
            tint = 0.8
        else:
            tint = 0.6
        colour = (int(self.menu_bg_color[0] * tint),
                  int(self.menu_bg_color[1] * tint),
                  int(self.menu_bg_color[2] * tint))
        
        pyglet.shapes.RoundedRectangle(
            x, y, width, height,
            color=colour,
            batch=None,
            radius=25
        ).draw()
        
        pyglet.text.Label(
            text,
            font_name=font_name,
            font_size=50,
            x=x + width // 2,
            y=y + height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 255)
        ).draw()
    
    def draw_hover_text(self, text: str, x: float, y: float) -> None:
        label = pyglet.text.Label(
            text,
            font_name='Arial',
            font_size=16,
            x=x, y=y,
            anchor_x='left', anchor_y='bottom',
            color=(255, 255, 255, 255),
            batch=None
        )
        
        padding = 5
        bg_width = label.content_width + 2 * padding
        bg_height = label.content_height + 2 * padding
        bg_x = x - padding
        bg_y = y - padding
        
        pyglet.shapes.Rectangle(
            bg_x, bg_y, bg_width, bg_height,
            color=(0, 0, 0, 180)
        ).draw()
        
        label.draw()
    
    def draw_menu(self, selected_hold: Optional[Dict[str, Any]], window_width: int,
                  window_height: int, font_name: str, side: str,
                  mouse_x: float, mouse_y: float) -> None:
        if not selected_hold:
            return

        self._draw_hold_title(selected_hold, window_width, window_height, font_name)
        
        menu_x_base, menu_y_base, width, height = self.get_menu_rect(window_width, window_height, side)
        self._draw_menu_background(menu_x_base, menu_y_base, width, height)
        self._draw_resource_icons(selected_hold, menu_x_base, menu_y_base, width, height)
        self._draw_menu_buttons(selected_hold, menu_x_base, menu_y_base, width, height,
                                font_name, mouse_x, mouse_y)
    
    def _draw_hold_title(self, selected_hold: Dict[str, Any], window_width: int,
                         window_height: int, font_name: str) -> None:
        menu_width = int(window_width * 0.3)
        menu_height = int(window_height * 0.05)
        menu_x = (window_width - menu_width) // 2
        menu_y = int(window_height * 0.9)

        pyglet.shapes.RoundedRectangle(
            menu_x, menu_y, menu_width, menu_height,
            color=self.menu_bg_color,
            batch=None,
            radius=25
        ).draw()

        pyglet.text.Label(
            selected_hold["name"],
            font_name=font_name,
            font_size=50,
            x=menu_x + menu_width // 2,
            y=menu_y + menu_height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 255)
        ).draw()
    
    def _draw_menu_background(self, x: float, y: float, width: float, height: float) -> None:
        pyglet.shapes.RoundedRectangle(
            x, y, width, height,
            color=self.menu_bg_color,
            batch=None,
            radius=20
        ).draw()
    
    def _draw_resource_icons(self, selected_hold: Dict[str, Any], menu_x_base: float,
                             menu_y_base: float, width: float, height: float) -> None:
        icon_y = menu_y_base + height - self.icon_size - self.menu_padding
        
        for i, (name, sprite_image) in enumerate(self.icons.items()):
            resource_count = selected_hold.get(name, 0)
            icon_x = menu_x_base + (width / (2 * len(self.icons))) + (i * (width / len(self.icons))) - (self.icon_size / 2)
            
            self._draw_resource_count(icon_x, icon_y, resource_count)
            self._draw_resource_icon(icon_x, icon_y, sprite_image)
    
    def _draw_resource_count(self, icon_x: float, icon_y: float, count: int) -> None:
        count_label = pyglet.text.Label(
            str(count),
            font_name='Arial',
            font_size=18,
            x=icon_x - 20,
            y=icon_y + self.icon_size / 2,
            anchor_x='right',
            anchor_y='center',
            color=(0, 0, 0, 255)
        )
        count_label.draw()
    
    def _draw_resource_icon(self, x: float, y: float, sprite_image: Any) -> None:
        sprite = pyglet.sprite.Sprite(sprite_image)
        scale = self.icon_size / max(sprite.image.width, sprite.image.height)
        sprite.scale = scale
        sprite.x = x
        sprite.y = y
        sprite.draw()
    
    def _draw_menu_buttons(self, selected_hold: Dict[str, Any], menu_x_base: float,
                           menu_y_base: float, width: float, height: float,
                           font_name: str, mouse_x: float, mouse_y: float) -> None:
        button_margin = 15
        button_width = width - (button_margin * 2)
        button_height = 50
        button_x = menu_x_base + button_margin

        buttons_to_draw = self._get_buttons_for_hold(selected_hold)
        
        for i, (button_text, status) in enumerate(buttons_to_draw.items()):
            y = menu_y_base + height - (3 * self.icon_size) - (button_margin + (i * (button_height + button_margin)))
            is_hovering = self.is_point_inside(mouse_x, mouse_y, (button_x, y, button_width, button_height))
            self.buttons_dict[button_text]["hovering"] = is_hovering
                
            self.draw_menu_button(button_text, button_x, y, button_height, button_width, font_name, is_hovering or status["pressed"])
            
            if is_hovering:
                self.draw_hover_text(buttons_to_draw[button_text]["hover_text"], mouse_x + 10, mouse_y + 10)
    
    def _get_buttons_for_hold(self, selected_hold: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        if selected_hold["size"] == "Large":
            return self.buttons_dict.copy()
        else:
            return {name: btn for name, btn in self.buttons_dict.items()
                    if btn["city_type"] == "all_city"}
    
    def get_button_status(self, selected_hold: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        buttons_to_return = self._get_buttons_for_hold(selected_hold)
        
        for button in buttons_to_return:
            self.buttons_dict[button]["pressed"] = False
        
        return buttons_to_return
    
    def on_mouse_press(self) -> None:
        for button_text, status in self.buttons_dict.items():
            if status["hovering"]:
                status["pressed"] = True
    
    def get_true_button(self, selected_hold: Dict[str, Any]) -> Optional[str]:
        buttons_to_check = self._get_buttons_for_hold(selected_hold)
        true_buttons = [name for name, status in buttons_to_check.items() if status["pressed"]]
        
        if len(true_buttons) > 1:
            print("Error: More than one button is True.")
            exit(2)
        elif len(true_buttons) == 1:
            return true_buttons[0]
        else:
            return None
        
menu_manager = MenuManager()