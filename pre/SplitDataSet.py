

def main():
    test_no_list = None
    with open("../data/selected_nos.csv") as fp:
        test_no_list = fp.read().split(",")
    test_no_list = list(map(lambda x: int(x), test_no_list))

    data_train = list()
    data_test = list()
    with open("../data/m_data.csv") as fp:
        data_all_list = fp.read().split("\n")

        for index, item in enumerate(data_all_list):
            if index in test_no_list:
                data_test.append(item)
            else:
                data_train.append(item)

    with open("../data/train_set_raw.csv", "w") as fp:
        train_str = '\n'.join(data_train)
        fp.write(train_str)

    with open("../data/test_set_raw.csv", "w") as fp:
        test_str = '\n'.join(data_test)
        fp.write(test_str)


if __name__ == '__main__':
    main()
