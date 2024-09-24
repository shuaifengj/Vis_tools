import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation

plt.rcParams['font.sans-serif']=['times']
plt.rcParams['mathtext.fontset']='stix'

legend_font = {"size":16,"weight":'bold'}
font1 = {"size":16,"weight":'bold'}

def read_pcd(file_path):
    """使用 open3d 读取 PCD 文件"""
    cloud = o3d.io.read_point_cloud(file_path)
    points = np.asarray(cloud.points)
    return points

def read_positions(file_path):
    """读取 poses.txt 文件并提取位姿信息"""
    with open(file_path) as f:
        lines = f.readlines()
    
    poses = []
    groundtruth = []
    
    for line in lines:
        values = list(map(float, line.split()))
        pose = np.array(values).reshape(3, 4)
        poses.append(pose)
        groundtruth.append([pose[0, 3], pose[2, 3]])
    
    poses = np.array(poses)
    groundtruth = np.array(groundtruth)
    x = groundtruth[:, 0]
    y = groundtruth[:, 1]

    return x, y
    

def plot_bev(points, queries, matches, scale=1, output_dir="cmpr_frames"):
    """绘制 BEV 图像，并动态显示 query 和 matched 点以及轨迹"""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    x_coords = points[:, 0]
    y_coords = points[:, 2]
    z_coords = points[:, 1]
    
    fig, ax = plt.subplots(figsize=(10, 10))
    scatter = ax.scatter(x_coords * scale, y_coords * scale, c=z_coords, cmap='viridis', s=1)
    
    plt.grid(False)
    plt.axis('equal')
    plt.tick_params(axis='both', labelsize=14)

    # 绘制 query 点和 matched 点
    query_x, query_y = queries
    matched_x, matched_y = matches
    
    query_plot, = ax.plot([], [], 'ro', markersize=10, label='Query image', zorder=2)  # Query 点在上层
    matched_plot, = ax.plot([], [], 'bo', markersize=17, label='Top-1 matched point cloud', zorder=1)  # Matched 点在下层

    def init():
        matched_plot.set_data([], [])
        query_plot.set_data([], [])
        return matched_plot, query_plot
    
    def update(frame):
        matched_plot.set_data(matched_x[frame] * scale, matched_y[frame] * scale)  # 先显示 matched 点
        query_plot.set_data(query_x[frame] * scale, query_y[frame] * scale)  # 后显示 query 点

        # 保存当前帧
        plt.savefig(os.path.join(output_dir, f"frame_{frame:04d}.png"))

        return matched_plot, query_plot
    
    ani = animation.FuncAnimation(fig, update, frames=len(query_x), init_func=init, blit=True, interval=200)
    
    plt.legend(prop=legend_font)
    plt.show()

def main():
    pcd_file = "./source_files/kitti.pcd"  # 替换为你的 PCD 文件路径
    query_csv_file = "./source_files/cmpr_query_kitti.txt"  # 替换为你的 query CSV 文件路径
    matched_csv_file = "./source_files/cmpr_matched_kitti.txt"  # 替换为你的 matched CSV 文件路径
    
    points = read_pcd(pcd_file)
    query_x, query_y = read_positions(query_csv_file)
    matched_x, matched_y = read_positions(matched_csv_file)
    
    plot_bev(points, (query_x, query_y), (matched_x, matched_y), scale=1)

if __name__ == "__main__":
    main()