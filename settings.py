class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (51, 153, 255)  # light gray
        self.fps = 60
        self.mode='windowed'

        # ship settings
        self.ship_speed = 6

        # bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10 # how much the fleet drops down when reaching right edge
        self.fleet_direction = 1  # 1 represents right; -1 represents left