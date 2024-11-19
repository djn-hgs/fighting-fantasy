import random


def dice_sum(num_dice):
    return sum(random.randint(1, 6) for _ in range(num_dice))


class Character:
    def __init__(self, skill, stamina, name):
        self.skill = skill
        self.stamina = stamina
        self.name = name
        self.last_roll = None
        self.fight_score = None
        self.is_dead = False

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
            self.is_dead = True

    @property
    def is_alive(self):
        if self.is_dead:
            return False
        else:
            return True



class MainPlayer(Character):
    ...


class Opponent(Character):
    ...


class Game:
    def __init__(self, game_hero: MainPlayer, opponents: list[Opponent]):
        self.hero = game_hero
        self.opponents = opponents
        self.boss_index = 0
        self.boss = None
        self.all_bosses_defeated = False
        self.round = 0

    def start_next_round(self):
        self.round += 1
        self.get_boss()

    def get_boss(self):
        if self.all_bosses_defeated:
            self.boss = None
        else:
            self.boss = self.opponents[self.boss_index]

            if self.boss.is_dead:
                self.next_boss()

    def next_boss(self):
        if self.all_bosses_defeated:
            self.boss = None
        else:
            seeking_next_boss = True
            while seeking_next_boss:
                self.boss_index += 1

                if self.boss_index == len(self.opponents):
                    self.boss_index = 0

                self.boss = self.opponents[self.boss_index]

                if self.boss.is_alive:
                    seeking_next_boss = False

    def check_bosses_available(self):
        boss_count = 0

        for boss in self.opponents:
            if boss.is_alive:
                boss_count += 1

        if boss_count == 0:
            self.all_bosses_defeated = True
        else:
            self.all_bosses_defeated = False

    def get_all_players(self):
        return [self.hero] + self.opponents

    def boss_fight(self):
        self.hero.roll_dice()
        self.hero.calculate_score()

        self.boss.roll_dice()
        self.boss.calculate_score()

    def check_status_of_combatants(self):
        self.hero.check_alive()
        self.boss.check_alive()

    def adjudicate_scores_after_boss_fight(self):
        adjudicate_scores(self.hero, self.boss)


def adjudicate_scores(player1, player2):
    if player1.fight_score > player2.fight_score:
        player2.take_hit(2)
    elif player1.fight_score < player2.fight_score:
        player1.take_hit(2)
    else:
        player1.take_hit(1)
        player2.take_hit(1)


class View:
    def __init__(self, game: Game):
        self.game = game

    def report_hero_win(self):
        print(f'Game over - {self.game.hero} wins\n')

    def introduce_fight(self):
        print(f'\nRound {self.game.round}: introducing a fight between {self.game.hero} and {self.game.boss}\n')

    def introduce_game(self):
        print(f'Hero is {self.game.hero}')
        for opp in self.game.opponents:
            print(f'Opponent is {opp}')

    def report_boss_fight_dice_rolls(self):
        print(f'Hero {self.game.hero.name} rolled a {self.game.hero.last_roll}')
        print(f'Opponent {self.game.boss.name} rolled a {self.game.boss.last_roll}\n')

    def report_scores_after_boss_fight(self):
        print(f'Reporting scores after fight between {self.game.hero.name} and {self.game.boss.name}')
        print(f'Hero status is now {self.game.hero}')
        print(f'Opponent status is now {self.game.boss}\n')
        if self.game.hero.is_dead:
            print(f'{self.game.hero.name} is dead')
        if self.game.boss.is_dead:
            print(f'{self.game.boss.name} is dead')


    def report_game_state(self):
        print(f'Hero status is {self.game.hero}')
        for opp in self.game.opponents:
            print(f'Opponent status is {opp}')
        print()

    def report_hero_died(self):
        print(f'Commiserations, your hero died {self.game.hero}\n')


class Controller:
    def __init__(self, game: Game, view: View):
        self.game = game
        self.view = view

    def game_loop(self):
        still_fighting = True

        while still_fighting:
            self.game.start_next_round()

            self.view.report_game_state()

            self.view.introduce_fight()

            self.game.boss_fight()

            self.game.adjudicate_scores_after_boss_fight()

            self.game.check_status_of_combatants()

            self.view.report_boss_fight_dice_rolls()

            self.view.report_scores_after_boss_fight()

            self.game.check_bosses_available()

            if self.game.all_bosses_defeated:
                self.view.report_hero_win()
                still_fighting = False

            elif self.game.hero.is_dead:
                self.view.report_hero_died()
                still_fighting = False

            self.game.next_boss()


my_hero = MainPlayer(name='Steve', skill=10, stamina=12)
ogre = Opponent(9, 8, 'Shrek')
donkey = Opponent(4, 3, 'Donkey')

my_game = Game(my_hero, [ogre, donkey])
my_view = View(my_game)

my_controller = Controller(my_game, my_view)

my_controller.game_loop()
