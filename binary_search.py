"""
二分查找算法实现
包含多种实现方式：迭代、递归、以及变体
"""


def binary_search_iterative(arr, target):
    """
    二分查找 - 迭代版本
    
    参数:
        arr: 已排序的数组
        target: 要查找的目标值
    
    返回:
        目标值的索引，如果不存在则返回 -1
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # 使用 (left + right) // 2 可能会导致整数溢出
        # 更安全的做法是使用 left + (right - left) // 2
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr, target, left=None, right=None):
    """
    二分查找 - 递归版本
    
    参数:
        arr: 已排序的数组
        target: 要查找的目标值
        left: 左边界索引
        right: 右边界索引
    
    返回:
        目标值的索引，如果不存在则返回 -1
    
    时间复杂度: O(log n)
    空间复杂度: O(log n) - 递归调用栈
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    # 基础情况：搜索区间为空
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr, target):
    """
    二分查找 - 查找最左侧的目标值
    适用于有重复元素的情况
    
    参数:
        arr: 已排序的数组（可能包含重复元素）
        target: 要查找的目标值
    
    返回:
        最左侧目标值的索引，如果不存在则返回 -1
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # 继续在左侧搜索
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_rightmost(arr, target):
    """
    二分查找 - 查找最右侧的目标值
    适用于有重复元素的情况
    
    参数:
        arr: 已排序的数组（可能包含重复元素）
        target: 要查找的目标值
    
    返回:
        最右侧目标值的索引，如果不存在则返回 -1
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # 继续在右侧搜索
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_insert_position(arr, target):
    """
    二分查找 - 查找插入位置
    返回目标值应该插入的位置，以保持数组有序
    
    参数:
        arr: 已排序的数组
        target: 要插入的目标值
    
    返回:
        应该插入的位置索引
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left


def binary_search_range(arr, target):
    """
    二分查找 - 查找目标值的范围
    返回目标值在数组中出现的起始和结束位置
    
    参数:
        arr: 已排序的数组（可能包含重复元素）
        target: 要查找的目标值
    
    返回:
        [起始位置, 结束位置]，如果不存在则返回 [-1, -1]
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    if not arr:
        return [-1, -1]
    
    left = binary_search_leftmost(arr, target)
    if left == -1:
        return [-1, -1]
    
    right = binary_search_rightmost(arr, target)
    return [left, right]


# ========== 测试代码 ==========

def test_binary_search():
    """测试所有二分查找实现"""
    
    print("=" * 60)
    print("二分查找算法测试")
    print("=" * 60)
    
    # 测试用例 1: 基本测试
    print("\n【测试1】基本二分查找")
    arr1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target1 = 7
    result_iter = binary_search_iterative(arr1, target1)
    result_rec = binary_search_recursive(arr1, target1)
    print(f"数组: {arr1}")
    print(f"目标值: {target1}")
    print(f"迭代版本结果: 索引 {result_iter}, 值 = {arr1[result_iter] if result_iter != -1 else '未找到'}")
    print(f"递归版本结果: 索引 {result_rec}, 值 = {arr1[result_rec] if result_rec != -1 else '未找到'}")
    assert result_iter == 3
    assert result_rec == 3
    print("✓ 测试通过")
    
    # 测试用例 2: 目标不存在
    print("\n【测试2】目标值不存在")
    target2 = 8
    result_iter = binary_search_iterative(arr1, target2)
    result_rec = binary_search_recursive(arr1, target2)
    print(f"数组: {arr1}")
    print(f"目标值: {target2}")
    print(f"迭代版本结果: {result_iter} (未找到)")
    print(f"递归版本结果: {result_rec} (未找到)")
    assert result_iter == -1
    assert result_rec == -1
    print("✓ 测试通过")
    
    # 测试用例 3: 边界测试
    print("\n【测试3】边界值测试")
    print(f"数组: {arr1}")
    # 查找第一个元素
    result_first = binary_search_iterative(arr1, arr1[0])
    print(f"查找第一个元素 {arr1[0]}: 索引 {result_first}")
    assert result_first == 0
    # 查找最后一个元素
    result_last = binary_search_iterative(arr1, arr1[-1])
    print(f"查找最后一个元素 {arr1[-1]}: 索引 {result_last}")
    assert result_last == len(arr1) - 1
    print("✓ 测试通过")
    
    # 测试用例 4: 空数组
    print("\n【测试4】空数组测试")
    arr_empty = []
    result_empty = binary_search_iterative(arr_empty, 5)
    print(f"数组: {arr_empty}")
    print(f"结果: {result_empty} (未找到)")
    assert result_empty == -1
    print("✓ 测试通过")
    
    # 测试用例 5: 单元素数组
    print("\n【测试5】单元素数组测试")
    arr_single = [42]
    result_found = binary_search_iterative(arr_single, 42)
    result_not_found = binary_search_iterative(arr_single, 43)
    print(f"数组: {arr_single}")
    print(f"查找 42: 索引 {result_found}")
    print(f"查找 43: {result_not_found} (未找到)")
    assert result_found == 0
    assert result_not_found == -1
    print("✓ 测试通过")
    
    # 测试用例 6: 重复元素 - 查找最左侧
    print("\n【测试6】重复元素 - 查找最左侧位置")
    arr_dup = [1, 2, 2, 2, 3, 4, 4, 5]
    target_dup = 2
    result_left = binary_search_leftmost(arr_dup, target_dup)
    print(f"数组: {arr_dup}")
    print(f"目标值: {target_dup}")
    print(f"最左侧位置: 索引 {result_left}")
    assert result_left == 1
    print("✓ 测试通过")
    
    # 测试用例 7: 重复元素 - 查找最右侧
    print("\n【测试7】重复元素 - 查找最右侧位置")
    result_right = binary_search_rightmost(arr_dup, target_dup)
    print(f"数组: {arr_dup}")
    print(f"目标值: {target_dup}")
    print(f"最右侧位置: 索引 {result_right}")
    assert result_right == 3
    print("✓ 测试通过")
    
    # 测试用例 8: 查找范围
    print("\n【测试8】查找目标值范围")
    range_result = binary_search_range(arr_dup, target_dup)
    print(f"数组: {arr_dup}")
    print(f"目标值: {target_dup}")
    print(f"范围: {range_result} (从索引 {range_result[0]} 到 {range_result[1]})")
    assert range_result == [1, 3]
    
    range_result2 = binary_search_range(arr_dup, 4)
    print(f"目标值: 4")
    print(f"范围: {range_result2} (从索引 {range_result2[0]} 到 {range_result2[1]})")
    assert range_result2 == [5, 6]
    print("✓ 测试通过")
    
    # 测试用例 9: 插入位置
    print("\n【测试9】查找插入位置")
    arr_insert = [1, 3, 5, 7, 9]
    targets = [0, 2, 4, 6, 8, 10]
    print(f"数组: {arr_insert}")
    for t in targets:
        pos = binary_search_insert_position(arr_insert, t)
        print(f"  值 {t} 应插入位置: 索引 {pos}")
    print("✓ 测试通过")
    
    # 测试用例 10: 大数组性能测试
    print("\n【测试10】大数组性能测试")
    import time
    large_arr = list(range(0, 1000000, 2))  # 50万个偶数
    target_large = 888888
    
    start = time.time()
    result_large = binary_search_iterative(large_arr, target_large)
    end = time.time()
    
    print(f"数组大小: {len(large_arr):,} 个元素")
    print(f"目标值: {target_large}")
    print(f"结果: 索引 {result_large}")
    print(f"耗时: {(end - start) * 1000:.4f} 毫秒")
    assert result_large == target_large // 2
    print("✓ 测试通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过! ✓")
    print("=" * 60)


if __name__ == "__main__":
    test_binary_search()
