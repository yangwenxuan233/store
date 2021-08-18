import pymysql
import xlrd
import xlwt


def excel_to_database(db_name, wb_name, sheet_name):
    con = pymysql.connect(host="localhost", user="root", password="root", database=db_name, charset="utf8")
    cursor = con.cursor()  # 数据库连接
    wb = xlrd.open_workbook(wb_name, encoding_override=True)  # 与.py同一目录下
    st = wb.sheet_by_name(sheet_name)
    rows = st.nrows
    cols = st.ncols
    title = st.row_values(0)
    cursor.execute("show tables")
    tables = cursor.fetchall()
    # 创建新表
    if sheet_name not in tables:
        cursor.execute("create table %s (`%s` varchar(50))" % (sheet_name, title[0]))
        for i in range(1, cols):
            cursor.execute("alter table %s add column `%s` varchar(50)" % (sheet_name, title[i]))
    # 写入数据
    for i in range(1, rows):
        data = st.row_values(i)
        cursor.execute("insert into %s (`"'%s'"`) values ('%s')" % (sheet_name, title[0], data[0]))
        con.commit()
        for j in range(1, cols):
            cursor.execute("update %s set `%s` = '%s' where `%s` = '%s'" % (sheet_name, title[j], data[j], title[0], data[0]))
    con.commit()  # 提交
    cursor.close()  # 关闭
    con.close()


def database_to_excel(db_name, table_name, save_path):
    con = pymysql.connect(host="localhost", user="root", password="root", database=db_name, charset="utf8")
    cursor = con.cursor()  # 数据库连接
    # 获取数据表所有数据
    cursor.execute("select * from `%s`" % table_name)
    data = cursor.fetchall()
    # 获取字段名
    fields = cursor.description
    field_name = [field[0] for field in fields]
    # 创建新表
    workbook = xlwt.Workbook(encoding='utf8')
    sheet = workbook.add_sheet(table_name)
    # 写入数据
    for key, value in enumerate(field_name):
        sheet.write(0, key, value)
    row = 1
    for i in data:
        for key, value in enumerate(i):
            sheet.write(row, key, value)
        row = row + 1
    workbook.save("%s/%s.xlsx" % (save_path, db_name))
    con.commit()  # 提交
    cursor.close()  # 关闭
    con.close()
