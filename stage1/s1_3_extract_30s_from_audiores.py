import json 
import re
import os 


# 解析audio res
res_videos = {}
# with open("/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/mp3_label.txt") as f:
#     c = 0
#     for line in f.readlines():
#         try:
#             resp_sta = line.index("response:")
#             resp_str = line.strip()[resp_sta+9: ]
#         except:
#             print(c)
#             continue 
#         try:
#             line_js = json.loads(resp_str.strip().replace("\\", ""))
#             # 文件名称处理
#             beat, bpm = line_js["beat"]["pattern"], line_js["beat"]["bpm"]
#             filename = line.strip()[5:resp_sta].strip()
#             filename = filename.split("_window")[0].replace("_", "%")
#             if float(bpm.lower().replace("bpm","").strip()) <= 90:
#                 if filename not in res_videos:
#                     res_videos[filename] = [1,0]  # 0号元素、1号元素分别为<=90、>90的片段个数
#                 else:
#                     res_videos[filename][0] = res_videos[filename][0] + 1
#             else:
#                 if filename not in res_videos:
#                     res_videos[filename] = [0,1]  # 0号元素、1号元素分别为<=90、>90的片段个数
#                 else:
#                     res_videos[filename][1] = res_videos[filename][1] + 1
#         except:
#             pattern = r'\d+\.\d+'
#             match = re.search(pattern, resp_str)
#             if match:
#                 # 获取匹配到的数字部分
#                 number = match.group()
#                 if float(number) <= 90:
#                     if filename not in res_videos:
#                         res_videos[filename] = [1,0]  # 0号元素、1号元素分别为<=90、>90的片段个数
#                     else:
#                         res_videos[filename][0] = res_videos[filename][0] + 1
#                 else:
#                     if filename not in res_videos:
#                         res_videos[filename] = [0,1]  # 0号元素、1号元素分别为<=90、>90的片段个数
#                     else:
#                         res_videos[filename][1] = res_videos[filename][1] + 1
#             else:
#                 print("json parse err: ", c, "###resp_str: ", resp_str)
        
#         c += 1
# print(len(res_videos))


# # 校验mp3是否==全部mp4，将过滤的video存到一个txt
# mp3filtered_videos_path = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/201910_anni_mp3filtered_videos.txt"
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
# # # todo：人工校验的需要单独维护一个列表，每一行为{videoname, label, reason}











# 开始每隔2s、15s、30s提取一帧，原图->每个视频3个文件夹，像素打乱后的图->当月主播下3个文件夹包括所有视频
import decord
import os
import random 
from PIL import Image
from decord import VideoReader
import cv2
from tqdm import tqdm 
import multiprocessing
from moviepy.video.io.VideoFileClip import VideoFileClip
import argparse


parser = argparse.ArgumentParser(description='传入必要的参数')
# 添加参数
parser.add_argument('--base_dir', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/",
                    help='所有图片所在目录')
parser.add_argument('--frame_2_15_30_output_foldername', type=str, default="201910_古阿扎/",
                    help='当前主播图片输出目录名称')
parser.add_argument('--video_dir', type=str, default="/media/yjc/新加卷/201910/古阿扎",
                    help='视频目录路径')
parser.add_argument('--process_num', type=int, default=32,
                    help='进程数量')
# 解析命令行参数
args = parser.parse_args()

base_dir = args.base_dir
frame_2_15_30_output_foldername = args.frame_2_15_30_output_foldername
print(frame_2_15_30_output_foldername)
zhubo_name = frame_2_15_30_output_foldername.strip().split("_")[1]
print(zhubo_name)
video_dir = args.video_dir
process_num = args.process_num  # 根据实际情况修改


def split_video_into_two(input_video_path, output_video_1_path, output_video_2_path):
    """
    暂未使用到
    """
    # 加载视频文件
    video = VideoFileClip(input_video_path)
    # 获取视频的总时长
    total_duration = video.duration
    # 计算分割点，即总时长的一半
    split_point = total_duration / 2

    # 切割前半部分视频
    first_half = video.subclipped(0, split_point)
    # 保存前半部分视频
    first_half.write_videofile(output_video_1_path, codec="libx264")

    # 切割后半部分视频
    second_half = video.subclipped(split_point, total_duration)
    # 保存后半部分视频
    second_half.write_videofile(output_video_2_path, codec="libx264")

    # 关闭视频文件
    video.close()
    first_half.close()
    second_half.close()


# 获取所有。mp4的分辨率、映射词典
def get_video_resolution(video_path):
    # 打开视频文件
    video_reader = decord.VideoReader(video_path)
    
    total_frames = len(video_reader)
    fps = video_reader.get_avg_fps()
    duration = total_frames / fps
    
    # 获取视频的第一帧
    first_frame = video_reader[0]
    # 获取第一帧的高度和宽度
    height, width = first_frame.shape[:2]
    
    return width, height, total_frames, fps, duration, video_path

frame_2_15_30_output_folder_abspath = base_dir + frame_2_15_30_output_foldername  # 根据实际情况修改
if not os.path.exists(frame_2_15_30_output_folder_abspath):
    os.makedirs(frame_2_15_30_output_folder_abspath)
file_failed_mp4 = open(frame_2_15_30_output_folder_abspath + zhubo_name[:-1] + "_failed_mp4.txt", "w")
print("file_failed_mp4: ", file_failed_mp4)
def try_get_video_resolution(vpath):
    global file_failed_mp4 
    try:
        width, height, total_frames, fps, duration, video_path = get_video_resolution(vpath)
        # print("split into: ", video_path)
        return [(width, height, total_frames, fps, duration, video_path)]
    except Exception as e:
        print(vpath)
        file_failed_mp4.write(vpath + "\n")
        return []



# 获取输入目录下的所有.mp4绝对路径
def get_mp4_files(video_dir):
    current_dir = video_dir
    mp4_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in tqdm(files):
            if file.endswith('.mp4') and ("baiduyun" not in file):
                mp4_files.append(os.path.join(root, file))
    return mp4_files


notmp3filter_mp4_paths = get_mp4_files(video_dir)
# mp4_paths = []
# for path in notmp3filter_mp4_paths:  # mp3类别过滤后，只提取剩下的video的frame30s
#     xx = os.path.basename(path)[:-4]
#     if xx in res_videos:
#         if res_videos[xx][1] >= 1:
#             mp4_paths.append(path)
# print("mp3 < thres, remaining mp4_paths numbers: ", len(mp4_paths))
mp4_paths = []
for path in notmp3filter_mp4_paths:
    mp4_paths.append(path)
print("mp3 < thres, remaining mp4_paths numbers: ", len(mp4_paths))



videoname__vlength_fps_allframes = {}
vidx = 0
for vpath in tqdm(mp4_paths):
    all_video_resolution_list = try_get_video_resolution(vpath)
    if all_video_resolution_list:
        for tup in all_video_resolution_list:
            width, height, total_frames, fps, duration, video_path = tup
        
            # print(f"视频{vpath}的分辨率为: {width}x{height}, 总帧数、帧率、视频总长：{total_frames}, {fps}, {duration}")  # 待用nohup > 写入txt文件
            videoname = str(os.path.basename(video_path)).split(".")[0]
            total_frames = int(total_frames)
            fps = int(fps)
            duration = int(duration)
            
            videoname__vlength_fps_allframes[videoname] = str(duration) + "_" + str(fps) + "_" + str(total_frames)
            
            vidx += 1
print(len(videoname__vlength_fps_allframes))


# 每一秒提取一帧
def extract_frames(video_path, output_folder):
    v_basename = os.path.basename(video_path)
    v_dir_path = os.path.dirname(video_path)
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        print("mkdir new output folder of extracted frames: ", output_folder)
        os.makedirs(output_folder)
    # 当前video的2s_frame存储目录
    v_frame2s_dir = os.path.join(output_folder + "/frame2s", v_basename.split(".mp4")[0])
    if not os.path.exists(v_frame2s_dir):
        os.makedirs(v_frame2s_dir)
    # 当前video的15s_frame存储目录
    v_frame15s_dir = os.path.join(output_folder + "/frame15s", v_basename.split(".mp4")[0])
    if not os.path.exists(v_frame15s_dir):
        os.makedirs(v_frame15s_dir)
    # 当前video的30s_frame存储目录
    v_frame30s_dir = os.path.join(output_folder + "/frame30s", v_basename.split(".mp4")[0])
    if not os.path.exists(v_frame30s_dir):
        os.makedirs(v_frame30s_dir)
    
    # 读取视频文件
    vr = VideoReader(video_path)
    # 获取视频的帧率
    fps = int(vr.get_avg_fps())
    # 计算每隔多少帧截取一帧（每2秒、15s、30s 1 帧）
    interval_2s = int(fps) * 2
    interval_15s = int(fps) * 15
    interval_30s = int(fps) * 30
    # 遍历视频帧，每隔 interval 帧截取一帧
    for i in range(1, len(vr)):
        # if i % interval_2s == 0:
        #     frame = vr[i].asnumpy()
        #     frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_LANCZOS4)
        #     # 生成保存图像的文件名
        #     file_name = str(os.path.basename(video_path)).split(".mp4")[0]
        #     frame_filename_2s = os.path.join(v_frame2s_dir, f"frame2s_{file_name}_{i:06d}.png")  # 按照实际情况修改
        #     # 使用 OpenCV 保存图像
        #     cv2.imwrite(frame_filename_2s, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        # if i % interval_15s == 0:
        #     frame = vr[i].asnumpy()
        #     frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_LANCZOS4)
        #     # 生成保存图像的文件名
        #     file_name = str(os.path.basename(video_path)).split(".mp4")[0]
        #     frame_filename_15s = os.path.join(v_frame15s_dir, f"frame15s_{file_name}_{i:06d}.png")  # 按照实际情况修改
        #     # 使用 OpenCV 保存图像
        #     cv2.imwrite(frame_filename_15s, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        if i % interval_30s == 0:
            frame = vr[i].asnumpy()
            frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_LANCZOS4)
            # 生成保存图像的文件名
            file_name = str(os.path.basename(video_path)).split(".mp4")[0]
            frame_filename_30s = os.path.join(v_frame30s_dir, f"frame30s_{file_name}_{i:06d}.png")  # 按照实际情况修改
            # 使用 OpenCV 保存图像
            cv2.imwrite(frame_filename_30s, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

for vpath in tqdm(mp4_paths):
    video_path = vpath
    extract_frames(video_path, frame_2_15_30_output_folder_abspath)

    
# 对图像进行切割变换处理
def crop_image(image_path):
    image = Image.open(image_path)
    # print(f"原图像模式: {image.mode}")  # 打印原图像模式
    
    width, height = image.size
    new_image = Image.new(image.mode, (width, height))
    # 待重新生成len=512的长度
    wd_list = [18, 484, 41, 384, 119, 13, 50, 391, 312, 90, 475, 482, 89, 373, 251, 118, 21, 381, 236, 334, 229, 20, 462, 336, 315, 471, 84, 430, 419, 78, 456, 83, 277, 137, 266, 498, 207, 40, 47, 294, 295, 22, 318, 185, 361, 355, 249, 386, 35, 5, 230, 233, 310, 342, 55, 225, 508, 470, 353, 62, 167, 109, 169, 195, 57, 341, 339, 401, 179, 221, 467, 477, 307, 165, 278, 172, 433, 64, 222, 93, 126, 27, 402, 314, 272, 510, 463, 255, 320, 437, 337, 200, 143, 79, 279, 34, 371, 157, 479, 95, 511, 108, 427, 38, 10, 206, 178, 348, 422, 494, 487, 324, 271, 115, 111, 226, 377, 290, 416, 141, 238, 97, 193, 331, 476, 415, 311, 256, 410, 379, 15, 224, 351, 133, 297, 454, 151, 24, 452, 244, 464, 149, 14, 335, 26, 217, 308, 424, 288, 30, 443, 383, 400, 413, 409, 3, 503, 138, 123, 33, 293, 376, 85, 358, 94, 164, 275, 276, 406, 17, 176, 194, 447, 253, 208, 31, 270, 4, 29, 488, 264, 366, 439, 466, 407, 201, 298, 254, 323, 403, 455, 101, 54, 309, 460, 490, 472, 347, 399, 369, 349, 302, 432, 82, 328, 325, 442, 319, 378, 338, 163, 187, 49, 252, 81, 392, 80, 389, 77, 245, 344, 120, 170, 142, 458, 43, 75, 504, 394, 155, 497, 486, 421, 404, 160, 216, 425, 117, 235, 398, 213, 299, 32, 284, 435, 16, 150, 46, 365, 110, 74, 197, 66, 56, 166, 177, 146, 431, 96, 184, 465, 181, 121, 412, 313, 367, 7, 134, 263, 135, 183, 436, 507, 375, 45, 87, 153, 204, 445, 408, 156, 67, 491, 265, 113, 305, 112, 182, 139, 127, 426, 382, 357, 283, 280, 125, 103, 350, 116, 343, 232, 128, 301, 261, 306, 273, 474, 363, 326, 434, 246, 198, 258, 446, 440, 461, 131, 423, 374, 152, 259, 189, 191, 186, 501, 59, 317, 303, 162, 69, 48, 60, 354, 269, 478, 390, 11, 345, 99, 214, 289, 159, 262, 286, 63, 37, 359, 282, 106, 448, 444, 429, 260, 267, 340, 250, 493, 2, 370, 218, 1, 418, 223, 296, 509, 428, 329, 12, 88, 327, 202, 356, 505, 396, 243, 385, 287, 174, 451, 496, 364, 227, 380, 316, 140, 352, 205, 228, 180, 203, 292, 489, 132, 330, 499, 360, 168, 483, 268, 291, 52, 76, 417, 107, 411, 300, 332, 71, 104, 234, 129, 51, 346, 220, 212, 39, 333, 171, 492, 173, 36, 154, 102, 25, 28, 53, 9, 231, 248, 247, 196, 145, 468, 393, 161, 6, 485, 147, 274, 304, 257, 395, 495, 65, 105, 481, 500, 130, 72, 148, 368, 0, 91, 136, 322, 457, 405, 209, 372, 192, 23, 506, 58, 240, 459, 453, 219, 237, 114, 420, 281, 190, 469, 86, 211, 19, 70, 502, 44, 124, 449, 8, 397, 241, 215, 122, 158, 441, 68, 199, 61, 144, 450, 100, 239, 242, 210, 473, 92, 480, 285, 321, 438, 188, 388, 175, 73, 387, 98, 414, 42, 362]
    hei_list = [246, 283, 30, 3, 409, 90, 195, 66, 311, 257, 417, 357, 496, 461, 185, 313, 420, 500, 79, 332, 356, 46, 275, 104, 449, 154, 60, 134, 424, 221, 
350, 218, 309, 42, 318, 458, 464, 302, 495, 122, 392, 103, 190, 216, 163, 450, 15, 1, 336, 498, 323, 227, 419, 63, 187, 36, 213, 173, 194, 328, 476, 273, 68, 80, 244, 265, 293, 83, 442, 240, 85, 377, 94, 234, 169, 109, 65, 322, 355, 14, 183, 259, 209, 210, 204, 148, 215, 115, 319, 74, 
12, 416, 338, 44, 358, 81, 374, 484, 47, 258, 429, 113, 137, 21, 128, 224, 149, 491, 342, 497, 182, 177, 317, 381, 161, 116, 184, 43, 501, 412, 469, 16, 121, 50, 393, 106, 88, 172, 307, 284, 179, 447, 2, 509, 271, 175, 207, 53, 510, 102, 159, 426, 127, 238, 222, 206, 77, 421, 267, 508, 64, 452, 123, 255, 232, 197, 470, 8, 167, 76, 40, 395, 129, 33, 408, 481, 198, 158, 214, 201, 270, 278, 25, 507, 247, 382, 383, 428, 59, 274, 
331, 138, 226, 250, 100, 345, 391, 180, 266, 269, 260, 457, 89, 10, 430, 437, 143, 364, 241, 291, 192, 456, 75, 17, 348, 151, 233, 114, 139, 219, 41, 373, 438, 31, 304, 205, 95, 71, 334, 372, 69, 471, 443, 346, 211, 144, 280, 379, 406, 369, 37, 446, 5, 402, 329, 54, 296, 110, 432, 254, 448, 276, 477, 454, 288, 414, 245, 367, 26, 375, 487, 453, 32, 427, 181, 13, 433, 478, 262, 171, 413, 511, 479, 505, 155, 362, 295, 162, 157, 
48, 164, 324, 281, 325, 290, 22, 176, 504, 153, 343, 410, 39, 415, 403, 440, 186, 389, 404, 349, 436, 401, 252, 335, 174, 55, 445, 466, 493, 118, 330, 297, 51, 203, 380, 78, 279, 390, 394, 200, 61, 489, 202, 248, 354, 277, 339, 189, 455, 141, 264, 488, 82, 7, 99, 422, 19, 72, 439, 397, 400, 107, 131, 133, 316, 503, 365, 327, 243, 486, 303, 468, 119, 212, 101, 268, 366, 299, 384, 34, 312, 292, 145, 475, 239, 387, 282, 208, 463, 170, 52, 289, 465, 462, 6, 20, 306, 225, 418, 386, 396, 87, 136, 337, 300, 18, 166, 91, 472, 483, 398, 105, 62, 117, 480, 160, 352, 425, 28, 
93, 96, 431, 156, 444, 287, 485, 434, 4, 147, 108, 340, 388, 168, 35, 45, 236, 460, 142, 191, 441, 135, 231, 253, 67, 353, 235, 188, 368, 371, 
261, 474, 217, 308, 320, 229, 256, 220, 405, 451, 237, 370, 199, 251, 341, 459, 92, 423, 351, 411, 111, 361, 305, 193, 378, 98, 492, 315, 150, 
494, 57, 49, 294, 73, 435, 132, 223, 399, 376, 58, 467, 286, 310, 363, 263, 23, 249, 473, 27, 272, 70, 347, 502, 344, 152, 0, 298, 125, 126, 326, 490, 407, 333, 86, 11, 120, 285, 228, 38, 482, 165, 140, 314, 359, 506, 24, 9, 112, 321, 230, 178, 97, 56, 242, 130, 360, 385, 84, 499, 29, 
146, 301, 124, 196]

    for y in range(height):
        for x in range(width):
            new_x = wd_list[x]
            new_y = hei_list[y]
            # 获取原图像指定位置的像素值
            pixel = image.getpixel((x, y))
            # 将像素值设置到新图像的反转位置
            new_image.putpixel((new_x, new_y), pixel)
    
    # print(f"新图像模式: {new_image.mode}")
    # 保存新图像
    # new_image.save(output_path, "jpeg")
    # new_image.save(output_path, "png")
    
    # resize_filename = str(os.path.basename(image_path)).split(".")[0]
    
    return (image_path, new_image)

def pil_image_save(pilimg, image_path, output_path):
    pilimg.save(output_path, "png")
    
all_frame2s_files = []
all_frame15s_files = []
all_frame30s_files = []
for root, dirs, files in os.walk(frame_2_15_30_output_folder_abspath):  # 根据实际情况修改
    for file in files:
        if file.endswith('.png'):  # 根据实际情况修改
            if "frame2s" in file:
                all_frame2s_files.append(os.path.join(root, file))
            if "frame15s" in file:
                all_frame15s_files.append(os.path.join(root, file))
            if "frame30s" in file:
                all_frame30s_files.append(os.path.join(root, file))

# # 串行
# cropped_output_folder = "/root/autodl-fs/examples/cropped"  # 根据实际情况修改
# if not os.path.exists(cropped_output_folder):
#         print("mkdir new output folder of cropped frames: ", output_folder)
#         os.makedirs(cropped_output_folder)
# for resized_file in tqdm(resized_files):
#     image_path = resized_file  # JPEG 格式在保存图像时会进行压缩，可能会导致一些色彩信息的损失。如果在多次保存和读取过程中，图像格式的兼容性出现问题,因此使用PNG（ PNG 是无损压缩格式）进行保存，可能会避免一些色彩信息的损失
#     output_path = cropped_output_folder + "/randomcropped_" + str(os.path.basename(image_path)).split(".")[0] + ".png"  # 后缀根据实际情况修改
#     crop_image(image_path, output_path)

# 多进程并行
shuffle_pixel_output_folder = base_dir + zhubo_name[:-1] + "_shuffle_pixel"  # 根据实际情况修改
process_num = 32  # 根据实际情况修改
if not os.path.exists(shuffle_pixel_output_folder):
    print("mkdir new output folder of cropped frames: ", shuffle_pixel_output_folder)
    os.makedirs(shuffle_pixel_output_folder)
# 当前video的2s_frame存储目录
v_frame2s_dir = os.path.join(shuffle_pixel_output_folder, "shufpix_frame2s")
if not os.path.exists(v_frame2s_dir):
    os.makedirs(v_frame2s_dir)
# 当前video的15s_frame存储目录
v_frame15s_dir = os.path.join(shuffle_pixel_output_folder, "shufpix_frame15s")
if not os.path.exists(v_frame15s_dir):
    os.makedirs(v_frame15s_dir)
# 当前video的30s_frame存储目录
v_frame30s_dir = os.path.join(shuffle_pixel_output_folder, "shufpix_frame30s")
if not os.path.exists(v_frame30s_dir):
    os.makedirs(v_frame30s_dir)
# for i in tqdm(range(0, len(all_frame2s_files), process_num)):
#     image_paths = all_frame2s_files[i:i+process_num]  # JPEG 格式在保存图像时会进行压缩，可能会导致一些色彩信息的损失。如果在多次保存和读取过程中，图像格式的兼容性出现问题,因此使用PNG（ PNG 是无损压缩格式）进行保存，可能会避免一些色彩信息的损失
#     imgpth_pilimg_list = []
#     with multiprocessing.Pool(processes=process_num) as pool:
#         imgpth_pilimg_list = pool.map(crop_image, image_paths)
#     for imgpth, pilimg in imgpth_pilimg_list:
#         output_path = v_frame2s_dir + "/shufpix_" + str(os.path.basename(imgpth)).split(".png")[0] + ".png"  # 后缀根据实际情况修改
#         pil_image_save(pilimg, imgpth, output_path)
# for i in tqdm(range(0, len(all_frame15s_files), process_num)):
#     image_paths = all_frame15s_files[i:i+process_num]  # JPEG 格式在保存图像时会进行压缩，可能会导致一些色彩信息的损失。如果在多次保存和读取过程中，图像格式的兼容性出现问题,因此使用PNG（ PNG 是无损压缩格式）进行保存，可能会避免一些色彩信息的损失
#     imgpth_pilimg_list = []
#     with multiprocessing.Pool(processes=process_num) as pool:
#         imgpth_pilimg_list = pool.map(crop_image, image_paths)
#     for imgpth, pilimg in imgpth_pilimg_list:
#         output_path = v_frame15s_dir + "/shufpix_" + str(os.path.basename(imgpth)).split(".png")[0] + ".png"  # 后缀根据实际情况修改
#         pil_image_save(pilimg, imgpth, output_path)
for i in tqdm(range(0, len(all_frame30s_files), process_num)):
    image_paths = all_frame30s_files[i:i+process_num]  # JPEG 会损失部分色彩信息，因此使用PNG（ PNG 是无损压缩格式）进行保存
    imgpth_pilimg_list = []
    with multiprocessing.Pool(processes=process_num) as pool:
        imgpth_pilimg_list = pool.map(crop_image, image_paths)
    for imgpth, pilimg in imgpth_pilimg_list:
        output_path = v_frame30s_dir + "/shufpix_" + str(os.path.basename(imgpth)).split(".png")[0] + ".png"  # 后缀根据实际情况修改
        pil_image_save(pilimg, imgpth, output_path)

        
import json 
with open(frame_2_15_30_output_folder_abspath + "/video_info.txt", "w") as f1:
    for k,v in tqdm(videoname__vlength_fps_allframes.items()):
        f1.write(json.dumps({k:v}, ensure_ascii=False) + "\n")
    f1.write("wd_list = " + str([18, 484, 41, 384, 119, 13, 50, 391, 312, 90, 475, 482, 89, 373, 251, 118, 21, 381, 236, 334, 229, 20, 462, 336, 315, 471, 84, 430, 419, 78, 456, 83, 277, 137, 266, 498, 207, 40, 47, 294, 295, 22, 318, 185, 361, 355, 249, 386, 35, 5, 230, 233, 310, 342, 55, 225, 508, 470, 353, 62, 167, 109, 169, 195, 57, 341, 339, 401, 179, 221, 467, 477, 307, 165, 278, 172, 433, 64, 222, 93, 126, 27, 402, 314, 272, 510, 463, 255, 320, 437, 337, 200, 143, 79, 279, 34, 371, 157, 479, 95, 511, 108, 427, 38, 10, 206, 178, 348, 422, 494, 487, 324, 271, 115, 111, 226, 377, 290, 416, 141, 238, 97, 193, 331, 476, 415, 311, 256, 410, 379, 15, 224, 351, 133, 297, 454, 151, 24, 452, 244, 464, 149, 14, 335, 26, 217, 308, 424, 288, 30, 443, 383, 400, 413, 409, 3, 503, 138, 123, 33, 293, 376, 85, 358, 94, 164, 275, 276, 406, 17, 176, 194, 447, 253, 208, 31, 270, 4, 29, 488, 264, 366, 439, 466, 407, 201, 298, 254, 323, 403, 455, 101, 54, 309, 460, 490, 472, 347, 399, 369, 349, 302, 432, 82, 328, 325, 442, 319, 378, 338, 163, 187, 49, 252, 81, 392, 80, 389, 77, 245, 344, 120, 170, 142, 458, 43, 75, 504, 394, 155, 497, 486, 421, 404, 160, 216, 425, 117, 235, 398, 213, 299, 32, 284, 435, 16, 150, 46, 365, 110, 74, 197, 66, 56, 166, 177, 146, 431, 96, 184, 465, 181, 121, 412, 313, 367, 7, 134, 263, 135, 183, 436, 507, 375, 45, 87, 153, 204, 445, 408, 156, 67, 491, 265, 113, 305, 112, 182, 139, 127, 426, 382, 357, 283, 280, 125, 103, 350, 116, 343, 232, 128, 301, 261, 306, 273, 474, 363, 326, 434, 246, 198, 258, 446, 440, 461, 131, 423, 374, 152, 259, 189, 191, 186, 501, 59, 317, 303, 162, 69, 48, 60, 354, 269, 478, 390, 11, 345, 99, 214, 289, 159, 262, 286, 63, 37, 359, 282, 106, 448, 444, 429, 260, 267, 340, 250, 493, 2, 370, 218, 1, 418, 223, 296, 509, 428, 329, 12, 88, 327, 202, 356, 505, 396, 243, 385, 287, 174, 451, 496, 364, 227, 380, 316, 140, 352, 205, 228, 180, 203, 292, 489, 132, 330, 499, 360, 168, 483, 268, 291, 52, 76, 417, 107, 411, 300, 332, 71, 104, 234, 129, 51, 346, 220, 212, 39, 333, 171, 492, 173, 36, 154, 102, 25, 28, 53, 9, 231, 248, 247, 196, 145, 468, 393, 161, 6, 485, 147, 274, 304, 257, 395, 495, 65, 105, 481, 500, 130, 72, 148, 368, 0, 91, 136, 322, 457, 405, 209, 372, 192, 23, 506, 58, 240, 459, 453, 219, 237, 114, 420, 281, 190, 469, 86, 211, 19, 70, 502, 44, 124, 449, 8, 397, 241, 215, 122, 158, 441, 68, 199, 61, 144, 450, 100, 239, 242, 210, 473, 92, 480, 285, 321, 438, 188, 388, 175, 73, 387, 98, 414, 42, 362]) + "\n")
    f1.write("hei_list = " + str([246, 283, 30, 3, 409, 90, 195, 66, 311, 257, 417, 357, 496, 461, 185, 313, 420, 500, 79, 332, 356, 46, 275, 104, 449, 154, 60, 134, 424, 221, 350, 218, 309, 42, 318, 458, 464, 302, 495, 122, 392, 103, 190, 216, 163, 450, 15, 1, 336, 498, 323, 227, 419, 63, 187, 36, 213, 173, 194, 328, 476, 273, 68, 80, 244, 265, 293, 83, 442, 240, 85, 377, 94, 234, 169, 109, 65, 322, 355, 14, 183, 259, 209, 210, 204, 148, 215, 115, 319, 74, 12, 416, 338, 44, 358, 81, 374, 484, 47, 258, 429, 113, 137, 21, 128, 224, 149, 491, 342, 497, 182, 177, 317, 381, 161, 116, 184, 43, 501, 412, 469, 16, 121, 50, 393, 106, 88, 172, 307, 284, 179, 447, 2, 509, 271, 175, 207, 53, 510, 102, 159, 426, 127, 238, 222, 206, 77, 421, 267, 508, 64, 452, 123, 255, 232, 197, 470, 8, 167, 76, 40, 395, 129, 33, 408, 481, 198, 158, 214, 201, 270, 278, 25, 507, 247, 382, 383, 428, 59, 274, 331, 138, 226, 250, 100, 345, 391, 180, 266, 269, 260, 457, 89, 10, 430, 437, 143, 364, 241, 291, 192, 456, 75, 17, 348, 151, 233, 114, 139, 219, 41, 373, 438, 31, 304, 205, 95, 71, 334, 372, 69, 471, 443, 346, 211, 144, 280, 379, 406, 369, 37, 446, 5, 402, 329, 54, 296, 110, 432, 254, 448, 276, 477, 454, 288, 414, 245, 367, 26, 375, 487, 453, 32, 427, 181, 13, 433, 478, 262, 171, 413, 511, 479, 505, 155, 362, 295, 162, 157, 48, 164, 324, 281, 325, 290, 22, 176, 504, 153, 343, 410, 39, 415, 403, 440, 186, 389, 404, 349, 436, 401, 252, 335, 174, 55, 445, 466, 493, 118, 330, 297, 51, 203, 380, 78, 279, 390, 394, 200, 61, 489, 202, 248, 354, 277, 339, 189, 455, 141, 264, 488, 82, 7, 99, 422, 19, 72, 439, 397, 400, 107, 131, 133, 316, 503, 365, 327, 243, 486, 303, 468, 119, 212, 101, 268, 366, 299, 384, 34, 312, 292, 145, 475, 239, 387, 282, 208, 463, 170, 52, 289, 465, 462, 6, 20, 306, 225, 418, 386, 396, 87, 136, 337, 300, 18, 166, 91, 472, 483, 398, 105, 62, 117, 480, 160, 352, 425, 28, 93, 96, 431, 156, 444, 287, 485, 434, 4, 147, 108, 340, 388, 168, 35, 45, 236, 460, 142, 191, 441, 135, 231, 253, 67, 353, 235, 188, 368, 371, 261, 474, 217, 308, 320, 229, 256, 220, 405, 451, 237, 370, 199, 251, 341, 459, 92, 423, 351, 411, 111, 361, 305, 193, 378, 98, 492, 315, 150, 494, 57, 49, 294, 73, 435, 132, 223, 399, 376, 58, 467, 286, 310, 363, 263, 23, 249, 473, 27, 272, 70, 347, 502, 344, 152, 0, 298, 125, 126, 326, 490, 407, 333, 86, 11, 120, 285, 228, 38, 482, 165, 140, 314, 359, 506, 24, 9, 112, 321, 230, 178, 97, 56, 242, 130, 360, 385, 84, 499, 29, 146, 301, 124, 196]) + "\n")
    
