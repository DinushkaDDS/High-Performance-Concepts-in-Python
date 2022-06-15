# first line: 17
@memory.cache

def calc_point_inside_circle_with_idx(num_of_estimates, idx):

    

    print(f"Executing calc_point_inside_circle with {num_of_estimates:,} and index {idx} on pid {os.getpid()}")



    trials_inside_circle = 0



    for step in range(int(num_of_estimates)):

        x = random.uniform(0,1)

        y = random.uniform(0,1)



        is_inside_circle = 1 if (x**2 + y**2) <= 1 else 0

        trials_inside_circle += is_inside_circle



    return trials_inside_circle
