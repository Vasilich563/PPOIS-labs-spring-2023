import enum


CREATOR = "Vodohleb04"

BASE_ECOSYSTEM_PARAMETERS = {
    "forest_vertical_length": 7,
    "forest_horizontal_length": 7,
    "deadly_worm_sleep_interval": 5,
    "deadly_worm_sleep_counter": 5,
    "blueberry_amount": 20,
    "hazel_amount": 10,
    "maple_amount": 10,
    "boar_amount": 12,
    "elk_amount": 6,
    "wolf_amount": 12,
    "bear_amount": 6
}


class LifeMedian(enum.Enum):

    BLUEBERRY_LM = 3
    HAZEL_LM = 70
    MAPLE_LM = 200

    BOAR_LM = 15
    ELK_LM = 14
    WOLF_LM = 10
    BEAR_LM = 25


class PlantOffspringDispersion(enum.Enum):

    BLUEBERRY_OD = 1
    HAZEL_OD = 1
    MAPLE_OD = 2


class PlantEatableOffspringPossibleAmount(enum.Enum):

    BLUEBERRY_EOPA = (10, 15)
    HAZEL_EOPA = (10, 15)
    MAPLE_EOPA = (25, 35)


class PlantHPReduction(enum.Enum):

    BLUEBERRY_HPR = 5
    HAZEL_HPR = 13
    MAPLE_HPR = 50


class PlantShrubReduction(enum.Enum):

    BLUEBERRY_SR = 5
    HAZEL_SR = 25
    MAPLE_SR = 50


class StartPower(enum.Enum):

    BLUEBERRY_SP = 1.0
    HAZEL_SP = 5.0
    MAPLE_SP = 10.0

    M_BOAR_SP = 10.0
    FEM_BOAR_SP = 8.0

    M_ELK_SP = 15
    FEM_ELK_SP = 10

    M_WOLF_SP = 12
    FEM_WOLF_SP = 10

    M_BEAR_SP = 15
    FEM_BEAR_SP = 12


class PowerFunctionCoefficient(enum.Enum):

    BLUEBERRY_PFC = 0.0
    HAZEL_PFC = (2. / 3.)
    MAPLE_PFC = 1.0

    M_BOAR_PFC = 6.0
    FEM_BOAR_PFC = (24. / 5.)

    M_ELK_PFC = 12.5
    FEM_ELK_PFC = (42.5 / 4)

    M_WOLF_PFC = (40.5 / 3.)
    FEM_WOLF_PFC = (35. / 3.)

    M_BEAR_PFC = (55. / 8)
    FEM_BEAR_PFC = (55.5 / 8)


class PersonalPowerCoefficientParameters(enum.Enum):

    BLUEBERRY_PPCP = {"min_numerator": 1, "max_numerator": 1, "denominator": 1}
    HAZEL_PPCP = {"min_numerator": 20, "max_numerator": 30, "denominator": 25}
    MAPLE_PPCP = {"min_numerator": 40, "max_numerator": 55, "denominator": 50}

    FEM_BOAR_PPCP = {"min_numerator": 25, "max_numerator": 35, "denominator": 30}
    M_BOAR_PPCP = {"min_numerator": 35, "max_numerator": 45, "denominator": 40}

    FEM_ELK_PPCP = {"min_numerator": 40, "max_numerator": 65, "denominator": 52.5}
    M_ELK_PPCP = {"min_numerator": 55, "max_numerator": 75, "denominator": 65}

    FEM_WOLF_PPCP = {"min_numerator": 35, "max_numerator": 55, "denominator": 45}
    M_WOLF_PPCP = {"min_numerator": 40, "max_numerator": 65, "denominator": 52.5}

    FEM_BEAR_PPCP = {"min_numerator": 55, "max_numerator": 80, "denominator": 67.5}
    M_BEAR_PPCP = {"min_numerator": 60, "max_numerator": 80, "denominator": 70}


class NutritionalValue(enum.Enum):

    START_BLUEBERRY_SNV = 30
    START_HAZEL_SNV = 50
    START_MAPLE_SNV = 100

    BLUEBERRY_OFFSPRING_NV = 5
    HAZEL_OFFSPRING_NV = 10
    MAPLE_OFFSPRING_NV = 5

    BOAR_NV = 250
    ELK_NV = 600
    WOLF_NV = 200
    BEAR_NV = 600


class Damage(enum.Enum):

    BOAR_D = 100
    ELK_D = 300
    WOLF_D = 200
    BEAR_D = 350


class UnprotectedDamageMultiplier(enum.Enum):

    BLUEBERRY_UDM = 0.1
    HAZEL_UDM = 0.05
    MAPLE_UDM = 0.075

    EVERY_ANIMAL_UDM = 0.1


class StartHP(enum.Enum):

    BLUEBERRY_START_HP = 5
    HAZEL_START_HP = 10
    MAPLE_START_HP = 10


class MaxHP(enum.Enum):

    BLUEBERRY_MHP = 10
    HAZEL_MHP = 400
    MAPLE_MHP = 1000

    BOAR_MHP = 200
    ELK_MHP = 350
    WOLF_MHP = 200
    BEAR_MHP = 300


class RequiredNutritionalValue(enum.Enum):

    BOAR_RNV = 100
    ELK_RNV = 125
    BEAR_RNV = 150


class HungerPerCycle(enum.Enum):

    BOAR_HPC = 75
    ELK_HPC = 100
    WOLF_HPC = 100
    BEAR_HPC = 150


class Genders(enum.Enum):

    FEMALE = "female"
    MALE = "male"


class ReproductionAgeInterval(enum.Enum):

    BLUEBERRY_RAI = (1, 4)
    HAZEL_RAI = (30, 70)
    MAPLE_RAI = (50, 200)

    BOAR_RAI = (5, 11)
    ELK_RAI = (4, 12)
    WOLF_RAI = (3, 9)
    BEAR_RAI = (8, 20)


class IdPrefix(enum.Enum):

    BLUEBERRY_PREF = "blueberry"
    HAZEL_PREF = "hazel"
    MAPLE_PREF = "maple"

    BOAR_PREF = "boar"
    ELK_PREF = "elk"
    WOLF_PREF = "wolf"
    BEAR_PREF = "bear"


class ChanceToProduceKids(enum.Enum):

    BLUEBERRY_CTPK = (0, 2)
    HAZEL_CTPK = (1, 10)
    MAPLE_CTPK = (1, 40)

    BOAR_CTPK = (1, 3)
    ELK_CTPK = (1, 2)
    WOLF_CTPK = (1, 3)
    BEAR_CTPK = (1, 2)


class PossibleKidsAmount(enum.Enum):

    BLUEBERRY_PKA = (2, 4)
    HAZEL_PKA = (2, 4)
    MAPLE_PKA = (1, 3)

    BOAR_PKA = (3, 5)
    ELK_PKA = (2, 3)
    WOLF_PKA = (3, 5)
    BEAR_PKA = (2, 3)


class SterilePeriods(enum.Enum):

    BOAR_SP = 2
    ELK_SP = 3
    WOLF_SP = 2
    BEAR_SP = 4

