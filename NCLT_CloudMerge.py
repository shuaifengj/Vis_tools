"""
Merging point clouds into a global point clohd for NCLT dataset
"""
import os
import numpy as np
import pandas as pd
import open3d as o3d
from tqdm import tqdm

data_type = np.dtype({
    'x': ('<u2', 0),
    'y': ('<u2', 2),
    'z': ('<u2', 4),
    'i': ('u1', 6),
    'l': ('u1', 7)})

def data2xyzi(data, flip=True):
    xyzil = data.view(data_type)
    xyz = np.hstack(
        [xyzil[axis].reshape([-1, 1]) for axis in ['x', 'y', 'z']])
    xyz = xyz * 0.005 - 100.0

    if flip:
        R = np.eye(3)
        R[2, 2] = -1
        xyz = np.matmul(xyz, R)
    return xyz, xyzil['i']

def read_ground_truth(pose_file):
    df = pd.read_csv(pose_file, header=None)
    poses = []
    for index, row in df.iterrows():
        timestamp, x, y, z, roll, pitch, yaw = row
        transform = create_transformation_matrix(x, y, z, roll, pitch, yaw)
        poses.append(transform)
    return poses

def create_transformation_matrix(x, y, z, roll, pitch, yaw):
    # 创建4x4的变换矩阵
    transform = np.eye(4)
    
    # 使用Euler角计算旋转矩阵
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    rotation = R_z @ R_y @ R_x
    transform[:3, :3] = rotation
    transform[:3, 3] = [x, y, z]
    
    return transform

def read_point_cloud(file_path):
    data = np.fromfile(file_path, dtype=np.uint8)
    points = data2xyzi(data)[0]
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

def transform_point_cloud(cloud, transform):
    return cloud.transform(transform)

def pointDepth(p):
    depth = np.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
    return depth

def depthCrop(pc, depth_threshold, height_threshold):
    points = np.asarray(pc.points)
    mask = (np.apply_along_axis(pointDepth, 1, points) <= depth_threshold) & (points[:, 2] <= height_threshold)
    cropped_points = points[mask]
    cropped_pc = o3d.geometry.PointCloud()
    cropped_pc.points = o3d.utility.Vector3dVector(cropped_points)
    return cropped_pc

def merge_point_clouds(cloud_folder, pose_file, depth_threshold, height_threshold):
    cloud_files = [f for f in os.listdir(cloud_folder) if f.endswith('.bin')]
    cloud_files.sort()
    poses = read_ground_truth(pose_file)
    
    if len(poses) != len(cloud_files):
        raise ValueError("The number of poses and point clouds do not match!")
    
    global_map = o3d.geometry.PointCloud()
    
    for i in tqdm(range(0, len(cloud_files), 20), desc="Processing point clouds"):
        cloud_path = os.path.join(cloud_folder, cloud_files[i])
        cloud = read_point_cloud(cloud_path)
        
        # 裁剪点云
        cloud = depthCrop(cloud, depth_threshold, height_threshold)
        
        # 变换点云
        transformed_cloud = transform_point_cloud(cloud, poses[i])
        
        # 合并到全局点云
        global_map += transformed_cloud
    
    # 体素下采样以减少点云数据量和噪声
    voxel_size = 1.5
    global_map = global_map.voxel_down_sample(voxel_size)
    
    return global_map

def main():
    cloud_folder = '/mnt/data/nclt/data/velodyne_data/2012-01-08_vel/velodyne_sync'
    pose_file = '/mnt/data/nclt/data/ground_truth/groundtruth_2012-01-08.csv'
    
    # 定义裁剪深度阈值和高度阈值，例如 50.0 和 1.5 (根据需要调整)
    depth_threshold = 50.0
    height_threshold = 40
    
    merged_cloud = merge_point_clouds(cloud_folder, pose_file, depth_threshold, height_threshold)
    
    # 保存合并后并裁剪的点云
    o3d.io.write_point_cloud("merged_cloud_01.pcd", merged_cloud)
    print("Cropped merged point cloud saved")
    
    # 可视化合并后并裁剪的点云
    o3d.visualization.draw_geometries([merged_cloud])

if __name__ == "__main__":
    main()