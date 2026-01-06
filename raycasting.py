import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height  # Avoid division by zero
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height  
                ) 
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))  
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_horz = 1, 1
        ray_angle = self.game.player.angle - HALF_FOV + EPSILON

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Horizontal checks
            y_horz, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - EPSILON, -1)
            depth_horz = (y_horz - oy) / (sin_a + 1e-6)  # Prevent division by zero
            x_horz = ox + depth_horz * cos_a

            delta_depth = dy / (sin_a + 1e-6)
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_horz = int(x_horz), int(y_horz)
                if tile_horz in self.game.map.world_map:
                    texture_horz = self.game.map.world_map[tile_horz]
                    break
                x_horz += dx * 1.001  # Small offset to fix floating-point errors
                y_horz += dy * 1.001
                depth_horz += delta_depth

            # Vertical checks
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - EPSILON, -1)
            depth_vert = (x_vert - ox) / (cos_a + 1e-6)
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / (cos_a + 1e-6)
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx * 1.001
                y_vert += dy * 1.001
                depth_vert += delta_depth

            # depth and texture offset
            if depth_vert < depth_horz:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_horz, texture_horz
                x_horz %= 1
                offset = (1 - x_horz) if sin_a < 0 else x_horz

            # Remove fisheye effect
            depth = max(depth * math.cos(self.game.player.angle - ray_angle), 0.0001)

            # Projection height
            proj_height = SCREEN_DIST / (depth + 0.0001)

            #draw walls
            #color = [255 / (1+ depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, color,
                         #(ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            # Store results
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
