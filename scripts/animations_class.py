import pyglet
import math

class Animation:
    def __init__(self, duration, update_func, on_complete=None):
        self.duration = duration  # in seconds
        self.elapsed = 0.0
        self.update_func = update_func
        self.on_complete = on_complete
        self.completed = False
    
    def update(self, dt):
        self.elapsed += dt
        progress = min(1.0, self.elapsed / self.duration)
        
        # Call the update function with progress (0.0 to 1.0)
        self.update_func(progress)
        
        if progress >= 1.0 and not self.completed:
            self.completed = True
            if self.on_complete:
                self.on_complete()
            return False  # Animation is complete
        return True  # Animation continues

class AnimationManager:
    def __init__(self):
        self.active_animations = []
        self.animation_id_counter = 0
    
    @staticmethod
    def ease_out_quad(t):
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out_quad(t):
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t
    
    def create_popup_animation(self, element, start_scale=0.5, end_scale=1.0, duration=0.3):
        original_scale = element.scale
        original_opacity = element.opacity if hasattr(element, 'opacity') else 255
        
        def update(progress):
            # Use easing function for smoother animation
            eased_progress = self.ease_out_quad(progress)
            scale = start_scale + (end_scale - start_scale) * eased_progress
            opacity = int(255 * eased_progress)
            
            element.scale = scale
            if hasattr(element, 'opacity'):
                element.opacity = opacity
        
        def on_complete():
            element.scale = end_scale
            if hasattr(element, 'opacity'):
                element.opacity = 255
        
        return Animation(duration, update, on_complete)
    
    def create_fade_animation(self, element, start_opacity=0, end_opacity=255, duration=0.3):
        if not hasattr(element, 'opacity'):
            raise ValueError("Element must have an opacity attribute")
        
        def update(progress):
            eased_progress = self.ease_in_out_quad(progress)
            opacity = int(start_opacity + (end_opacity - start_opacity) * eased_progress)
            element.opacity = opacity
        
        def on_complete():
            element.opacity = end_opacity
        
        return Animation(duration, update, on_complete)
    
    def create_move_animation(self, element, start_pos, end_pos, duration=0.5):
        def update(progress):
            eased_progress = self.ease_in_out_quad(progress)
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * eased_progress
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * eased_progress
            element.x = x
            element.y = y
        
        def on_complete():
            element.x = end_pos[0]
            element.y = end_pos[1]
        
        return Animation(duration, update, on_complete)
    
    def start_animation(self, animation):
        self.animation_id_counter += 1
        animation.id = self.animation_id_counter
        self.active_animations.append(animation)
        return animation.id
    
    def cancel_animation(self, animation_id):
        self.active_animations = [a for a in self.active_animations if getattr(a, 'id', None) != animation_id]
    
    def cancel_all_animations(self):
        self.active_animations = []
    
    def update(self, dt):
        animations_to_remove = []
        for animation in self.active_animations:
            if not animation.update(dt):
                animations_to_remove.append(animation)
        
        # Remove completed animations
        for animation in animations_to_remove:
            self.active_animations.remove(animation)
    
    def create_animation_chain(self, animations):
        """Chain animations together to run sequentially"""
        if not animations:
            return None
            
        current = animations[0]
        
        def next_animation():
            nonlocal current
            animations.pop(0)
            if animations:
                current = animations[0]
                self.start_animation(current)
        
        current.on_complete = next_animation
        return current