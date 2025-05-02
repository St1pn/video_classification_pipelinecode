import math
from transformers import AutoTokenizer, AutoModel
import numpy as np
import torch
import torchvision.transforms as T
from decord import VideoReader, cpu
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer
import os 
from tqdm import tqdm 
import multiprocessing
import time 
import json 


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

# def load_image(image_file, input_size=448, max_num=12):
#     image = Image.open(image_file).convert('RGB')
#     transform = build_transform(input_size=input_size)
#     images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
#     pixel_values = [transform(image) for image in images]
#     pixel_values = torch.stack(pixel_values)
#     return pixel_values

def load_image(image_file):
    
    image = Image.open(image_file).convert('RGB')
    # 获取图像的宽度和高度
    width, height = image.size
    # 创建一个新的图像对象
    new_image = Image.new(image.mode, (width, height))
    
    # 脚本开始后待注释
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
            # # 计算反转后的列索引
            new_x = wd_list.index(x)
            new_y = hei_list.index(y)
            
            # 获取原图像指定位置的像素值
            pixel = image.getpixel((x, y))
            # 将像素值设置到新图像的反转位置
            new_image.putpixel((new_x, new_y), pixel)
    
    # for调试
    # assert new_image == new_image1
    # print(np.array(new_image)[0][1])
    
    
    new_image = new_image.resize([448, 448], resample=Image.LANCZOS, box=None, reducing_gap=None)  # 根据实际情况修改
    tiaoshi_filename = str(os.path.basename(image_file)).split(".")[0]

    # new_image.save(f"./for_tiaoshi_{tiaoshi_filename}.png", "png")
    
    return (image_file, new_image)


def preprocess_load_image(image_pil, input_size=448, max_num=1):
    transform = build_transform(input_size=input_size)
    # images = dynamic_preprocess(new_image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    # print([img.size for img in images])
    # print([np.array(img).shape for img in images])
    # pixel_values = [transform(img) for img in images]
    
    pixel_values = [transform(image_pil)]
    pixel_values = torch.stack(pixel_values)
    
    
    return pixel_values

# # 3块L20的最大限度使用GPU的分配模型层的方式
# def split_model(model_name):
#     device_map = {}
#     world_size = torch.cuda.device_count()
#     num_layers = {
#         'InternVL2_5-1B': 24, 'InternVL2_5-2B': 24, 'InternVL2_5-4B': 36, 'InternVL2_5-8B': 32,
#         'InternVL2_5-26B': 48, 'InternVL2_5-38B': 64, 'InternVL2_5-78B': 80}[model_name]
#     # Since the first GPU will be used for ViT, treat it as half a GPU.
#     num_layers_per_gpu = math.ceil(num_layers / (world_size - 0.5))
#     num_layers_per_gpu = [num_layers_per_gpu] * world_size
#     num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0 + 9)
#     num_layers_per_gpu[1] = math.ceil(22)
#     num_layers_per_gpu[2] = math.ceil(32)
#     layer_cnt = 0
#     for i, num_layer in enumerate(num_layers_per_gpu):
#         for j in range(num_layer):
#             device_map[f'language_model.model.layers.{layer_cnt}'] = i
#             layer_cnt += 1
#     device_map['vision_model'] = 1
#     device_map['mlp1'] = 0
#     device_map['language_model.model.tok_embeddings'] = 0
#     device_map['language_model.model.embed_tokens'] = 0
#     device_map['language_model.output'] = 0
#     device_map['language_model.model.norm'] = 0
#     device_map['language_model.lm_head'] = 0
#     device_map[f'language_model.model.layers.{num_layers - 1}'] = 2
#     print(device_map)

#     return device_map

# # 2块L20的最大限度使用GPU的分配模型层的方式
# def split_model(model_name):
#     device_map = {}
#     world_size = torch.cuda.device_count()
#     num_layers = {
#         'InternVL2_5-1B': 24, 'InternVL2_5-2B': 24, 'InternVL2_5-4B': 36, 'InternVL2_5-8B': 32,
#         'InternVL2_5-26B': 48, 'InternVL2_5-38B': 64, 'InternVL2_5-78B': 80}[model_name]
#     # Since the first GPU will be used for ViT, treat it as half a GPU.
#     num_layers_per_gpu = math.ceil(num_layers / (world_size - 0.5))
#     num_layers_per_gpu = [num_layers_per_gpu] * world_size
#     num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0 + 19)
#     num_layers_per_gpu[1] = math.ceil(44)
#     layer_cnt = 0
#     for i, num_layer in enumerate(num_layers_per_gpu):
#         for j in range(num_layer):
#             device_map[f'language_model.model.layers.{layer_cnt}'] = i
#             layer_cnt += 1
#     device_map['vision_model'] = 0
#     device_map['mlp1'] = 0
#     device_map['language_model.model.tok_embeddings'] = 0
#     device_map['language_model.model.embed_tokens'] = 0
#     device_map['language_model.output'] = 0
#     device_map['language_model.model.norm'] = 0
#     device_map['language_model.lm_head'] = 0
#     device_map[f'language_model.model.layers.{num_layers - 1}'] = 0
#     print(device_map)

#     return device_map

# 2块H20的最大限度使用GPU的分配模型层的方式
def split_model(model_name):
    device_map = {}
    world_size = torch.cuda.device_count()
    num_layers = {
        'InternVL2_5-1B': 24, 'InternVL2_5-2B': 24, 'InternVL2_5-4B': 36, 'InternVL2_5-8B': 32,
        'InternVL2_5-26B': 48, 'InternVL2_5-38B': 64, 'InternVL2_5-78B': 80}[model_name]
    # Since the first GPU will be used for ViT, treat it as half a GPU.
    num_layers_per_gpu = math.ceil(num_layers / (world_size - 0.5))
    num_layers_per_gpu = [num_layers_per_gpu] * world_size
    num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0 + 9)
    num_layers_per_gpu[1] = math.ceil(54)
    layer_cnt = 0
    for i, num_layer in enumerate(num_layers_per_gpu):
        for j in range(num_layer):
            device_map[f'language_model.model.layers.{layer_cnt}'] = i
            layer_cnt += 1
    device_map['vision_model'] = 0
    device_map['mlp1'] = 0
    device_map['language_model.model.tok_embeddings'] = 0
    device_map['language_model.model.embed_tokens'] = 0
    device_map['language_model.output'] = 0
    device_map['language_model.model.norm'] = 0
    device_map['language_model.lm_head'] = 0
    device_map[f'language_model.model.layers.{num_layers - 1}'] = 0
    print(device_map)

    return device_map



path = "/root/autodl-fs/InternVL2_5-38B"
# path = "/root/autodl-tmp/InternVL2_5-38B"
device_map = split_model('InternVL2_5-38B')
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    use_flash_attn=True,
    trust_remote_code=True,
    device_map=device_map).eval()
tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True, use_fast=False)
generation_config = dict(max_new_tokens=1024, do_sample=True)


# # single-image single-round conversation (单图单轮对话)
# pixel_values = load_image('/root/autodl-fs/examples/for_tiaoshi_randomcropped_resize_outputvideo_00063.png', max_num=12).to(torch.bfloat16).cuda()
# question = '<image>\nPlease describe the image in details.'
# # question = '<image>\nPlease describe the image shortly.'
# response = model.chat(tokenizer, pixel_values, question, generation_config)
# print(f'User: {question}\nAssistant: {response}')


# 读取已经处理过的图片名称，以支持断点继续预测
img_names = set()
try:
    with open("./infered_res_1.txt") as f1:
        for line in f1.readlines():
            line_js = json.loads(line.strip())
            img_n = line_js["image_name"]
            sta = img_n.index("QLAN%")
            if img_n[sta:] not in img_names:
                img_names.add(img_n[sta:])
    print(list(img_names)[:5])
    print(len(img_names))
except:
    print("No already infered_res!!!")


# 遍历经过裁剪图片目录下的所有png文件的绝对路径
current_dir = "/root/autodl-fs/examples/thumos14_sample_1"  # 根据实际情况修改
all_pngs = []
for root, dirs, files in os.walk(current_dir):
    for file in files:
        if file.endswith('.png'):
            if file[file.index("QLAN%"):] not in img_names:
                all_pngs.append(os.path.join(root, file))
print("all_pngs_len: ", len(all_pngs))

# 并行推理（多进程预处理输入）
interval = 80
with open("./infer_res.txt", "w") as f:  #输出文件根据实际情况修改
    for i in tqdm(range(0, len(all_pngs), interval)):  # interval大小根据实际情况修改
        load_image_fn_pil_list = []
        with multiprocessing.Pool(processes=interval) as pool:
            # pool = multiprocessing.Pool(processes=8)  # 创建4个进程
            load_image_fn_pil_list = pool.map(load_image, all_pngs[i:i+interval])  # interval大小根据实际情况修改

        load_image_files = [fn_pil[0] for fn_pil in load_image_fn_pil_list]
        load_image_list = [fn_pil[1] for fn_pil in load_image_fn_pil_list]
        pixel_values_list = []
        for loaded_image in load_image_list:
            pixel_values_list.append(preprocess_load_image(loaded_image).to(torch.bfloat16).cuda())

        num_patches_list = [pixel_values.size(0) for pixel_values in pixel_values_list]
        # print("num_patches_list: ", num_patches_list)
        pixel_values = torch.cat(tuple(pixel_values for pixel_values in pixel_values_list), dim=0)
        
        # 脚本开始后待注释
        q = """Ignore the person shown in the background picture frame. Now answer the following questions by selecting one option from the given choices, output the result in JSON format as {"question1": your choice, "question2": your choice, ...}:
                question1: How many fully-formed heads of different people can be spotted in this picture? (numbers)
                question2: Does the shot capture less than half of the left/right body figure? (yes/no)
                question3: Is she dancing or twisting her body? (yes/no)
                question4: Is she sticking the buttocks out toward us? (yes/no)
                question5: Can we see the frontal part of her buttocks? (yes/no)
                question6: In which direction is the entire back oriented? (directly towards us in a straight way/away from us/sideways to us)
                question7: Can we see her calf or thigh? (calf/thigh/both)
                question8: Can we see her all facial features? (yes/no)
                question9: what is her posture right now?(standing/kneeling/sitting)"""
        questions = ['<image>\n' + q] * len(num_patches_list)

        generation_config = dict(max_new_tokens=1024, do_sample=True)
        responses = model.batch_chat(tokenizer, pixel_values,
                                     num_patches_list=num_patches_list,
                                     questions=questions,
                                     generation_config=generation_config)
        for fn, question, response in zip(load_image_files, questions, responses):
            f.write(json.dumps({"image_name": fn, "User": question, "Assistant": response}, ensure_ascii=False)+"\n")
        
        # 调用 f.flush() 把数据刷新到磁盘
        f.flush()