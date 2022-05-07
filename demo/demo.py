# def quickSort(list, start=0, end=0):
#     if start == 0 and end == 0:
#         end = len(list) - 1

#     if start >= end:
#         return list

#     mid = list[start]
#     left = start
#     right = end

#     while left < right:
#         while left < right and list[right] <= mid:
#             right -= 1
#         list[left] = list[right]

#         while left < right and list[left] > mid:
#             left += 1
#         list[right] = list[left]

#     list[left] = mid
#     quickSort(list, start, left-1)
#     quickSort(list, left+1, end)


# list1 = [54, 26, 93, 17, 77, 31, 44, 55, 20]
# # quickSort(list)
# # print(list)

# string = "  aabb CCDD  "

# # for i in set(string):
# #     print(i+"是小写，出现次数"+str(string.count(i)) if i.islower() else i+"是大写，出现次数"+str(string.count(i)))

# # print(list1[::-1])

# # print(list(reversed(list1)))
# # for i in range(5):
# #     print(type(reversed(list1).__next__))

# print(string.strip())
# print(string.capitalize())
# print(string.upper())
# print(string.lower())
# print(string[1:4].find("a"))
# print(string.swapcase())
# print(string.strip("/n"))

# file = open(r"D:\pycode\py202107\day15hw\scores.txt", mode="r+", encoding="utf-8")
# data = file.readline()


# class Printer(object):

#     print = None

#     @classmethod
#     def get(cls):
#         if cls.print is None:
#             cls.print = Printer()
#             return cls.print
#         else:
#             return cls.print


# d1 = Printer.get()
# print(id(d1))
# d2 = Printer.get()
# print(id(d2))
# d3 = Printer.get()
# print(id(d3))
# d4 = Printer()
# d4 = d4.get()
# print(id(d4))

# list2 = ['a', 'b', 'c']
# b = 'a'.join(list2)
# print(b)

a = [1, 2, 3]
# print(id(a))
# a.append(4)
# print(id(a))

b = 5
print(bin(b))