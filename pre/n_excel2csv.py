import xlrd


def main():
    wb = xlrd.open_workbook("../data/n_train_set.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            if not any(j == k for k in [0, 3, 4, 5]):
                tem_list.append(str(sheet.cell_value(i, j)))
        data_list.append(','.join(tem_list))

    # write data to csv
    with open("../data/train_set_raw.csv", "w") as fp:
        for i in range(len(data_list)):
            print(data_list[i])
            fp.write(data_list[i])
            if i != (len(data_list) - 1):
                fp.write("\n")

    wb = xlrd.open_workbook("../data/n_test_set.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            if not any(j == k for k in [0, 3, 4, 5]):
                tem_list.append(str(sheet.cell_value(i, j)))
        data_list.append(','.join(tem_list))

    # write data to csv
    with open("../data/test_set_raw.csv", "w") as fp:
        for i in range(len(data_list)):
            print(data_list[i])
            fp.write(data_list[i])
            if i != (len(data_list) - 1):
                fp.write("\n")

    wb = xlrd.open_workbook("../data/vali.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            if not any(j == k for k in [0, 3, 4, 5]):
                tem_list.append(str(sheet.cell_value(i, j)))
        data_list.append(','.join(tem_list))

    # write data to csv
    with open("../data/vali_set_raw.csv", "w") as fp:
        for i in range(len(data_list)):
            print(data_list[i])
            fp.write(data_list[i])
            if i != (len(data_list) - 1):
                fp.write("\n")


if __name__ == '__main__':
    main()
