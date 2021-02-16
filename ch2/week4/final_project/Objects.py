from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC): # FIXME
    @abstractmethod
    def __init__(self):
        self.sprite = None
        self.position = None
        self.min_x = self.min_y = 0

    def draw(self, display): # test расчитать сдвиги картинки
        sprite_size = self.sprite.get_size()[0]
        display.blit(self.sprite, [(self.position[0])* sprite_size, (self.position[1])* sprite_size])


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.stats = stats
        self.xp = xp
        self.position = position

    def interact(self, engine, hero):
        hero.exp += self.xp
        #engine.delete_object()
        while hero.exp >= 100 * (2 ** (hero.level - 1)):
            engine.notify ("level up!")
            hero.level += 1
            hero.stats["strength"] += 2
            hero.stats["endurance"] += 2
            hero.calc_max_HP()
            hero.hp = hero.max_hp

class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    
        


class Effect(Hero, ABC):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()
        # добавить супер?

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect): #????
    
    def apply_effect(self):
        stats, hp = self.base.apply_effect()
        stats["strength"] += 3
        stats["endurance"] += 2
        stats["luck"] -= 1
        stats["intelligence"] -= 3
        hp += 20
        return stats, hp
        
class Blessing(Effect): #????
    
    def apply_effect(self):
        stats, hp = self.base.apply_effect()
        stats["strength"] += 2
        stats["endurance"] += 2
        stats["luck"] += 2
        stats["intelligence"] += 2
        return stats, hp
        
class Weakness(Effect): #????
    
    def apply_effect(self):
        stats, hp = self.base.apply_effect()
        stats["strength"] -= 2
        stats["endurance"] -= 2
        stats["luck"] -= 2
        stats["intelligence"] -= 2
        return stats, hp
        

# FIXME
