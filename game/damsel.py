import pygame
import random
import time
from spriteSheet import SpriteSheet
from entity import Entity

# consts for damsel
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20


class Damsel(Entity):
    """Damsel in distress that the player saves
    Each damsel is initialized with their starting position,
    which sprite groups it is part of, boundary sprites,
    and enemy/interactable sprites.
    ...

    Methods
    -------
    import_damsel_assets(self)
        Handles importing damsel assets.
    move(self, speed)
        Handles movement of the damsel
    set_status_by_curr_direction(self)
        Updates state based on movement logic.
    set_image_direction(self, image)
        Updates the image sprite based on the current direction.
    animate(self)
        Controls animation loop.
    collision_check(self, direction)
        Handles interaction with environment.
    update(self)
        Update damsel with current game state information.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        """Initialize a Damsel with level info

        Each damsel is initialized with their starting position,
        which sprite groups it is part of, boundary sprites,
        and enemy/interactable sprites.

        Parameters
        ----------
            pos : Tuple
                starting x, y coordinates
            groups : list of sprite groups
                which groups in level it is a part of
            obstacle_sprites : list of sprite groups
                which sprites in the level damsel cannot walk through
        """

        super().__init__(groups)

        damselMovementImagePath = "graphics/damsel/damselWalking.png"
        self.damselAnimations = SpriteSheet(damselMovementImagePath)
        damselSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        # r,g,b vals for key color
        self.colorKeyBlack = (0, 0, 0)
        self.image = self.damselAnimations.image_at(
            damselSelfImageRect, self.colorKeyBlack
        )
        self.rect = self.image.get_rect(topleft=pos)
        # modify model rect to be a slightly less tall hitbox.
        self.hitbox = self.rect.inflate(0, -10)

        self.speed = 0.5
        random.seed(time.time())
        self.timer = 100

        self.obstacle_sprites = obstacle_sprites

        # starting position is facing down
        self.direction.y = 1
        self.status = "down"
        self.import_damsel_assets()

    def import_damsel_assets(self):
        """Initializes all animations from the image"""

        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # animation states in dictionary
        self.animations = {
            "up": self.damselAnimations.load_strip(
                walkingUpRect, 3, self.colorKeyBlack
            ),
            "down": self.damselAnimations.load_strip(
                walkingDownRect, 3, self.colorKeyBlack
            ),
            "left": self.damselAnimations.load_strip(
                walkingLeftRect, 3, self.colorKeyBlack
            ),
            "right": self.damselAnimations.load_strip(
                walkingRightRect, 3, self.colorKeyBlack
            ),
        }

    def move(self, speed):
        """Handles movement of the damsel

        Movement logic is as described in documentation using current speed.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position.
        """

        self.timer += 1
        # update direction every 100 ticks. Still moves every tick
        if self.timer >= 10:
            # update/randomize direction
            # get random number
            seed = random.randint(1, 1000)
            # if odd turn left else right
            if seed % 2:
                self.direction.x = -1
            else:
                self.direction.x = 1
            # if %3 false turn up else down
            if seed % 3:
                self.direction.y = -1
            else:
                self.direction.y = 1
            self.timer = 0

        # prevent diagonal moving from increasing speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # update hitbox based on move speed
        self.hitbox.x += self.direction.x * speed
        self.collision_check("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision_check("vertical")
        self.rect.center = self.hitbox.center

    def set_status_by_curr_direction(self):
        """Sets the correct status based on the current direction

        This function inspects the current direction and determines
        what the status should be.
        """

        # will only display "up" and "down". Need to rework
        if self.direction.x > 0 and self.status != "right":
            self.status = "right"
        elif self.direction.x < 0 and self.status != "left":
            self.status = "left"
        if self.direction.y > 0 and self.status != "down":
            self.status = "down"
        elif self.direction.y < 0 and self.status != "up":
            self.status = "up"

    def set_image_direction(self, image):
        """Sets a new image to the correct cardinal direction

        Return the image correlating to the correct cardinal direction.

        Parameters
        ----------
        image : png file
            image facing the current direction that will be displayed
        """

        if self.status == "right":
            self.direction.x = 1
            direction = "x"
        if self.status == "left":
            self.direction.x = -1
            direction = "x"
        if self.status == "up":
            self.direction.y = -1
            direction = "y"
        if self.status == "down":
            self.direction.y = 1
            direction = "y"

        if direction == "y":
            return pygame.transform.rotate(image, self.direction.y)
        if direction == "x":
            return pygame.transform.rotate(image, self.direction.x)

    def animate(self):
        """Method to loop through damsel animations"""

        animation = self.animations[self.status]
        # loop over fram index
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = self.set_image_direction(animation[int(self.frameIndex)])
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def collision_check(self, direction):
        """Method to handle interaction with environment

        Parameter required for vertical and horizontal checking.

        Parameters
        ----------
        direction : string
            used to determine horizontal/vertical check.
        """

        # horizontal collision detection
        if direction == "horizontal":
            # look at all obstacle sprites
            for sprite in self.obstacle_sprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        # vertical collision detection
        if direction == "vertical":
            # look at all sprites
            for sprite in self.obstacle_sprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        """Update status. Will be run every game tick"""

        self.set_status_by_curr_direction()
        self.animate()
        self.move(self.speed)
