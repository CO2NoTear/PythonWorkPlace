# %%
import numpy as np
import pandas as pd 
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader, TensorDataset

# %%
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'
print(device)

# %%
train_data = pd.read_csv("./abalone_test.data", names=['label','Length','Diameter','Height','WholeWeight', 'ShuckedWeight', 'VisceraWeight', 'ShellWight', 'Rings'])
test_data = pd.read_csv("./abalone_test.data", names=['label','Length','Diameter','Height','WholeWeight', 'ShuckedWeight', 'VisceraWeight', 'ShellWight', 'Rings'])

# `sort = True` to make sure the consistance of train/test data
train_data['label'], unique_seq = pd.factorize(train_data.label, sort=True)
test_data['label'], unique_seq = pd.factorize(test_data.label, sort=True)

classes_num = unique_seq.shape[0]
print(train_data)
print(test_data)
print(classes_num)

# %%
train_data = np.asarray(train_data)
test_data = np.asarray(test_data)

train_x = train_data[:,1:]
print(train_x)
train_y = train_data[:,0]

test_x = test_data[:,1:]
# print(test_x)
test_y = test_data[:,0]

print(train_y[:10])
print(test_y[:10])

# train_x = torch.tensor(train_x, dtype=torch.float).to(device) 
# train_y = torch.tensor(train_y, dtype=torch.long).to(device)
# test_x = torch.tensor(test_x, dtype=torch.float).to(device)
# test_y = torch.tensor(test_y, dtype=torch.long).to(device)

train_x = torch.tensor(train_x, dtype=torch.float)
train_y = torch.tensor(train_y, dtype=torch.long)
test_x = torch.tensor(test_x, dtype=torch.float)
test_y = torch.tensor(test_y, dtype=torch.long)
# %%
batch_size = 256

train_ds = TensorDataset(train_x, train_y)
train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)

test_ds = TensorDataset(test_x, test_y)
test_dl = DataLoader(test_ds, batch_size=batch_size)

input_features = train_x.shape[1]
output_features = classes_num

# %%
class ABNeuroNetwork(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = nn.Sequential(
            nn.Linear(input_features,32),
            nn.Sigmoid(),
            # nn.Linear(32,128),
            # nn.ReLU(),
            # nn.Linear(128,32),
            # nn.ReLU(),
            nn.Linear(32,output_features),
        )

    def forward(self, input):
        return self.linear(input)

# %%
lr_model = ABNeuroNetwork()
print(lr_model)

loss_func = nn.CrossEntropyLoss()

lr = 1e-2

optimizer = optim.Adam(lr_model.parameters(), lr=lr)

# %%
def accuracy(y_pred, y_true):
    y_pred = torch.argmax(y_pred, dim=1)
    acc = (y_pred == y_true).float()
    acc = acc.mean()
    return acc

# %%
itreation = 10000
train_acc = np.zeros(itreation)
train_loss = np.zeros(itreation)
test_acc = np.zeros(itreation)
test_loss = np.zeros(itreation)


for epoch in range(itreation):
    for x, y in train_dl:
        y_pred = lr_model(x)
        loss = loss_func(y_pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    with torch.no_grad():
        epoch_acc = accuracy(lr_model(train_x), train_y)
        epoch_loss = loss_func(lr_model(train_x), train_y).data

        test_epoch_acc = accuracy(lr_model(test_x), test_y)
        test_epoch_loss = loss_func(lr_model(test_x), test_y).data

        if (epoch+1) % 20 == 0:
            print("epoch:%d"%(epoch+1))
            print(f"loss:{epoch_loss.item():.3}, acc:{epoch_acc.item():.3}")
            print(f"test_loss:{test_epoch_loss.item():.3}, test_acc:{test_epoch_acc.item():.3}")
            print('-'*30)

        train_loss[epoch] = epoch_loss.item()
        train_acc[epoch] = epoch_acc.item()
        test_loss[epoch] = test_epoch_loss.item()
        test_acc[epoch] = test_epoch_acc.item()

# %%
import matplotlib.pyplot as plt

plt.figure(dpi=150)
plt.plot(range(epoch), train_loss, label='train_loss')
plt.plot(range(epoch), test_loss, label='test_loss')
plt.legend()
plt.show()

# %%
plt.figure(dpi=150)
plt.plot(range(epoch), train_acc, label='train_acc')
plt.plot(range(epoch), test_acc, label='test_acc')
plt.legend()
plt.show()

