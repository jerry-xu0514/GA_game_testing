import GA_character_testing
from collections import defaultdict

population = GA_character_testing.load_popluation("results/10_49_00_aug_23/best.json")

teams = defaultdict(int)
job_val = 1
ind_job_id = defaultdict(int)

for team in population:
    for job in team['Characters']:
        job_hash = GA_character_testing.generate_job_hashkey(job)
        if ind_job_id[job_hash] == 0:
            ind_job_id[job['JobId']] = job_val
            job_val += 1

for team in population:
    hashkey = GA_character_testing.generate_team_hashkey(team['Characters'], ind_job_id)
    if hashkey == '228228228228':
        print(team)
    teams[hashkey] += 1

for team in teams:
    if teams[team] >= 4: print(team, teams[team])

for team in population:
    hashkey = GA_character_testing.generate_team_hashkey(team['Characters'], ind_job_id)
    if hashkey == '228228228228':
        print(team)