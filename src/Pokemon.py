import random
import asyncio
import json
from PokemonNames import PokemonNames

class Pokemon():
    def __init__(self, name, type, hp, max_hp, attack, speed):
        try:
            if not isinstance(name, str):
                raise ValueError("Jméno pokémona musí být str.")
            if not isinstance(type, str):
                raise ValueError("Typ pokémona musí být str.")

            if not isinstance(max_hp, int) or max_hp <= 0:
                raise ValueError("Maximální životy pokémona musí int a musí být větší než 0.")
            if not isinstance(attack, int) or attack <= 0:
                raise ValueError("Útok pokémona musí být int a musí být větší než 0.")
            if not isinstance(speed, int) or speed <= 0:
                raise ValueError("Rychlost pokémona musí být int a musí být větší než 0.")
            if type not in ["Fire", "Grass", "Water"]:
                raise ValueError("Typ pokémona musí být Fire, Grass nebo Water")
            
            self.name = name
            self.type = type
            self.hp = hp
            self.max_hp = max_hp
            self.attack = attack
            self.speed = speed
        
        except ValueError as e:
            print(f"Error: {e}")
            raise

    def __str__(self):
        return f"----------Pokémon----------\nJméno: {self.name}\nTyp: {self.type}\nŽivoty: {self.hp}/{self.max_hp}\nÚtok: {self.attack}\nRychlost: {self.speed}"

    def take_damage(self, damage):
        """Sníží životy pokémona o dané poškození."""
        try:
            if not isinstance(damage, (int, float)) or damage < 0:
                raise ValueError("Poškození musí být kladné číslo.")
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0
        except ValueError as e:
            print(f"Error: {e}")
            raise

    def is_alive(self):
        """Zjišťuje, zda je Pokémon stále naživu."""
        return self.hp > 0

    def effectiveness(self, type):
        """Vypočítá efektivitu typu proti jinému typu."""
        try:
            if not isinstance(type, str):
                raise ValueError("Typ musí být string.")
            chart = {
                ("Fire", "Grass"): 2,
                ("Water", "Fire"): 2,
                ("Grass", "Water"): 2,
                ("Fire", "Water"): 0.5,
                ("Grass", "Fire"): 0.5,
                ("Water", "Grass"): 0.5
            }
            return chart.get((self.type, type), 1)
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    async def train(self):
        """Trénink pokémona a vylepšení statistik"""
        try:
            print(f"{self.name} začíná trénink...")
            await asyncio.sleep(random.randint(1, 3))
            training_result = random.choice(['attack', 'speed', 'max_hp'])
            boost = random.randint(1, 3)
            if training_result == 'attack':
                self.attack += boost
                print(f"{self.name} zlepšil svůj útok o {boost}.")
            elif training_result == 'speed':
                self.speed += boost
                print(f"{self.name} zlepšil svou rychlost o {boost}.")
            elif training_result == 'max_hp':
                self.max_hp += boost
                self.hp += boost
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                print(f"{self.name} zlepšil své maximální životy o {boost}.")
        except Exception as e:
            print(f"Error: {e}")
            raise

def generate_pokemon(difficulty="medium"):
    """Generování pokémona s náhodnými statistikami"""
    try:
        diff = {
            "easy": 0.8,
            "medium": 1.0,
            "hard": 1.5,
        }
        modifier = diff.get(difficulty, 1.0)
        pokemon = random.choice(list(PokemonNames))
        name, type = pokemon.value
        max_hp = int(random.randint(50, 100) * modifier)
        attack = int(random.randint(10, 30) * modifier)
        speed = int(random.randint(2, 10) * modifier)
        hp = max_hp
        return Pokemon(name, type, hp, max_hp, attack, speed)
    except Exception as e:
        print(f"Error: {e}")
        raise

def save_pokemon(pokemon):
    """Uložení pokémona do souboru"""
    try:
        saved_pokemon = {
            "name": pokemon.name,
            "type": pokemon.type,
            "hp": pokemon.hp,
            "max_hp": pokemon.max_hp,
            "attack": pokemon.attack,
            "speed": pokemon.speed
        }
        with open("saved_pokemon.json", "w") as f:
            json.dump(saved_pokemon, f)
        print("Pokémon byl uložen do souboru.")
    except Exception as e:
        print(f"Chyba při ukládání pokémona: {e}")

def load_pokemon():
    """Načtení pokémona ze souboru"""
    try:
        with open("saved_pokemon.json", "r") as f:
            saved_pokemon = json.load(f)
        pokemon = Pokemon(
            saved_pokemon["name"],
            saved_pokemon["type"],
            saved_pokemon["hp"],
            saved_pokemon["max_hp"],
            saved_pokemon["attack"],
            saved_pokemon["speed"]
        )
        print("Pokémon se načetl.")
        return pokemon
    except FileNotFoundError:
        print("Soubor pro načtení pokémona nebyl nalezen.")
    except Exception as e:
        print(f"Error: {e}")
