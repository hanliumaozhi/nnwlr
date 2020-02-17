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
    loss_ff = torch.nn.MSELoss(reduction='none')

    y_hat = None

    with torch.no_grad():
        model.eval()
        y_hat = model(sub_nn_data, lr_data)
        val_loss = loss_f(y_hat, target_y)
        val_loss = val_loss.item()
        print(val_loss)
        val_loss = loss_ff(y_hat, target_y)
        print(val_loss)

    with open("output/test_data.csv", "w") as fp:
        str_list = list()
        for i in y_hat:
            str_list.append(str(i.item()))
        str_output = ','.join(str_list)
        fp.write(str_output)

    weight_item_list = list()
    for key in model.state_dict().keys():
        tmp_list = list()
        tmp_list.append(str(key))
        tt = model.state_dict()[key].cpu()
        tmp_list.append(str(tt.numpy()).replace("\n", ""))
        tmp_list = ','.join(tmp_list)
        weight_item_list.append(tmp_list)
    with open("output/weight.csv", "w") as fp:
        str_output = '\n'.join(weight_item_list)
        fp.write(str_output)



if __name__ == '__main__':
    main()
