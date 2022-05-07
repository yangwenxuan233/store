# -*- coding:utf-8 -*-
# 本程序用于Standard_Modbus_Tcp进行状态解析
# 用于对寄存器状态码的解读
# 状态码详情参考SROS-Modbus通信协议


class ReadInputRegister:
    """
    输入寄存器内容解析，使用功能码 04（Read Input Register）进行读取
    """

    @staticmethod
    def system_status(data: str) -> str:
        """
        系统状态获取 寄存器地址30001
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '1': '系统正在初始化',
            '2': '系统空闲',
            '3': '系统出错',
            '4': '正在启动定位',
            '5': '导航正在初始化',
            '6': '导航正在寻路',
            '7': '等待到达目标位置',
            '8': '检测到障碍, 减速',
            '9': '导航正在重新寻路',
            'A': '遇到障碍暂停运动',
            'B': '无法抵达目标位置',
            'E': '初始化执行固定路径',
            'F': '等待固定路径执行结束',
            '10': '执行固定路径检测到障碍, 减速前进',
            '11': '执行固定路径遇到障碍暂停运动',
            '12': '无法检测到目标站点'
        }
        return status[str(data)]

    @staticmethod
    def positioning_status(data: str) -> str:
        """
        定位状态获取，寄存器地址30002
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '1': '定位未启动',
            '2': '定位正在初始化',
            '3': '定位成功',
            '4': '正在重定位',
            '5': '定位错误，需要重新启动定位'
        }
        return status[str(data)]

    @staticmethod
    def operating_status(data: str) -> str:
        """
        操作状态获取，寄存器地址30016
        :param data:状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '状态不可用',
            '1': '自动控制模式',
            '2': '手动控制模式'
        }
        return status[str(data)]

    @staticmethod
    def mission_operating_status(data: str) -> str:
        """
        mission运行状态获取，寄存器地址：30099
        :param data:状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '2': '任务在队列中，但是又还没有启动的状态',
            '3': '正在执行',
            '4': '暂停执行',
            '5': '执行结束',
            '6': '正在取消'
        }
        return status[str(data)]

    @staticmethod
    def mission_operating_result(data: str) -> str:
        """
        Mission执行结果
        :param data:状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '1': '任务执行成功',
            '2': '任务取消',
            '3': '任务执行出错'
        }
        return status[str(data)]

    @staticmethod
    def battery_info_state(data: str) -> str:
        """
        当前电池的状态
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '2': '正在充电',
            '3': '未充电'
        }
        return status[str(data)]

    @staticmethod
    def mobile_task_status(data: str) -> str:
        """
        移动任务状态
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '2': '等待开始执行',
            '3': '正在执行',
            '4': '暂停执行',
            '5': '执行结束',
            '6': '正在取消',
            '8': '交通管制'
        }
        return status[str(data)]

    @staticmethod
    def mobile_task_result(data: str) -> str:
        """
        移动任务结果
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '1': '任务执行成功',
            '2': '任务取消',
            '3': '任务执行出错'
        }
        return status[str(data)]

    @staticmethod
    def action_task_status(data: str) -> str:
        """
        动作任务状态
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲状态',
            '2': '等待开始执行',
            '3': '正在执行',
            '4': '暂停执行',
            '5': '执行结束',
            '6': '正在取消'
        }
        return status[str(data)]

    @staticmethod
    def action_task_result(data: str) -> str:
        """
        动作任务结果
        :param data: 状态码
        :return: 状态码对应的中文状态
        """
        status = {
            '0': '空闲',
            '1': '任务执行成功',
            '2': '任务取消',
            '3': '任务执行出错'
        }
        return status[str(data)]


class WriteSingleCoil:
    """
    使用功能码0x05写入写单个线圈
    """

    @staticmethod
    def functional_group(function: str) -> str:
        """
        常用功能组
        :param function:功能名称
        :return: 功能名称对应状态码 如果输入不存在则返回None
        """
        function_list = {
            '暂停运动': 1,
            '继续运动': 2,
            '停止运动': 3,
            '停止定位': 5,
            '屏蔽避障区域': 6,  # 0xFF00：开启屏蔽蔽障模式 0x0000： 退出屏蔽蔽障模式
            '触发急停': 7,
            '解除急停': 8,
            '开始充电': 9,
            '停止充电': 10,
            '进入低功耗模式': 11,
            '退出低功耗模式': 12,
            '系统重启': 14,
            '启动手动控制': 15,
            '关闭手动控制': 16,
            '向前移动': 17,  # 以0.495m/s向前移动(每设置一次移动100ms，此处是提供给开关专用，不支持速度配置，推荐使用40022-40024寄存器进行手动控制）
            '向后移动': 18,  # 以0.495m/s向后移动(每设置一次移动100ms）
            '向左旋转': 19,  # 以0.389rad/s向左旋转(每设置一次移动100ms）
            '向右旋转': 20,  # 以0.389rad/s向左旋转(每设置一次移动100ms）
            'DO_0': 33,
            'DO_1': 34,
            'DO_2': 35,
            'DO_3': 36,
            'DO_4': 37,
            'DO_5': 38,
            'DO_6': 39,
            'DO_7': 40,
            '放行': 49,  # 放行，即:发送此信号动作（131,0,0）会结束
            '调度模式': 51,  # 0xFF00：进入调度模式 0x0000： 退出调度模式
            '暂停mission任务': 97,
            '继续mission任务': 98,
            '取消mission任务': 99
        }
        return function_list.get(function, None)


if __name__ == "__main__":
    pass
