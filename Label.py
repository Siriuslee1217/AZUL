file_bonus = open("bonus test final.txt", "r")
file_bonus_labeled = open("bonus test final labeled.txt", "a")
lines = []
while 1:
    line = file_bonus.readline()

    if not line:
        break

    line = int(line)

    if line <= 7:
        line = 5
    elif 7 < line <= 15:
        line = 12
    else:
        line = 20

    file_bonus_labeled.write(str(line) + "\n")

file_bonus.close()
file_bonus_labeled.close()

print("finished")
