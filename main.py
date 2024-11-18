import random


def dice_sum(num_dice):
    return sum(random.randint(1,6) for _ in range(num_dice))


class Character:
    def __init__(self, skill, stamina, name):
        self.skill = skill
        self.stamina = stamina
        self.name = name
        self.last_roll = None
        self.fight_score = None

    def __repr__(self):
        return f'Character(name={self.name}, stamina={self.stamina}, skill={self.skill})'

    def roll_dice(self):
        self.last_roll = dice_sum(2)

    def get_score(self):
        self.fight_score = self.skill + self.last_roll

    def take_hit(self, damage):
        self.stamina -= damage

    def attack(self, enemy):
        self.roll_dice()
        enemy.roll_dice()
        self.get_score()
        enemy.get_score()


        if self.fight_score > enemy.fight_score:
            enemy.take_hit(2)
        elif self.fight_score < enemy.fight_score:
            self.take_hit(2)
        else:
            self.take_hit(1)
            enemy.take_hit(1)

class MainPlayer(Character):
    ...

class Opponent(Character):
    ...

class Game:
    def __init__(self, game_hero: MainPlayer, opponents: list[Opponent]):
        self.hero = game_hero
        self.opponents = opponents

hero = MainPlayer(name='Steve', skill=10, stamina=12)
ogre = Opponent(9, 8, 'Shrek')

my_game = Game(hero, [ogre])

while True:
    print(hero)
    print(ogre)
    input()

    hero.attack(ogre)


