import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def extract_frames(video_path, start_time, end_time, output_folder):
    """
    提取指定时间段内的视频帧
    :param video_path: 视频文件路径
    :param start_time: 开始时间（秒）
    :param end_time: 结束时间（秒）
    :param output_folder: 输出帧图片的文件夹
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 计算开始和结束的帧数
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 设置视频读取位置到开始帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_count = start_frame
    while cap.isOpened() and frame_count < end_frame:
        ret, frame = cap.read()
        if ret:
            # 保存帧图片
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        else:
            break

    # 释放视频捕获对象
    cap.release()

def extract_video_clip(video_path, start_time, end_time, output_path):
    """
    提取指定时间段的视频片段
    :param video_path: 视频文件路径
    :param start_time: 开始时间（秒）
    :param end_time: 结束时间（秒）
    :param output_path: 输出视频片段的文件路径
    """
    # 加载视频文件
    clip = VideoFileClip(video_path)

    # 剪辑指定时间段的视频
    subclip = clip.subclip(start_time, end_time)

    # 保存剪辑后的视频
    subclip.write_videofile(output_path, codec="libx264")

    # 关闭视频剪辑对象
    clip.close()
    subclip.close()

if __name__ == "__main__":
    video_path = "your_video.mp4"
    start_time = 10  # 开始时间（秒）
    end_time = 20    # 结束时间（秒）
    frames_output_folder = "extracted_frames"
    clip_output_path = "extracted_clip.mp4"

    # 提取帧图片
    extract_frames(video_path, start_time, end_time, frames_output_folder)

    # 提取视频片段
    extract_video_clip(video_path, start_time, end_time, clip_output_path)
    