import GA_character_testing

response = [{"BattleId":7,"Result":0,"Milliseconds":47860,"Damage":3706668322},{"BattleId":5,"Result":0,"Milliseconds":63860,"Damage":5180549905},{"BattleId":2,"Result":0,"Milliseconds":72370,"Damage":5755266194},{"BattleId":4,"Result":0,"Milliseconds":74650,"Damage":6396612675},{"BattleId":6,"Result":0,"Milliseconds":70200,"Damage":7337596248},{"BattleId":9,"Result":0,"Milliseconds":44520,"Damage":3511765937},{"BattleId":3,"Result":0,"Milliseconds":75770,"Damage":5527369055},{"BattleId":0,"Result":0,"Milliseconds":85940,"Damage":5792862864},{"BattleId":1,"Result":0,"Milliseconds":73930,"Damage":4147769428},{"BattleId":8,"Result":0,"Milliseconds":74090,"Damage":6175754373}]
all_damages = [i['Damage'] for i in response]
print(max(all_damages))
fitness = GA_character_testing.fitness_func(battle_results=response, max_damage=max(all_damages))
print(fitness[:5])
print(response[6])