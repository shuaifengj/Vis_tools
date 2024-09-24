import csv

# 定义文件路径
ground_truth_file = '/media/shorwin/Shorwin/NCLT/data/ground_truth/groundtruth_2012-02-05.csv'
distance_file = 'modalink_distances_result.txt'
output_file = 'modalink_with_distances.csv'

# 读取 ground truth 数据
ground_truth_data = []
with open(ground_truth_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        ground_truth_data.append(row)

# 读取 distance 数据
distances = []
with open(distance_file, 'r') as file:
    for line in file:
        parts = line.strip().split(', ')
        distance_str = parts[2].split(': ')[1]
        distances.append(distance_str)

# 确认大小一致
if len(ground_truth_data) != len(distances):
    print(f"行数不匹配：ground truth 有 {len(ground_truth_data)} 行，distance 有 {len(distances)} 行。")
else:
    # 添加 distance 列
    for row, distance in zip(ground_truth_data, distances):
        row.append(distance)

    # 写入到新的 CSV 文件中
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(ground_truth_data)

    print(f"已将结果写入到 {output_file}")
