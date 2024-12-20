import datetime
import json
import asyncio
import random
from Pokemon import Pokemon, generate_pokemon

class Trainer:
    def __init__(self, name):
        try:
            if not isinstance(name, str):
                raise ValueError("Jméno trenéra musí být str.")
            self.name = name
            self.defeated_pokemons = 0
            self.completed_arenas = 0
            self.account_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.pokemon_team = []
        except ValueError as e:
            print(f"Chyba při vytváření trenéra: {e}")
            raise

    def __str__(self):
        return f"----------Trenér----------\nJméno: {self.name}\nPoražených pokémonů: {self.defeated_pokemons}\nDokončené arény: {self.completed_arenas}\nDatum vytvoření účtu: {self.account_created}\nPočet pokémonů: {len(self.pokemon_team)}"


    def add_pokemon(self, pokemon):
        """Přidá pokémona do týmu trenéra"""
        try:
            if len(self.pokemon_team) < 6:
                self.pokemon_team.append(pokemon)
                print(f"{pokemon.name} byl přidán trenérovi {self.name}.")
            else:
                print(f"Nemůžeš mít víc jak 6 Pokémonů.")
        except Exception as e:
            print(f"Error: {e}")

    def remove_pokemon(self, index):
        """Odstraní pokémona z týmu podle indexu"""
        try:
            if 0 <= index < len(self.pokemon_team):
                removed_pokemon = self.pokemon_team.pop(index)
                print(f"{removed_pokemon.name} byl odstraněn od trenéra {self.name}.")
            else:
                raise IndexError(f"Špatný index pokémona: {index}.")
        except IndexError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    async def heal_pokemons(self):
        """Vyléčí všechny pokémony v týmu"""
        if not self.pokemon_team:
            print("Trenér nemá žádné pokémony k vyléčení.")
            return
        for pokemon in self.pokemon_team:
            heal_time = random.randint(3, 5) 
            print(f"Léčení {pokemon.name} ({heal_time} sekundy)")
            await asyncio.sleep(heal_time) 
            pokemon.hp = pokemon.max_hp  
            print(f"{pokemon.name} byl vyléčen.")

        print("Všichni pokémoni byli vyléčeni.")    

    async def start_battle(self):
        """Spustí souboj s nepřítelem"""
        try:
            print("Vyberte obtížnost souboje:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty_choice = input("Zadejte číslo: ").strip()
            if difficulty_choice == "1":
                difficulty = "easy"
            elif difficulty_choice == "2":
                difficulty = "medium"
            elif difficulty_choice == "3":
                difficulty = "hard"
            else:
                print("Neplatná volba, nastavuji obtížnost na 'medium'.")
                difficulty = "medium"
            print("Vyberte pokémona pro souboj:")
            if not self.pokemon_team:
                print("Nemáte žádné Pokémony v týmu, souboj se nemůže konat.")
                return
            for i, pokemon in enumerate(self.pokemon_team):
                print(f"{i + 1}. {pokemon.name}")   
            valid_choice = False
            player_pokemon = None
            while not valid_choice:
                choice = input(f"Zadejte číslo (1 - {len(self.pokemon_team)}): ").strip()
                try:
                    choice = int(choice) - 1 
                    if 0 <= choice < len(self.pokemon_team):
                        player_pokemon = self.pokemon_team[choice]
                        valid_choice = True
                    else:
                        print(f"Neplatná volba, zadejte číslo mezi 1 a {len(self.pokemon_team)}.")
                except ValueError:
                    print("Zadejte platné číslo.")
            if player_pokemon is None:
                print("Nezvolil jsi si pokémona, souboj skončil.")
                return
            opponent = generate_pokemon(difficulty)
            print("Nepřítel:")
            print(opponent)
            winner = await self.simple_battle(player_pokemon, opponent)
            if winner == "player":
                print(f"Trenér {self.name} vyhrál souboj!")
                self.defeated_pokemons += 1
            elif winner == "opponent":
                print(f"Pokémon {opponent.name} vyhrál souboj!")
            else:
                print("Souboj skončil remízou.")
        except Exception as e:
            print(f"Error: {e}")


    async def simple_battle(self, player, opponent):
        """Provádí jednoduchý souboj mezi dvěma pokémony"""
        try:
            turn_order = [player, opponent] if player.speed >= opponent.speed else [opponent, player]
            while player.is_alive() and opponent.is_alive():
                for attacker in turn_order:
                    defender = opponent if attacker == player else player
                    await self.attack_turn(attacker, defender)
            if player.is_alive():
                return "player"
            elif opponent.is_alive():
                return "opponent"
            else:
                return "draw"
        except Exception as e:
            print(f"Error: {e}")
            return "draw"

    async def attack_turn(self, attacker, defender):
        """Provádí útok pokémona během souboje"""
        try:
            attack_delay = max(1.0, 2.0 - attacker.speed / 10.0)
            await asyncio.sleep(attack_delay)
            damage = attacker.attack * attacker.effectiveness(defender.type)
            defender.take_damage(damage)
            print(f"{attacker.name} způsobil {damage} poškození {defender.name}.")
            if defender.is_alive():
                print(f"{defender.name} má {defender.hp} životů.")
            else:
                print(f"{defender.name} je poražen!")
        except Exception as e:
            print(f"Error: {e}")

    def save_trainer(trainer):
        """Uloží data trenéra do souboru"""
        try:
            saved_trainer = {
                "name": trainer.name,
                "defeated_pokemons": trainer.defeated_pokemons,
                "completed_arenas": trainer.completed_arenas,
                "account_created": trainer.account_created,
                "pokemon_team": [
                    {
                        "name": pokemon.name,
                        "type": pokemon.type,
                        "hp": pokemon.hp,
                        "max_hp": pokemon.max_hp,
                        "attack": pokemon.attack,
                        "speed": pokemon.speed,
                    }
                    for pokemon in trainer.pokemon_team
                ],
            }
            with open("saved_trainer.js", "w") as f:
                json.dump(saved_trainer, f)
            print("Trenér byl uložen do souboru.")
        except Exception as e:
            print(f"Error: {e}")

    def load_trainer():
        """Načte data trenéra ze souboru"""
        try:
            with open("saved_trainer.js", "r") as f:
                saved_trainer = json.load(f)
            trainer = Trainer(saved_trainer["name"])
            trainer.defeated_pokemons = saved_trainer["defeated_pokemons"]
            trainer.completed_arenas = saved_trainer["completed_arenas"]
            trainer.account_created = saved_trainer["account_created"]
            for saved_pokemon in saved_trainer["pokemon_team"]:
                pokemon = Pokemon(
                    saved_pokemon["name"],
                    saved_pokemon["type"],
                    saved_pokemon["hp"],
                    saved_pokemon["max_hp"],
                    saved_pokemon["attack"],
                    saved_pokemon["speed"],
                )
                trainer.add_pokemon(pokemon)
            print("Trenér byl načten ze souboru.")
            return trainer
        except FileNotFoundError:
            print("Soubor s trenérem nebyl nalezen.")
        except Exception as e:
            print(f"Error: {e}")
        return None
