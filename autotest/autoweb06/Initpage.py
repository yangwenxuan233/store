class Initpage:

    # 成功用例的数据
    login_success_data = [
        {"username": "1075361524@qq.com", "password": "justinbieber", "expect": "返回"},
        {"username": "1075361524@qq.com", "password": "justin", "expect": "返回"}
    ]

    # 失败用例的数据：msg_uname
    login_error_data = [
        {"username": "1282398184@qq.com", "password": "1234567", "expect": "帐号或密码错误"},
        {"username": "1075361524@qq.com", "password": "justinbieber", "expect": "帐号或密码错误"}
    ]
