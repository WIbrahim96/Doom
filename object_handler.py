from sprite_object import *
from npc import *
class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.animated_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}

        # sprite map
        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprite(game))
        self.add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        self.add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        self.add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        self.add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        self.add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        self.add_sprite(AnimatedSprite(game, path=self.animated_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, path=self.animated_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, path=self.animated_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))

        # npc map
        self.add_npc(NPC(game))
        self.add_npc(NPC(game, pos=(11.5, 4.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

