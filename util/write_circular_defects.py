import numpy as np

radius = 20
l_cube = 1000

basis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype = int)

def get_pos(translations):
    t = np.array(translations, dtype = int)
    return np.matmul(t, basis)

with open("defects_circular_cutout.txt", 'w') as f:
    center = get_pos([l_cube/2, l_cube/2, 0])

    for a in range(l_cube):
        for b in range(l_cube):
                d = np.linalg.norm( get_pos([a, b, 0]) - center)
                if d <= radius:
                    f.write("0 {0} {1} {2} -1\n".format(a, b, 0))

