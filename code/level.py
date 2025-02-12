import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import *
from weapon import Weapon

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None

        #sprite setup
        self.create_map()

    def create_map(self):

        '''
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites],self.obstacle_sprites)
        '''

        layouts = {
            'boundary': import_csv_layout('C:/Users/willi/Py Projects/zeldaproject/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('C:/Users/willi/Py Projects/zeldaproject/map/map_Grass.csv'),
            'object': import_csv_layout('C:/Users/willi/Py Projects/zeldaproject/map/map_LargeObjects.csv')
        }

        graphics = {
            'grass': import_folder('C:/Users/willi/Py Projects/zeldaproject/graphics/grass'),
            'objects': import_folder('C:/Users/willi/Py Projects/zeldaproject/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary': #creating map layout
                            #Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                            Tile((x, y), [self.obstacle_sprites], 'invisible') #removing the visible sprites group to not draw the impassible terrain
                        if style == 'grass': #creating grass detail in map
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object': #creating object detail in map
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

        self.player = Player((1970, 1410), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        
        #update and draw the game
        #self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2 #index 0 meaning size of x plane
        self.half_height = self.display_surface.get_size()[1] // 2 #index 1 meaning size of y plane
        self.offset = pygame.math.Vector2(100,200)

        #creating the floor
        self.floor_surf = pygame.image.load('C:/Users/willi/Py Projects/zeldaproject/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        #obtaining offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #ordering the drawing of the sprites so that the player interacts well with terrain
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


