"""
Visualizing the localization process for NCLT dataset
"""
import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
from matplotlib.collections import LineCollection

plt.rcParams['font.sans-serif']=['times']
plt.rcParams['mathtext.fontset']='stix'

legend_font = {"size":17,"weight":'bold'}
font1 = {"size":18,"weight":'bold'}

def read_pcd(file_path):
    """使用 open3d 读取 PCD 文件"""
    cloud = o3d.io.read_point_cloud(file_path)
    points = np.asarray(cloud.points)
    return points

def read_positions(csv_file):
    """使用 pandas 读取 CSV 文件中的坐标"""
    df = pd.read_csv(csv_file, header=None)
    x = df.iloc[:, 1].values
    y = df.iloc[:, 2].values
    return x, y

def calculate_distances(query_x, query_y, matched_x, matched_y):
    """计算 query 和 matched 点之间的欧几里得距离"""
    distances = np.sqrt((query_x - matched_x)**2 + (query_y - matched_y)**2)
    return distances

def plot_bev(points, queries, matches, distances, scale=1,output_dir="cmpr_frames"):
    """绘制 BEV 图像，并动态显示 query 和 matched 点以及轨迹"""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    z_coords = points[:, 2]
    
    fig, ax = plt.subplots(figsize=(18, 11))
    scatter = ax.scatter(y_coords * scale, x_coords * scale, c=z_coords, cmap='viridis', s=1)
    
    # plt.title("Bird's Eye View (BEV) of Point Cloud with Query and Matched Points")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    plt.grid(False)
    plt.axis('equal')
    plt.tick_params(axis='both',labelsize=18)
    # cbar = plt.colorbar(scatter, ax=ax)
    # cbar.set_label('Z Coordinate')
    
    # 绘制 query 点和 matched 点
    query_x, query_y = queries
    matched_x, matched_y = matches
    
    # 使用颜色表示距离
    norm = plt.Normalize(distances.min(), 550)
    colors = plt.cm.jet(norm(distances))
    query_plot, = ax.plot([], [], 'ro', markersize=13, label='Query image', zorder=2)  # Query 点在上层
    matched_plot, = ax.plot([], [], 'bo', markersize=18, label='Top-1 matched point cloud', zorder=1)  # Matched 点在下层

    
    # 创建 LineCollection 用于动态更新轨迹颜色
    lines = [((query_y[i] * scale, query_x[i] * scale), (query_y[i+1] * scale, query_x[i+1] * scale)) for i in range(len(query_x) - 1)]
    lc = LineCollection(lines, cmap='jet', norm=norm)
    lc.set_array(distances)
    lc.set_linewidth(6)  # 设置轨迹线宽度为 4
    ax.add_collection(lc)
    
    # 添加距离颜色条
    distance_cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='jet'), ax=ax)
    distance_cbar.set_label('Error Distance',fontdict=font1)
    distance_cbar.ax.tick_params(labelsize=18)  # 设置颜色条刻度的字体大小

    def init():
        matched_plot.set_data([], [])
        query_plot.set_data([], [])
        lc.set_segments([])
        return matched_plot, query_plot, lc
    
    def update(frame):
        matched_plot.set_data(matched_y[frame] * scale, matched_x[frame] * scale)  # 先显示 matched 点
        query_plot.set_data(query_y[frame] * scale, query_x[frame] * scale)  # 后显示 query 点
        
        if frame > 0:
            lc.set_segments([((query_y[i] * scale, query_x[i] * scale), (query_y[i+1] * scale, query_x[i+1] * scale)) for i in range(frame)])
         # 保存当前帧
        plt.savefig(os.path.join(output_dir, f"frame_{frame:04d}.png"))

        return matched_plot, query_plot, lc
    
    ani = animation.FuncAnimation(fig, update, frames=len(query_x), init_func=init, blit=True, interval=200)
    
    plt.legend(prop=legend_font)
    plt.show()




def main():
    pcd_file = "./source_files/merged_cloud_01.pcd"  # 替换为融合后的全局点云文件路径
    query_csv_file = "./source_files/cmpr_query.csv"  # 替换为你的 query CSV 文件路径
    matched_csv_file = "./source_files/cmpr_matched.csv"  # 替换为你的 matched CSV 文件路径
    
    points = read_pcd(pcd_file)
    query_x, query_y = read_positions(query_csv_file)
    matched_x, matched_y = read_positions(matched_csv_file)
    
    distances = calculate_distances(query_x, query_y, matched_x, matched_y)
    
    plot_bev(points, (query_x, query_y), (matched_x, matched_y), distances, scale=1)

if __name__ == "__main__":
    main()
