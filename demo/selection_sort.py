class SelectionSort():

    def selection_sort(self, list):
        for i in range(0, len(list)-1):
            index = i  # 记录待排列位置的索引
            for j in range(i+1, len(list)):
                if list[j] < list[index]:
                    index = j
            if i != index:
                list[i], list[index] = list[index], list[i]
        return list


list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
ss = SelectionSort()
new_list = ss.selection_sort(list)
print(new_list)
