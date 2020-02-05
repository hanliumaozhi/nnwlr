import xlrd


def main():
    wb = xlrd.open_workbook("../data/1.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            tem_list.append(str(sheet.cell_value(i, j)))
        tem_list[3], tem_list[(total_col_num-1)] = tem_list[(total_col_num-1)], tem_list[3]
        data_list.append(','.join(tem_list))

    # write data to csv
    with open("../data/1.csv", "w") as fp:
        for i in range(len(data_list)):
            fp.write(data_list[i])
            if i != (len(data_list) - 1):
                fp.write("\n")


if __name__ == '__main__':
    main()
