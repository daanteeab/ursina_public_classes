from numpy import arctan2
from math import *
from random import random
from numpy import *
from ursina import *
from ursina.input_handler import *

class PlayerController():
    def __init__(self, entity, height):
        self.entity = entity
        self.height = height
                
    def player_position(self):
        if self.entity.health > 0:
            self.entity.direction = Vec3(
                self.entity.forward * (held_keys['w'] - held_keys['s'])
                + self.entity.right * (held_keys['d'] - held_keys['a'])
                ).normalized()

            feet_ray = raycast(self.entity.position+Vec3(0,0.3,0), self.entity.direction, ignore=(self.entity,), distance=.5, debug=False)
            head_ray = raycast(self.entity.position+Vec3(0,self.height-.1,0), self.entity.direction, ignore=(self.entity,), distance=.5, debug=False)
            if not feet_ray.hit and not head_ray.hit:
                self.entity.position += self.entity.direction * self.entity.speed * time.dt
        
    def update(self):
        self.player_position()
            
class ThirdPersonCamera():
    def __init__(self, player):
        self.player = player
        self.mouse_dt = Vec2(0,0)
        self.last_mouse_right = (0,0)
        self.camera_angle = 0
        self.camera_radius = 50
        self.camera_y = 0.3
        self.last_y_rot = 0

    def rmb_pivot(self):
        self.last_mouse_right = (mouse.position[0], mouse.position[1])

    def input(self, keys):
        if keys == "right mouse down":
            self.rmb_pivot()
            self.last_mouse_right = Vec2(self.last_mouse_right) - self.mouse_dt
        if keys == "left mouse down":
            self.rmb_pivot()
            self.last_mouse_right = Vec2(self.last_mouse_right) - self.mouse_dt

        if keys == "scroll up":
            self.camera_radius -= time.dt*50
        if keys == "scroll down":
            self.camera_radius += time.dt*50
            
    def update(self):
        if mouse.right:
            self.mouse_dt = Vec2(mouse.position[0], mouse.position[1]) - Vec2(self.last_mouse_right)
            self.camera_angle = -self.mouse_dt[0]*3.14
            self.camera_y = -self.mouse_dt[1]*2
            self.last_y_rot = camera.rotation_y
            self.player.rotation_y = self.last_y_rot
        if mouse.left:
            self.mouse_dt = Vec2(mouse.position[0], mouse.position[1]) - Vec2(self.last_mouse_right)
            self.camera_angle = -self.mouse_dt[0]*3.14
            self.camera_y = -self.mouse_dt[1]*2
        target_position = self.player.position + (abs(cos(self.camera_y))*self.camera_radius*cos(self.camera_angle), self.camera_y*self.camera_radius, abs(cos(self.camera_y))*self.camera_radius*sin(self.camera_angle)) + (0,2,0)
        camcast = raycast(origin = self.player.position + (0,2,0), direction = target_position - (self.player.position + (0,2,0)), distance = distance(target_position, self.player.position + (0,2,0))*0.95, ignore = (self.player,))
        if camcast.hit is True:
            target_position = camcast.world_point
        camera.position = lerp(camera.position, target_position, time.dt * 20)
        camera.look_at(self.player.position + (0,2,0))

        #case-d-only
        #d_only = (1-held_keys["w"])*(1-held_keys["a"])*(1-held_keys["s"])*held_keys["d"]
        #a_only = (1-held_keys["w"])*(1-held_keys["d"])*(1-held_keys["s"])*held_keys["a"]
        #sd_strafe = (1-held_keys["w"])*(1-held_keys["a"])*held_keys["s"]*held_keys["d"]*-22.5
        #as_strafe = (1-held_keys["w"])*(1-held_keys["d"])*held_keys["a"]*held_keys["s"]*22.5
        #wd_strafe = (1-held_keys["a"])*(1-held_keys["s"])*held_keys["w"]*held_keys["d"]*22.5
        #wa_strafe = (1-held_keys["d"])*(1-held_keys["s"])*held_keys["w"]*held_keys["a"]*-22.5
        self.player.rotation_y = self.last_y_rot #+ sd_strafe + as_strafe + wd_strafe + wa_strafe

if __name__ == "__main__":
    app = Ursina()
    b1 = Entity(model="cube", scale=(10,10,1), color = color.red, position = (-5,5,-10), collision = True)
    b1.collider = BoxCollider(entity = b1)
    b2 = Entity(model="cube", scale=(10,1,10), color = color.blue, position = (0,-1,2), collision = True)
    b2.collider = BoxCollider(entity = b2)
    b3 = Entity(model="cube", scale=(1,10,10), color = color.green, position = (5,5,5), collision = True)
    b3.collider = BoxCollider(entity = b3)
    b4 = Entity(model="cube", scale=(10,1,10), color = color.white, position = (0,10,0), collision = True)
    b4.collider = BoxCollider(entity = b4)

    p = Entity(model="sphere")
    p.health=1
    p.speed=5
    p.add_script(PlayerController(entity = p, height=2))
    p.add_script(ThirdPersonCamera(player=p))
    
    app.run()