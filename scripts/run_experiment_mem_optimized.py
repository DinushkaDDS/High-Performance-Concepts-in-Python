
import time
from numpy import roll, zeros, copyto


def shift_vals(grid, next_grid):
    copyto(next_grid, grid)
    next_grid +=  roll(grid, +1, 0)
    next_grid +=  roll(grid, -1, 0)
    next_grid +=  roll(grid, +1, 1)
    next_grid +=  roll(grid, -1, 1)
    next_grid *= -4

@profile
def step(grid, next_grid, dt, D = 1.0):
    shift_vals(grid, next_grid)
    next_grid *= dt * D
    grid += next_grid


def run_experiment(num_iterations, grid_shape):

    # Initial grid
    max_y, max_x = grid_shape
    grid = zeros((max_y, max_x))
    next_grid = zeros((max_y, max_x))

    # Simulating a drop of dye in the middle of our simulated region
    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)

    grid[block_low:block_high, block_low:block_high] = 0.005

    # Running the experiment
    st = time.time()
    for _ in range(num_iterations):
        step(grid, next_grid, 0.1)
        grid, next_grid = next_grid, grid # Inplace variable swap

    return time.time() - st

if __name__== '__main__':
    run_experiment(150, (640,640))
