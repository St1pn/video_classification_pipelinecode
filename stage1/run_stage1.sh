#!/bin/bash

# 定义要传递给 Python 脚本的参数
base_dir="/home/yjc/Projects/VideoClassify/all_video_frames/"
frame_2_15_30_output_foldername="201910_金水丶张昔由/"
video_dir="/media/yjc/新加卷/201910/金水丶张昔由/2019年10月"
process_num=16

# s1_3
python3 s1_3_extract_30s_from_audiores.py \
    --base_dir "$base_dir" \
    --frame_2_15_30_output_foldername "$frame_2_15_30_output_foldername" \
    --video_dir "$video_dir" \
    --process_num "$process_num"

frame_type="frame30s"
# s1_5
python3 s1_5_filter_maleface.py \
    --base_dir "$base_dir" \
    --frame_2_15_30_output_foldername "$frame_2_15_30_output_foldername" \
    --video_dir "$video_dir" \
    --frame_type "$frame_type"
