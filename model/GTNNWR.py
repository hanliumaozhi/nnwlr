import torch.nn as nn
import torch.nn.functional as f
from torch.nn import Module
import torch
from model.SpatialTemporalPNN import SpatialTemporalPNN


class GeoTimWR(Module):
    def __init__(self, n_in, n_regress, is_cuda):
        super(GeoTimWR, self).__init__()
        self.hidden1 = nn.Linear(n_in, 400)
        self.hidden2 = nn.Linear(400, 40)
        self.out = nn.Linear(40, n_regress)
        self.n_in = n_in
        self.bn0 = nn.BatchNorm1d(num_features=n_in)

        #self.sub_nn = dict()
        self.is_cuda = is_cuda
        self.construct_sub_nn()
        self.w = torch.nn.Parameter(torch.rand(n_regress))

        self.init_weight()

    def construct_sub_nn(self):
        for i in range(self.n_in):
            name_str = "sub_nn_{}".format(i)
            # self.sub_nn[i] = SpatialTemporalPNN(i)
            tmp_model = SpatialTemporalPNN(i)
            tmp_model.init_weight()
            if self.is_cuda:
                tmp_model.cuda()
            self.__setattr__(name_str, tmp_model)

    def init_weight(self):
        init = nn.init.xavier_normal_
        init(self.hidden1.weight)
        init(self.hidden2.weight)
        init(self.out.weight)

    def sub_nn_f(self, sub_nn):
        ret_list = list()
        for i in range(self.n_in):
            name_str = "sub_nn_{}".format(i)
            tmp_model = self.__getattr__(name_str)
            ret_list.append(tmp_model(sub_nn[i]))
        return ret_list

    def forward(self, sub_nn, lr):
        ret_list = self.sub_nn_f(sub_nn)
        ret_tensor = torch.cat(ret_list, dim=1)
        x = self.bn0(ret_tensor)
        x = self.hidden1(x)
        x = f.relu(x)
        x = self.hidden2(x)
        x = f.relu(x)
        x = self.out(x)

        lr = lr*x
        y = lr*self.w
        y = torch.sum(y, dim=1)

        return y, x


