from geopy import distance
from utils.tools import timethis


@timethis
def main():
    raw_train_data_list = list()
    raw_data_list = list()
    with open("../data/train_set_raw.csv") as fp:
        raw_train_data_list = [i.split(',') for i in fp.read().split("\n")]

    with open("../data/test_set_raw.csv") as fp:
        raw_data_list = [i.split(',') for i in fp.read().split("\n")]

    item_num = len(raw_data_list)
    item_len = len(raw_train_data_list[0])
    raw_item_num = len(raw_train_data_list)

    cal_list = list()

    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list[i][1]), float(raw_data_list[i][0]))
        for j in range(raw_item_num):
            tmp_lat_long = (float(raw_train_data_list[j][1]), float(raw_train_data_list[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list[i][2])-float(raw_train_data_list[j][2])))
            tem_list.append(str(abs_distance))
            tem_list.append(str(abs_time))
        for j in range(3, item_len):
            tem_list.append(raw_data_list[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/test_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)


if __name__ == '__main__':
    main()
