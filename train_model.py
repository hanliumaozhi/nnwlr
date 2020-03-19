import torch

from utils.tools import get_train_set
from model.GTNNWR import GeoTimWR

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def main():
    # manual rand
    torch.manual_seed(35544235435)

    # use gpu
    use_cuda = True
    sub_nn_data, lr_data, target_y, sub_nn_len = get_train_set('data/train_set.csv', use_cuda)
    sub_nn_data_t, lr_data_t, target_y_t, sub_nn_len_t = get_train_set('data/test_set.csv', use_cuda)

    print(sub_nn_len)
    print(sub_nn_len_t)

    model = GeoTimWR(sub_nn_len, 8, use_cuda)
    model.cuda()

    loss_f = torch.nn.MSELoss()
    loss_ff = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4, momentum=0.9)

    epochs = 3000

    loss_data = list()
    validation_loss_data = list()

    for epoch in range(epochs):
        model.train()
        output, lr_w = model(sub_nn_data, lr_data)
        loss = loss_f(output, target_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_data.append(loss.item())

        with torch.no_grad():
            model.eval()
            output_t, lr_x = model(sub_nn_data_t, lr_data_t)
            loss = loss_ff(output_t, target_y_t)
            validation_loss_data.append(loss.item())
        if epoch % 10 == 0:
            print(epoch)
            p_str = "train_{}, test_{}".format(loss_data[epoch], validation_loss_data[epoch])
            print(p_str)

    torch.save(model.state_dict(), "output/Model.DATA")

    x = [i for i in range(epochs)]
    x = np.array(x)
    loss_data = np.array(loss_data)
    test_loss_data = np.array(validation_loss_data)

    with open("output/loss_data.csv", "w") as fp:
        loss_data_str = list()
        for i in loss_data:
            loss_data_str.append(str(i))
        loss_data_str = ','.join(loss_data_str)
        fp.write(loss_data_str)

    with open("output/loss_test_data.csv", "w") as fp:
        loss_data_str = list()
        for i in validation_loss_data:
            loss_data_str.append(str(i))
        loss_data_str = ','.join(loss_data_str)
        fp.write(loss_data_str)

    plt.plot(x, loss_data, x, test_loss_data)
    plt.show()


if __name__ == '__main__':
    main()
