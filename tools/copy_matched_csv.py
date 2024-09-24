import csv

# 读取匹配的索引
def read_matched_indices(txt_file):
    matched_indices = []
    with open(txt_file, 'r') as file:
        for line in file:
            if 'matched index' in line:
                parts = line.split(',')
                matched_index = int(float(parts[1].split(':')[1].strip()))+3001
                matched_indices.append(matched_index)
    return matched_indices

# 从CSV文件中提取对应的行并写入到新的CSV文件中
def extract_rows_from_csv(csv_file, matched_indices, output_csv_file):
    matched_rows = []
    
    # 读取整个CSV文件到一个列表中，以便后续按索引访问
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        all_rows = list(reader)
    
    # 根据 matched_indices 提取对应的行
    for index in matched_indices:
        if index < len(all_rows):  # 确保索引不超出范围
            matched_rows.append(all_rows[index])
    
    # 写入新的CSV文件
    with open(output_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matched_rows)
    
    print(f"已将匹配的行写入到 {output_csv_file}")
# 定义文件路径
txt_file = 'cmpr_00.txt'  # 替换为实际的txt文件路径
csv_file = '/home/shorwin/work/SemanticKitti/dataset/poses/00.txt'           # 替换为实际的csv文件路径
output_csv_file = 'cmpr_matched.csv'    # 替换为实际的输出csv文件路径

# 读取匹配的索引
matched_indices = read_matched_indices(txt_file)

# 从CSV文件中提取对应的行并写入到新的CSV文件中
extract_rows_from_csv(csv_file, matched_indices, output_csv_file)
