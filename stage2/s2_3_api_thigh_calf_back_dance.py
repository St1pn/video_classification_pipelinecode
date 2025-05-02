# """请求qwenl-plus-latest的api接口, 判断图片中是否正在跳舞或者扭动身体、是否能看到背部、大腿/小腿"""
# from openai import OpenAI
# import os
# import base64
# import time
# from tqdm import tqdm 
# import json
# import random


# # #  base 64 编码格式
# # def encode_image(image_path):
# #     with open(image_path, "rb") as image_file:
# #         return base64.b64encode(image_file.read()).decode("utf-8")

# # q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calves: true if knee-to-ankle area visible.Back turned: true if spine faces viewer.Dance/twist: true if she is actively dancing or rhythmically twisting her body.Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool ,dance:bool },...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
# # # 将xxxx/test.png替换为你本地图像的绝对路径
# # base64_image = encode_image("/home/yjc/Projects/d/resize_QLAN%2019-10-16%23-36%60%2min%5_02320.png")
# # client = OpenAI(
# #     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# #     api_key="sk-bfbb9d51e96249138f1b7bb5cf1f2cca",
# #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# # )
# # completion = client.chat.completions.create(
# #     model="qwen-vl-max-latest",
# #     messages=[
# #     	{
# #     	    "role": "system",
# #             "content": [{"type":"text","text": "You are a helpful assistant."}]},
# #         {
# #             "role": "user",
# #             "content": [
# #                 {
# #                     "type": "image_url",
# #                     # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
# #                     # PNG图像：  f"data:image/png;base64,{base64_image}"
# #                     # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
# #                     # WEBP图像： f"data:image/webp;base64,{base64_image}"
# #                     "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
# #                 },
# #                 {"type": "text", "text": q},
# #             ],
# #         }
# #     ],
# # )
# # print(completion.choices[0].message.content)








# import base64
# import multiprocessing
# from openai import OpenAI

# # base 64 编码格式
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# def process_image(image_path):
#     q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calf: true if knee-to-ankle area visible. Back turned: true if spine faces viewer. Dance/twist: true if she is actively dancing or rhythmically twisting her body.Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool ,dance:bool },...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
#     # q = """描述下她的穿着，颜色、材质等等特点"""
#     base64_image = encode_image(image_path)
#     client = OpenAI(
#         # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
#         api_key="sk-bfbb9d51e96249138f1b7bb5cf1f2cca",
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     )
#     completion = client.chat.completions.create(
#         model="qwen-vl-max-latest",
#         messages=[
#             {
#                 "role": "system",
#                 "content": [{"type": "text", "text": "You are a helpful assistant."}]
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
#                         # PNG图像：  f"data:image/png;base64,{base64_image}"
#                         # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
#                         # WEBP图像： f"data:image/webp;base64,{base64_image}"
#                         "image_url": {"url": f"data:image/png;base64,{base64_image}"},
#                     },
#                     {"type": "text", "text": q},
#                 ],
#             }
#         ],
#     )
#     return completion.choices[0].message.content

# if __name__ == '__main__':

    
#     partial_inferred_res_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group5_thigh_calf_back_dance.txt"
#     infered_imgname_paths = set()
#     try:
#         with open(partial_inferred_res_path) as f:
#             for line in f.readlines():
#                 line_js = json.loads(line.strip())
#                 infered_imgname = os.path.basename(line_js["image_path"]).split(".png")[0]
#                 infered_imgname_paths.add(infered_imgname)
#         print("already infered img len: ", len(infered_imgname_paths))
#     except:
#         print("No infered img")

#     input_imgs_path = "/home/yjc/Projects/VideoClassify/resized/group_6"
#     image_paths = []
#     for root, dirs, files in os.walk(input_imgs_path):
#         for file in files:
#             if file.endswith(".png") and file[:-4] not in infered_imgname_paths:
#                 image_paths.append(os.path.join(root, file))
#     # image_paths = random.sample(image_paths, 10)
#     print(len(image_paths))

#     infer_res_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group6_thigh_calf_back_dance.txt"
#     # 创建进程池
#     processor_nums = 16
#     with open(infer_res_path, "w") as f:
#         for i in tqdm(range(0, len(image_paths), processor_nums)):
#             pool = multiprocessing.Pool(processes=processor_nums)

#             # 并行处理图像
#             cur_image_paths = image_paths[i:i+processor_nums]
#             results = pool.map(process_image, cur_image_paths)

#             # 关闭进程池
#             pool.close()
#             pool.join()

#             # 输出结果
#             for ii in range(len(results)):
#                 f.write(json.dumps({"image_path": image_paths[i+ii], "answer": results[ii]}, ensure_ascii=False) + "\n")
#             f.flush()











"""请求qwenl-plus-latest的api接口, 判断图片中是否正在跳舞或者扭动身体、是否能看到背部、大腿/小腿"""
from openai import OpenAI
import os
import base64
import time
from tqdm import tqdm 
import json
import random
import argparse


# #  base 64 编码格式
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calves: true if knee-to-ankle area visible.Back turned: true if spine faces viewer.Dance/twist: true if she is actively dancing or rhythmically twisting her body.Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool ,dance:bool },...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
# # 将xxxx/test.png替换为你本地图像的绝对路径
# base64_image = encode_image("/home/yjc/Projects/d/resize_QLAN%2019-10-16%23-36%60%2min%5_02320.png")
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








import base64
import multiprocessing
from openai import OpenAI

# base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image(image_path):
    q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calf: true if knee-to-ankle area visible. Back turned: true if spine faces viewer. Dance/twist: true if she is actively dancing or rhythmically twisting her body.Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool ,dance:bool },...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
    # q = """Ignore figures in the photo frames within the image. Analyze screens left-to-right (screen_1, screen_2...): Thighs: true if hip-to-knee area visible. Calf: true if knee-to-ankle area visible. Back turned: true if spine faces viewer. Output only a parsable JSON: {screen_1:{thighs:bool ,calves:bool ,back:bool},...}. Return null for uncertainty. Multi-screen requires per-screen analysis."""
    
    # q = """Ignore figures in the photo frames within the image and tell me what she's wearing. You have to strictly choose from the following options: black stockings, black pantyhose, mesh stockings, bodycon dress, yoga leggings, booty shorts, mini dress, micro miniskirt, slit skirt, ladies' skinny denim pants, hip-hugging skirt or None of them. Provide your answer in this format: [item selection]"""
    # q = """描述下她的穿着，颜色、材质等等特点"""
    base64_image = encode_image(image_path)
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key="sk-bfbb9d51e96249138f1b7bb5cf1f2cca",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
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



parser = argparse.ArgumentParser(description='传入必要的参数')
# 添加参数
parser.add_argument('--partial_inferred_res_path', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group5_thigh_calf_back_dance.txt",
                    help='所有图片所在目录')
parser.add_argument('--input_imgs_path', type=str, default="/home/yjc/Projects/VideoClassify/resized/group_6",
                    help='所有图片所在目录')
parser.add_argument('--infer_res_path', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group6_thigh_calf_back_dance.txt",
                    help='所有图片所在目录')

args = parser.parse_args()
partial_inferred_res_path = args.partial_inferred_res_path
infered_imgname_paths = set()
try:
    with open(partial_inferred_res_path) as f:
        for line in f.readlines():
            line_js = json.loads(line.strip())
            infered_imgname = os.path.basename(line_js["image_path"]).split(".png")[0]
            infered_imgname_paths.add(infered_imgname)
    print("already infered img len: ", len(infered_imgname_paths))
except:
    print("No infered img")

input_imgs_path = args.input_imgs_path
print(input_imgs_path)
image_paths = []
for root, dirs, files in os.walk(input_imgs_path):
    for file in files:
        if file.endswith(".png") and file[:-4] not in infered_imgname_paths:
        # if file.endswith(".jpg") and file[:-4] not in infered_imgname_paths:
            image_paths.append(os.path.join(root, file))
# image_paths = random.sample(image_paths, 10)
print(len(image_paths))

infer_res_path = args.infer_res_path
# 创建进程池
processor_nums = 16
with open(infer_res_path, "w") as f:
    for i in tqdm(range(0, len(image_paths), processor_nums)):
        pool = multiprocessing.Pool(processes=processor_nums)

        # 并行处理图像
        try:
            cur_image_paths = image_paths[i:i+processor_nums]
            results = pool.map(process_image, cur_image_paths)
        except:
            results = ["No result from api"] * len(image_paths[i:i+processor_nums])

        # 关闭进程池
        pool.close()
        pool.join()

        # 输出结果
        for ii in range(len(results)):
            f.write(json.dumps({"image_path": image_paths[i+ii], "answer": results[ii]}, ensure_ascii=False) + "\n")
        f.flush()
