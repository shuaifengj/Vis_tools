# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # 读取CSV文件
# data = pd.read_csv('updated_ground_truth.csv', header=None)
# x = data[1]  # x坐标数据
# y = data[2]  # y坐标数据
# error = data[7]  # 误差值数据

# # 将误差值归一化到[0, 1]区间
# norm_error = (error - np.min(error)) / (np.max(error) - np.min(error))

# # 绘制轨迹图，使用Viridis伪彩色
# plt.scatter(y, x, c=norm_error, cmap='viridis', s=50)  # s为点的大小
# plt.colorbar(label='Error')  # 添加颜色条
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Trajectory with Error Visualization (Viridis)')

# # 标注每隔100个点的序号
# interval = 100
# for i in range(0, len(x), interval):
#     plt.annotate(str(i), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV文件
data = pd.read_csv('modalink_with_distances.csv', header=None)
x = data[1]  # x坐标数据
y = data[2]  # y坐标数据
error = data[7]  # 误差值数据

# 将误差值归一化到[0, 1]区间
norm_error = (error - np.min(error)) / (np.max(error) - np.min(error))

# 绘制轨迹图，使用Viridis伪彩色
plt.scatter(y, x, c=norm_error, cmap='viridis', s=50)  # s为点的大小
# plt.colorbar(label='Error')  # 添加颜色条
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Trajectory with Error Visualization (Viridis)')

# 标注每隔100个点的序号，并将这些点标记为红色
interval = 100
for i in range(0, len(x), interval):
    plt.scatter(y[i], x[i], color='red', s=100)  # 用红色标记点
    plt.annotate(str(i), (y[i], x[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')

plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # 读取CSV文件
# data = pd.read_csv('cmpr.csv', header=None)
# x = data[1]  # x坐标数据
# y = data[2]  # y坐标数据
# error = data[7]  # 误差值数据

# # 将误差值归一化到[0, 1]区间
# norm_error = (error - np.min(error)) / (np.max(error) - np.min(error))

# # 筛选出误差小于等于10的点
# mask = error <= 10
# x_filtered = x[mask].reset_index(drop=True)
# y_filtered = y[mask].reset_index(drop=True)
# norm_error_filtered = norm_error[mask].reset_index(drop=True)

# # 绘制轨迹图，使用Viridis伪彩色
# plt.scatter(y_filtered, x_filtered, c=norm_error_filtered, cmap='viridis', s=50)  # s为点的大小
# plt.colorbar(label='Error')  # 添加颜色条
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Trajectory with Error Visualization (Viridis)')

# # 标注每隔100个点的序号，并将这些点标记为红色
# interval = 100
# for i in range(0, len(x_filtered), interval):
#     plt.scatter(y_filtered.iloc[i], x_filtered.iloc[i], color='red', s=100)  # 用红色标记点
#     plt.annotate(str(i), (y_filtered.iloc[i], x_filtered.iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')

# plt.show()


