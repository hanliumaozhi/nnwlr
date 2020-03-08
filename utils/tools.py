from functools import wraps
import time
import numpy as np
import torch


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
    s_length_double = total_length - (7+5)
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
    ng_tensor = list()
    for i in range(train_set_length):
        # we assume first item is lr offset
        tmp_list = [1]
        for j in range((s_length_double+5), (s_length_double+6+5)):
            tmp_list.append(float(raw_data_list[i][j]))

        ts_list = list()
        for j in range(s_length_double, (s_length_double + 5)):
            ts_list.append(float(raw_data_list[i][j]))

        ng_tensor.append(ts_list)
        lr_tensor.append(tmp_list)
    lr_tensor = torch.FloatTensor(np.array(lr_tensor))
    ng_tensor = torch.FloatTensor(np.array(ng_tensor))
    if is_cuda:
        lr_tensor = lr_tensor.cuda()
        ng_tensor = ng_tensor.cuda()

    target_y = list()
    for i in range(train_set_length):
        target_y.append(float(raw_data_list[i][(s_length_double+6+5)]))
    target_y = torch.FloatTensor(np.array(target_y))
    if is_cuda:
        target_y = target_y.cuda()

    return s_nn_data_dict, lr_tensor, target_y, s_length, ng_tensor


def test_mul():
    x = torch.FloatTensor([[1, 1, 1], [2, 2, 2]])
    y = torch.FloatTensor([2, 2, 2])
    z = torch.rand(3)
    print(z)


def get_test_data():
    raw_data_list = list()
    test_data_list = list()
    test_no_list = list()
    y_hat = list()

    with open("../data/selected_nos.csv") as fp:
        str_all = fp.read().split(',')
        for i in range(len(str_all)):
            test_no_list.append(int(str_all[i]))

    with open("../data/1.csv") as fp:
        str_all = fp.read()
        raw_data_list = str_all.split('\n')
        for i in range(len(raw_data_list)):
            if i in test_no_list:
                test_data_list.append(raw_data_list[i].split(','))

    with open("../output/test_data.csv") as fp:
        tmp_list = fp.read().split(",")
        for i in range(len(tmp_list)):
            test_data_list[i].append(tmp_list[i])
            test_data_list[i] = ','.join(test_data_list[i])

    with open("../output/test_data_all.csv", "w") as fp:
        str_all = '\n'.join(test_data_list)
        fp.write(str_all)


if __name__ == '__main__':
    get_test_data()
