import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import time
import argparse


sta = time.time()

# def extract_frames(video_path):
#     """
#     从视频中提取所有帧
#     :param video_path: 视频文件路径
#     :return: 帧列表
#     """
#     cap = cv2.VideoCapture(video_path)
#     frames = []
#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if frame_count % 3 == 0:  # 每隔2帧取1帧，即每3帧中取第1帧
#             frame = cv2.resize(frame, (512, 512))
#             frames.append(frame)
#         frame_count += 1
#         # 跳过接下来的2帧
#         for _ in range(2):
#             cap.read()
#     cap.release()
#     return frames


# def frame_to_feature(frame):
#     """
#     将帧转换为特征向量
#     :param frame: 视频帧
#     :return: 特征向量
#     """
#     # 这里简单地将帧转换为一维向量作为特征
#     return frame.flatten()


# def kmeans_keyframe_selection(frames, num_clusters):
#     """
#     使用K-Means算法选择关键帧
#     :param frames: 视频帧列表
#     :param num_clusters: 聚类的数量，即关键帧的数量
#     :return: 关键帧列表
#     """
#     features = [frame_to_feature(frame) for frame in frames]
#     features = np.array(features)
#     kmeans = KMeans(n_clusters=num_clusters)
#     kmeans.fit(features)
#     # 获取每个聚类的中心索引
#     labels = kmeans.labels_
#     centers = kmeans.cluster_centers_
#     keyframes = []
#     for i in range(num_clusters):
#         # 找到距离聚类中心最近的帧
#         cluster_indices = np.where(labels == i)[0]
#         cluster_features = features[cluster_indices]
#         distances = np.linalg.norm(cluster_features - centers[i], axis=1)
#         closest_index = cluster_indices[np.argmin(distances)]
#         keyframes.append(frames[closest_index])
#     return keyframes


# def save_keyframes(keyframes, output_folder):
#     """
#     保存关键帧到指定文件夹
#     :param keyframes: 关键帧列表
#     :param output_folder: 输出文件夹路径
#     """
#     import os
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#     for i, keyframe in enumerate(keyframes):
#         output_path = os.path.join(output_folder, f'keyframe_{i}.jpg')
#         cv2.imwrite(output_path, keyframe)


# if __name__ == "__main__":
#     video_path = '/media/yjc/新加卷/201910/ZMiKo/201910_ZMiKo_stage1_remain/ZMiKo_2019-10-07_00-18_60.3min_4.mp4'
#     num_clusters = 30  # 关键帧的数量
#     output_folder = 'keyframes'
#     frames = extract_frames(video_path)
#     keyframes = kmeans_keyframe_selection(frames, num_clusters)
#     save_keyframes(keyframes, output_folder)






















def extract_frames(video_path):
    """
    从视频中提取所有帧
    :param video_path: 视频文件路径
    :return: 帧列表和对应的帧号列表
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"视频的帧率为: {fps} 帧/秒")
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    total_duration = total_frames / fps
    print(f"视频的总时长为: {total_duration} 秒")
    num_clusters = int(total_duration / 6)  # 以每6s一帧这样大致估算聚类中心
    print(f"聚类中心个数：{num_clusters}")
    frames = []
    frame_numbers = []
    frame_count = 0
    frames_4dataset = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 4 == 0:  # 每隔4帧取1帧
            frame = cv2.resize(frame, (336, 256))
            frame_4dataset = cv2.resize(frame, (640, 512))

            frames.append(frame)
            frame_numbers.append(frame_count)
            frames_4dataset.append(frame_4dataset)
        frame_count += 1
    cap.release()
    return frames, frame_numbers, num_clusters, frames_4dataset, fps


def frame_to_feature(frame):
    """
    将帧转换为特征向量
    :param frame: 视频帧
    :return: 特征向量
    """
    # 这里简单地将帧转换为一维向量作为特征
    return frame.flatten()


def kmeans_keyframe_selection(frames, num_clusters):
    """
    使用K-Means算法选择关键帧
    :param frames: 视频帧列表
    :param num_clusters: 聚类的数量，即关键帧的数量
    :return: 关键帧索引列表
    """
    features = [frame_to_feature(frame) for frame in frames]
    features = np.array(features)
    kmeans = KMeans(n_clusters=num_clusters, max_iter=10000000)
    kmeans.fit(features)
    # 获取每个聚类的中心索引
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    keyframe_indices = []
    for i in range(num_clusters):
        # 找到距离聚类中心最近的帧
        cluster_indices = np.where(labels == i)[0]
        cluster_features = features[cluster_indices]
        distances = np.linalg.norm(cluster_features - centers[i], axis=1)
        closest_index = cluster_indices[np.argmin(distances)]
        keyframe_indices.append(closest_index)
    return keyframe_indices


def save_keyframes(keyframes, frame_numbers, fps, output_folder):
    """
    保存关键帧到指定文件夹
    :param keyframes: 关键帧列表
    :param frame_numbers: 关键帧对应的帧号列表
    :param output_folder: 输出文件夹路径
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for i, keyframe in enumerate(keyframes):
        frame_number = frame_numbers[i]
        output_path = os.path.join(output_folder, f'keyframe_frame_{frame_number}_{int(frame_number/fps)}.png')
        cv2.imwrite(output_path, keyframe)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='传入必要的参数')
    # parser.add_argument('--partial_inferred_res_path', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/201910_安妮/label_group5_thigh_calf_back_dance.txt",
    #                 help='所有图片所在目录')
    parser.add_argument('--video_path', type=str, default="/media/yjc/新加卷/201910/MH丶CICI/201910_MH丶CICI_stage1_remain/MH丶CICI_2019-10-01_13-13_60.2min_2.mp4",
                    help='所有图片所在目录')
    parser.add_argument('--output_folder', type=str, default="/home/yjc/Projects/VideoClassify/all_video_frames/201910_MH丶CICI/keyframes_6s4interval/MH丶CICI_2019-10-01_13-13_60.2min_2",
                    help='所有图片所在目录')
    args = parser.parse_args()

    # num_clusters = 36  # 关键帧的数量
    video_path = args.video_path
    output_folder = args.output_folder
    print(output_folder)
    if not os.path.exists(output_folder):
        frames, frame_numbers, num_clusters, frames_4dataset, fps = extract_frames(video_path)
        keyframe_indices = kmeans_keyframe_selection(frames, num_clusters)
        keyframes = [frames_4dataset[i] for i in keyframe_indices]
        selected_frame_numbers = [frame_numbers[i] for i in keyframe_indices]
        save_keyframes(keyframes, selected_frame_numbers, fps, output_folder)

        print(f"total time: {(time.time()-sta)}")
    else:
        import sys
        sys.exit(1)
        # print(output_folder + "!!!Already Exists!!!")