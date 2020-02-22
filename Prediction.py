import torch
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from matplotlib.pyplot import *
from pylab import *
from Nets import Net

net = torch.load("net218 10000 finalregression.pkl")
net.eval()

print(net)

file_bonus = open("bonus test final labeled.txt", "r")
file_records = open("records test final.txt", "r")
regression = False_
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


while 1:
    line = file_bonus.readline()
    if not line:
        break

    for i in range(rounds[round]):
        bonus.append(line)
    round += 1

predictions = []
difference = []
MSE = []
for i in range(bonus.__len__()):
    tensor = torch.FloatTensor(np.array(records[i], dtype="float32"))
    record = Variable(tensor, requires_grad=True)
    if regression:
        predictions.append((net(record).item()))
        difference.append(abs((int(bonus[i]) - predictions[i])))
        MSE.append(difference[i])
    else:
        predictions.append(torch.argmax((net(record))).item())
        if (predictions[i] == 0 and int(bonus[i]) == 5) or(predictions[i] == 1 and int(bonus[i] == 12)) or (predictions[i] == 2 and int(bonus[i] == 20)):
            difference.append(1)

        else:
            difference.append(0)
        MSE.append(difference[i])

    if difference.__len__() > 1:
        difference[i] += difference[i-1]
        MSE[i] = difference[i] / (i+1)
x = arange(0, len(bonus), 1)

plot(x, MSE, "b")
# plot(x, predictions, "r")
show()