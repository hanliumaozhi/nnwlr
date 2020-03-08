from geopy import distance


def main():
    data_list = list()
    with open("../data/1.csv") as fp:
        data_all_list = fp.read().split("\n")
        for index, item in enumerate(data_all_list):
            data_list.append(item.split(','))

    # get list for data
    process_data_list = list()
    for i in range(len(data_list)):
        latitude_longitude = (float(data_list[i][1]), float(data_list[i][0]))
        tem_list = list()
        for j in range(len(data_list)):
            if j != i and abs(float(data_list[i][2]) - float(data_list[j][2])) < 0.5:
                tmp_lat_long = (float(data_list[j][1]), float(data_list[j][0]))
                abs_distance = abs(distance.distance(latitude_longitude, tmp_lat_long).km)
                tem_list.append([abs_distance, float(data_list[j][-1])])
        tem_list.sort(key=lambda x: x[0])
        new_list = [str(x[1]) for x in tem_list[:5]]
        process_data_list.append(new_list)

    save_data = list()
    for i in range(len(process_data_list)):
        save_data.append(','.join(process_data_list[i]))

    with open("../data/N_data.csv", "w") as fp:
        train_str = '\n'.join(save_data)
        fp.write(train_str)


if __name__ == '__main__':
    main()
