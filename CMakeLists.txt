# cmake_minimum_required(VERSION 3.1)
# project(CloudMerger)

# set(CMAKE_CXX_FLAGS "-std=c++14")

# set(CMAKE_BUILD_TYPE release)

# find_package(PCL REQUIRED)

# add_executable(merge src/merge.cpp) 
# target_link_libraries(merge ${PCL_LIBRARIES})
cmake_minimum_required(VERSION 3.1)
project(CloudMerger)

# 设置C++标准
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置构建类型为Release
set(CMAKE_BUILD_TYPE Release)

# 查找PCL库
find_package(PCL REQUIRED)

# 查找Boost库
find_package(Boost REQUIRED COMPONENTS filesystem system iostreams)

# 查找OpenCV库
find_package(OpenCV REQUIRED)

# 包含PCL头文件
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

# 包含Boost头文件
include_directories(${Boost_INCLUDE_DIRS})

# 包含OpenCV头文件
include_directories(${OpenCV_INCLUDE_DIRS})

# 源文件
set(SOURCE_FILES src/merge.cpp src/point_cloud.h)

# 生成可执行文件
add_executable(merge ${SOURCE_FILES})

# 链接库
target_link_libraries(merge ${PCL_LIBRARIES} ${Boost_LIBRARIES} ${OpenCV_LIBS})

# 打印一些信息
message(STATUS "PCL_INCLUDE_DIRS: ${PCL_INCLUDE_DIRS}")
message(STATUS "PCL_LIBRARIES: ${PCL_LIBRARIES}")
message(STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")
message(STATUS "OpenCV_INCLUDE_DIRS: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV_LIBS: ${OpenCV_LIBS}")
