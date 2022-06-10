
import time
from numpy import roll, zeros


def shift_vals(grid):

    return (roll(grid, +1, 0) +  
            roll(grid, -1, 0) +
            roll(grid, +1, 1) +
            roll(grid, -1, 1) -
            4 * grid )


@profile
def step(grid, dt, D = 1.0):
    return grid + dt * D * shift_vals(grid)


def run_experiment(num_iterations, grid_shape):

    # Initial grid
    max_y, max_x = grid_shape

    grid = zeros((max_y, max_x))

    # Simulating a drop of dye in the middle of our simulated region
    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)

    grid[block_low:block_high, block_low:block_high] = 0.005

    # Running the experiment
    st = time.time()
    for _ in range(num_iterations):
        grid = step(grid, 0.1)

    return time.time() - st

if __name__== '__main__':
    run_experiment(150, (640,640))
