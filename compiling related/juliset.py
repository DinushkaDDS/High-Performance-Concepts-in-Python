import cythonfn
import time

# area of imaginary space to calculate pixel values
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_img = -0.62772, -.42193



def calculate_juliaset_serial(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


def calc_juliaset_time_cython(desired_width, max_iterations):
    """Create a list of complex coordinates (zs) and complex parameters (cs), to build Julia set"""

    x_step = (x2 - x1) / desired_width
    y_step = (y1 - y2) / desired_width

    x = []
    y = []

    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_img))
    
    st = time.time()
    output = cythonfn.calculate_juliaset_serial(max_iterations, zs, cs)
    et = time.time()
    print(f'Cython compiled code ran for {et-st:0.2f} seconds.')

    return output
    

def calc_juliaset_time_regular(desired_width, max_iterations):
    """Create a list of complex coordinates (zs) and complex parameters (cs), to build Julia set"""

    x_step = (x2 - x1) / desired_width
    y_step = (y1 - y2) / desired_width

    x = []
    y = []

    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_img))
    
    st = time.time()
    output = calculate_juliaset_serial(max_iterations, zs, cs)
    et = time.time()
    print(f'Regular python code ran for {et-st:0.2f} seconds.')

    return output

if __name__== '__main__':
    x = calc_juliaset_time_cython(1000, 300)
    y = calc_juliaset_time_regular(1000, 300)

