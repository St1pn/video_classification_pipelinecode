# 选出正例video和正例图片样本
import json 
import os 
import re



# stage1 所有label汇总
# 形式：
# {video_name: {mp3_label: xx, label_cloth: xx, ...}}
stage1_labels_all = {}


# 解析mp3_label(audio res)
mp3_label_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_mp3/mp3_label.txt"
res_videos = {}
with open(mp3_label_path) as f:
    c = 0
    for line in f.readlines():

        try:
            resp_sta = line.index("response:")
            resp_str = line.strip()[resp_sta+9: ]
            filename = line.strip()[5:resp_sta].strip()
            filename = filename.split("_window")[0].replace("_", "%")
        except:
            print(c)
            continue 
        try:
            line_js = json.loads(resp_str.strip().replace("\\", ""))
            # 文件名称处理
            beat, bpm = line_js["beat"]["pattern"], line_js["beat"]["bpm"]
            if float(bpm.lower().replace("bpm","").strip()) <= 90:
                if filename not in res_videos:
                    res_videos[filename] = [1,0]  # 0号元素、1号元素分别为<=90、>90的片段个数
                else:
                    res_videos[filename][0] = res_videos[filename][0] + 1
            else:
                if filename not in res_videos:
                    res_videos[filename] = [0,1]  # 0号元素、1号元素分别为<=90、>90的片段个数
                else:
                    res_videos[filename][1] = res_videos[filename][1] + 1
        except:
            pattern = r'\d+\.\d+'
            match = re.search(pattern, resp_str)
            if match:
                # 获取匹配到的数字部分
                number = match.group()
                if float(number) <= 90:
                    if filename not in res_videos:
                        res_videos[filename] = [1,0]  # 0号元素、1号元素分别为<=90、>90的片段个数
                    else:
                        res_videos[filename][0] = res_videos[filename][0] + 1
                else:
                    if filename not in res_videos:
                        res_videos[filename] = [0,1]  # 0号元素、1号元素分别为<=90、>90的片段个数
                    else:
                        res_videos[filename][1] = res_videos[filename][1] + 1
            else:
                print("json parse err: ", c, "###resp_str: ", resp_str)
        
        c += 1
print(len(res_videos))
for k, v in res_videos.items():
    if k not in stage1_labels_all:
        stage1_labels_all[k] = {"mp3_label": v}
    else:
        stage1_labels_all[k]["mp3_label"] = v
print(len(stage1_labels_all))

# 校验mp3是否==全部mp4，将漏掉没预测的video，人工校验的需要单独维护一个txt
mp3filtered_videos_path = ""
# mp3filtered_videos_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/201910_anni_whitelist_mp3filtered_videos.txt"
# with open(mp3filtered_videos_path, "w") as f:
#     for root, dirs, files in os.walk("/media/yjc/新加卷/201910/安妮/2019年10月"):
#         for file in files:
#             if file.endswith(".mp4") and ("baidu" not in file):
#                 if file[:-4] not in res_videos:
#                     f.write(file + "\n")
# # # 过滤掉的video人工校验，比如：
# # QLAN%2019-10-01%02-57%19%9min%1.mp4 1
# # QLAN%2019-10-07%23-37%60%3min%3.mp4 1
# # QLAN%2019-10-07%23-37%60%3min%4.mp4 1 
# # QLAN%2019-10-08%01-38%60%3min%0.mp4 1
# # QLAN%2019-10-08%01-38%60%3min%1.mp4 1
# # QLAN%2019-10-08%22-37%60%3min%0.mp4 1
# # QLAN%2019-10-08%22-37%60%3min%1.mp4 1
# # QLAN%2019-10-07%23-37%60%3min%0.mp4 1
# # QLAN%2019-10-07%23-37%60%3min%2.mp4 1
# # QLAN%2019-10-01%02-57%19%9min%0.mp4 0


# 解析label_cloth
res_videos_bs = {}
label_black_stockings_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_cloth/label_black_stockings.txt"
with open(label_black_stockings_path) as f:
    for line in f.readlines():
        try:
            line_js = json.loads(line.strip())
            resp_str = line_js["Assistant"].lower()
            img_name = line_js["image_name"]
            video_name = img_name.split("resize512_")[1][:-11]
            if resp_str.startswith("yes"):
                if video_name not in res_videos_bs:
                    res_videos_bs[video_name] = [1,1]
                else:
                    res_videos_bs[video_name][0] = res_videos_bs[video_name][0] + 1
                    res_videos_bs[video_name][1] = res_videos_bs[video_name][1] + 1
            else:
                if video_name not in res_videos_bs:
                    res_videos_bs[video_name] = [0,1]
                else:
                    res_videos_bs[video_name][1] = res_videos_bs[video_name][1] + 1
        except:
            print(line)
            continue
print(len(res_videos_bs))

res_videos_other_target_cloth = {}
label_clothing_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_cloth/label_cloth.txt"
all_target_clothing_type = []
with open(label_clothing_path) as f:
    for line in f.readlines():
        try:
            line_js = json.loads(line.strip())
            resp_str = line_js["Assistant"].lower()
            if "none of them" not in resp_str:
                img_name = os.path.basename(line_js["image_name"])
                video_name = img_name.split("resize512_")[1][:-11]
                clothing_type = resp_str[1:-1] if resp_str[0] == "[" else resp_str[0:-1]
                if video_name not in res_videos_other_target_cloth:
                    res_videos_other_target_cloth[video_name] = {clothing_type: 1}
                else:
                    if clothing_type not in res_videos_other_target_cloth[video_name]:
                        res_videos_other_target_cloth[video_name][clothing_type] = 1
                    else:
                        res_videos_other_target_cloth[video_name][clothing_type] += 1
            else:
                img_name = os.path.basename(line_js["image_name"])
                video_name = img_name.split("resize512_")[1][:-11]
                clothing_type = "none of them"
                if video_name not in res_videos_other_target_cloth:
                    res_videos_other_target_cloth[video_name] = {clothing_type: 1}
                else:
                    if clothing_type not in res_videos_other_target_cloth[video_name]:
                        res_videos_other_target_cloth[video_name][clothing_type] = 1
                    else:
                        res_videos_other_target_cloth[video_name][clothing_type] += 1
        except:
            print(line)  # 别看看左右觉得怎么老天给你的都是那么消极的东西，因为你就正站在最积极的位置。
            continue
print(len(res_videos_other_target_cloth)) 

    






