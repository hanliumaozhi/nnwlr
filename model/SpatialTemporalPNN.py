import torch.nn as nn
import torch.nn.functional as f
from torch.nn import Module
import torch


class SpatialTemporalPNN(Module):
    def __init__(self, no_nn, n_in=2, n_out=1):
        super(SpatialTemporalPNN, self).__init__()
        self.hidden = nn.Linear(n_in, 3)
        self.out = nn.Linear(3, n_out)
        self.no = no_nn

    def init_weight(self):
        init = nn.init.xavier_normal_
        init(self.hidden.weight)
        init(self.out.weight)

    def forward(self, x):
        x = f.relu(self.hidden(x))
        x = self.out(x)
        return x


if __name__ == '__main__':
    pass
