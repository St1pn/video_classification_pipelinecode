from io import BytesIO
from urllib.request import urlopen
import librosa
from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor
from tqdm import tqdm 

processor = AutoProcessor.from_pretrained("/root/autodl-fs/Qwen2-Audio-7B-Instruct")
model = Qwen2AudioForConditionalGeneration.from_pretrained("/root/autodl-fs/Qwen2-Audio-7B-Instruct", device_map="auto")


# conversation1 = [
#     {"role": "user", "content": [
#         {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/glass-breaking-151256.mp3"},
#         {"type": "text", "text": "What's that sound?"},
#     ]},
#     {"role": "assistant", "content": "It is the sound of glass shattering."},
#     {"role": "user", "content": [
#         {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/f2641_0_throatclearing.wav"},
#         {"type": "text", "text": "What can you hear?"},
#     ]}
# ]

# conversation2 = [
#     {"role": "user", "content": [
#         {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/1272-128104-0000.flac"},
#         {"type": "text", "text": "What does the person say?"},
#     ]},
# ]



q = """Analyze the song's rhythm and style, output JSON format:
{
  "beat": {"pattern": "time signature", "bpm": "beats per minute"}, 
  "style": [
    {
      "type": "main genre", 
      "subtype": "specific subgenre", 
      "confidence": "confidence score 0-1",
      "features": ["characteristic features (e.g. strong bass pulses/flute timbre/Breath vocals/etc.)"]
    }
  ],
  "mood_tags": ["emotional perceptions (at least 5 words. e.g. energetic/nostalgic/sad/...)"]
}"""
# q = """请分析这首歌的节奏和风格，输出JSON格式：
# {
#   "beat": {"pattern": "拍号（如4/4）", "bpm": "每分钟节拍数"}, 
#   "style": [
#     {
#       "type": "风格大类（如电子舞曲）", 
#       "subtype": "具体子类（如Melbourne Bounce）", 
#       "confidence": "置信度0-1",
#       "features": ["引发该判断的特征（如：强烈的低频脉冲/笛子音色）"]
#     }
#   ],
#   "mood_tags": ["带给人的感觉（如：激情/怀旧）"]
# }"""
# q = """里面的歌词是什么"""

import os 
all_conversations = []
file_names = []
for root, dirs, files in os.walk("/root/autodl-fs/examples/all_mp3"):
    for file in files:
        conversation = [
        {"role": "user", "content": [
            {"type": "audio", "audio_url": "file://" + str(os.path.join(root, file)).replace("%", "_")},
            {"type": "text", "text": q},
            ]}
        ]
        all_conversations.append(conversation)
        file_names.append(file)

interval = 8
with open("/root/autodl-fs/examples/infer_res.txt", "w") as f:
    for i in tqdm(range(0, len(all_conversations), interval)):
        conversations = all_conversations[i:i+interval]

        text = [processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False) for conversation in conversations]

        audios = []
        for conversation in conversations:
            for message in conversation:
                if isinstance(message["content"], list):
                    for ele in message["content"]:
                        if ele["type"] == "audio":
                            audios.append(
                                librosa.load(
                                    BytesIO(urlopen(ele['audio_url']).read()), 
                                    sr=processor.feature_extractor.sampling_rate)[0]
                            )

        inputs = processor(text=text, audios=audios, return_tensors="pt", padding=True)
        for key in inputs.keys():
            inputs[key] = inputs[key].to("cuda")
        generate_ids = model.generate(**inputs, max_length=1024)
        # generate_ids = generate_ids[:, inputs.input_ids.size(1):]
        generate_ids = generate_ids[:, inputs["input_ids"].size(1):]

        response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        
        for resp_idx in range(len(response)):
            f.write("file: "+ file_names[i+resp_idx] + str("response: ") + str(response[resp_idx])+"\n")
        f.flush()





















# import os 
# from tqdm import tqdm 
# def rename_files_in_directory(directory, rename_f):
#     # 遍历指定目录及其子目录
#     with open(rename_f, "w") as f1:
#         for root, dirs, files in os.walk(directory):
#             for file in tqdm(files):
#                 if file.split(".")[-1] != "mp3":
#                     continue 

#                 # 获取文件的绝对路径
#                 file_path = os.path.join(root, file)
                
#                 absolute_path = os.path.abspath(file_path)
#                 absolute_path_dir = os.path.dirname(absolute_path)
#                 # print(f"文件的绝对路径: {absolute_path}")

#                 # 获取文件的 basename
#                 base_name = os.path.basename(file_path)
#                 # print(f"文件的 basename: {base_name}")

#                 # 生成新的文件名
#                 new_base_name = "_".join(base_name.split(".")[:-1]) + ".mp3"
#                 # 生成新的文件路径
#                 new_file_path = os.path.join(absolute_path_dir, new_base_name.replace("%", "_"))
#                 print(new_file_path)

#                 # 重命名文件
#                 rename_f = os.path.join(absolute_path_dir, "rename_f.txt")
            
#                 try:
#                     os.rename(file_path, new_file_path)
#                     f1.write(f"文件{file_path}已重命名为: {new_file_path}" + "\n")
#                     f1.flush()
#                 except FileExistsError:
#                     print(f"重命名失败，文件 {new_file_path} 已存在。")
#                 except Exception as e:
#                     print(f"重命名失败，发生错误: {e}")

# # 指定要处理的目录
# directory = '/root/autodl-fs/examples/all_mp3'
# rename_f = "/root/autodl-fs/examples/all_mp3/rename_log"
# rename_files_in_directory(directory, rename_f)