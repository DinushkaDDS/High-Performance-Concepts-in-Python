
import time
from numpy import roll, zeros, copyto, asarray, all
from numexpr import evaluate

def shift_sum_optimized(grid, shift_val, axis, next_grid):
    '''
    This is faster because this does the addition along with the numpy fast indexing operations.
    Therefore we dont need to do the addition operations separately.
    
    '''
    if(axis==0):
        next_grid[shift_val:,:] += grid[:-shift_val,:]
        next_grid[:shift_val,:] += grid[-shift_val:,:]
    elif(axis==1):
        next_grid[:,shift_val:] += grid[:,:-shift_val]
        next_grid[:,:shift_val] += grid[:,-shift_val:]

def test_shift_sum_optimized():
    rollee = asarray([[1, 2], [3, 4]])
    for shift in (+1, -1):
        for axis in (0, 1):
            out = asarray([[6, 3], [9, 2]])

            expected_result = roll(rollee, shift, axis=axis) + out
            shift_sum_optimized(rollee, shift, axis, out)

            assert all(expected_result == out)

def shift_vals(grid, next_grid):
    copyto(next_grid, grid)
    shift_sum_optimized(grid, +1, 0, next_grid)
    shift_sum_optimized(grid, -1, 0, next_grid)
    shift_sum_optimized(grid, +1, 1, next_grid)
    shift_sum_optimized(grid, -1, 1, next_grid)
    next_grid *= -4

@profile
def step(grid, next_grid, dt, D = 1.0):
    shift_vals(grid, next_grid)
    evaluate("next_grid * D * dt + grid", out=next_grid)


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
            
test_shift_sum_optimized()

if __name__== '__main__':
    run_experiment(150, (640,640))
