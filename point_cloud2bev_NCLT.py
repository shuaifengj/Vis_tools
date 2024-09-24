"""
Convert point cloud to BEV for NCLT dataset
"""
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import os
import glob

# 定义数据类型
data_type = np.dtype({
    'x': ('<u2', 0),
    'y': ('<u2', 2),
    'z': ('<u2', 4),
    'i': ('u1', 6),
    'l': ('u1', 7)})

def data2xyzi(data, flip=True):
    """将二进制数据转换为点云坐标和强度"""
    xyzil = data.view(data_type)
    xyz = np.hstack(
        [xyzil[axis].reshape([-1, 1]) for axis in ['x', 'y', 'z']])
    xyz = xyz * 0.005 - 100.0

    if flip:
        R = np.eye(3)
        R[2, 2] = -1
        xyz = np.matmul(xyz, R)
    return xyz, xyzil['i']

def plot_bev(points, scale=1, output_dir='bev_frames', frame_id=0):
    """绘制一帧点云的 BEV 图像并保存为图片"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    z_coords = points[:, 2]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(x_coords * scale, y_coords * scale, c=z_coords, cmap='viridis', s=1)
    
    # 去掉坐标轴和网格线
    ax.axis('off')
    
    # 保存图像
    output_path = os.path.join(output_dir, f"bev_frame_{frame_id:04d}.png")
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close(fig)
    print(f"Frame {frame_id} saved to {output_path}")

def process_folder(folder_path):
    """批量处理文件夹中的所有 bin 文件"""
    bin_files = glob.glob(os.path.join(folder_path, '*.bin'))
    for frame_id, bin_file in enumerate(bin_files):
        print(f"Processing file: {bin_file}")
        data = np.fromfile(bin_file)
        points, intensities = data2xyzi(data)
        
        # # 使用 Open3D 可视化点云
        # pcd = o3d.geometry.PointCloud()
        # pcd.points = o3d.utility.Vector3dVector(points)
        # o3d.visualization.draw_geometries([pcd])
        
        # 绘制并保存 BEV
        plot_bev(points, frame_id=frame_id)



def main():
    folder_path = "/media/shorwin/Shorwin/NCLT/data/2012-02-05/source2/velodyne/matched"  # 替换为存放 bin 文件的文件夹路径
    process_folder(folder_path)

if __name__ == "__main__":
    main()
