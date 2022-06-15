

import os

import random



def calc_point_inside_circle(num_of_estimates):

    

    print(f"Executing calc_point_inside_circle with {num_of_estimates:,} on pid {os.getpid()}")



    trials_inside_circle = 0



    for step in range(int(num_of_estimates)):

        x = random.uniform(0,1)

        y = random.uniform(0,1)



        is_inside_circle = 1 if (x**2 + y**2) <= 1 else 0

        trials_inside_circle += is_inside_circle



    return trials_inside_circle





from multiprocessing import Pool # This is process based

# from multiprocessing import Pool # This is thread based

import time



if __name__ == "__main__":

    total_trials = 1e8

    num_workers = 4



    pool = Pool(processes=num_workers)

    trials_per_worker = total_trials/num_workers

    trials_per_processes = [trials_per_worker]*num_workers



    start_time = time.time()

    trials_inside_circle = pool.map(calc_point_inside_circle, trials_per_processes)

    pi_estimate = (sum(trials_inside_circle)*4)/float(total_trials)

    print(pi_estimate)

    print(f"Time consumed: {time.time()-start_time}")

