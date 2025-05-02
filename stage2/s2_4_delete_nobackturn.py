import argparse
import os 
import json
import subprocess


parser = argparse.ArgumentParser(description='传入必要的参数')
parser.add_argument('--keyframe_dir', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/201910_MH丶CICI/keyframes_6s4interval",
                    help='所有图片所在目录')
parser.add_argument('--filtered_mp4_dir', type=str, default="/media/yjc/新加卷/201910/MH丶CICI/201910_MH丶CICI_stage1_remain",
                help='所有图片所在目录')
args = parser.parse_args()

filter_videos = []
keyframe_dir = args.keyframe_dir
for root, dirs, files in os.walk(keyframe_dir):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root, file)) as f:
                all_num = 0
                backturn_num = 0
                for line in f.readlines():
                    line_js = json.loads(line.strip())
                    img_pth = line_js["image_path"]
                    ans = json.loads(line_js["answer"].replace("```json", "").replace("```", "").strip())
                    for k,v in ans.items():
                        if v["back"] == True:
                            backturn_num += 1
                            break 
                    all_num += 1
                if backturn_num < 2:
                    filter_videos.append(os.path.basename(root))
print("filter_videos len: ", len(filter_videos))
filtered_mp4_dir = args.filtered_mp4_dir
for mp4 in filter_videos:
    command = ['mv', os.path.join(os.path.dirname(filtered_mp4_dir), mp4)+".mp4", filtered_mp4_dir]
    result = subprocess.run(command, check=True)

                    
