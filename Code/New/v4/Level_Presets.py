# # Used in Ray Casting
# self.pos = createVector(x, y)
# self.vel = createVector()
# self.facing = dir * RADIAN
# self.angleOfVision = deg
# self.step = step
# self.col = col
# self.rayData = []  # Holds Ray coordinates
# self.MapCell = []  # Players map cell coordinate (x: 0 - 79, y: 0 - 79)

# # Item Tracking
# self.isShootAnim = False
# self.AnimUntil = 0
# self.shooting = False
# self.flashlight = False
# self.hasFlashlight = False
# self.on_star = -1
# self.__AMMO_CAP = WeaponKit[STARTING_WEAPON].ammo_cap
# self.ammo_count = WeaponKit[STARTING_WEAPON].ammo_cap
# self.weapon: gun = WeaponKit[STARTING_WEAPON]  # starting weapons for player
# self.ZOMBIES_ARE_COMING = True

# # Player Stats
# self.radius = 3
# self.health = HEALTH_MAX
# self.canMove = True

from TurretDefinition import HEALTH_MAX, WeaponKit

# health, ZAC, Weapon, ammo_count, hasFlashlight, direction
Level_Defaults = {
    "0" : (85, False, "Pistol", 10, False, 0),  # Tutorial Level
    "1" : (HEALTH_MAX, False, "Pistol", "max", False, 0),  # Level 1...
    "2" : (HEALTH_MAX, True, "Pistol", "max", False, 270),
    "3" : (HEALTH_MAX, False, "Pistol", "max", True, 270),
    "4" : (HEALTH_MAX, False, "Pistol", "max", False, 270),
    "5" : (HEALTH_MAX, False, "Pistol", "max", False, 270)
}
