import numpy as np
import matplotlib.pyplot as plt
# 这里需要更改数据位置
filename = '/home/shorwin/work/SemanticKitti/dataset/poses/00.txt'

dataset = []
groundtruth = []
with open(filename) as f:
    list_file = f.readlines()

    # 将每一行数据转为数组
    for i in range(len(list_file)):
        list_line = list_file[i].split(' ')
        # 将元素由字符串转为float
        list_line = list(map(float, list_line))
        # 向量转矩阵
        list_line = np.array(list_line)
        list_line.resize(3, 4)
        dataset.append(list_line)
        groundtruth.append([list_line[0, 3], list_line[2, 3]])
    # 最后得到两个numpu矩阵，dataset是存放所有真值的矩阵，groundtruth是存放xy真值的矩阵
    dataset = np.array(dataset)
    groundtruth = np.array(groundtruth)

x_data = []
y_data = []
for i in range(len(dataset)):
    x_data.append(float(dataset[i][0, 3]))
    y_data.append(float(dataset[i][2, 3]))

# 绘制
plt.plot(x_data,y_data)
plt.show()


