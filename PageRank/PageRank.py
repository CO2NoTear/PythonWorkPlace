from audioop import reverse
import numpy as np
from scipy import sparse

#常数alpha
ALPHA = 0.85

f = open('web-Google.txt','r')
# 读取节点数和边数
rawinputstr = f.readline().split(' ')
# 这个n好像没什么用
n = int(rawinputstr[0])
m = int(rawinputstr[1])
row = []
col = []
maxnode = 0
for x in range(0,m):
    # 读入边 u --> v
    rawinputstr = f.readline().split('\t')
    u = int(rawinputstr[0])
    v = int(rawinputstr[1])
    # # 储存最大节点编号
    # maxnode = max(maxnode, u+1)
    # maxnode = max(maxnode, v+1)
    # 行列储存到row[] 和 col[]
    # 从u到v的一条链接，在S矩阵中表示为第v行第u列有值1/n_u
    col.append(u)
    row.append(v)
data = np.ones(m)
print('完成读入')

# 建立稀疏矩阵coo_mat，表示出链情况
coo_mat = sparse.coo_matrix((data,(row,col)),dtype=float)
# 转换为csc_mat，便于后续处理
csc_mat = coo_mat.tocsc()
# 最大点编号:维度
N = csc_mat.shape[0]
s_row = []
s_data = []
for i in range(0,N):
    # 造一个初等矩阵的积E_s，使得csc_mat dot E_s == S,
    # 每列都乘1/n_u
    s_row.append(i)
    # 利用csc_mat的累加数组，很方便地得到第i列的出链数
    n_u = csc_mat.indptr[i+1]-csc_mat.indptr[i]
    # 特殊情况，孤立点，E_s不做改变
    if n_u == 0:
        n_u = 1
    s_data.append(1/n_u)
E_s = sparse.csc_matrix((s_data,(s_row,s_row)),dtype=float)
print(E_s)

# 得到S矩阵
S = sparse.csc_matrix(csc_mat.dot(E_s))
# 得到一维全1向量e
e = np.ones(shape=(N,1),dtype=float)
# 然而无法得到全1 N*N矩阵（太大），故使用迭代法 PR_n+1 = ((1-ALPHA)/N)*e + ALPHA*np.dot(S,PR_n)
maxiter = 24
# 初始化PR
Pr = np.full(shape=(N,1),fill_value=1/N)
for iter in range(0,maxiter):
    Pr = ((1-ALPHA)/N)*e + ALPHA*sparse.csc_matrix.dot(S,Pr)
    # print('第{0}次迭代，Pr='.format(iter+1)) 
    # print(Pr)
# 排序
print('前10名网站以及PR的值：')
index_sorted_Pr = np.argsort(Pr,axis=None)
index_sorted_Pr = index_sorted_Pr[-1::-1]
for x in range (0,min(10,N)):
    print('Pr[{0}] = {1}'.format(index_sorted_Pr[x],float(Pr[index_sorted_Pr[x]])))

