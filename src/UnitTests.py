import unittest
import os
import json
from Arena import Arena 
from Pokemon import Pokemon,generate_pokemon
from Trainer import Trainer



class TestPokemon(unittest.TestCase):

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Pokemon(10, "Fire", 1, 1, 1, 1)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            Pokemon("Charmander", 1, 1, 1, 1, 1)

    def test_invalid_max_hp(self):
        with self.assertRaises(ValueError):
            Pokemon("Charmander", "Fire", 1, 0, 1, 1)

    def test_invalid_attack(self):
        with self.assertRaises(ValueError):
            Pokemon("Charmander", "Fire", 1, 1, 0, 1)

    def test_invalid_speed(self):
        with self.assertRaises(ValueError):
            Pokemon("Charmander", "Fire", 1, 1, 1, 0)

    def test_wrong_type(self):
        with self.assertRaises(ValueError):
            Pokemon("Charmander", "Fairy", 1, 1, 1, 1)

    def test_str(self):
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        self.assertEqual(pokemon.__str__(), '----------Pokémon----------\nJméno: Charmander\nTyp: Fire\nŽivoty: 1/1\nÚtok: 1\nRychlost: 1')

    def test_take_damage(self):
        pokemon = Pokemon("Charmander", "Fire", 20, 20, 1, 1)
        pokemon.take_damage(10)
        self.assertEqual(pokemon.hp, 10)
        pokemon.take_damage(10)
        self.assertEqual(pokemon.hp, 0)

    def test_is_alive(self):
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        self.assertTrue(pokemon.is_alive())
        
    def test_is_not_alive(self):
        pokemon = Pokemon("Charmander", "Fire", 0, 1, 1, 1)
        self.assertFalse(pokemon.is_alive())

    def test_fire_vs_grass(self):
        fire = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        grass = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        effectiveness = fire.effectiveness(grass.type)
        self.assertEqual(effectiveness, 2)  

    def test_water_vs_fire(self):
        water = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        fire = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        effectiveness = water.effectiveness(fire.type)
        self.assertEqual(effectiveness, 2)  

    def test_grass_vs_water(self):
        grass = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        water = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        effectiveness = grass.effectiveness(water.type)
        self.assertEqual(effectiveness, 2)

    def test_fire_vs_fire(self):
        fire1 = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        fire2 = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        effectiveness = fire1.effectiveness(fire2.type)
        self.assertEqual(effectiveness, 1)

    def test_water_vs_water(self):
        water1 = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        water2 = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        effectiveness = water1.effectiveness(water2.type)
        self.assertEqual(effectiveness, 1)

    def test_grass_vs_grass(self):
        grass1 = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        grass2 = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        effectiveness = grass1.effectiveness(grass2.type)
        self.assertEqual(effectiveness, 1)

    def test_fire_vs_water(self):
        fire = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        water = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        effectiveness = fire.effectiveness(water.type)
        self.assertEqual(effectiveness, 0.5)  

    def test_water_vs_grass(self):
        water = Pokemon("Squirtle", "Water", 1, 1, 1, 1)
        grass = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        effectiveness = water.effectiveness(grass.type)
        self.assertEqual(effectiveness, 0.5)

    def test_grass_vs_fire(self):
        grass = Pokemon("Bulbasaur", "Grass", 1, 1, 1, 1)
        fire = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        effectiveness = grass.effectiveness(fire.type)
        self.assertEqual(effectiveness, 0.5)

    def test_generate_pokemon(self):
        generated_pokemon = generate_pokemon(difficulty="medium")
        self.assertTrue(isinstance(generated_pokemon, Pokemon))
        self.assertTrue(generated_pokemon.hp > 0)
        self.assertTrue(generated_pokemon.max_hp > 0)
        self.assertTrue(generated_pokemon.attack > 0)
        self.assertTrue(generated_pokemon.speed > 0)
        self.assertIn(generated_pokemon.type, ["Fire", "Water", "Grass"])
        self.assertTrue(generated_pokemon.is_alive())

    def test_trainer(self):
        trainer = Trainer("Joe Pajdal")
        self.assertEqual(trainer.name, "Joe Pajdal")
        self.assertEqual(trainer.defeated_pokemons, 0)
        self.assertEqual(len(trainer.pokemon_team), 0)

    def test_invalid_trainer_name(self):
        with self.assertRaises(ValueError):
            Trainer(10)

    def test_add_pokemon(self):
        trainer = Trainer("Joe Pajdal")
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        trainer.add_pokemon(pokemon)
        self.assertEqual(len(trainer.pokemon_team), 1)

    def test_add_pokemon_max(self):
        trainer = Trainer("Joe Pajdal")
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        for i in range(6):
            trainer.add_pokemon(pokemon)
        self.assertEqual(len(trainer.pokemon_team), 6)
        trainer.add_pokemon(pokemon)
        self.assertEqual(len(trainer.pokemon_team), 6)

    def test_remove_pokemon(self):
        trainer = Trainer("Joe Pajdal")
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        trainer.add_pokemon(pokemon)
        self.assertEqual(len(trainer.pokemon_team), 1)
        trainer.remove_pokemon(0)
        self.assertEqual(len(trainer.pokemon_team), 0)

    def test_remove_wrong_index(self):
        trainer = Trainer("Joe Pajdal")
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        trainer.add_pokemon(pokemon)
        self.assertEqual(len(trainer.pokemon_team), 1)
        trainer.remove_pokemon(8)
        self.assertEqual(len(trainer.pokemon_team), 1)

    def test_save_trainer(self):
        trainer = Trainer("Joe Pajdal")
        pokemon = Pokemon("Charmander", "Fire", 1, 1, 1, 1)
        trainer.add_pokemon(pokemon)
        trainer.save_trainer()
        self.assertTrue(os.path.exists("saved_trainer.js"))
        with open("saved_trainer.js", "r") as f:
            saved_trainer = json.load(f)       
        self.assertEqual(saved_trainer["name"], "Joe Pajdal")
        self.assertEqual(saved_trainer["defeated_pokemons"], 0)
        self.assertEqual(len(saved_trainer["pokemon_team"]), 1)
        self.assertEqual(saved_trainer["pokemon_team"][0]["name"], "Charmander")

    def test_create_arena_invalid_pokemon_count(self):
        with self.assertRaises(ValueError):
            Arena(pokemon_count=-1, difficulty="easy")

    def test_create_arena_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            Arena(pokemon_count=3, difficulty="superhard")
    
if __name__ == "__main__":
    unittest.main()

