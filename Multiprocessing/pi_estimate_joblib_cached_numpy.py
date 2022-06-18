
import os
import random
import time
from joblib import Parallel, delayed
from joblib import Memory
import numpy as np

memory = Memory("./Multiprocessing/joblib_cache", verbose=0)

@memory.cache
def calc_point_inside_circle_with_numpy(num_of_estimates, idx):
    
    print(f"Executing calc_point_inside_circle with {num_of_estimates:,} and index {idx} on pid {os.getpid()}")
    import numpy as np
    np.random.seed()

    xs = np.random.uniform(0, 1, num_of_estimates)
    ys = np.random.uniform(0, 1, num_of_estimates)

    sqr_zs = (xs*xs + ys*ys) <= 1 # returns a boolean array with condition checked

    trials_inside_circle = np.sum(sqr_zs)
    return trials_inside_circle

if __name__ == "__main__":

    total_trials = 1e8
    num_workers = 4

    trials_per_worker = int(total_trials/num_workers)
    trials_per_processes = [trials_per_worker]*num_workers


    parrallel_obj = Parallel(n_jobs=num_workers, verbose=1)
    async_function = delayed(calc_point_inside_circle_with_numpy)

    start_time = time.time()
    trials_inside_circle =  parrallel_obj(async_function(trials_per_worker, i) for i in range(num_workers))
    pi_estimate = (np.sum(trials_inside_circle)*4)/float(total_trials)

    print(pi_estimate)
    print(f"Time consumed: {time.time()-start_time}")
