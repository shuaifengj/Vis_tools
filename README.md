# Vis_tools
Visualization of KITTI and NCLT datasets.

# Usage
1.Merge LiDAR point clouds to a global map with known poses on KITTI odometry dataset.
```bash
cd Vis_tools
mkdir build
cd build
cmake ..
make
./merge
```

![image](./assets/kitti.png)

2.Merge LiDAR point clouds to a global map with known poses on NCLT dataset.
```bash
python NCLT_CloudMerge.py
```
![image](./assets/nclt.png)

3.Visualization of localization process on KITTI dataset.
```bash
python Vis_localization_KITTI.py
```
![image](./assets/kitti_loc.png)

4.Visualization of localization process on NCLT dataset.
```bash
python Vis_localization_NCLT.py
```
![image](./assets/nclt_loc.png)

5.Convert point cloud to on KITTI dataset.
```bash
python point_cloud2bev_KITTI.py
```
![image](./assets/bev_KITTI.png)

