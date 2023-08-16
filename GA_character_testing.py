import numpy as np
import pandas as pd
import sys
import time
import simulations
import json

BATTLEID_TITLE = 'BattleId'
JOBID_TITLE = 'JobId'
SKILL_TITLE = 'Skills'
CHARACTER_TITLE = 'Characters'

RETURN_TIME = 'Milliseconds'
RETURN_RESULT = 'Result'
RETURN_DAMAGE = 'Damage'

battle_id = 0
population_warning = True
job_to_skills = {}

# TODO: skill mutation

"""
read data from excel
returns a dictionary of job_id to list of skill_ids
"""
def read_data(file_path):
    global battle_id
    global job_to_skills
    print(f"reading data from {file_path}...")
    xls = pd.ExcelFile(file_path)
    jobs = pd.read_excel(xls, 'job')
    skills = pd.read_excel(xls, 'skill')

    # just take the first 7
    for i in range(8):
        job_id = jobs.loc[:7, 'job_id'][i]
        skills_id = []
        job_to_skills[job_id] = skills_id

    # for skill in skills.loc:
    for index, row in skills.iterrows():
        skill_id = row['id']
        job_id = row['job_id']
        assert job_id in job_to_skills, f"job_id {job_id} not in job_to_skills"
        job_to_skills[job_id].append(skill_id)

"""
generates a random population of size n
sample template: '[{"BattleId":1,"Characters":[{"JobId":14,"Skills":[109,110,111,112]},{"JobId":15,"Skills":[104,103,106,107]},{"JobId":16,"Skills":[446,448,449,447]},{"JobId":17,"Skills":[1116,1119,1117,1118]}]}]'
"""
def generate_first_population(population_size):
    sys.stdout.write("generating first population...\n")
    global battle_id
    global job_to_skills
    population = []
    for i in range(population_size):
        population.append(generate_character())
    return population, generate_id_to_idx(population)

"""
generates a random character
sample template: {"BattleId":1,"Characters":[{"JobId":14,"Skills":[109,110,111,112]},{"JobId":15,"Skills":[104,103,106,107]},{"JobId":16,"Skills":[446,448,449,447]},{"JobId":17,"Skills":[1116,1119,1117,1118]}]}
"""
def generate_character():
    global battle_id
    global job_to_skills
    character = {}
    character[BATTLEID_TITLE] = battle_id
    battle_id += 1
    character[CHARACTER_TITLE] = []
    job_ids = np.random.choice(list(job_to_skills.keys()), 4, replace=False)
    for job_id in job_ids:
        job = {}
        job[JOBID_TITLE] = job_id
        job[SKILL_TITLE] = np.random.choice(job_to_skills[job_id], 4, replace=False).tolist()
        character[CHARACTER_TITLE].append(job)
    return character

"""
the function that converts population into json and tests
returns json file
sample template: [{"BattleId":1,"Result":1,"Milliseconds":158000,"Damage":1111111111}]
"""
def test_population(population):
    sys.stdout.write("running simulations...\n")
    url = 'http://10.41.0.159:8080/simulator'
    results = simulations.get_results(population, url)
    all_damages = [i['Damage'] for i in results]
    return results, max(all_damages)

"""
sorts the population by fitness
returns sorted population by fitness value
return template [(battle_id, fitness_value)]
"""
def fitness_func(battle_results, max_damage): 
    fitness = []
    for i, e in enumerate(battle_results):
        fitness_value = 2 + 1 / int(e[RETURN_TIME]/1000) if e[RETURN_RESULT] else e[RETURN_DAMAGE]/ max_damage
        fitness.append((battle_results[i][BATTLEID_TITLE], fitness_value))
    fitness.sort(key=lambda x: x[1], reverse=True)
    return fitness

"""
given a sorted population, generate a new population
returns a new population
@params:
    population: previous generation population
    fitness: sorted fitness of previous generation population
    keep_population: number of population to keep
    crossover_population: number of population to crossover
    mutation_percentage: percentage of population to mutate
    crossover_percentage: percentage of population to crossover as the total population
"""
def generate_new_population(prev_population, fitness, keep_percentage, dead_percentage, mutation_percentage, population_size, id_to_idx):
    sys.stdout.write("genearting new population... \n")
    global battle_id
    global job_to_skills
    if(keep_percentage != dead_percentage and population_warning):
        sys.stderr.write(f'[WARNING]: {keep_percentage} DOES NOT EQUAL TO {dead_percentage}, WILL CAUSE POPULATION SIZE TO VARY')
        population_warning = False

    new_population = []
    for i in range(int(keep_percentage * population_size)):
        idx = id_to_idx[fitness[i][0]]
        new_character = prev_population[idx]
        new_character[BATTLEID_TITLE] = battle_id
        battle_id += 1
        new_population.append(new_character)
    one_point_crossover(new_population, prev_population, fitness, dead_percentage, population_size, id_to_idx)
    # mutation(new_population, mutation_percentage)
    check_dup(new_population)
    return new_population, generate_id_to_idx(new_population)

"""
generates a portion of the new population by one point crossover
returns a list of new characters
@params:
    prev_population: previous generation population 
    fitness: sorted fitness of previous generation population
    keep_population: number of population to keep
    dead_population: number of population to kill
    population_size: total population size
"""     
def one_point_crossover(new_population, prev_population, fitness, dead_percentage, population_size, id_to_idx, cross_neighbor=True):
    global battle_id
    global job_to_skills
    assert dead_percentage < 1 and dead_percentage > 0, f'you have to take out at least some of the bad genes man... but you can\'t take out more than the entire population'
    
    # loop through all but the last dead population, onepoint crossover with the next one, then append the new character to the list
    for i in range(int(population_size * (1-dead_percentage))):
        new_character = {}
        new_character[BATTLEID_TITLE] = battle_id
        battle_id += 1
        # take previous population index i, and randomly choose one_point_crossover with i+1, majority inherited from parent1 
        idx = id_to_idx[fitness[i][0]]
        if cross_neighbor:
            parent1, parent2 = prev_population[idx], prev_population[id_to_idx[fitness[i+1][0]]]
        else:
            parent1, parent2 = prev_population[idx], prev_population[np.random.randint(0,population_size)]

        all_parent1_jobs = [jobs[JOBID_TITLE] for jobs in parent1[CHARACTER_TITLE]]

        crossover_trait = np.random.randint(0,4)
        crossover_job = parent2[CHARACTER_TITLE][crossover_trait][JOBID_TITLE]
        new_character_jobs = []
        if crossover_job not in all_parent1_jobs:
            for i in range(4):
                new_character_jobs.append(parent1[CHARACTER_TITLE][i] if i != crossover_trait else parent2[CHARACTER_TITLE][i])
        else:
            for i, e in enumerate(all_parent1_jobs):
                if e == crossover_job:
                    to_switch = i
            for i in range(4):
                new_character_jobs.append(parent1[CHARACTER_TITLE][i] if i != to_switch else parent2[CHARACTER_TITLE][crossover_trait])
        new_character[CHARACTER_TITLE] = new_character_jobs
        new_population.append(new_character)

def generate_id_to_idx(population):
    new_id_to_idx = {}
    for i, battle in enumerate(population):
        new_id_to_idx[battle[BATTLEID_TITLE]] = i
    return new_id_to_idx

"""
take the top n groups and store them
"""
def store_population(filename, population_to_store, fitness, prev_population, generation, id_to_idx, max_damage, results):
    victories = sum(i[RETURN_RESULT] for i in results)
    sys.stdout.write(f"storing population for geneartion: {generation}\n")
    sys.stdout.write(f'Win\'s this generation: {victories}\n')
    results_itoi = generate_id_to_idx(results)
    assert len(prev_population) >= population_to_store, f'the population you wish to store: {population_to_store} is greater than the total population size: {len(prev_population)}'
    with open(filename, 'a') as f:
        f.write(f"Generation: {generation}\n")
        f.write(f"this generation's max damage is {max_damage}\n")
        for i in range(population_to_store):
            ridx = results_itoi[fitness[i][0]]
            idx = id_to_idx[fitness[i][0]]
            f.write("\t" + str(population[idx]))
            f.write("\n")
            f.write("\tbattleID and fitness level:" + str(fitness[i]))
            f.write("\n")
            f.write("\t" + str(results[ridx]) + "\n")
        f.write('\n')


def store_entire(filename, population):
    simulations.store(filename, population)

"""
Randomly changes certain jobs in a team with a new job that is not in the exisiting party
"""
def mutation(new_population, mutation_percentage):
    assert mutation_percentage < 1 and mutation_percentage >= 0, f'{mutation_percentage} must be a percent value greater than or equal to 0 and less than 1'
    to_mutate = np.random.choice(len(new_population), int(mutation_percentage * len(new_population)))
    for idx in to_mutate:
        character = new_population[idx][CHARACTER_TITLE]
        existing_jobs = [job[JOBID_TITLE] for job in character]
        while True:
            job_id = np.random.choice(list(job_to_skills.keys()), 1, replace=False)
            if job_id not in existing_jobs: break
        job_id = job_id[0]
        job = {}
        job[JOBID_TITLE] = job_id
        job[SKILL_TITLE] = np.random.choice(job_to_skills[job_id], 4, replace=False).tolist()
        character[np.random.randint(0,4)] = job

def check_dup(population):
    for team in population:
        all_jobs = set()
        all_jobs_e = [jobs['JobId'] for jobs in team[CHARACTER_TITLE]]
        for jobs in team[CHARACTER_TITLE]:
            if(jobs['JobId'] in all_jobs): print(all_jobs_e)
            assert jobs['JobId'] not in all_jobs, f'duplates found {all_jobs_e}'
            all_jobs.add(jobs['JobId'])

if __name__ == '__main__':
    # parameters:
    population_size = 10
    number_to_store_per_gen = 5
    mutation_percentage = 0.1
    keep_percentage = 0.2
    dead_percentage = 0.2
    iterations = 2
    storage_txt = "results/test.txt"
    job_skill_file = "job-skill.xlsx"
    population_store = "results/test.json"

    read_data(job_skill_file)
    population, id_to_idx = generate_first_population(population_size)

    for i in range(iterations):
        start = time.time()
        results, max_damage = test_population(population)
        fitness = fitness_func(battle_results=results, max_damage=max_damage)
        store_population(storage_txt, number_to_store_per_gen, fitness, population, i, id_to_idx, max_damage, results)
        population, id_to_idx = generate_new_population(population, fitness, keep_percentage, dead_percentage, mutation_percentage, population_size, id_to_idx)
        end = time.time()
        sys.stdout.write(f"generation {i} took {end - start} seconds\n")

        mutation_percentage = max(mutation_percentage * 0.95, 0.05)

    
    store_entire(population_store, population)