# -*- coding:utf-8 -*-

__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class ExcelGenerator(object):
    def __init__(self, name):
        self.name = name
        import xlwt

        self.book = xlwt.Workbook(encoding="utf-8")

    def add_sheet(self, sheet_name, titles, rows):
        '''
        titles, 标题数组
        rows，数据数据，每个row都是一组数据
        '''
        sheet = self.book.add_sheet(sheet_name)
        col_len = titles.__len__()
        for i in range(0, col_len):
            sheet.write(0, i, titles[i])
        row_num = 1
        for row in rows:
            for col in range(0, col_len):
                sheet.write(row_num, col, row[col])
            row_num += 1

    def save(self):
        self.book.save(self.name)
