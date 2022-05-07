'''
    继承路由：__mro__
    python 2.x 纵向查找
    python 3.x 横向查找
'''
class  A:
    pass
class B(A):
    pass

class C(A):
    pass


class D(B,C):
    pass


print(D.__mro__)