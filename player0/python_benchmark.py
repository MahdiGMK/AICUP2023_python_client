import time , copy

N = int(1e5)
lst = []
for i in range(N) :
    lst.append(1)


t = -time.time()
l0 = lst[:]
print('lst[:]' , t + time.time())
t = -time.time()
l1 = lst * 1
print('lst * 1' , t + time.time())
t = -time.time()
l2 = list(lst)
print('list()' , t + time.time())
t = -time.time()
l3 = copy.copy(lst)
print('copy : ' , t + time.time())
t = -time.time()
l4 = copy.deepcopy(lst)
print('deepcopy : ' , t + time.time())
t = -time.time()
l5 = [x for x in lst]
print('deepcopy : ' , t + time.time())