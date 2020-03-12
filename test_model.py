import torch

from utils.tools import get_train_set
from model.GTNNWR import GeoTimWR


def main():
    # torch.manual_seed(35545)
    use_cuda = True
    sub_nn_data, lr_data, target_y, sub_nn_len, ng_data = get_train_set('data/p_set.csv', use_cuda)

    model = GeoTimWR(sub_nn_len, 7, use_cuda, 5)
    model.cuda()

    model.load_state_dict(torch.load("output/Model.DATA"))

    loss_f = torch.nn.MSELoss()
    loss_ff = torch.nn.MSELoss(reduction='none')

    y_hat = None

    with torch.no_grad():
        model.eval()
        y_hat, lr_w = model(sub_nn_data, lr_data, ng_data)
        val_loss = loss_f(y_hat, target_y)
        val_loss = val_loss.item()
        print(val_loss)
        lr_ww = lr_w.cpu().numpy()

    with open("output/p_data.csv", "w") as fp:
        str_list = list()
        for i in range(len(lr_ww)):
            tmp_list = list()
            for j in lr_ww[i]:
                tmp_list.append(str(j))
            tmp_list.append(str(y_hat[i].item()))
            str_list.append(','.join(tmp_list))
        str_output = '\n'.join(str_list)
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
