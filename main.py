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
        self.dead = False

    def __repr__(self):
        return f'Character(name={self.name}, stamina={self.stamina}, skill={self.skill})'

    def roll_dice(self):
        self.last_roll = dice_sum(2)

    def calculate_score(self):
        self.fight_score = self.skill + self.last_roll

    def take_hit(self, damage):
        self.stamina -= damage

    def check_alive(self):
        if self.stamina <= 0:
            self.dead = True

    def is_alive(self):
        if self.dead:
            return False
        else:
            return True
    def is_dead(self):
        if self.dead:
            return True
        else:
            return False


class MainPlayer(Character):
    ...



class Opponent(Character):
    ...



class Game:
    def __init__(self, game_hero: MainPlayer, opponents: list[Opponent]):
        self.hero = game_hero
        self.opponents = opponents
        self.boss_number = 0

    def get_boss(self):
        next_boss = self.opponents[self.boss_number]
        if next_boss.is_alive():
            return next_boss
        else:
            return None

    def next_boss(self):
        self.boss_number += 1

        if self.boss_number == len(self.opponents):
            self.boss_number = 0

    def bosses_available(self):
        boss_count = 0

        for boss in self.opponents:
            if boss.is_alive():
                boss_count += 1

        return boss_count



    def get_all_players(self):
        return [self.hero] + self.opponents

    def boss_fight(self, boss):
        self.hero.roll_dice()
        self.hero.calculate_score()

        if boss not in self.opponents:
            raise Exception('Boss not in fight')

        boss.roll_dice()
        boss.calculate_score()

        self.update_scores(self.hero, boss)

        self.hero.check_alive()
        boss.check_alive()


    def update_scores(self, player1, player2):
        if player1 not in self.get_all_players():
            raise Exception('{player1} not in fight')

        if player2 not in self.get_all_players():
            raise Exception('{player2} not in fight')

        if player1.fight_score > player2.fight_score:
            player2.take_hit(2)
        elif player1.fight_score < player2.fight_score:
            player1.take_hit(2)
        else:
            player1.take_hit(1)
            player2.take_hit(1)



class View:
    def report_hero_win(self, hero: Character):
        print(f'Game over - {hero.name} wins')

    def introduce_fight(self, hero, boss):
        print(f'Introducing a fight between {hero} and {boss}')

    def introduce_game(self, game):
        print(f'Hero is {game.hero}')
        for opp in game.opponents:
            print(f'Opponent is {opp}')

    def report_fight_result(self, hero, boss):
        print(f'Hero rolled a {hero.last_roll}')
        print(f'Opponent rolled a {boss.last_roll}')

    def report_scores(self, hero, boss):
        print(f'Hero is now {hero}')
        print(f'Opponent is now {boss}')

    def report_game_state(self, game):
        print(f'Hero is {game.hero}')
        for opp in game.opponents:
            print(f'Opponent is {opp}')


class Controller:
    def __init__(self, game: Game, view: View):
        self.game = game
        self.view = view

    def game_loop(self):
        self.view.introduce_game(self.game)

        still_fighting = True

        while still_fighting:
            boss = self.game.get_boss()

            self.view.introduce_fight(self.game.hero, boss)

            self.game.boss_fight(boss)

            self.view.report_fight_result(self.game.hero, boss)

            self.game.update_scores(self.game.hero, boss)

            self.view.report_scores(self.game.hero, boss)

            self.view.report_game_state(self.game)

            boss_count = self.game.bosses_available()

            if boss_count == 0:
                self.view.report_hero_win(self.game.hero)
                still_fighting = False
            elif self.game.hero.is_dead():
                self.view.report_hero_died(self.game.hero)
                still_fighting = False
            else:
                seeking_next_boss = True
                while seeking_next_boss:
                    self.game.next_boss()

                    next_boss = self.game.get_boss()

                    if next_boss.is_alive():
                        seeking_next_boss = False















my_hero = MainPlayer(name='Steve', skill=10, stamina=12)
ogre = Opponent(9, 8, 'Shrek')

my_game = Game(my_hero, [ogre])




my_view = View()
my_controller = Controller(my_game, my_view)

my_controller.game_loop()

