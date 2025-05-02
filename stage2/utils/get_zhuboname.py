import argparse
import os 

parser = argparse.ArgumentParser(description='传入必要的参数')
parser.add_argument('--video_abs_path', type=str, default="/media/yjc/新加卷/201910/MH丶CICI/201910_MH丶CICI_stage1_remain/MH丶CICI_2019-10-01_13-13_60.2min_2.mp4",
                    help='当前处理mp4的绝对路径')
args = parser.parse_args()

video_abs_path = args.video_abs_path
mp4_name = os.path.basename(video_abs_path)
print(mp4_name.split("_")[0])