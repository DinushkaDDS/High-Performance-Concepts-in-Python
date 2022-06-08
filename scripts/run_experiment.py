
import time

@profile
def step(grid, dt, D = 1.0):

    max_y, max_x = len(grid), len(grid[0])

    grid_next = [[0.0]*max_x]*max_y

    for i in range(max_y):
        for j in range(max_x):
            
            y_dir_gradient2 = (grid[(i + 1) % max_y][j] + grid[(i - 1) % \
                                                    max_y][j] - 2 * grid[i][j]) 
            x_dir_gradient2 = (grid[i][(j + 1) % max_x] + grid[i][(j - 1) % \
                                                     max_x] - 2 * grid[i][j])

            grid_next[i][j] = grid[i][j] + D * dt * (x_dir_gradient2 + y_dir_gradient2)

    return grid_next

def run_experiment(num_iterations, grid_shape):

    # Initial grid
    max_y, max_x = grid_shape

    grid = [[0.0]*max_x]*max_y

    # Simulating a drop of dye in the middle of our simulated region
    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)

    for i in range(block_low, block_high):
        for j in range(block_low, block_high):
            grid[i][j] = 0.005

    # Running the experiment
    st = time.time()
    for _ in range(num_iterations):
        grid = step(grid, 0.1)

    return time.time() - st

if __name__== '__main__':
    run_experiment(150, (640, 640))
