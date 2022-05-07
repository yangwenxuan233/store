import xlsxwriter


wb = xlsxwriter.Workbook('img.xlsx')

for i in range(2, 31, 2):
    st = wb.add_worksheet(str(i))
    if i == 10:
        name1 = '0109'
        name2 = '0110'
    elif i < 10:
        name1 = '010{m}'.format(m=str(i-1))
        name2 = '010{n}'.format(n=str(i))
    else:
        name1 = '01{m}'.format(m=str(i-1))
        name2 = '01{n}'.format(n=str(i))
    st.set_column(0, 2, 53.5)
    for j in range(4):
        st.set_row(j, 285)
        st.insert_image('A' + str(j + 1), 'D:\pycode\image\{name1}\{name1}010{number}.jpg'.format(name1=name1, number=j+1))
        st.insert_image('B' + str(j + 1), 'D:\pycode\image\{name2}\{name2}010{number}.jpg'.format(name2=name2, number=j+1))

wb.close()