class QuickSort():

    def quick_sort(self, list, start, end):
        """快速排序"""
        # 递归的退出条件
        if start >= end:
            return
        # 设定起始元素为要寻找位置的基准元素
        mid = list[start]
        # left为序列左边的由左向右移动的指针
        left = start
        # right为序列右边的由右向左移动的指针
        right = end

        while left < right:
            # 如果left与right未重合，right指向的元素不比基准元素小，则right向左移动
            while left < right and list[right] >= mid:
                right -= 1
            # 将right指向的元素放到left的位置上
            list[left] = list[right]
            # 如果left与right未重合，left指向的元素比基准元素小，则left向右移动
            while left < right and list[left] < mid:
                left += 1
            # 将left指向的元素放到right的位置上
            list[right] = list[left]
        # 退出循环后，left与right重合，此时所指位置为基准元素的正确位置

        # 将基准元素放到该位置
        list[left] = mid
        # 对基准元素左边的子序列进行快速排序
        self.quick_sort(list, start, left-1)
        # 对基准元素右边的子序列进行快速排序
        self.quick_sort(list, left+1, end)


list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
qs = QuickSort()
qs.quick_sort(list, 0, len(list)-1)
print(list)
