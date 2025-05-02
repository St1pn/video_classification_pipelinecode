import json
import os 


res_videos_bs = {}
label_black_stockings_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_black_stockings.txt"
with open(label_black_stockings_path) as f:
    for line in f.readlines():
        try:
            line_js = json.loads(line.strip())
            resp_str = line_js["Assistant"].lower()
            if resp_str.startswith("yes,"):
                img_name = line_js["image_name"]
                video_name = img_name.split("resize512_")[1][:-11]
                if video_name not in res_videos_bs:
                    res_videos_bs[video_name] = 1
                else:
                    res_videos_bs[video_name] += 1
        except:
            print(line)
            continue
print(len(res_videos_bs))

res_videos_other_targets = {}
label_clothing_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_clothing.txt"
all_target_clothing_type = []
with open(label_clothing_path) as f:
    for line in f.readlines():
        try:
            line_js = json.loads(line.strip())
            resp_str = line_js["Assistant"].lower()
            if "none of them" not in resp_str:
                img_name = os.path.basename(line_js["image_name"])
                video_name = img_name.split("resize512_")[1][:-11]
                clothing_type = resp_str[1:-1]  
                if video_name not in res_videos_other_targets:
                    res_videos_other_targets[video_name] = {clothing_type: 1}
                else:
                    if clothing_type not in res_videos_other_targets[video_name]:
                        res_videos_other_targets[video_name][clothing_type] = 1
                    else:
                        res_videos_other_targets[video_name][clothing_type] += 1
            else:
                img_name = os.path.basename(line_js["image_name"])
                video_name = img_name.split("resize512_")[1][:-11]
                clothing_type = "none of them"
                if video_name not in res_videos_other_targets:
                    res_videos_other_targets[video_name] = {clothing_type: 1}
                else:
                    if clothing_type not in res_videos_other_targets[video_name]:
                        res_videos_other_targets[video_name][clothing_type] = 1
                    else:
                        res_videos_other_targets[video_name][clothing_type] += 1

        except:
            print(line)  # 别看看左右觉得怎么老天给你的都是那么消极的东西，因为你就正站在最积极的位置。
            continue
print(len(res_videos_other_targets)) 


# 除了"baiduyun"，全量videos里，均不在res_videos_bs、res_videos_other_targets这两个预测结果中的那些video，理论上应该全都在才对，原因待查
allv_notin_bs_tarcloth_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/201910_anni_allv_notin_bs_tarcloth.txt"
with open(allv_notin_bs_tarcloth_path, "w") as f:
    for root, dirs, files in os.walk("/media/yjc/新加卷/201910/安妮/2019年10月"):
        for file in files:
            if file.endswith(".mp4") and ("baidu" not in file):
                if not((file[:-4] in res_videos_other_targets) or (file[:-4] in res_videos_bs)):
                    f.write(file+"\n")
