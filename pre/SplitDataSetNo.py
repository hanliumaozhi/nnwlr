import random


def main():
    data_list = list()
    with open("../data/1.csv") as fp:
        data_list = fp.readlines()
    num_of_sample = len(data_list)
    # we should get 20% sample as test set
    selected_items = random.sample(range(num_of_sample), num_of_sample//5)
    selected_items = map(lambda x: str(x), selected_items)

    with open("../data/selected_nos.csv", "w") as fp:
        fp.write(','.join(selected_items))


if __name__ == '__main__':
    main()
