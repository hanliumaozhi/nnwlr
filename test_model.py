import torch

from utils.tools import get_train_set
from model.GTNNWR import GeoTimWR


def main():
    # torch.manual_seed(35545)
    use_cuda = True
    sub_nn_data, lr_data, target_y, sub_nn_len = get_train_set('data/test_set.csv', use_cuda)

    model = GeoTimWR(sub_nn_len, 7, use_cuda)
    model.cuda()

    model.load_state_dict(torch.load("output/Model.DATA"))

    loss_f = torch.nn.MSELoss()

    with torch.no_grad():
        model.eval()
        y_hat = model(sub_nn_data, lr_data)
        val_loss = loss_f(y_hat, target_y)
        val_loss = val_loss.item()
        print(val_loss)


if __name__ == '__main__':
    main()
