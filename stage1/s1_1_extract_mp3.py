import os
from moviepy import *
from moviepy import VideoFileClip 
from tqdm import tqdm 
import random 
from pydub import AudioSegment
from pydub.utils import make_chunks


# def split_audio(input_dir, output_dir, segment_length=30):
#     """
#     处理目录中的所有MP4文件，提取音频并按指定时长分割
#     :param input_dir: 输入目录路径
#     :param output_dir: 输出目录路径
#     :param segment_length: 分段时长（秒），默认为30秒（0.5分钟）
#     """
#     # 确保输出目录存在
#     if os.path.exists(output_dir):
#         print("output_dir already exists, skip makedirs")
#     else:
#         os.makedirs(output_dir)

#     # 遍历输入目录中的所有MP4文件
#     for root, dirs, files in os.walk(input_dir):
#         for filename in tqdm(files):
#             # 检查文件扩展名是否为 .mp4
#             if not filename.lower().endswith('.mp4'):
#                 continue

#             input_path = os.path.join(root, filename)
#             base_name = os.path.splitext(filename)[0]

#             try:
#                 # 使用moviepy提取音频
#                 with VideoFileClip(input_path) as video:
#                     audio = video.audio
#                     if audio is None:
#                         print(f"警告: {filename} 没有音频轨道，跳过处理")
#                         continue
                    
#                     # 创建临时wav文件
#                     temp_audio_path = os.path.join(output_dir, f"temp_{base_name}.wav")
#                     audio.write_audiofile(temp_audio_path, codec='pcm_s16le')

#                 # 使用pydub处理音频分割
#                 audio = AudioSegment.from_file(temp_audio_path, format="wav")
#                 duration_ms = len(audio)
#                 segment_ms = segment_length * 1000  # 转换为毫秒

#                 # 创建分段
#                 chunks = make_chunks(audio, segment_ms)

#                 # 保存所有分段
#                 for i, chunk in enumerate(chunks):
#                     if len(chunk) < 15 * 1000:
#                         # print(f"len: {len(chunk)//1000}, 跳过小于1分钟的片段: {base_name}_part{i+1}.mp3")
#                         continue
#                     output_filename = f"{base_name}_part{i+1}.mp3"
#                     output_path = os.path.join(output_dir, output_filename)
#                     chunk.export(output_path, format="mp3")
#                     # print(f"已保存: {output_path}")

#                 # 删除临时文件
#                 os.remove(temp_audio_path)

#             except Exception as e:
#                 print(f"处理 {filename} 时发生错误: {str(e)}")

# if __name__ == "__main__":
#     # 使用示例
#     input_directory = "/media/yjc/新加卷/201910/安妮/2019年10月"
#     output_directory = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/all_mp3"

#     # for debug
#     # input_directory = "/home/yjc/Projects/VideoClassify/pipeline_code/stage1/"
#     # output_directory = "./"
#     split_audio(input_directory, output_directory)








# def split_audio(input_dir, output_dir, window_length=90, segment_length=30):
#     """
#     处理目录中的所有MP4文件，提取音频并按指定窗口时长分割，每个窗口中随机采样一段连续音频
#     :param input_dir: 输入目录路径
#     :param output_dir: 输出目录路径
#     :param window_length: 窗口时长（秒），默认为90秒（1.5分钟）
#     :param segment_length: 采样音频的时长（秒），默认为30秒
#     """
#     # 确保输出目录存在
#     os.makedirs(output_dir, exist_ok=True)

#     # 遍历输入目录中的所有MP4文件
#     for root, dirs, files in os.walk(input_dir):
#         for filename in tqdm(files):
#             # 检查文件扩展名是否为 .mp4
#             if not filename.lower().endswith('.mp4'):
#                 continue

#             input_path = os.path.join(root, filename)
#             base_name = os.path.splitext(filename)[0]

#             try:
#                 # 使用moviepy提取音频
#                 with VideoFileClip(input_path) as video:
#                     audio = video.audio
#                     if audio is None:
#                         print(f"警告: {filename} 没有音频轨道，跳过处理")
#                         continue
                    
#                     # 创建临时wav文件
#                     temp_audio_path = os.path.join(output_dir, f"temp_{base_name}.wav")
#                     audio.write_audiofile(temp_audio_path, codec='pcm_s16le')

#                 # 使用pydub处理音频分割
#                 audio = AudioSegment.from_file(temp_audio_path, format="wav")
#                 duration_ms = len(audio)
#                 segment_window_ms = window_length * 1000  # 窗口时长（毫秒）
#                 segment_length_ms = segment_length * 1000  # 采样时长（毫秒）

#                 s = 0
#                 while s < duration_ms:
#                     window_index = s // segment_window_ms  # 计算窗口索引
#                     s_end = s + segment_window_ms
#                     actual_s_end = min(s_end, duration_ms)
#                     window_duration = actual_s_end - s

#                     # 只有当窗口时长大于等于采样时长时才处理
#                     if window_duration >= segment_length_ms:
#                         max_start = actual_s_end - segment_length_ms
#                         # 生成随机起始点（包含边界）
#                         random_start = random.randint(s, max_start)
#                         # 提取音频片段
#                         chunk = audio[random_start : random_start + segment_length_ms]
#                         # 生成输出文件名
#                         output_filename = f"{base_name}_window{window_index+1}_{(random_start / 1000.0):.1f}_{((random_start + segment_length_ms) / 1000.0):.1f}.mp3"
#                         output_path = os.path.join(output_dir, output_filename)
#                         # 保存音频片段
#                         chunk.export(output_path, format="mp3")
                    
#                     # 移动到下一个窗口
#                     s += segment_window_ms

#                 # 删除临时文件
#                 os.remove(temp_audio_path)

#             except Exception as e:
#                 print(f"处理 {filename} 时发生错误: {str(e)}")

# if __name__ == "__main__":
#     input_directory = "/media/yjc/新加卷/201910/安妮/2019年10月"
#     output_directory = "/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/all_mp3"
#     # input_directory = "/home/yjc/Projects/VideoClassify/pipeline_code/stage1/"
#     # output_directory = "./"
#     split_audio(input_directory, output_directory)




# # 重要！！！校验生成的mp3数量是否等于原mp4数量
# import os 
# mp3_dict = set()
# for root, dirs, files in os.walk("/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/all_mp3"):
#     for file in files:
#         if file.endswith(".mp3"):
#             # basename = file.split(".mp3")[0]
#             basename = file.split(".mp3")[0].split("_window")[0]
#             if basename not in mp3_dict:
#                 mp3_dict.add(basename)
# for root, dirs, files in os.walk("/media/yjc/新加卷/201910/安妮/2019年10月"):
#     for file in files:
#         if file.endswith(".mp4"):
#             basename = file.split(".mp4")[0]
#             if basename not in mp3_dict:
#                 print(file)