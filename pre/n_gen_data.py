from geopy import distance
from utils.tools import timethis


@timethis
def main():
    raw_data_list_train = list()
    with open("../data/train_set_raw.csv") as fp:
        raw_data_list_train = [i.split(',') for i in fp.read().split("\n")]

    raw_data_list_p = list()
    with open("../data/p_raw.csv") as fp:
        raw_data_list_p = [i.split(',') for i in fp.read().split("\n")]

    raw_data_list_test = list()
    with open("../data/test_set_raw.csv") as fp:
        raw_data_list_test = [i.split(',') for i in fp.read().split("\n")]

    raw_data_list_vali = list()
    with open("../data/vali_set_raw.csv") as fp:
        raw_data_list_vali = [i.split(',') for i in fp.read().split("\n")]

    data_list = list()
    data_list.extend(raw_data_list_train)
    data_list.extend(raw_data_list_p)
    data_list.extend(raw_data_list_test)
    data_list.extend(raw_data_list_vali)

    item_num = len(raw_data_list_train)
    item_nums = len(raw_data_list_train)
    tem_num = len(raw_data_list_train)
    item_len = len(raw_data_list_train[0])
    cal_list = list()
    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list_train[i][1]), float(raw_data_list_train[i][0]))
        for j in range(item_num):
            tmp_lat_long = (float(raw_data_list_train[j][1]), float(raw_data_list_train[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list_train[i][2]) - float(raw_data_list_train[j][2])))
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
            tem_list.append(raw_data_list_train[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/train_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)

    item_num = len(raw_data_list_test)
    item_len = len(raw_data_list_test[0])
    cal_list = list()
    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list_test[i][1]), float(raw_data_list_test[i][0]))
        for j in range(item_nums):
            tmp_lat_long = (float(raw_data_list_train[j][1]), float(raw_data_list_train[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list_test[i][2])-float(raw_data_list_train[j][2])))
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
            tem_list.append(raw_data_list_test[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/test_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)



    item_num = len(raw_data_list_p)
    tem_num = len(raw_data_list_p)
    item_len = len(raw_data_list_p[0])
    cal_list = list()
    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list_p[i][1]), float(raw_data_list_p[i][0]))
        for j in range(item_nums):
            tmp_lat_long = (float(raw_data_list_train[j][1]), float(raw_data_list_train[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list_p[i][2]) - float(raw_data_list_train[j][2])))
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
            tem_list.append(raw_data_list_p[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/p_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)

    item_num = len(raw_data_list_vali)
    tem_num = len(raw_data_list_vali)
    item_len = len(raw_data_list_vali[0])
    cal_list = list()
    for i in range(item_num):
        tem_list = list()
        # its order is (latitude, longitude) see:https://geopy.readthedocs.io/en/latest/index.html#module-geopy.distance
        latitude_longitude = (float(raw_data_list_vali[i][1]), float(raw_data_list_vali[i][0]))
        for j in range(item_nums):
            tmp_lat_long = (float(raw_data_list_train[j][1]), float(raw_data_list_train[j][0]))
            abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
            abs_time = abs((float(raw_data_list_vali[i][2]) - float(raw_data_list_train[j][2])))
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
            tem_list.append(raw_data_list_vali[i][j])
        cal_list.append(','.join(tem_list))

    with open("../data/vali_set.csv", "w") as fp:
        write_str = '\n'.join(cal_list)
        fp.write(write_str)


if __name__ == '__main__':
    main()