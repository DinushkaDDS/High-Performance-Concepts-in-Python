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

@profile
def calculate_juliaset_serial_expanded(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while True:
            not_yet_escaped = abs(z) < 2
            iterations_left = n < maxiter
            if not_yet_escaped and iterations_left:
                z = z * z + c
                n += 1
            else:
                break
        output[i] = n
    return output


def calc_juliaset_time(desired_width, max_iterations):
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
    
    print("Length of x:", len(x))
    print("Total elements:", len(zs))

    output = calculate_juliaset_serial_expanded(max_iterations, zs, cs)

    return output
    

if __name__== '__main__':
    x = calc_juliaset_time(1000, 300)

