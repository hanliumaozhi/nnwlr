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
    s_length_double = total_length - 7
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
        for j in range(s_length_double, (s_length_double+6)):
            tmp_list.append(float(raw_data_list[i][j]))
        lr_tensor.append(tmp_list)
    lr_tensor = torch.FloatTensor(np.array(lr_tensor))
    if is_cuda:
        lr_tensor = lr_tensor.cuda()

    target_y = list()
    for i in range(train_set_length):
        target_y.append(float(raw_data_list[i][(s_length_double+6)]))
    target_y = torch.FloatTensor(np.array(target_y))
    if is_cuda:
        target_y = target_y.cuda()

    return s_nn_data_dict, lr_tensor, target_y, s_length


def test_mul():
    x = torch.FloatTensor([[1, 1, 1], [2, 2, 2]])
    y = torch.FloatTensor([2, 2, 2])
    z = torch.rand(3)
    print(z)


if __name__ == '__main__':
    test_mul()
