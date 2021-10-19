'''
    excel表格的数据统计和分析：
    1.联网安装 xlrd(读取) xlwt(写入)
    xlrd(1.2)
        cmd  -->  python  -m pip  install   xlrd==0.9.3
    2.写代码
        2.1 导入这个工具
            import  xlrd
        2.2 打开工作簿
            wd = xlrd.open_workbook("data.xlsx", encoding_override=True)
        2.3 打开选项卡
            st = wd.sheet_by_name("用户管理")
        2.4 读取数据
任务：
    每个月的销售总金额：
    全年的销售总额：
    每种衣服的销售总额：
    每个季度销售总额占比：
    全年每种销售数量占比：

'''
import xlrd

year = {}  # 空数据库
month_keys = []
total = {}

wd = xlrd.open_workbook(r"D:\pycode\py202107\2020年每个月的销售情况.xlsx", encoding_override=True)

for k in range(12):
    month = str(k + 1) + "月"  # 遍历sheet
    st = wd.sheet_by_name(month)
    row = st.nrows
    clothes = {}  # 清空数据表
    for i in range(1, row, 1):
        data = st.row_values(i)  # 按行遍历表格除首行外数据
        year_keys = list(year.keys())
        for j in year_keys:
            month_keys.append(year[j].keys())
        if data[1] in month_keys:
            count = year[month][data[1]]["count"]
        else:
            count = 0
        clothes[data[1]] = {
            "price": data[2],
            "count": count + data[4],
            "sales": data[2] * (count + data[4])
        }
        if data[1] not in total:
            count_clothes = 0
        else:
            count_clothes = total[data[1]]["count"]
        total[data[1]] = {
            "price": data[2],
            "count": count_clothes + data[4],
            "sales": data[2] * (count_clothes + data[4])
        }
    year[month] = clothes

print(year)

sales_year = 0
for i in year:
    sales_month = 0
    for j in year[i]:
        for k in year[i][j]:
            sales_month = sales_month + year[i][j]["sales"]
    sales_year = sales_year + sales_month
    print(i, "销售总额:", round(sales_month, 2))

print("\n全年销售总额：", round(sales_year, 2), "\n")

for i in total:
    sales_total = total[i]["sales"]
    print(i, "销售总额:", round(sales_total, 2))
print(" ")

for i in range(4):
    sales_season = 0
    for j in range(i*3, i*3 + 3, 1):
        for k in year[str(j + 1) + "月"]:
            for m in year[str(j + 1) + "月"][k]:
                sales_season = year[str(j + 1) + "月"][k]["sales"] + sales_season
    print("第", i + 1, "季度销售额：", round(sales_season, 2))
print(" ")

count_total = 0
for i in total:
    count_total = count_total + total[i]["count"]

for i in total:
    print(i, "销售量占比", round(total[i]["count"]/count_total, 4) * 100, "%")
