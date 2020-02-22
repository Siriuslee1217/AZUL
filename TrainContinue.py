import torch
import torch.nn.functional as F     # 激励函数都在这
from torch.autograd import Variable
import numpy as np

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()

        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):

        x = F.relu(self.hidden(x))
        x = self.predict(x)
        return x


net = torch.load("net210.pkl")

optimizer = torch.optim.SGD(net.parameters(), lr=0.001)
loss_func = torch.nn.MSELoss()

file_bonus = open("Bonus2.10.txt", "r")
file_records = open("Records2.10.txt", "r")

records = []
longgames = []
numgame = 0
while 1:
    line = file_records.readline()
    if not line:
        break

    records.append(line.split())

bonus = []

flag = 0
rounds = []
round = 0

for record in records:
    if (int(record[0])) > flag:
        flag = int(record[0])
    else:
        rounds.append(flag)
        round += 1
        flag = 0

rounds.append(flag)

round = 0

print(len(rounds))

while 1:
    line = file_bonus.readline()
    if not line:
        break

    for i in range(rounds[round]):
        bonus.append(line)
    round += 1
print(records[0])
print(bonus[0])

import matplotlib.pyplot as plt

plt.ion()
plt.show()

for t in range(100):
    loss_epoch = 0
    for i in range(records.__len__()):
        optimizer.zero_grad()

        tensor = torch.FloatTensor(np.array(records[i], dtype="float32"))
        record = Variable(tensor, requires_grad = True)

        prediction = net(record)

        tensor2 = torch.FloatTensor(np.array([bonus[i]], dtype="float32"))
        b = Variable(tensor2, requires_grad = True)

        loss = loss_func(prediction, b)
        loss_epoch += loss.data
        loss.backward()
        optimizer.step()
    print(net(record))
    print(b)
    print(str(t + 1) + " round:")
    # for name, param in net.named_parameters():
    #     print(name)
    #     print(param)
    print()
    print("loss: " + str(loss_epoch))

torch.save(net, "net2101.pkl")