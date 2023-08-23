import GA_character_testing
from collections import defaultdict

population = GA_character_testing.load_popluation("results/10_49_00_aug_23/best.json")

teams = defaultdict(int)
job_val = 1
ind_job_id = defaultdict(int)

for team in population:
    for job in team['Characters']:
        hashkey = GA_character_testing.generate_job_hashkey(job)
        ind_job_id[hashkey] += 1

counter = 0
for key in ind_job_id:
    if ind_job_id[key] >= 2:
        print(key, ind_job_id[key])
        counter += 1

print(counter)

for team in population:
    for job in team['Characters']:
        if GA_character_testing.generate_job_hashkey(job) == '151324128312791942':
            print(job)