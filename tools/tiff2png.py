import os
from PIL import Image

# 定义源文件夹和目标文件夹路径
source_folder = '/media/shorwin/Shorwin/NCLT/data/2012-02-05/source2/image/Cam'
destination_folder = '/media/shorwin/Shorwin/NCLT/data/2012-02-05/source2/image/Cam1'


# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

# 获取源文件夹中的所有 TIFF 文件
tiff_files = [f for f in os.listdir(source_folder) if f.lower().endswith('.tiff') or f.lower().endswith('.tif')]

# 遍历每个 TIFF 文件并转换为 PNG 格式
for tiff_file in tiff_files:
    try:
        # 构建完整的文件路径
        source_file_path = os.path.join(source_folder, tiff_file)
        # 打开 TIFF 文件
        with Image.open(source_file_path) as img:
            # 检查图像模式并转换为 L 或 RGB 模式
            if img.mode == 'F':
                img = img.convert('L')  # 转换为 8-bit 像素
            # 构建目标文件路径
            png_filename = os.path.splitext(tiff_file)[0] + '.png'
            destination_file_path = os.path.join(destination_folder, png_filename)
            # 保存为 PNG 格式
            img.save(destination_file_path, 'PNG')
            print(f"已成功将 {tiff_file} 转换为 {png_filename}")
    except Exception as e:
        print(f"无法转换 {tiff_file}: {e}")

print("所有文件转换完成。")
