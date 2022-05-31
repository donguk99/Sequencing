import random
f = open('dataset.txt', 'w')
l = []
num = 4000 # 몇개나 만들지
max_time = 3600
total_node = 9

for i in range(num):
    t = random.randint(0,max_time) # 시간 몇초까지
    departure = random.randint(1,total_node)
    arrival = random.randint(1,total_node)
    l.append([t, departure, arrival])
l.sort()
s = ''
for i in range(num):
    for j in range(3):
        s += str(l[i][j])
        s += ' '
    s += str(i+1)
    f.write(s)
    f.write('\n')
    s = ''

f.close()