import torch
import torch.nn.functional as F     # 激励函数都在这
from torch.autograd \
import Variable
import numpy as np

print("adfdsafdasfdasfdsafads")
class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()

        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):

        x = F.relu(self.hidden(x))
        x = self.predict(x)
        return x


net = Net(n_feature = 26, n_hidden=10, n_output = 1)

optimizer = torch.optim.SGD(net.parameters(), lr=0.0002)
loss_func = torch.nn.MSELoss()

file_bonus = open("Bonus2.18 final.txt", "r")
file_records = open("Records2.18 final.txt", "r")

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
print(records[0].__len__())

print(bonus[0])
epoch = 100
from matplotlib.pyplot import *
from pylab import *

round_loss = []
for t in range(epoch):
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
    round_loss.append(int(loss_epoch.item()));
    print("loss: " + str(int(loss_epoch.item())))


x = arange(0, epoch, 1)
y = round_loss

plot(x, y, "b")
legend(["Loss/Epoch"])
show()

torch.save(net, "net218 10000 finalregression.pkl")