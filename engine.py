import random
import copy
import keyboard

from typing import List
from venv import logger

from write_in_file import write_in_file
from model.plants import Plants
from model.entity.cucumber import Cucumber
from model.entity.potato import Potato
from model.entity.tomato import Tomato
from model.entity.chamomile import Chamomile
from model.entity.narcissus import Narcissus
from model.entity.rose import Rose
from model.entity.apple import Apple
from model.entity.pear import Pear
from model.entity.mandarin import Mandarin


def rand_list_plants(mas_plant: list) -> list:
    list_plants = []
    for i in mas_plant:
        el1 = mas_plant.index(i)
        el2 = random.randint(0, 2)
        list_plants.append(mas_plant[el1][el2])
    return list_plants


class EngineGarden:
    _plants: List[Plants] = []
    harvest: dict = {}
    week = 0
    weed = 0
    check_long_dur = 0
    die_status = 0
    lim_die_status = 0
    not_die_status = 0
    ill_die_status = 0
    chance_ill = 0
    choose_plant = 0
    plant_die = 0

    def __init__(self, list_of_plants: List[Plants]) -> None:
        for i in list_of_plants:
            self._plants.append(i)

    def get_plants(self) -> list:
        return self._plants

    def collect_harvest(self, plants, num_harvest: int) -> dict:
        self.harvest.update({plants.get_name(): [num_harvest]})
        return self.harvest

    def get_harvest(self):
        return self.harvest

    @staticmethod
    def add_new_rand_plants(mas_plant: list, num_plants: int):
        for i in range(0, num_plants):
            el1 = random.randint(0, 2)
            el2 = random.randint(0, 2)
            if mas_plant[el1][el2] in Garden.get_plants():
                print('Растение нельзя посадить, так как оно уже есть на грядке')
                write_in_file('Растение нельзя посадить, так как оно уже есть на грядке')
                continue
            else:
                Garden.get_plants().append(mas_plant[el1][el2])
                print(f"Посажено новое растение: {Garden.get_plants()[len(Garden.get_plants()) - 1].get_name()}")
                write_in_file(
                    f"Посажено новое растение: {Garden.get_plants()[len(Garden.get_plants()) - 1].get_name()}")

    @staticmethod
    def grow_all() -> None:
        for plants in Garden.get_plants():
            plants.grow()

    @staticmethod
    def check_rotten() -> None:
        list_plant = copy.copy(Garden.get_plants())
        for plants in list_plant:
            if plants.is_rotten():
                print(f'{plants.get_name()} сгнил. Растение выкапывается из грядки.')
                write_in_file(f'{plants.get_name()} сгнил. Растение выкапывается из грядки.')
                Garden.get_plants().remove(plants)

    @staticmethod
    def check_weather_cond() -> None:
        list_plant = copy.copy(Garden.get_plants())
        for plants in list_plant:
            if plants.get_weather_cond() >= plants.get_limit_weather_cond_w():
                print(f'{plants.get_name()} потребил слишком много воды, он погиб.\nРастение выкапывается из грядки')
                write_in_file(f'{plants.get_name()} потребил слишком много воды, он погиб.'
                              f'\nРастение выкапывается из грядки')
                Garden.get_plants().remove(plants)
            elif plants.get_weather_cond() <= plants.get_limit_weather_cond_d():
                print(f'{plants.get_name()} был слишком долго без воды, он погиб.\nРастение выкапывается из грядки')
                write_in_file(f'{plants.get_name()} был слишком долго без воды, он погиб.'
                              f'\nРастение выкапывается из грядки')
                Garden.get_plants().remove(plants)

    def set_grow_weed(self, weed: int) -> None:
        self.weed += weed

    def grow_weed(self) -> None:
        Garden.set_grow_weed(10)
        print(f'Количество сорников в процентах: {self.weed}')
        write_in_file(f'Количество сорников в процентах: {self.weed}')
        if self.weed >= 100:
            list_plant = copy.copy(Garden.get_plants())
            print('Грядка слишком сильно заросла, все растения погибают.')
            write_in_file('Грядка слишком сильно заросла, все растения погибают.')
            for plants in list_plant:
                Garden.get_plants().remove(plants)

    def check_ill(self) -> None:
        if self.ill_die_status == 0:
            if self.chance_ill > 30:
                if len(Garden.get_plants()) >= 2:
                    self.choose_plant = random.randint(0, len(Garden.get_plants()) - 1)
                elif len(Garden.get_plants()) == 1:
                    self.choose_plant = 0
                choose_ill = random.randint(0, 1)
                self.ill_die_status += 1
                Garden.get_plants()[self.choose_plant].set_ill(choose_ill)
                Garden.get_plants()[self.choose_plant].ill()
                self.plant_die = Garden.get_plants()[self.choose_plant]
        elif 1 <= self.ill_die_status < 3:
            self.ill_die_status += 1
        elif self.ill_die_status >= 3:
            print(f'{self.plant_die.get_name()} погибает из-за болезни')
            write_in_file(f'{self.plant_die.get_name()} погибает из-за болезни')
            Garden.get_plants().remove(self.plant_die)
            self.ill_die_status = 0

    def set_sum_chance_ill(self, chance_ill: int) -> None:
        self.chance_ill += chance_ill

    def set_chance_ill(self, chance_ill: int) -> None:
        self.chance_ill = chance_ill

    def set_ill_die_status(self, ill_die_status: int) -> None:
        self.ill_die_status = ill_die_status

    def weeding(self) -> None:
        if self.weed > 0:
            self.weed = 0
            print('Грядка была прополена')
            write_in_file('Грядка была прополена')
        else:
            list_plant = copy.copy(Garden.get_plants())
            print('Вы решили прополоть грядку без сорников, все растения погибают')
            write_in_file('Вы решили прополоть грядку без сорников, все растения погибают')
            for plants in list_plant:
                Garden.get_plants().remove(plants)

    def fertilizer(self) -> None:
        print('Грядка была удобрена')
        write_in_file('Грядка была удобрена')
        for plants in Garden.get_plants():
            plants.set_state(0.20)
        self.die_status += 1
        Garden.set_chance_ill(0)
        Garden.set_ill_die_status(0)
        self.lim_die_status = self.lim_die_status + 3
        if self.lim_die_status <= self.week and self.die_status < 3:
            self.die_status = 0
        elif self.die_status == 3:
            list_plant = copy.copy(Garden.get_plants())
            print('Вы чрезмерно использовали удобрение, все растения погибают')
            write_in_file('Вы чрезмерно использовали удобрение, все растения погибают')
            for plants in list_plant:
                Garden.get_plants().remove(plants)

    def change_week(self) -> None:
        self.week += 1
        print(f'Сейчас {self.week} неделя')
        write_in_file(f'Сейчас {self.week} неделя')

    @staticmethod
    def change_weather(rand: int, rule: int = None) -> None:
        if rand == 0:
            chance = random.randint(0, 1)
            match chance:
                case 0:
                    print('Ясная погода')
                    write_in_file('Ясная погода')
                    Garden.set_grow_weed(5)
                    for plants in Garden.get_plants():
                        plants.set_state(0.10)
                        plants.set_weather_cond(0.15)
                case 1:
                    print('Пасмурная погода')
                    write_in_file('Пасмурная погода')
                    Garden.set_sum_chance_ill(3)
        elif rand == 1:
            match rule:
                case 0:
                    print('Ясная погода')
                    write_in_file('Ясная погода')
                    Garden.set_grow_weed(5)
                    for plants in Garden.get_plants():
                        plants.set_state(0.10)
                        plants.set_weather_cond(0.15)
                case 1:
                    print('Пасмурная погода')
                    write_in_file('Пасмурная погода')

    def long_watering_drought(self) -> None:
        if self.check_long_dur == 0:
            Garden.watering_drought()
        elif self.check_long_dur == 1:
            self.check_long_dur = 0
            print("Ливень продолжает идти в течении 1 недели")
            write_in_file("Ливень продолжает идти в течении 1 недели")
            for plants in Garden.get_plants():
                plants.watering()
        elif self.check_long_dur == 2:
            self.check_long_dur = 0
            print("Засуха будет продолжатся в течении 1 недели")
            write_in_file("Засуха будет продолжатся в течении 1 недели")
            for plants in Garden.get_plants():
                plants.drought()

    def watering_drought(self) -> None:
        chance = random.randint(0, 3)
        match chance:
            case 0:
                print('Осадков и засухи нет')
                write_in_file('Осадков и засухи нет')
                Garden.change_weather(0)
            case 1:
                print('Осадков и засухи нет')
                write_in_file('Осадков и засухи нет')
                Garden.change_weather(0)
            case 2:
                duration = random.randint(1, 2)
                if duration == 2:
                    self.check_long_dur = 1
                print(f'Начался ливень, он будет идти в течении {duration} недель')
                write_in_file(f'Начался ливень, он будет идти в течении {duration} недель')
                Garden.set_grow_weed(10)
                Garden.set_sum_chance_ill(7)
                Garden.change_weather(1, 1)
                for plants in Garden.get_plants():
                    plants.watering()
            case 3:
                duration = random.randint(1, 2)
                if duration == 2:
                    self.check_long_dur = 2
                print(f'Началась засуха, она будет идти в течении {duration} недель')
                write_in_file(f'Началась засуха, она будет идти в течении {duration} недель')
                Garden.set_grow_weed(-10)
                Garden.set_sum_chance_ill(7)
                Garden.change_weather(1, 0)
                for plants in Garden.get_plants():
                    plants.drought()

    @staticmethod
    def watering() -> None:
        print("Грядка была полита")
        write_in_file("Грядка была полита")
        for plants in Garden.get_plants():
            plants.watering()

    def are_all_ripe(self) -> None:
        list_plant = copy.copy(Garden.get_plants())
        Garden.check_rotten()
        Garden.check_ill()
        for plants in list_plant:
            if plants.is_ripe():
                if plants.get_can_harvest():
                    print(f'{plants.get_name()} созрел! Можно собирать!\n')
                    write_in_file(f'{plants.get_name()} созрел! Можно собирать!\n')
                    plants.num_harvest = plants.max_harvest()
                    check = False
                    while not check:
                        strings = input("Вы хотите собрать урожай?\n")
                        write_in_file("Вы хотите собрать урожай?\n")
                        match strings:
                            case "Да":
                                check = True
                                write_in_file("Да")
                                EngineGarden.collect_harvest(self, plants, plants.num_harvest)
                                print(f"Урожай: {Garden.get_harvest()}")
                                write_in_file(f"Урожай: {Garden.get_harvest()}")
                                print("Урожай был собран")
                                write_in_file("Урожай был собран")
                                Garden.get_plants().remove(plants)
                            case "Нет":
                                check = True
                                print("Урожай был не собран")
                                write_in_file("Урожай был не собран")
                            case _:
                                logger.warning("Невалидный аргумент")
                                write_in_file("Невалидный аргумент")


potato = Potato()
cucumber = Cucumber()
tomato = Tomato()
chamomile = Chamomile()
narcissus = Narcissus()
rose = Rose()
apple = Apple()
pear = Pear()
mandarin = Mandarin()

mas_plants = [[potato, cucumber, tomato], [chamomile, narcissus, rose], [apple, pear, mandarin]]
Garden = EngineGarden(rand_list_plants(mas_plants))

print('Для начала нажмите >')
f = open('history.txt', 'w')
f.close()
while True:
    b = input()
    match b:
        case ">":
            write_in_file(">")
            keyboard.send("ctrl+l")
            print('Номер недели, природные явления, состояние погоды:')
            write_in_file('Номер недели, природные явления, состояние погоды:')
            Garden.change_week()
            Garden.long_watering_drought()
            print()
            Garden.check_weather_cond()
            Garden.grow_all()
            Garden.grow_weed()
            Garden.are_all_ripe()
            print('\nВзаимодействия с грядкой:\nДля прополки грядки нажмите /\nДля удобрения грядки нажмите }'
                  '\nДля полива грядки нажмите {\nДля посадки нового растения нажмите *'
                  '\nДля просмотра урожая нажмите p\nДля просмотра истории нажмите h')
            write_in_file('\nВзаимодействия с грядкой:\nДля прополки грядки нажмите /\nДля удобрения грядки нажмите }'
                          '\nДля полива грядки нажмите {\nДля посадки нового растения нажмите *'
                          '\nДля просмотра урожая нажмите p\nДля просмотра истории нажмите h')
        case "/":
            write_in_file("/")
            Garden.weeding()
        case "}":
            write_in_file("}")
            Garden.fertilizer()
        case "{":
            write_in_file("{")
            Garden.watering()
        case "*":
            write_in_file("*")
            check = False
            try:
                num = int(input("Введите количество растений, которое вы хотите посадить, меньше 4: "))
            except ValueError:
                print("Вы ввели строку, а надо число")
                check = True
            if not check:
                write_in_file(f"Введите количество растений, которое вы хотите посадить, меньше 4: {num}")
                if 0 < num < 4:
                    Garden.add_new_rand_plants(mas_plants, num)
                else:
                    print("Вы ввели неверное количество растений")
                    write_in_file("Вы ввели неверное количество растений")
        case "p":
            if len(Garden.get_harvest()) == 0:
                print("Урожая пока нет")
                write_in_file("Урожая пока нет")
            else:
                print(Garden.get_harvest())
                write_in_file(Garden.get_harvest())
        case "h":
            f = open("history.txt")
            print(f.read())
            f.close()
        case "c":
            keyboard.send("ctrl+l")
        case _:
            logger.warning("Невалидный аргумент")
            write_in_file("Невалидный аргумент")
