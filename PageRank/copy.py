import numpy as np
class CPageRank(object):
    '''实现PageRank Alogrithm
    '''
    def __init__(self):
        self.PR = []  # PageRank值
    def GetPR(self, IOS, alpha, max_itrs, min_delta):
        '''幂迭代⽅法求PR值
        :param IOS       表⽰⽹页出链⼊链关系的矩阵,是⼀个左出链矩阵
        :param alpha     阻尼系数α，⼀般alpha取值0.85
        :param max_itrs  最⼤迭代次数
        :param min_delta 停⽌迭代的阈值
        '''
        # IOS左出链矩阵, a阻尼系数alpha, N⽹页总数
        N = np.shape(IOS)[0]
        # 所有分量都为1的列向量
        e = np.ones(shape=(N, 1))
        # 计算⽹页出链个数统计
        L = [np.count_nonzero(e) for e in IOS.T]
        # 计算⽹页PR贡献矩阵helpS，是⼀个左贡献矩阵
        helps_efunc = lambda ios, l: ios / l
        helps_func = np.frompyfunc(helps_efunc, 2, 1)
        helpS = helps_func(IOS, L)
        # P[n+1] = AP[n]中的矩阵A
        A = alpha * helpS + ((1 - alpha) / N) * np.dot(e, e.T)
        print('左出链矩阵:\n', IOS)
        print('左PR值贡献概率矩阵:\n', helpS)
        # 幂迭代法求PR值
        for i in range(max_itrs):
            if 0 == np.shape(self.PR)[0]:  # 使⽤1.0/N初始化PR值表
                self.PR = np.full(shape=(N, 1), fill_value=1.0 / N)
                print('初始化的PR值表:', self.PR)
            # 使⽤PR[n+1] = APR[n]递推公式，求PR[n+1]
            old_PR = self.PR
            self.PR = np.dot(A, self.PR)
            # 如果所有⽹页PR值的前后误差都⼩于⾃定义的误差阈值，则停⽌迭代
            D = np.array([old - new for old, new in zip(old_PR, self.PR)])
            ret = [e < min_delta for e in D]
            print('迭代次数:%d, succeed PR:\n' % (i + 1), self.PR)
            if ret.count(True) == N:
                print('迭代次数:%d, succeed PR:\n' % (i + 1), self.PR)
                break
        return self.PR
def CPageRank_manual():
    # 表⽰⽹页之间的出⼊链的关系矩阵，是⼀个左关系矩阵，可以理解成右⼊链矩阵
    # IOS[i, j]表⽰⽹页j对⽹页i有出链
    IOS = np.array([[0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                    [0, 1, 1, 1, 0]], dtype=float)
    pg = CPageRank()
    ret = pg.GetPR(IOS, alpha=0.85, max_itrs=100, min_delta=0.0001)
    print('最终的PR值:\n', ret)
if __name__ == '__main__':
    CPageRank_manual()