"""
有以下二维列表，求该列表中是否存在鞍点。若有，请编程求出。
(ps：鞍点，就是这个数在当前行中最大，在当前列中最小。)
[
 [10 , 14 ,  9 ,  15],
 [7  , 4 ,  8 ,  10 ],
 [6  , 8 ,  4 ,   9 ],
 [8  , 51,  10,  23]
]
"""
import numpy as np

list1 = [[10, 14, 9, 15],
         [7, 4, 8, 10],
         [6, 8, 4, 9],
         [8, 51, 10, 23]]

for i in list1:
    for x in i:
        if all([x == max(i), x == min([t[i.index(x)] for t in list1])]):
            print(x, "是鞍点，位于矩阵的第", list1.index(i) + 1, "行，第", i.index(x) + 1, "列")


"""
编程实现列表进行回型初始化。
[
 [1 , 1 , 1 , 1],
 [1 , 2 , 2 , 1],
 [1 , 2 , 2 , 1],
 [1 , 1 , 1 , 1]
]
或者实现：
[
 [1 , 1 , 1 , 1 , 1],
 [1 , 2 , 2 , 2 , 1],
 [1 , 2 , 3 , 2 , 1],
 [1 , 2 , 2 , 2 , 1],
 [1 , 1 , 1 , 1 , 1]
]
"""
n = 6
randArray = np.random.randint(100, size=(n, n))
print(randArray)


for i in range(n):
    randArray[:, i:n-i][i:n-i] = i + 1

print(randArray)
