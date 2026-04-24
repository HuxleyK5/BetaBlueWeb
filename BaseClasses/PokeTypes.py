from TVPoke.BaseClasses.PokeParentClass import Pokemon

TYPE_CHART = {
    "NORMAL": {
        "weak": ["FIGHTING"],
        "resist": [],
        "immune": ["GHOST"]
    },
    "FIRE": {
        "weak": ["WATER", "GROUND", "ROCK"],
        "resist": ["FIRE", "GRASS", "ICE", "BUG", "STEEL", "FAIRY"],
        "immune": []
    },
    "WATER": {
        "weak": ["ELECTRIC", "GRASS"],
        "resist": ["FIRE", "WATER", "ICE", "STEEL"],
        "immune": []
    },
    "ELECTRIC": {
        "weak": ["GROUND"],
        "resist": ["ELECTRIC", "FLYING", "STEEL"],
        "immune": []
    },
    "GRASS": {
        "weak": ["FIRE", "ICE", "POISON", "FLYING", "BUG"],
        "resist": ["WATER", "ELECTRIC", "GRASS", "GROUND"],
        "immune": []
    },
    "ICE": {
        "weak": ["FIRE", "FIGHTING", "ROCK", "STEEL"],
        "resist": ["ICE"],
        "immune": []
    },
    "FIGHTING": {
        "weak": ["FLYING", "PSYCHIC", "FAIRY"],
        "resist": ["BUG", "ROCK", "DARK"],
        "immune": []
    },
    "POISON": {
        "weak": ["GROUND", "PSYCHIC"],
        "resist": ["GRASS", "FIGHTING", "POISON", "BUG", "FAIRY"],
        "immune": []
    },
    "GROUND": {
        "weak": ["WATER", "GRASS", "ICE"],
        "resist": ["POISON", "ROCK"],
        "immune": ["ELECTRIC"]
    },
    "FLYING": {
        "weak": ["ELECTRIC", "ICE", "ROCK"],
        "resist": ["GRASS", "FIGHTING", "BUG"],
        "immune": ["GROUND"]
    },
    "PSYCHIC": {
        "weak": ["BUG", "GHOST", "DARK"],
        "resist": ["FIGHTING", "PSYCHIC"],
        "immune": []
    },
    "BUG": {
        "weak": ["FIRE", "FLYING", "ROCK"],
        "resist": ["GRASS", "FIGHTING", "GROUND"],
        "immune": []
    },
    "ROCK": {
        "weak": ["WATER", "GRASS", "FIGHTING", "GROUND", "STEEL"],
        "resist": ["NORMAL", "FIRE", "POISON", "FLYING"],
        "immune": []
    },
    "GHOST": {
        "weak": ["GHOST", "DARK"],
        "resist": ["POISON", "BUG"],
        "immune": ["NORMAL", "FIGHTING"]
    },
    "DRAGON": {
        "weak": ["ICE", "DRAGON", "FAIRY"],
        "resist": ["FIRE", "WATER", "ELECTRIC", "GRASS"],
        "immune": []
    },
    "DARK": {
        "weak": ["FIGHTING", "BUG", "FAIRY"],
        "resist": ["GHOST", "DARK"],
        "immune": ["PSYCHIC"]
    },
    "STEEL": {
        "weak": ["FIRE", "FIGHTING", "GROUND"],
        "resist": ["NORMAL", "GRASS", "ICE", "FLYING", "PSYCHIC", "BUG", "ROCK", "DRAGON", "STEEL", "FAIRY"],
        "immune": ["POISON"]
    },
    "FAIRY": {
        "weak": ["POISON", "STEEL"],
        "resist": ["FIGHTING", "BUG", "DARK"],
        "immune": ["DRAGON"]
    }
}