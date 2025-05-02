#!/bin/bash


# base_dir="/home/yjc/Projects/VideoClassify/all_video_frames/"
# frame_2_15_30_output_foldername="201910_金水丶张昔由_stage2/"
# # video_dir="/media/yjc/新加卷/201910/金水丶张昔由/2019年10月"
# video_dir="/media/yjc/新加卷/201910/金水丶张昔由/201910_金水丶张昔由_stage1_remain"
# process_num=16
# # s2_1_exact_2s
# python3 s2_1_extract_2s_30s_from_s1.py \
#     --base_dir "$base_dir" \
#     --frame_2_15_30_output_foldername "$frame_2_15_30_output_foldername" \
#     --video_dir "$video_dir" \
#     --process_num "$process_num"


# partial_inferred_res_path="/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group5_thigh_calf_back_dance.txt_"
# input_imgs_path="/home/yjc/Projects/VideoClassify/all_video_frames/201910_鲸夕bingo_stage2/frame30s"
# infer_res_path="/home/yjc/Projects/VideoClassify/all_video_frames/201910_鲸夕bingo_stage2/infer_res_clothtype.txt"
# # s2_1_infer_clothtype
# python3 s2_1_infer_internvl38B_multigpus_frame30s_clothing_api.py \
#     --partial_inferred_res_path "$partial_inferred_res_path" \
#     --input_imgs_path "$input_imgs_path" \
#     --infer_res_path "$infer_res_path" 




# 遍历目录下的所有MP4文件
all_video_zhubo_dir="/media/yjc/新加卷/201910"
find "$all_video_zhubo_dir" -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' dir; do
    # 提取目录名称
    cur_zhubo_dir_name=$(basename "$dir")
    echo "$cur_zhubo_dir_name"

    if [ -f "$all_video_zhubo_dir/$cur_zhubo_dir_name/s2_filtered_flag.txt" ]; then
        echo "目录 $all_video_zhubo_dir/$cur_zhubo_dir_name 下存在 s2_filtered_flag.txt，跳过。"
        continue
    fi

    for file in "$all_video_zhubo_dir/$cur_zhubo_dir_name"/*/*.mp4; do
        if [ -f "$file" ]; then
            # 获取绝对路径
            absolute_path=$(realpath "$file")
            # 获取文件名
            file_name=$(basename "$file")
            echo "绝对路径: $absolute_path"
            echo "文件名: $file_name"
            
            zhubo_name=$(python3 /home/yjc/Projects/VideoClassify/pipeline_code/stage2/utils/get_zhuboname.py \
                --video_abs_path "$absolute_path")
            mp4_name="${absolute_path%????}"
            mp4_name="$(basename "$mp4_name")"
            echo "$zhubo_name"
            echo "$mp4_name"

            filtered_dir=$(dirname "$absolute_path")/filtered_mp4
            if [ -d "$filtered_dir" ]; then
                echo "目录 $filtered_dir 已存在。"
            else
                # 使用mkdir命令创建目录
                mkdir -p "$filtered_dir"
                echo "目录 $filtered_dir 不存在，已成功创建。"
            fi

            
            output_f=/home/yjc/Projects/VideoClassify/all_video_frames/201910_$zhubo_name/keyframes_6s4interval/$mp4_name
            if [ -d "$output_f" ]; then
                echo ">>>>>output_folder $output_f 已存在。跳过"
                continue
            fi

            # kmeans聚类出关键帧
            python3 /home/yjc/Projects/VideoClassify/pipeline_code/stage2/kmeans_keyframe_analyse.py \
                --video_path "$absolute_path" \
                --output_folder "/home/yjc/Projects/VideoClassify/all_video_frames/201910_$zhubo_name/keyframes_6s4interval/$mp4_name"
            # if [ $? -eq 1 ]; then
            #     echo "output_folder 已经存在 跳过"
            #     continue
            # fi

            # 对关键帧进行身体position预测
            partial_inferred_res_path1="/home/yjc/Projects/VideoClassify/all_video_frames/201910_Sun佐伊/keyfram_"
            input_imgs_path1="/home/yjc/Projects/VideoClassify/all_video_frames/201910_$zhubo_name/keyframes_6s4interval/$mp4_name"
            infer_res_path1="/home/yjc/Projects/VideoClassify/all_video_frames/201910_$zhubo_name/keyframes_6s4interval/$mp4_name/infer_res_pose.txt"
            python3 s2_3_api_thigh_calf_back_dance.py \
                --partial_inferred_res_path "$partial_inferred_res_path1" \
                --input_imgs_path "$input_imgs_path1" \
                --infer_res_path "$infer_res_path1" 

            # 对backturn==true小于阈值的视频进行删除
            keyframe_dir="/home/yjc/Projects/VideoClassify/all_video_frames/201910_$zhubo_name/keyframes_6s4interval/$mp4_name"
            python3 s2_4_delete_nobackturn.py \
                --keyframe_dir "$keyframe_dir" \
                --filtered_mp4_dir "$filtered_dir"

            # 对预测出的backturn==true的以及漏掉的目标帧，在视频中人工定位帧范围，人工截取出帧范围中的图片
        fi
        echo "################process finished################"
    done
    touch "$all_video_zhubo_dir/$cur_zhubo_dir_name/s2_filtered_flag.txt"
    # break
done


