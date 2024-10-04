import pygame

from Models.Animal import Animal
class Platypus(Animal):

    def eat(self, chick):
        if self.hitbox.colliderect(chick.hitbox):
            return True