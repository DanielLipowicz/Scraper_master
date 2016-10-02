import matplotlib.pyplot as plt


def plot_two_keyword_data_list(two_keywords_data_list, first_label='first', second_label='second', ylim=25):
    x = []
    xticks = []
    y = []
    x2 = []
    y2 = []
    for row in two_keywords_data_list[1:]:
        x.append(row[0])
        x2.append(row[0])
        y.append(row[1])
        y2.append(row[2])
        xticks.append(row[3])
    plt.xticks(x, xticks , rotation='vertical')
    first = plt.scatter(x, y, 50, marker='o', alpha=0.5, color='blue', label=first_label)
    second = plt.scatter(x2, y2, 50, marker='o', alpha=0.5, color='green', label=second_label)
    plt.legend(handles=[first, second])
    plt.ylim((-1, ylim))
    plt.grid(True)
    plt.subplots_adjust(bottom=0.35)
    plt.xlabel('keyword')
    plt.ylabel('density')
    plt.show()

