import numpy as np
l_sheet = 10
h_sheet = 10

basis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype = int)

def get_pos(translations):
    t = np.array(translations, dtype = int)
    return np.matmul(t, basis)

with open("defects_sheet.txt", 'w') as f:
    for a in range(l_sheet):
        for b in range(l_sheet):
            for c in range(1, h_sheet):
                f.write("0 {0} {1} {2} -1\n".format(a, b, c))
