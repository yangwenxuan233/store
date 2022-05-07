import pandas as pd

data = {'Name':['TOM','JOHN','JONY','JONY','JSON'],'Age':[19,20,17,17,21],'Score':[80,90,91,93,85]}
df = pd.DataFrame(data,index=[1,2,3,4,5])
print(df)
print(df.sort_values(by=['Name', 'Age','Score']))
