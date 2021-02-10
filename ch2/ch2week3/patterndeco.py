from abc import ABC, abstractmethod

class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points, 
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость 
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        return self.base.get_negative_effects()    
    
    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass
        

class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_negative_effects(self):
        pass


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        effects = self.base.get_positive_effects()
        effects.append("Berserk")
        return effects

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        stats["HP"] += 50
        return stats


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        effects = self.base.get_positive_effects()
        effects.append("Blessing")
        return effects

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Endurance"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2
        stats["Perception"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        return stats

class Weakness(AbstractNegative):
    def get_negative_effects(self):
        effects = self.base.get_negative_effects()
        effects.append("Weakness")
        return effects

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats

class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        effects = self.base.get_negative_effects()
        effects.append("EvilEye")
        return effects

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        effects = self.base.get_negative_effects()
        effects.append("Curse")
        return effects

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Endurance"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2
        stats["Perception"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        return stats

if __name__ == "__main__":
    hero = Hero()
    hero.get_stats()
    hero.stats
    hero.get_positive_effects()
    hero.get_negative_effects()

    brs1 = Berserk(hero)
    brs1.get_stats()
    brs1.get_positive_effects()
    brs1.get_negative_effects()

    brs2 = Berserk(brs1)
    cur1 = Curse(brs2)

    cur1.get_stats()
    cur1.get_negative_effects()
    cur1.get_positive_effects()

    cur1.base = brs1
    cur1.get_stats()
    cur1.get_negative_effects()
    cur1.get_positive_effects()