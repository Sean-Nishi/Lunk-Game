import pygame
from game.settings import TILESIZE
from wall import Wall
from plant import Plant
from player import Player
from enemy1 import Enemy1


class Level:
    def __init__(self):
        # display surface
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # default world map
        # KEY: x = wall, p = player
        self.world_map = [
            [
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                "p",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "e",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "e",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                "x",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                "x",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
            ],
        ]
        # map size in number of 64 pixels = (20x, 20y size)
        self.map_size = pygame.math.Vector2(20, 20)

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.world_map):  # in enumerate(WORLD_MAP)
            for col_index, col in enumerate(row):  # in enumerate(row)
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Wall((x, y), [self.visible_sprites, self.obstacle_sprites])

                if col == "t":
                    Plant((x, y), [self.visible_sprites, self.obstacle_sprites])

                if col == "e":
                    Enemy1(
                        (x, y),
                        [self.visible_sprites, self.enemy_sprites],
                        self.obstacle_sprites,
                    )

        # pass in map size so player can do wrap around if needed
        self.player = Player(
            (1400, 500), [self.visible_sprites], self.obstacle_sprites, self.map_size
        )

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.enemy_sprites.update()
        # debug(self.player.direction)


# Class to handle camera movement centered around player
# Called YSort because of sprite overlap
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = (
            self.display_surface.get_size()[0] // 2
        )  # floor div, returns int
        self.half_height = (
            self.display_surface.get_size()[1] // 2
        )  # floor div, returns int
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load(
            "graphics/floor_surface/ground.png"
        ).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    # Drawing the map with the offset of the player, keeps screen centered on player
    def custom_draw(self, player):
        # calculate offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # draw floor and give camera offset
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        # draw the sprites, sort by center y-coord for overlap
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset)