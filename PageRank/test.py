import numpy as np
import scipy.sparse
from pygraph.classes.digraph import digraph

IOS = np.array([    [0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                    [0, 1, 1, 1, 0]], dtype=float)
sparsed_mat = scipy.sparse.csr_matrix(IOS)
print(sparsed_mat)