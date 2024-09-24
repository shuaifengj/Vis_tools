import csv
import numpy as np

# 读取 ground truth 数据
query_data = []
match_data = []

with open('/media/shorwin/Shorwin/NCLT/data/ground_truth/groundtruth_2012-02-05.csv', 'r') as file:
    reader = csv.reader(file)
    # next(reader)  # 跳过header行，如果有header的话
    for row in reader:
        query_data.append([float(row[1]), float(row[2])])  # 假设第2和第3列是 x 和 y
print(len(query_data))

with open('/media/shorwin/Shorwin/NCLT/data/ground_truth/groundtruth_2012-01-08.csv', 'r') as file:
    reader = csv.reader(file)
    # next(reader)  # 跳过header行，如果有header的话
    for row in reader:
        match_data.append([float(row[1]), float(row[2])])  # 假设第2和第3列是 x 和 y
print(len(match_data))
# 读取 query 和 matched 的索引文件
query_indices = []
matched_indices = []
with open('cmpr_2012-02-05.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(', ')
        query_index = int(parts[0].split(': ')[1])
        matched_index = int(parts[1].split(': ')[1])
        query_indices.append(query_index)
        matched_indices.append(matched_index)
print(len(query_indices))
print(len(matched_indices))

# 计算欧几里得距离
distances = []
result_lines = []
for q_idx, m_idx in zip(query_indices, matched_indices):
    if q_idx < len(query_data) and m_idx < len(match_data):
        query_point = np.array(query_data[q_idx])  # 提取 x 和 y
        match_point = np.array(match_data[m_idx])  # 提取 x 和 y
        distance = np.linalg.norm(query_point - match_point)  # 计算欧几里得距离
        distances.append(distance)
        result_lines.append(f'query index: {q_idx}, matched index: {m_idx}, distance: {distance}\n')
    else:
        print(f'Skipping invalid indices - query index: {q_idx}, matched index: {m_idx}')

# 将结果写入到一个txt文件中
output_filepath = 'cmpr_distances_result.txt'
with open(output_filepath, 'w') as output_file:
    output_file.writelines(result_lines)

print(f'Results have been written to {output_filepath}')

