import os
from PIL import Image

# 定义源文件夹和目标文件夹路径
source_folder = '/home/shorwin/work/SemanticKitti/dataset/sequences/source/image/Cam'
destination_folder = '/home/shorwin/work/SemanticKitti/dataset/sequences/source/image/Cam1'

# 定义裁剪区域 (left, upper, right, lower)
crop_box = (120, 0, 2840, 200)  # 例如: crop_box = (100, 100, 400, 400)


# 定义新的图像大小
new_size = (1500, 300)  # 例如: new_size = (800, 600)

# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

# 获取源文件夹中的所有 PNG 文件
png_files = [f for f in os.listdir(source_folder) if f.lower().endswith('.png')]

# 遍历每个 PNG 文件并裁剪和调整大小
for png_file in png_files:
    try:
        # 构建完整的文件路径
        source_file_path = os.path.join(source_folder, png_file)
        # 打开 PNG 文件
        with Image.open(source_file_path) as img:
            # 裁剪图像
            cropped_img = img
            # 调整图像大小
            resized_img = cropped_img.resize(new_size, Image.ANTIALIAS)
            # 构建目标文件路径
            destination_file_path = os.path.join(destination_folder, png_file)
            # 保存裁剪和调整大小后的图像
            resized_img.save(destination_file_path, 'PNG')
            print(f"已成功裁剪和调整 {png_file} 的大小并保存到 {destination_folder}")
    except Exception as e:
        print(f"无法处理 {png_file}: {e}")

print("所有文件裁剪和调整大小完成。")

