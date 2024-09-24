"""
根据索引复制对应的文件
"""
import shutil
import os

# 定义文件路径和文件夹路径
distance_file = 'cmpr.txt'
source_folder_query = '/media/shorwin/Shorwin/NCLT/data/2012-02-05/image/Cam'
query_destination_folder = '/media/shorwin/Shorwin/NCLT/data/2012-02-05/source2/image/Cam'

source_folder_matched = '/home/shorwin/work/NCLT/data/2012-01-08/lidar/depth'
matched_destination_folder = '/media/shorwin/Shorwin/NCLT/data/2012-02-05/source2/lidar/depth'

# 确保目标文件夹存在
os.makedirs(query_destination_folder, exist_ok=True)
os.makedirs(matched_destination_folder, exist_ok=True)

# 读取 distance 数据
query_indices = []
matched_indices = []
with open(distance_file, 'r') as file:
    for line in file:
        if line.startswith('query index'):
            parts = line.strip().split(', ')
            query_index_str = parts[0].split(': ')[1]
            matched_index_str = parts[1].split(': ')[1]
            query_indices.append(int(query_index_str))
            matched_indices.append(int(matched_index_str))

# 获取源文件夹中的所有文件
all_query_files = sorted(os.listdir(source_folder_query))  # 确保文件按顺序排列
all_matched_files = sorted(os.listdir(source_folder_matched))  # 确保文件按顺序排列

# 根据 query index 复制并重命名对应的图片
for query_index in query_indices:
    try:
        # 文件名应该是按 query index 排序的第 n 个文件
        filename = all_query_files[query_index]
        source_file = os.path.join(source_folder_query, filename)
        file_extension = os.path.splitext(filename)[1]  # 获取文件后缀
        new_filename = f"{query_index}{file_extension}"
        destination_file = os.path.join(query_destination_folder, new_filename)
        shutil.copy2(source_file, destination_file)
        print(f"已复制并重命名 {filename} 为 {new_filename} 到 {query_destination_folder}")
    except IndexError:
        print(f"警告: 源文件夹中没有足够的文件来匹配 query index {query_index}")

# 根据 matched index 复制并重命名对应的图片
for query_index, matched_index in zip(query_indices, matched_indices):
    try:
        # 文件名应该是按 matched index 排序的第 n 个文件
        filename = all_matched_files[matched_index]
        source_file = os.path.join(source_folder_matched, filename)
        file_extension = os.path.splitext(filename)[1]  # 获取文件后缀
        new_filename = f"{query_index}_{matched_index}{file_extension}"
        destination_file = os.path.join(matched_destination_folder, new_filename)
        shutil.copy2(source_file, destination_file)
        print(f"已复制并重命名 {filename} 为 {new_filename} 到 {matched_destination_folder}")
    except IndexError:
        print(f"警告: 源文件夹中没有足够的文件来匹配 matched index {matched_index}")

print("文件复制和重命名完成。")