"""
Convert point cloud to BEV for KITTI dataset
"""
import numpy as np
import open3d as o3d
import os
import glob
import cv2

def load_kitti_bin_file(bin_file_path):
    """
    加载 KITTI 点云数据的 .bin 文件，并返回点云坐标
    """
    return np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)

def generate_bev_image(points, x_range=(-100, 100), y_range=(-100, 100), resolution=0.1, output_dir='bev_frames', frame_id=0):
    """
    生成一帧点云的 BEV 图像并保存为图片
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 保留前半周的点云数据 (即 -90 度到 90 度)
    angles = np.arctan2(points[:, 1], points[:, 0]) * 180 / np.pi  # 计算每个点的角度 (以度为单位)
    mask = (angles >= -90) & (angles <= 90)
    points = points[mask]

    # 再次裁剪点云数据
    mask = (points[:, 0] >= x_range[0]) & (points[:, 0] <= x_range[1]) & (points[:, 1] >= y_range[0]) & (points[:, 1] <= y_range[1])
    points = points[mask]

    # 计算图像尺寸
    x_min, x_max = x_range
    y_min, y_max = y_range
    width = int((x_max - x_min) / resolution)
    height = int((y_max - y_min) / resolution)

    # 初始化 BEV 图像
    bev_image = np.zeros((height, width, 3), dtype=np.uint8)

    # 转换点云坐标到图像坐标
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    z_coords = points[:, 2]

    img_x = ((x_coords - x_min) / resolution).astype(int)
    img_y = ((y_coords - y_min) / resolution).astype(int)

    # 边界检查，确保索引在有效范围内
    valid_indices = (img_x >= 0) & (img_x < width) & (img_y >= 0) & (img_y < height)
    img_x = img_x[valid_indices]
    img_y = img_y[valid_indices]

    # 绘制点云到 BEV 图像
    bev_image[img_y, img_x, :] = 255

    # 裁剪掉左半边
    half_width = width // 2
    bev_image_cropped = bev_image[:, half_width:]

    # 保存图像
    output_path = os.path.join(output_dir, f"bev_frame_{frame_id:04d}.png")
    cv2.imwrite(output_path, bev_image_cropped)
    print(f"Frame {frame_id} saved to {output_path}")

def process_folder(folder_path, x_range=(-100, 100), y_range=(-100, 100), resolution=0.1):
    """
    批量处理文件夹中的所有 bin 文件
    """
    bin_files = sorted(glob.glob(os.path.join(folder_path, '*.bin')))  # 按名称排序
    for frame_id, bin_file in enumerate(bin_files):
        print(f"Processing file: {bin_file}")
        points = load_kitti_bin_file(bin_file)
        
        # # 可选：使用 Open3D 可视化点云
        # pcd = o3d.geometry.PointCloud()
        # pcd.points = o3d.utility.Vector3dVector(points[:, :3])
        # o3d.visualization.draw_geometries([pcd])
        
        # 生成并保存 BEV 图像
        generate_bev_image(points, x_range=x_range, y_range=y_range, resolution=resolution, frame_id=frame_id)

def main():
    folder_path = "/home/shorwin/work/SemanticKitti/dataset/sequences/source/velodyne"  # 替换为存放 bin 文件的文件夹路径
    process_folder(folder_path)

if __name__ == "__main__":
    main()