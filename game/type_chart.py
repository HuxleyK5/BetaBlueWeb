"""Complete defensive type chart used by every battle mode."""


TYPE_DEFENSES = {
    "Normal": {"weak": {"Fighting"}, "resist": set(), "immune": {"Ghost"}},
    "Fire": {"weak": {"Water", "Ground", "Rock"}, "resist": {"Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"}, "immune": set()},
    "Water": {"weak": {"Electric", "Grass"}, "resist": {"Fire", "Water", "Ice", "Steel"}, "immune": set()},
    "Electric": {"weak": {"Ground"}, "resist": {"Electric", "Flying", "Steel"}, "immune": set()},
    "Grass": {"weak": {"Fire", "Ice", "Poison", "Flying", "Bug"}, "resist": {"Water", "Electric", "Grass", "Ground"}, "immune": set()},
    "Ice": {"weak": {"Fire", "Fighting", "Rock", "Steel"}, "resist": {"Ice"}, "immune": set()},
    "Fighting": {"weak": {"Flying", "Psychic", "Fairy"}, "resist": {"Bug", "Rock", "Dark"}, "immune": set()},
    "Poison": {"weak": {"Ground", "Psychic"}, "resist": {"Grass", "Fighting", "Poison", "Bug", "Fairy"}, "immune": set()},
    "Ground": {"weak": {"Water", "Grass", "Ice"}, "resist": {"Poison", "Rock"}, "immune": {"Electric"}},
    "Flying": {"weak": {"Electric", "Ice", "Rock"}, "resist": {"Grass", "Fighting", "Bug"}, "immune": {"Ground"}},
    "Psychic": {"weak": {"Bug", "Ghost", "Dark"}, "resist": {"Fighting", "Psychic"}, "immune": set()},
    "Bug": {"weak": {"Fire", "Flying", "Rock"}, "resist": {"Grass", "Fighting", "Ground"}, "immune": set()},
    "Rock": {"weak": {"Water", "Grass", "Fighting", "Ground", "Steel"}, "resist": {"Normal", "Fire", "Poison", "Flying"}, "immune": set()},
    "Ghost": {"weak": {"Ghost", "Dark"}, "resist": {"Poison", "Bug"}, "immune": {"Normal", "Fighting"}},
    "Dragon": {"weak": {"Ice", "Dragon", "Fairy"}, "resist": {"Fire", "Water", "Electric", "Grass"}, "immune": set()},
    "Dark": {"weak": {"Fighting", "Bug", "Fairy"}, "resist": {"Ghost", "Dark"}, "immune": {"Psychic"}},
    "Steel": {"weak": {"Fire", "Fighting", "Ground"}, "resist": {"Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"}, "immune": {"Poison"}},
    "Fairy": {"weak": {"Poison", "Steel"}, "resist": {"Fighting", "Bug", "Dark"}, "immune": {"Dragon"}},
}


def effectiveness(attack_type, defender_types):
    multiplier = 1.0
    for defender_type in defender_types:
        defense = TYPE_DEFENSES[defender_type]
        if attack_type in defense["immune"]:
            return 0.0
        if attack_type in defense["weak"]:
            multiplier *= 2.0
        elif attack_type in defense["resist"]:
            multiplier *= 0.5
    return multiplier
