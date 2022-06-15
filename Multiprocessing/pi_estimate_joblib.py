
import os
import random
import time

def calc_point_inside_circle(num_of_estimates):
    
    print(f"Executing calc_point_inside_circle with {num_of_estimates:,} on pid {os.getpid()}")

    trials_inside_circle = 0

    for step in range(int(num_of_estimates)):
        x = random.uniform(0,1)
        y = random.uniform(0,1)

        is_inside_circle = 1 if (x**2 + y**2) <= 1 else 0
        trials_inside_circle += is_inside_circle

    return trials_inside_circle

from joblib import Parallel, delayed
if __name__ == "__main__":

    total_trials = 1e8
    num_workers = 4

    trials_per_worker = total_trials/num_workers
    trials_per_processes = [trials_per_worker]*num_workers


    parrallel_obj = Parallel(n_jobs=num_workers, verbose=1)
    async_function = delayed(calc_point_inside_circle)

    start_time = time.time()
    trials_inside_circle =  parrallel_obj(async_function(trials_per_worker) for _ in range(num_workers))
    pi_estimate = (sum(trials_inside_circle)*4)/float(total_trials)

    print(pi_estimate)
    print(f"Time consumed: {time.time()-start_time}")
