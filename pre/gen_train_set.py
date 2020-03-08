from geopy import distance
from utils.tools import timethis


@timethis
def main():
    raw_data_list = list()
    with open("../data/train_set_raw.csv") as fp:
        raw_data_list = [i.split(',') for i in fp.read().split("\n")]

    data_list = list()
    with open("../data/1.csv") as fp:
        data_all_list = fp.read().split("\n")
        for index, item in enumerate(data_all_list):
            data_list.append(item.split(','))

    item_num = len(raw_data_list)
    item_len = len(raw_data_list[0])
    cal_list = list()
    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list[i][1]), float(raw_data_list[i][0]))
        for j in range(item_num):
            tmp_lat_long = (float(raw_data_list[j][1]), float(raw_data_list[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list[i][2])-float(raw_data_list[j][2])))
            tem_list.append(str(abs_distance))
            tem_list.append(str(abs_time))

        tem_n_list = list()
        for j in range(len(data_list)):
            if abs(float(data_list[i][2]) - float(data_list[j][2])) < 0.5:
                tmp_lat_long = (float(data_list[j][1]), float(data_list[j][0]))
                abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
                if abs_distance > 1:
                    tem_n_list.append([abs_distance, float(data_list[j][-1])])
        tem_n_list.sort(key=lambda x: x[0])

        # it's for neigh data
        for j in range(5):
            tem_list.append(str(tem_n_list[j][1]))

        for j in range(3, item_len):
            tem_list.append(raw_data_list[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/train_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)


if __name__ == '__main__':
    main()
