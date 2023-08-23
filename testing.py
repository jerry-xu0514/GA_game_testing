import GA_character_testing
import unittest

response = [{"BattleId":7,"Result":0,"Milliseconds":47860,"Damage":3706668322},{"BattleId":5,"Result":0,"Milliseconds":63860,"Damage":5180549905},{"BattleId":2,"Result":0,"Milliseconds":72370,"Damage":5755266194},{"BattleId":4,"Result":0,"Milliseconds":74650,"Damage":6396612675},{"BattleId":6,"Result":0,"Milliseconds":70200,"Damage":7337596248},{"BattleId":9,"Result":0,"Milliseconds":44520,"Damage":3511765937},{"BattleId":3,"Result":0,"Milliseconds":75770,"Damage":5527369055},{"BattleId":0,"Result":0,"Milliseconds":85940,"Damage":5792862864},{"BattleId":1,"Result":0,"Milliseconds":73930,"Damage":4147769428},{"BattleId":8,"Result":0,"Milliseconds":74090,"Damage":6175754373}]
all_damages = [i['Damage'] for i in response]

population_size = 10
number_to_store_per_gen = 2
mutation_percentage = 0.5
keep_percentage = 0.2
dead_percentage = 0.2
iterations = 2
CHARACTER_TITLE = 'Characters'


class TestMethods(unittest.TestCase):

    def test_test(self):
        self.assertEqual(max(all_damages), 7337596248)

    def test_fitness(self):
        fitness, population_fitness = GA_character_testing.fitness_func(battle_results=response, max_damage=max(all_damages))
        first = fitness[0][0]
        print(fitness)
        self.assertEqual(first, 6)
    
    def test_load(self):
        best_store = "results" + "/try2august17/" + "best.json"
        GA_character_testing.read_data('job-skill-separated.xlsx')
        population = GA_character_testing.load_popluation(best_store)
        self.assertEqual(len(population), 1000)
        
    def test_mutate(self):
        best_store = "results" + "/try2august17/" + "best.json"
        GA_character_testing.read_data('job-skill-separated.xlsx')
        population = GA_character_testing.load_popluation(best_store)
        for i in range(10):
            GA_character_testing.mutate_dup(population)
        print(population[:3])
    
    def test_mutate_dup(self):
        GA_character_testing.read_data("job-skill-separated.xlsx")
        population, id_to_idx = GA_character_testing.generate_first_population(1)
        # for i in range(14):


    # def test_generate_next_gen(self):
    #     GA_character_testing.read_data('job-skill.xlsx')
    #     fitness = GA_character_testing.fitness_func(battle_results=response, max_damage=max(all_damages))
    #     population = [{'BattleId': 0, 'Characters': [{'JobId': 25, 'Skills': [854, 918, 582, 138]}, {'JobId': 14, 'Skills': [1375, 1371, 1948, 1955]}, {'JobId': 15, 'Skills': [1297, 1304, 241, 1248]}, {'JobId': 16, 'Skills': [1241, 1637, 449, 1960]}]}, {'BattleId': 1, 'Characters': [{'JobId': 18, 'Skills': [1032, 1043, 1040, 1706]}, {'JobId': 15, 'Skills': [1938, 1564, 438, 1620]}, {'JobId': 14, 'Skills': [1376, 1364, 1340, 1666]}, {'JobId': 25, 'Skills': [866, 865, 394, 875]}]}, {'BattleId': 2, 'Characters': [{'JobId': 14, 'Skills': [444, 1327, 1358, 1361]}, {'JobId': 19, 'Skills': [134, 957, 131, 942]}, {'JobId': 26, 'Skills': [786, 809, 803, 1702]}, {'JobId': 16, 'Skills': [1641, 1637, 1231, 118]}]}, {'BattleId': 3, 'Characters': [{'JobId': 15, 'Skills': [1306, 1262, 1566, 1299]}, {'JobId': 25, 'Skills': [869, 898, 874, 895]}, {'JobId': 18, 'Skills': [1038, 1010, 1026, 1057]}, {'JobId': 17, 'Skills': [1110, 1139, 1576, 1091]}]}, {'BattleId': 4, 'Characters': [{'JobId': 26, 'Skills': [816, 834, 839, 824]}, {'JobId': 18, 'Skills': [1065, 1049, 1039, 2003]}, {'JobId': 15, 'Skills': [1262, 379, 1245, 1624]}, {'JobId': 19, 'Skills': [1982, 953, 939, 1434]}]}, {'BattleId': 5, 'Characters': [{'JobId': 26, 'Skills': [1991, 1996, 770, 576]}, {'JobId': 25, 'Skills': [922, 137, 890, 393]}, {'JobId': 17, 'Skills': [1680, 1129, 1686, 1094]}, {'JobId': 16, 'Skills': [253, 1211, 1634, 1200]}]}, {'BattleId': 6, 'Characters': [{'JobId': 16, 'Skills': [1175, 1239, 1244, 1630]}, {'JobId': 25, 'Skills': [585, 882, 904, 1598]}, {'JobId': 17, 'Skills': [1136, 1124, 1152, 1576]}, {'JobId': 14, 'Skills': [1365, 112, 1333, 445]}]}, {'BattleId': 7, 'Characters': [{'JobId': 19, 'Skills': [561, 134, 130, 970]}, {'JobId': 26, 'Skills': [1993, 1701, 822, 573]}, {'JobId': 15, 'Skills': [1291, 1258, 1250, 1265]}, {'JobId': 17, 'Skills': [385, 1123, 1096, 1092]}]}, {'BattleId': 8, 'Characters': [{'JobId': 18, 'Skills': [1022, 1051, 1035, 608]}, {'JobId': 26, 'Skills': [761, 834, 794, 828]}, {'JobId': 25, 'Skills': [589, 893, 909, 266]}, {'JobId': 16, 'Skills': [1961, 1962, 1185, 448]}]}, {'BattleId': 9, 'Characters': [{'JobId': 18, 'Skills': [1070, 399, 1712, 1416]}, {'JobId': 17, 'Skills': [1144, 1086, 1683, 122]}, {'JobId': 19, 'Skills': [1424, 1425, 1583, 963]}, {'JobId': 16, 'Skills': [1226, 1638, 1203, 1959]}]}]
    #     id_to_idx = GA_character_testing.generate_id_to_idx(population)
    #     population, id_to_idx = GA_character_testing.generate_new_population(population, fitness, keep_percentage, dead_percentage, mutation_percentage, population_size, id_to_idx)

    # def test_generate_first_gen_nodup(self):
    #     GA_character_testing.read_data('job-skill.xlsx')
    #     population, id_to_idx = GA_character_testing.generate_first_population(1000)
    #     for team in population:
    #         all_jobs = set()
    #         all_jobs_e = [jobs['JobId'] for jobs in team[CHARACTER_TITLE]]
    #         for jobs in team[CHARACTER_TITLE]:
    #             if(jobs['JobId'] in all_jobs): print(all_jobs_e)
    #             self.assertEqual(jobs['JobId'] not in all_jobs, True)
    #             all_jobs.add(jobs['JobId'])

    # def test_generate_next_gen_nodup(self):
    #     GA_character_testing.read_data('job-skill.xlsx')
    #     population, id_to_idx = GA_character_testing.generate_first_population(100)
    #     print(id_to_idx)
    #     response2, max_damage = GA_character_testing.test_population(population)
    #     fitness = GA_character_testing.fitness_func(response2, max_damage)
    #     for i in range(100):
    #         print(i)
    #         population, id_to_idx = GA_character_testing.generate_new_population(population, fitness, keep_percentage, dead_percentage, mutation_percentage, population_size, id_to_idx)
    #         for team in population:
    #             all_jobs = set()
    #             all_jobs_e = [jobs['JobId'] for jobs in team[CHARACTER_TITLE]]
    #             for jobs in team[CHARACTER_TITLE]:
    #                 if(jobs['JobId'] in all_jobs): print(all_jobs_e)
    #                 self.assertEqual(jobs['JobId'] not in all_jobs, True)
    #                 all_jobs.add(jobs['JobId'])





if __name__ == '__main__':
    unittest.main()