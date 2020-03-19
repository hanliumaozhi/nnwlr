from functools import wraps
import time
import numpy as np
import torch
import xlrd
import codecs


def timethis(func,*args,**kwargs):
    @wraps(func)
    def wrapper(*args,**kwargs):
        s = time.time()
        ret = func(*args,**kwargs)
        elapse = time.time()-s
        print("{} use {}s".format(func.__name__, elapse))
        return ret
    return wrapper


def get_feature_no(csv_path):
    raw_data_list = list()
    with open(csv_path) as fp:
        raw_data_list = [i.split(',') for i in fp.read().split("\n")]
    return len(raw_data_list[0]), raw_data_list


@timethis
def get_train_set(csv_path, is_cuda):
    total_length,  raw_data_list = get_feature_no(csv_path)
    s_length_double = total_length - 8
    s_length = s_length_double//2
    s_nn_data_dict = dict()
    train_set_length = len(raw_data_list)
    for i in range(s_length):
        s_nn_data_dict[i] = list()
        for j in range(train_set_length):
            tmp_list = [float(raw_data_list[j][2*i]), float((raw_data_list[j][(2*i+1)]))]
            s_nn_data_dict[i].append(tmp_list)
        s_nn_data_dict[i] = np.array(s_nn_data_dict[i])
        s_nn_data_dict[i] = torch.FloatTensor(s_nn_data_dict[i])
        if is_cuda:
            s_nn_data_dict[i] = s_nn_data_dict[i].cuda()

    lr_tensor = list()
    for i in range(train_set_length):
        # we assume first item is lr offset
        tmp_list = [1]
        for j in range(s_length_double, (s_length_double+7)):
            try:
                tmp_list.append(float(raw_data_list[i][j]))
            except:
                tmp_list.append(0.0)
        lr_tensor.append(tmp_list)
    lr_tensor = torch.FloatTensor(np.array(lr_tensor))
    if is_cuda:
        lr_tensor = lr_tensor.cuda()

    target_y = list()
    for i in range(train_set_length):
        target_y.append(float(raw_data_list[i][(s_length_double+7)]))
    target_y = torch.FloatTensor(np.array(target_y))
    if is_cuda:
        target_y = target_y.cuda()

    return s_nn_data_dict, lr_tensor, target_y, s_length


def test_mul():
    x = torch.FloatTensor([[1, 1, 1], [2, 2, 2]])
    y = torch.FloatTensor([2, 2, 2])
    z = torch.rand(3)
    print(z)


def get_test_data():
    wb = xlrd.open_workbook("../data/p.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            tem_list.append(str(sheet.cell_value(i, j)))
        data_list.append(','.join(tem_list))

    additional_data = list()
    with open("../output/p_data.csv") as fp:
        additional_data = fp.read().split("\n")
    print(len(additional_data), len(data_list))
    for i in range(len(data_list)):
        data_list[i] = data_list[i] + ',' + additional_data[i]

    fp = codecs.open("../output/p_g.csv", "w", "utf-8")
    write_str = '\n'.join(data_list)
    fp.write(write_str)
    fp.close()


def import_all_data():
    test_nos = list()
    with open("../data/selected_nos.csv") as fp:
        test_nos = fp.read().split(',')

    data_train = list()
    with open("../output/train_data.csv") as fp:
        data_train = fp.read().split('\n')

    data_test = list()
    with open("../output/test_data.csv") as fp:
        data_test = fp.read().split('\n')

    for i in range(len(test_nos)):
        test_nos[i] = int(test_nos[i])

    test_nos.sort()

    wb = xlrd.open_workbook("../data/newll.xlsx")
    sheet = wb.sheet_by_index(0)
    total_row_num = sheet.nrows
    total_col_num = sheet.ncols

    data_list = list()
    # read data from excel
    for i in range(1, total_row_num):
        tem_list = list()
        for j in range(total_col_num):
            tem_list.append(str(sheet.cell_value(i, j)))
        data_list.append(','.join(tem_list))

    test_index = 0
    train_index = 0
    for i in range(len(data_list)):
        if i in test_nos:
            data_list[i] = data_list[i] + ',' + data_test[test_index]
            test_index = test_index + 1
        else:
            data_list[i] = data_list[i] + ',' + data_train[train_index]
            train_index = train_index + 1

    fp = codecs.open("../output/all_g.csv", "w", "utf-8")
    write_str = '\n'.join(data_list)
    fp.write(write_str)
    fp.close()


if __name__ == '__main__':
    import_all_data()
