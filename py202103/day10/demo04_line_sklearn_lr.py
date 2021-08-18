from sklearn.linear_model import LinearRegression
import numpy as np
x = np.array([[4,6,8,10,12]]).T
y = np.array([9,11.9,17,19,25])

model = LinearRegression()
model.fit(x,y)
print(model.coef_)  # 斜率
print(model.intercept_)  # 截距

x = np.array([[14,16,5,7]]).T
y = np.array([30,31,11,13])
model.predict(x)

r = model.score(x,y)
print(r)
