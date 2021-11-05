import xlwt

i = 0
wb = xlwt.Workbook(encoding='utf8')
sheet = wb.add_sheet("")

while i < 64:
    # 为样式创建字体
    font = xlwt.Font()

    # 字体类型
    font.name = 'name Times New Roman'
    # 字体颜色
    font.colour_index = i
    # 字体大小，11为字号，20为衡量单位
    font.height = 20*11
    # 字体加粗
    font.bold = False
    # 下划线
    font.underline = True
    # 斜体字
    font.italic = True

    # 设置单元格对齐方式
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x02
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x01

    # 设置自动换行
    alignment.wrap = 1

    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 2
    borders.top = 3
    borders.bottom = 4
    borders.left_colour = i
    borders.right_colour = i
    borders.top_colour = i
    borders.bottom_colour = i

    # 设置列宽，一个中文等于两个英文等于两个字符，11为字符数，256为衡量单位
    sheet.col(1).width = 11 * 256

    # 设置背景颜色
    pattern = xlwt.Pattern()
    # 设置背景颜色的模式
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # 背景颜色
    pattern.pattern_fore_colour = i

    # 初始化样式
    style0 = xlwt.XFStyle()
    style0.font = font

    style1 = xlwt.XFStyle()
    style1.pattern = pattern

    style2 = xlwt.XFStyle()
    style2.alignment = alignment

    style3 = xlwt.XFStyle()
    style3.borders = borders

    # 设置文字模式
    font.num_format_str = '#,##0.00'

    sheet.write(i, 0, u'字体', style0)
    sheet.write(i, 1, u'背景', style1)
    sheet.write(i, 2, u'对齐方式', style2)
    sheet.write(i, 3, u'边框', style3)

    # 合并单元格，合并第2行到第4行的第4列到第5列
    sheet.write_merge(2, 4, 4, 5, u'合并')
    i = i + 1
