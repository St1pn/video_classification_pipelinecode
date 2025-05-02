from moviepy.video.io.VideoFileClip import VideoFileClip

def split_video_into_two(input_video_path, output_video_1_path, output_video_2_path):
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

input_video = "/media/yjc/新加卷/201910/由悠yoyo/2019年10月/由悠yoyo_2019-10-18_20-24_60.3min_0.mp4"
output_video_1 = "first_half_video.mp4"
output_video_2 = "second_half_video.mp4"

split_video_into_two(input_video, output_video_1, output_video_2)






# import subprocess

# def split_video_ffmpeg(input_path, output_first_half, output_second_half):
#     # 获取视频时长
#     cmd_get_duration = f'ffmpeg -i {input_path} 2>&1 | grep "Duration" | cut -d " " -f 4 | sed s/,//'
#     result = subprocess.run(cmd_get_duration, shell=True, capture_output=True, text=True)
#     duration_str = result.stdout.strip()
#     hours, minutes, seconds = map(float, duration_str.split(':'))
#     total_seconds = hours * 3600 + minutes * 60 + seconds
#     mid_point = total_seconds / 2

#     # 切割前半部分
#     cmd_first_half = f'ffmpeg -i {input_path} -t {mid_point} -c copy {output_first_half}'
#     subprocess.run(cmd_first_half, shell=True)

#     # 切割后半部分
#     cmd_second_half = f'ffmpeg -i {input_path} -ss {mid_point} -c copy {output_second_half}'
#     subprocess.run(cmd_second_half, shell=True)

# input_video = '/media/yjc/新加卷/201910/由悠yoyo/2019年10月/由悠yoyo_2019-10-18_20-24_60.3min_0.mp4'
# first_half_output = 'first_half_ffmpeg.mp4'
# second_half_output = 'second_half_ffmpeg.mp4'
# split_video_ffmpeg(input_video, first_half_output, second_half_output)
