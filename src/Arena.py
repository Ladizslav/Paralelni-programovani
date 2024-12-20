from Pokemon import generate_pokemon

class Arena:
    def __init__(self, pokemon_count, difficulty):
        try:
            if not isinstance(pokemon_count, int) or pokemon_count <= 0:
                raise ValueError("Počet Pokémonů musí být kladné celé číslo.")
            if difficulty not in ["easy", "medium", "hard"]:
                raise ValueError("Obtížnost musí být 'easy', 'medium' nebo 'hard'.")

            self.pokemon_count = pokemon_count
            self.difficulty = difficulty
            self.completed_battles = 0
        except ValueError as e:
            print(f"Error: {e}")
            raise

    def __str__(self):
        return f"----------Aréna----------\nPočet Pokémonů: {self.pokemon_count}\nObtížnost: {self.difficulty}\nDokončené souboje: {self.completed_battles}"

    def generate_arena_pokemon(self):
        """Vygenerování Pokémonů podle obtížnosti"""
        try:
            if self.difficulty == "easy":
                return [generate_pokemon("easy") for _ in range(self.pokemon_count)]
            elif self.difficulty == "medium":
                return [generate_pokemon("medium") for _ in range(self.pokemon_count)]
            elif self.difficulty == "hard":
                return [generate_pokemon("hard") for _ in range(self.pokemon_count)]
            else:
                raise ValueError("Neplatná obtížnost.")
        except ValueError as e:
            print(f"Error: {e}")
            raise

    async def battle_in_arena(self, trainer):
        """Simulace pro boj v aréně"""
        try:
            if len(trainer.pokemon_team) == 0:
                print("Trenér nemá žádné pokémony, nemůže vstoupit do arény.")
                return
            print(f"\nVstupujete do arény. Obtížnost: {self.difficulty}\n")
            arena_pokemons = self.generate_arena_pokemon() 
            for opponent in arena_pokemons:
                print("Nepřítel:")
                print(opponent)
                print("Vyberte pokémona pro souboj:")
                for i in range(len(trainer.pokemon_team)):
                    pokemon = trainer.pokemon_team[i]
                    print(f"{i + 1}. {pokemon.name} ({pokemon.hp}/{pokemon.max_hp} životů)")

                valid_choice = False
                player_pokemon = None
                while not valid_choice:
                    try:
                        choice = input(f"Zadejte číslo (1 - {len(trainer.pokemon_team)}): ").strip()
                        choice = int(choice) - 1  
                        if 0 <= choice < len(trainer.pokemon_team):
                            player_pokemon = trainer.pokemon_team[choice]
                            valid_choice = True
                        else:
                            print(f"Neplatná volba, zadejte číslo mezi 1 a {len(trainer.pokemon_team)}")
                    except ValueError:
                        print("Zadejte platné číslo.")
                if player_pokemon is None:
                    print("Nezvolil jsi si pokémona, souboj skončil.")
                    return
                winner = await trainer.simple_battle(player_pokemon, opponent)
                if winner == "player":
                    print(f"Trenér {trainer.name} vyhrál souboj proti {opponent.name}!")
                    trainer.defeated_pokemons += 1
                elif winner == "opponent":
                    print(f"Pokémon {opponent.name} vyhrál souboj!")
                    return
                else:
                    print("Souboj skončil remízou.")
            self.completed_battles += 1
            print(f"\nTrenér {trainer.name} dokončil arénu a porazil všechny Pokémony!")
            trainer.completed_arenas += 1

        except Exception as e:
            print(f"Chyba při souboji v aréně: {e}")
            raise
