import random
from typing import NoReturn, List, Tuple
from forest import Forest
from blueberry import Blueberry
from hazel import Hazel
from maple import Maple
from boar import Boar
from elk import Elk
from wolf import Wolf
from bear import Bear
from creature_interfaces import Movable, Hunger, Aging, Dieable
from reproduction import GenderReproduction, NonGenderReproduction, Reproduction
from plant import Plant
from animal import Animal
import json
import os


class EcoSystem:

    @staticmethod
    def _define_creature_type(creature) -> str:
        if isinstance(creature, Blueberry):
            return "blueberry"
        elif isinstance(creature, Hazel):
            return "hazel"
        elif isinstance(creature, Maple):
            return "maple"
        elif isinstance(creature, Boar):
            return "boar"
        elif isinstance(creature, Elk):
            return "elk"
        elif isinstance(creature, Wolf):
            return "wolf"
        elif isinstance(creature, Bear):
            return "bear"
        else:
            raise TypeError(f"Not part of ecosystem: {type(creature)}")

    @staticmethod
    def _save_creature_to_dict(creature) -> dict:
        if not isinstance(creature, Animal) and not isinstance(creature, Plant):
            raise TypeError(f"Not part of ecosystem: {type(creature)}")
        creature_info = creature.get_dict_of_info()
        creature_info["type"] = EcoSystem._define_creature_type(creature)
        return creature_info

    def _fill_forest_with_creatures(self, **kwargs) -> NoReturn:
        kwargs["blueberry_amount"] = kwargs.get("blueberry_amount", 20)
        kwargs["hazel_amount"] = kwargs.get("hazel_amount", 10)
        kwargs["maple_amount"] = kwargs.get("maple_amount", 10)
        kwargs["boar_amount"] = kwargs.get("boar_amount", 12)
        kwargs["elk_amount"] = kwargs.get("elk_amount", 6)
        kwargs["wolf_amount"] = kwargs.get("wolf_amount", 12)
        kwargs["bear_amount"] = kwargs.get("bear_amount", 6)
        for key, value in kwargs.items():
            if key.endswith("_amount"):
                new_key = key.replace("_amount", "")
                for _ in range(value):
                    random_line_number = random.randint(0, self.forest.vertical_length - 1)
                    random_column_number = random.randint(0, self.forest.horizontal_length - 1)
                    self.fill_creatures(new_key, 1, (random_line_number, random_column_number))

    def _unpack_creatures(self, creatures_info_dicts: List) -> NoReturn:
        for creature_info_dict in creatures_info_dicts:
            i, j = creature_info_dict["position"]
            if creature_info_dict["type"] == "blueberry":
                self._forest.hectares[i][j].creations.append(Blueberry(unpack_dict_flag=True,
                                                                       info_d=creature_info_dict))
            elif creature_info_dict["type"] == "hazel":
                self._forest.hectares[i][j].creations.append(Hazel(unpack_dict_flag=True, info_d=creature_info_dict))
            elif creature_info_dict["type"] == "maple":
                self._forest.hectares[i][j].creations.append(Maple(unpack_dict_flag=True, info_d=creature_info_dict))
            elif creature_info_dict["type"] == "boar":
                self._forest.hectares[i][j].creations.append(Boar(unpack_dict_flag=True, info_d=creature_info_dict))
            elif creature_info_dict["type"] == "elk":
                self._forest.hectares[i][j].creations.append(Elk(unpack_dict_flag=True, info_d=creature_info_dict))
            elif creature_info_dict["type"] == "wolf":
                self._forest.hectares[i][j].creations.append(Wolf(unpack_dict_flag=True, info_d=creature_info_dict))
            elif creature_info_dict["type"] == "bear":
                self._forest.hectares[i][j].creations.append(Bear(unpack_dict_flag=True, info_d=creature_info_dict))
            else:
                raise ValueError

    @staticmethod
    def _unpack_id_counters(id_counters_dict) -> NoReturn:
        Blueberry.set_id_counter(id_counters_dict["blueberry_id_counter"])
        Hazel.set_id_counter(id_counters_dict["hazel_id_counter"])
        Maple.set_id_counter(id_counters_dict["maple_id_counter"])
        Boar.set_id_counter(id_counters_dict["boar_id_counter"])
        Elk.set_id_counter(id_counters_dict["elk_id_counter"])
        Wolf.set_id_counter(id_counters_dict["wolf_id_counter"])
        Bear.set_id_counter(id_counters_dict["bear_id_counter"])

    def __init__(self, unpack_dict_flag=False, *args, **kwargs):
        kwargs["forest_vertical_length"] = kwargs.get("forest_vertical_length", 7)
        kwargs["forest_horizontal_length"] = kwargs.get("forest_horizontal_length", 7)
        kwargs["deadly_worm_sleep_interval"] = kwargs.get("deadly_worm_sleep_interval", 5)
        if unpack_dict_flag:
            kwargs["deadly_worm_sleep_counter"] = kwargs.get("deadly_worm_sleep_counter", 5)
        self._forest = Forest(vertical_length=kwargs["forest_vertical_length"],
                              horizontal_length=kwargs["forest_horizontal_length"])
        self._deadly_worm_sleep_interval = kwargs["deadly_worm_sleep_interval"]
        if unpack_dict_flag:
            self._deadly_worm_sleep_counter = kwargs["deadly_worm_sleep_counter"]
            EcoSystem._unpack_id_counters(args[0])
            self._unpack_creatures(args[1:])
            return

        self._deadly_worm_sleep_counter = self._deadly_worm_sleep_interval
        self._fill_forest_with_creatures(**kwargs)

    def _find_max_id_size(self) -> int:
        max_id_size = 0
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if max_id_size < len(creature.id):
                        max_id_size = len(creature.id)
        return max_id_size

    def _find_max_amount_in_hectare(self) -> int:
        max_amount = 0
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                if len(hectare.creations) > max_amount:
                    max_amount = len(hectare.creations)
        return max_amount

    def __str__(self):
        from math import log10
        if self._is_wasteland():
            return self._show_wasteland()
        max_id = self._find_max_id_size()
        max_amount_in_hectare = self._find_max_amount_in_hectare()
        res_str = f"{'':<{int(log10(self.forest.vertical_length) + 1)}}|"
        for i in range(self.forest.horizontal_length):
            res_str += f"{i:<{max_id}}|"
        res_str += "\n"

        for i in range(self.forest.vertical_length):
            res_str += ("-" * int(log10(self.forest.vertical_length) + 1)) + "+"
            for _ in range(self.forest.horizontal_length):
                res_str += ("-" * max_id) + "+"
            res_str += "\n"

            print_number = True
            for k in range(max_amount_in_hectare):
                vertical_number_of_hectare = str(i) if print_number else ""
                print_number = False
                res_str += f"{vertical_number_of_hectare:<{int(log10(self.forest.vertical_length) + 1)}}|"
                for j in range(self._forest.horizontal_length):
                    try:
                        res_str += f"{str(self.forest.hectares[i][j].creations[k]):<{max_id}}|"
                    except IndexError:
                        res_str += f"{'':<{max_id}}|"
                res_str += f"\n"
        return res_str

    def _is_wasteland(self) -> bool:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Plant) or isinstance(creature, Animal):
                        return False
        return True

    def _show_wasteland(self) -> str:
        from math import log10
        max_id = len("great_wasteland")
        res_str = f"{'':<{int(log10(self.forest.vertical_length) + 1)}}|"
        for i in range(self.forest.horizontal_length):
            res_str += f"{i:<{max_id}}|"
        res_str += "\n"
        for i in range(self.forest.vertical_length):
            res_str += ("-" * int(log10(self.forest.vertical_length) + 1)) + "+"
            for _ in range(self.forest.horizontal_length):
                res_str += ("-" * max_id) + "+"
            res_str += "\n"
            res_str += f"{i:<{int(log10(self.forest.vertical_length) + 1)}}|"
            for _ in range(self.forest.horizontal_length):
                res_str += "great_wasteland|"
            res_str += "\n"
        return res_str

    def _provoke_on_move(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Movable):
                        creature.move(self._forest)

    def _provoke_on_nutrition(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Hunger):
                        creature.search_for_food(hectare)

    def _provoke_animals_on_reproduction(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, GenderReproduction):
                        hectare.extend_hectare(creature.reproduction(hectare))

    def _find_position_in_forest(self, creature: Reproduction) -> Tuple[int, int]:
        not_found_flag = True
        i = 0
        j = 0
        for hectare_line in self.forest.hectares:
            j = 0
            for hectare in hectare_line:
                if creature in hectare.creations:
                    not_found_flag = False
                    break
                j += 1
            else:
                i += 1
                continue
            break
        if not_found_flag:
            raise ValueError(f"Creature with id {creature.id} wasn't found in forest")
        return i, j

    def _disperse_offsprings(self, offsprings: List[NonGenderReproduction], parent_pos: Tuple[int, int]) -> NoReturn:
        vert_pos, horiz_pos = parent_pos
        for offspring in offsprings:
            if not isinstance(offspring, Plant):
                raise TypeError(f'Offspring must be Plant. {type(offspring)} got instead')
            vertical_shift = random.randint(-offspring.offspring_dispersion, offspring.offspring_dispersion)
            horizontal_shift = random.randint(-offspring.offspring_dispersion, offspring.offspring_dispersion)
            while vert_pos + vertical_shift >= self.forest.vertical_length or \
                    horiz_pos + horizontal_shift >= self.forest.horizontal_length:
                vertical_shift = random.randint(-1, 1)
                horizontal_shift = random.randint(-1, 1)
            self.forest.hectares[vert_pos + vertical_shift][horiz_pos + horizontal_shift].creations.append(offspring)

    def _provoke_plants_on_reproduction(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, NonGenderReproduction):
                        offsprings = creature.reproduction()
                        parent_position = self._find_position_in_forest(creature)
                        self._disperse_offsprings(offsprings=offsprings, parent_pos=parent_position)

    def _period(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Aging):
                        creature.live_time_cycle()
        self._normal_deadly_worm_period()

    def _normal_deadly_worm_period(self) -> NoReturn:
        if self._deadly_worm_sleep_counter == 0:
            self.provoke_deadly_worm()
            self._deadly_worm_sleep_counter = self._deadly_worm_sleep_interval
        else:
            self._deadly_worm_sleep_counter -= 1

    def cycle(self) -> NoReturn:
        if not self._is_wasteland():
            self._provoke_on_nutrition()
            self._provoke_animals_on_reproduction()
            self._provoke_plants_on_reproduction()
            self._provoke_on_move()
            self._period()
            # self.sa
            apocalypse_chance = random.randint(1, 100000)
            if apocalypse_chance == 1:
                self.apocalypse()

    def apocalypse(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Dieable):
                        creature.die()
        self._deadly_worm_sleep_counter = 0

    def provoke_deadly_worm(self) -> NoReturn:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                not_dead_creatures = [creature for creature in hectare.creations if not creature.is_dead()]
                hectare.update_hectare(not_dead_creatures)

    @property
    def forest(self) -> Forest:
        return self._forest

    def remove_creature(self, creature_id: str) -> NoReturn:
        for hectare_line in self.forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Reproduction) and creature_id == creature.id:
                        hectare.creations.remove(creature)
                        return
        raise ValueError(f"No creature with id {creature_id}")

    def fill_creatures(self, creature_type: str, creature_amount: int, hectare_number: Tuple[int, int]) -> NoReturn:
        if not 0 <= hectare_number[0] < self.forest.vertical_length or\
                not 0 <= hectare_number[0] < self.forest.horizontal_length:
            raise IndexError("Hectare out of forest")
        creature_type = creature_type.lower()
        if creature_type == "blueberry":
            creatures = [Blueberry() for _ in range(creature_amount)]
        elif creature_type == "hazel":
            creatures = [Hazel() for _ in range(creature_amount)]
        elif creature_type == "maple":
            creatures = [Maple() for _ in range(creature_amount)]
        elif creature_type == "boar":
            creatures = [Boar() for _ in range(creature_amount)]
        elif creature_type == "elk":
            creatures = [Elk() for _ in range(creature_amount)]
        elif creature_type == "wolf":
            creatures = [Wolf() for _ in range(creature_amount)]
        elif creature_type == "bear":
            creatures = [Bear() for _ in range(creature_amount)]
        else:
            raise TypeError(f"Incorrect type of creature: {creature_type}")
        self.forest.hectares[hectare_number[0]][hectare_number[1]].extend_hectare(creatures)

    @staticmethod
    def load(filename):
        with open(filename, "r") as save_file:
            loaded_info = json.load(save_file)
            ecosystem_info = loaded_info[0]
            unpack_dict_flag = True
            return EcoSystem(unpack_dict_flag, *loaded_info[1:], **ecosystem_info)

    def save(self, filename) -> NoReturn:
        res_lst = [
            {
                "deadly_worm_sleep_interval": self._deadly_worm_sleep_interval,
                "deadly_worm_sleep_counter": self._deadly_worm_sleep_counter,
                "forest_horizontal_length": self._forest.horizontal_length,
                "forest_vertical_length": self._forest.vertical_length
            },
            {
                "blueberry_id_counter": Blueberry.get_id_counter(),
                "hazel_id_counter": Hazel.get_id_counter(),
                "maple_id_counter": Maple.get_id_counter(),
                "boar_id_counter": Boar.get_id_counter(),
                "elk_id_counter": Elk.get_id_counter(),
                "wolf_id_counter": Wolf.get_id_counter(),
                "bear_id_counter": Bear.get_id_counter()
            }
        ]
        i = 0
        for hectare_line in self.forest.hectares:
            j = 0
            for hectare in hectare_line:
                if hectare.creations:
                    for creature in hectare.creations:
                        if isinstance(creature, Animal) or isinstance(creature, Plant):
                            creature_info = EcoSystem._save_creature_to_dict(creature)
                            creature_info["position"] = (i, j)
                            res_lst.append(creature_info)
                j += 1
            i += 1
        with open(filename, "w") as save_file:
            json.dump(res_lst, save_file, indent="\t")

    def creature_stats(self, creature_id) -> str:
        for hectare_line in self._forest.hectares:
            for hectare in hectare_line:
                for creature in hectare.creations:
                    if isinstance(creature, Animal) or isinstance(creature, Plant):
                        return creature.stats()
        raise ValueError(f"No creature with id {creature_id}")


if __name__ == "__main__":
    d = {
        "forest_vertical_length": 5,
        "forest_horizontal_length": 5,
        "deadly_worm_sleep_interval": 3,
        "blueberry_amount": 0,
        "hazel_amount": 20,
        "maple_amount": 0,
        "boar_amount": 0,
        "elk_amount": 15,
        "wolf_amount": 0,
        "bear_amount": 0
    }
    a = EcoSystem(**d)
    print(a)
    for i in range(100000):
        print(i)
        a.cycle()
        print(a)
        os.system("clear")
    input()
    a.apocalypse()
    print(a)
    input()
    a.cycle()
    print(a)
    input()

