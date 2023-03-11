class Settings:
    """A class to restore all settings for jet Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        
        # tank settings

        self.tank_limit = 3
        
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 650
        self.bg_color = (255, 255, 255)
        
        # Bullet settings
      
        self.bombshell_width = 5
        self.bombshell_height = 5
        self.bombshell_color = (60,60,60)
        self.bombshells_allowed = 5
        
        #warthog settings 
        self.wspeed = 3
        self.wdirection = 1
        self.warthog_limit = 3
        
        #Missile settings
        self.missile_speed = 3
        
        # jet settings
        self.jet_speed = .3
        self.fleet_drop_speed = 10.0
        # fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1
        
        #How fast the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.tank_speed = .5
        self.bombshell_speed = 2
        self.jet_speed = .3
        
        # fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1
    
        self.jet_points = 50
         
    def increase_speed(self):
        """Increase speed settings"""
        self.tank_speed *= self.speedup_scale 
        self.bombshell_speed *= self.speedup_scale
        self.jet_speed *= self.speedup_scale
        