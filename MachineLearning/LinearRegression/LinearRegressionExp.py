# %%
import numpy as np
import matplotlib.pyplot as plt   

# %%
class LinearRegression:
    def __init__(self,x,y,w):
        x = np.concatenate((np.ones((x.shape[0], 1, 1)), x), axis=1)
        print(x[0].shape)
        print(w.shape)
        self.input = x
        self.real = y
        print(self.real.shape)
        self.weight = w
        self.m = x.shape[0]
    def predict(self):
        self.pred = np.zeros(self.input.shape[0])
        for i in range(self.input.shape[0]):
            # self.predict[i] = x[i].T*w
            # print((x[i].T.dot(w)).shape)
            # self.pred[i] = np.expand_dims(self.input[i].T.dot(self.weight), axis=0)
            self.pred[i] = self.input[i].T.dot(self.weight)
    def loss_func(self):
        loss_arr = (self.pred-self.real)**2
        return np.sum(loss_arr)/self.m
    def gradient_decent(self, lr):
        self.predict()
        accumulated_weight = np.zeros(self.weight.shape, dtype=float)
        for i in range(self.input.shape[0]):
            accumulated_weight += ((self.pred[i] - self.real[i])*self.input[i])
        accumulated_weight /= self.input.shape[0]
        self.weight -= lr*accumulated_weight
            # self.weight -= lr* ((self.pred[i] - self.real[i])*self.input[i]) / self.m


# %%
m = 200
dim = 3
learning_rate = 1e-5
x = np.random.rand(m,dim) * 2
x = np.expand_dims(x, axis=2)
# y = x[:,0]*2 + x[:,1]*3 + x[:,2]*(-2) + np.random.randn(m) + 10
y = x[:,0]*2 + x[:,1]*3 + x[:,2]*(-2) + 10
y += np.random.randn(m,1)*0.1
y = np.reshape(y, m)
# print(y)
w = np.random.randn(dim+1,1)

model = LinearRegression(x,y,w)
for epoch in range(20000):
    model.gradient_decent(1e-1)
print(model.weight)
print(model.input[1])
model.predict()
error = model.pred-model.real
print(error.shape, error)
print(model.loss_func())