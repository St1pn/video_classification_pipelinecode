from openai import OpenAI
import os
import base64
import time
from tqdm import tqdm 
import json
import random
import argparse
import base64
import multiprocessing
from openai import OpenAI


"""请求qwenl-plus-latest的api接口, 判断图片中是否正在跳舞或者扭动身体、是否能看到背部、大腿/小腿"""
from openai import OpenAI
import os
import base64
import time
from tqdm import tqdm 
import json
import random


# #  base 64 编码格式
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")
# # q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calves: true if knee-to-ankle area visible.Back turned: true if spine faces viewer.Dance/twist: true if she is actively dancing or rhythmically twisting her body.Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool ,dance:bool },...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
# q = """Analyze the provided live stream screenshot and answer the following three questions with only "yes" or "no":
# 1. [Co-host Connection] 
# Check for:
# - Split-screen layout or pic-in-pic layout or ring layout with two or more distinct video sources showing the video feeds of different individuals, rather than a dual split-screen or a triple split-screen or mirrored screen originating from the same individual broadcaster.

# 2. [Replay Window] 
# Check for:
# - Smaller secondary window overlaying the main footage
# - Mismatch between main content and secondary window's visuals

# 3. [Standing Posture]
# Check for:
# - Visible posture characteristics suggesting upright stance

# 4. [Male Presence] 
# check for:
# - if there is any male presence in this image

# Respond in this exact JSON format:
# {
#   "co_hosting": "yes/no",
#   "replay_window": "yes/no", 
#   "standing_posture": "yes/no",
#   "male_present": "yes/no"
# }"""
# # q = """这种主播连麦方式的screen布局是怎么样的，就是在整个screen的最左边或在最右边 放着别的主播的screen，英文怎么表述，注意这里需要和画面中的另一个画中画的跳舞主播区分开、识别出两个坐着主播的screen"""
# # 将xxxx/test.png替换为你本地图像的绝对路径
# base64_image = encode_image("/home/yjc/Projects/d/frame30s_血色古阿扎_2019-10-14_01-09_60.3min_0_000900.png")
# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
#     api_key="sk-bfbb9d51e96249138f1b7bb5cf1f2cca",
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-vl-max-latest",
#     messages=[
#     	{
#     	    "role": "system",
#             "content": [{"type":"text","text": "You are a helpful assistant."}]},
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image_url",
#                     # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
#                     # PNG图像：  f"data:image/png;base64,{base64_image}"
#                     # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
#                     # WEBP图像： f"data:image/webp;base64,{base64_image}"
#                     "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
#                 },
#                 {"type": "text", "text": q},
#             ],
#         }
#     ],
# )
# print(completion.choices[0].message.content)



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image(image_path):
    q = """Analyze the provided live stream screenshot and answer the following three questions with only "yes" or "no":
1. [Co-host Connection] 
Check for:
- Split-screen layout or pic-in-pic layout or ring layout with two or more distinct video sources showing the video feeds of different individuals, rather than a dual split-screen or a triple split-screen or mirrored screen originating from the same individual broadcaster.

2. [Replay Window] 
Check for:
- Smaller secondary window overlaying the main footage
- Mismatch between main content and secondary window's visuals

3. [Standing Posture]
Check for:
- Visible posture characteristics suggesting upright stance

4. [Male Presence] 
check for:
- if there is any male presence in this image

Respond in this exact JSON format:
{
  "co_hosting": "yes/no",
  "replay_window": "yes/no", 
  "standing_posture": "yes/no",
  "male_present": "yes/no"
}"""
    # q = """描述下她的穿着，颜色、材质等等特点"""
    base64_image = encode_image(image_path)
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key="sk-bfbb9d51e96249138f1b7bb5cf1f2cca",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    try:
        completion = client.chat.completions.create(
            model="qwen-vl-max-latest",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are a helpful assistant."}]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                            # PNG图像：  f"data:image/png;base64,{base64_image}"
                            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图像： f"data:image/webp;base64,{base64_image}"
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                        {"type": "text", "text": q},
                    ],
                }
            ],
        )
        return completion.choices[0].message.content
    except:
        return "null"

if __name__ == '__main__':

    base_dir = "/home/yjc/Projects/VideoClassify/all_video_frames/"
    frame_2_15_30_output_foldername = "201910_ZMiKo/"
    video_dir = "/media/yjc/新加卷/201910/ZMiKo/2019年10月"
    frame_type = "frame30s"
    print(base_dir)
    print(frame_2_15_30_output_foldername)
    print(video_dir)
    print(frame_type)


    # partial_inferred_res_path = "/home/yjc/Projects/VideoClassify/all_video_frames/zmiko_label_male_exist.txt"
    # infered_imgname_paths = set()
    # try:
    #     with open(partial_inferred_res_path) as f:
    #         for line in f.readlines():
    #             line_js = json.loads(line.strip())
    #             infered_imgname = os.path.basename(line_js["image_path"]).split(".png")[0]
    #             infered_imgname_paths.add(infered_imgname)
    #     print("already infered img len: ", len(infered_imgname_paths))
    # except:
    #     print("No infered img")


    # input_imgs_path = base_dir + frame_2_15_30_output_foldername + frame_type
    # image_paths = []
    # for root, dirs, files in os.walk(input_imgs_path):
    #     for file in files:
    #         if file.endswith(".png") and file[:-4] not in infered_imgname_paths:
    #             image_paths.append(os.path.join(root, file))
    # # image_paths = random.sample(image_paths, 10)
    # print(len(image_paths))
    # # # for debug
    # # image_paths = [
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-13_22-41_60.3min_0/frame30s_由悠yoyo_2019-10-13_22-41_60.3min_0_006300.png",
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-17_23-59_60.3min_0/frame30s_由悠yoyo_2019-10-17_23-59_60.3min_0_005400.png",
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-17_23-59_60.3min_0/frame30s_由悠yoyo_2019-10-17_23-59_60.3min_0_000900.png",
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-15_00-38_60.2min_0/frame30s_由悠yoyo_2019-10-15_00-38_60.2min_0_003600.png",
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-17_19-38_60.3min_0/frame30s_由悠yoyo_2019-10-17_19-38_60.3min_0_002610.png",
    # #     "/home/yjc/Projects/VideoClassify/all_video_frames/youyouyoyo/frame30s/由悠yoyo_2019-10-14_00-42_60.3min_1/frame30s_由悠yoyo_2019-10-14_00-42_60.3min_1_004500.png"
    # # ]

    # infer_res_path = base_dir + frame_2_15_30_output_foldername + "label_male_exist.txt"
    # # 创建进程池
    # processor_nums = 16
    # with open(infer_res_path, "w") as f:
    #     for i in tqdm(range(0, len(image_paths), processor_nums)):
    #         pool = multiprocessing.Pool(processes=processor_nums)

    #         # 并行处理图像
    #         cur_image_paths = image_paths[i:i+processor_nums]
    #         results = pool.map(process_image, cur_image_paths)

    #         # 关闭进程池
    #         pool.close()
    #         pool.join()

    #         # 输出结果
    #         for ii in range(len(results)):
    #             f.write(json.dumps({"image_path": image_paths[i+ii], "answer": results[ii]}, ensure_ascii=False) + "\n")
           
    #         f.flush()








    # video分文件夹：请求拿到api返回结果后，看co_hosting、replay_window、Standing Posture、male_present各个标签的计数，过滤过大于阈值的video
    infer_res_path = base_dir + frame_2_15_30_output_foldername + "label_male_exist.txt"
    print(infer_res_path)
    img_label = {}
    with open(infer_res_path) as f:
        for line in f.readlines():
            line_js = json.loads(line.strip())
            ans_js = json.loads(line_js["answer"].replace("```json", "").replace("```", "").strip())
            try:
                co_hosting = ans_js["co_hosting"]
                replay_window = ans_js["replay_window"]
                standing_posture = ans_js["standing_posture"]
                male_present = ans_js["male_present"]
            except:
                print("items not exist!", "  ", line_js["image_path"])
            if "yes" in co_hosting:
                co_hosting_digi_label = 1
            else:
                co_hosting_digi_label = 0
            if "yes" in replay_window:
                replay_window_label = 1
            else:
                replay_window_label = 0
            if "yes" in standing_posture:
                standing_posture_label = 1
            else:
                standing_posture_label = 0
            if "yes" in male_present:
                male_present_label = 1
            else:
                male_present_label = 0
            

            video_name = line_js["image_path"][:-11]
            if video_name not in img_label:
                img_label[video_name] = {
                    "co_hosting": co_hosting_digi_label,
                    "replay_window": replay_window_label,
                    "standing_posture": standing_posture_label,
                    "male_present": male_present_label,
                    "total": 1
                    }
            else:
                img_label[video_name]["co_hosting"] += co_hosting_digi_label
                img_label[video_name]["replay_window"] += replay_window_label
                img_label[video_name]["standing_posture"] += standing_posture_label
                img_label[video_name]["male_present"] += male_present_label
                img_label[video_name]["total"] += 1
    print(len(img_label))

    import subprocess
    with open(base_dir + frame_2_15_30_output_foldername + "stage1_remained_videos.txt", "w")as f:
        for k, v in img_label.items():
            if not ((float(v["co_hosting"] / v["total"]) >= 0.2) or (float(v["replay_window"] / v["total"]) >= 0.4) or (float(v["male_present"] / v["total"]) >= 0.2) or (float(v["standing_posture"] / v["total"]) <= 0.2)):
                source_file = video_dir + "/" + os.path.basename(os.path.dirname(k)) + ".mp4"
                if not os.path.exists(source_file):
                    print(source_file)
                    continue 
                destination_directory = os.path.dirname(video_dir) + "/" + frame_2_15_30_output_foldername[:-1] + "_stage1_remain/"
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)
                command = ['mv', source_file, destination_directory]
                result = subprocess.run(command, check=True)
                print("MV " + source_file + " to " + destination_directory)
                f.write(os.path.basename(os.path.dirname(k)) + ".mp4\n")






    # 人工复审source_file所在当前目录下的所有被过滤掉的video，把能过白名单的移动到destination_directory的exception文件夹下




    # # 把提取video_info失败的视频(_failed_mp4.txt)单独mv到/home/yjc/Projects/VideoClassify/all_video_frames/下的 某个文件夹 中
    # with open("/home/yjc/Projects/VideoClassify/all_video_frames/201910_11_youyouyoyo/youyouyoyo_failed_mp4.txt", "w") as f:
    #     for line in f.readlines():
    #         if line.strip():
    #             pass # mv xxx





    # dump source_file所在当前目录下的所有被过滤掉的video对应的png和对应的标签
    import subprocess
    import json 
    png_dir = base_dir + frame_2_15_30_output_foldername + frame_type
    remain_png_pos_dir = base_dir + frame_2_15_30_output_foldername + "stage1_frame30s_pos"
    remain_png_neg_dir = base_dir + frame_2_15_30_output_foldername + "stage1_frame30s_neg"
    if not os.path.exists(remain_png_pos_dir):
        os.makedirs(remain_png_pos_dir)
    if not os.path.exists(remain_png_neg_dir):
        os.makedirs(remain_png_neg_dir)

    infer_res_path = base_dir + frame_2_15_30_output_foldername + "label_male_exist.txt"
    count = 0
    count_neg = 0
    img_label = {}
    with open(remain_png_pos_dir+"/label_pos.txt", "a") as f1:
        with open(infer_res_path) as f:
            for line in f.readlines():
                line_js = json.loads(line.strip())
                ans_js = json.loads(line_js["answer"].replace("```json", "").replace("```", "").strip())
                try:
                    co_hosting = ans_js["co_hosting"]
                    replay_window = ans_js["replay_window"]
                    standing_posture = ans_js["standing_posture"]
                    male_present = ans_js["male_present"]
                except:
                    print("items not exist!", "  ", line_js["image_path"])
                if "yes" in co_hosting:
                    co_hosting_digi_label = 1
                else:
                    co_hosting_digi_label = 0
                if "yes" in replay_window:
                    replay_window_label = 1
                else:
                    replay_window_label = 0
                if "yes" in standing_posture:
                    standing_posture_label = 1
                else:
                    standing_posture_label = 0
                if "yes" in male_present:
                    male_present_label = 1
                else:
                    male_present_label = 0
                
                if (co_hosting_digi_label or replay_window_label or male_present_label or male_present_label):
                    count += 1
                    f1.write(line)
                    try:
                        command = ['mv', line_js["image_path"], remain_png_pos_dir]
                        result = subprocess.run(command, check=True)
                    except:
                        print(line_js["image_path"] + " not exist")
                    
                else:
                    count_neg += 1
            print(count, count_neg)
    count_neg_dumped = 0
    for root, dir, files in os.walk(png_dir):
        for file in files:
            f_pth = os.path.join(root, file)
            command = ['mv', f_pth, remain_png_neg_dir]
            result = subprocess.run(command, check=True)
            count_neg_dumped += 1
            if count_neg_dumped > count:
                break 
        if count_neg_dumped > count:
                break 
