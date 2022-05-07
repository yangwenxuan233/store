class BubbleSort():

    def bubble_sort(self, list):
        for i in range(1, len(list)):
            for j in range(0, len(list)-i):
                if list[j] > list[j+1]:
                    list[j], list[j+1] = list[j+1], list[j]
        return list


list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
bs = BubbleSort()
new_list = bs.bubble_sort(list)
print(new_list)
