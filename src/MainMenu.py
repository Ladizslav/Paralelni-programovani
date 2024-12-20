import asyncio
from Trainer import Trainer
from Pokemon import generate_pokemon
from Arena import Arena

def main_menu():
    print("Vítejte v Pokémon hře!")
    while True:
        print("\n1. Vytvořit nového trenéra")
        print("2. Načíst existujícího trenéra")
        print("3. Konec")       
        choice = input("Vyberte možnost: ").strip()
        try:
            if choice == "1":
                name = input("Zadejte jméno nového trenéra: ").strip()
                if not name:
                    print("Jméno trenéra nemůže být prázdné.")
                    continue
                trainer = Trainer(name)
                print(f"Trenér {trainer.name} byl vytvořen!")
                trainer_actions(trainer)
            elif choice == "2":
                try:
                    trainer = Trainer.load_trainer()
                    print(f"Trenér {trainer.name} byl úspěšně načten!")
                    trainer_actions(trainer)
                except FileNotFoundError:
                    print("Soubor s trenérem nebyl nalezen.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == "3":
                print("Konec hry.")
                break
            else:
                print("Neplatná volba, zkuste to znovu.")
        except FileNotFoundError:
            print(".")
        except Exception as e:
            print(f"Error: {e}")

def trainer_actions(trainer):
    while True:
        print(f"\nNyní ovládáte trenéra {trainer.name}.")
        print("1. Zobrazit informace o trenérovi")
        print("2. Přidat Pokémona do týmu")
        print("3. Odebrat Pokémona z týmu")
        print("4. Trénovat Pokémona")
        print("5. Zobrazit informace o Pokémonovi")
        print("6. Uzdravit Pokémony.")
        print("7. Zahájit souboj")
        print("8. Vstoupit do arény")
        print("9. Uložit trenéra")
        print("10. Vrátit se do hlavního menu")
        choice = input("Vyberte možnost: ").strip()
        try:
            if choice == "1":
                print(trainer)        
            elif choice == "2":
                pokemon = generate_pokemon()
                trainer.add_pokemon(pokemon)
            elif choice == "3":
                if trainer.pokemon_team:
                    print("Vyberte Pokémona k trénování:")
                    for i in range(len(trainer.pokemon_team)):
                        print(f"{i + 1}. {trainer.pokemon_team[i].name}")
                    index = int(input("Zadejte číslo Pokémona: ")) - 1    
                    trainer.remove_pokemon(index)
                else:
                    print("Nemáte žádné Pokémony v týmu.")
            elif choice == "4":
                if trainer.pokemon_team:
                    print("Vyberte Pokémona k trénování:")
                    for i in range(len(trainer.pokemon_team)):
                        print(f"{i + 1}. {trainer.pokemon_team[i].name}")
                    index = int(input("Zadejte číslo Pokémona: ")) - 1
                    if 0 <= index < len(trainer.pokemon_team):
                        asyncio.run(trainer.pokemon_team[index].train())  
                    else:
                        print("Neplatný výběr.")
                else:
                    print("Nemáte žádné Pokémony v týmu.")
            elif choice == "5":
                if trainer.pokemon_team:
                    print("Vyberte Pokémona, o kterém chcete zobrazit informace:")
                    for i in range(len(trainer.pokemon_team)):
                        print(f"{i + 1}. {trainer.pokemon_team[i].name}")
                    index = int(input("Zadejte číslo Pokémona: ")) - 1
                    if 0 <= index < len(trainer.pokemon_team):
                        print(trainer.pokemon_team[index])
                    else:
                        print("Neplatný výběr.")
                else:
                    print("Nemáte žádné Pokémony v týmu.")
            elif choice == "6":
                asyncio.run(trainer.heal_pokemons()) 
            elif choice == "7":
                if trainer.pokemon_team:
                    asyncio.run(trainer.start_battle())
                else:
                    print("Nemáte žádné Pokémony v týmu.")
            elif choice == "8":
                try:
                    pokemon_count = int(input("Zadejte počet Pokémonů v aréně: ").strip())
                    if pokemon_count < 1:
                        print("Počet Pokémonů musí být alespoň 1.")
                    else:
                        print("\nVyberte obtížnost arény:")
                        print("1. Easy")
                        print("2. Medium")
                        print("3. Hard")
                        valid_choice = False
                        while not valid_choice:
                            try:
                                choice = int(input("Zadejte číslo (1 - 3): ").strip())
                                if choice == 1:
                                    difficulty = "easy"
                                    valid_choice = True
                                elif choice == 2:
                                    difficulty = "medium"
                                    valid_choice = True
                                elif choice == 3:
                                    difficulty = "hard"
                                    valid_choice = True
                                else:
                                    print("Neplatná volba, zadejte číslo mezi 1 a 3.")
                            except ValueError:
                                print("Zadejte platné číslo.")
                        arena = Arena(pokemon_count, difficulty)
                        asyncio.run(arena.battle_in_arena(trainer))
    
                except ValueError:
                    print("Počet Pokémonů musí být číslo.")


            elif choice == "9":
                trainer.save_trainer()
                print(f"Trenér {trainer.name} byl uložen.")
            elif choice == "10":
                break
            else:
                print("Neplatná volba, zkuste to znovu.")
        except ValueError:
            print("Zadejte prosím platnou volbu.")
        except Exception as e:
            print(f"Error: {e}")

