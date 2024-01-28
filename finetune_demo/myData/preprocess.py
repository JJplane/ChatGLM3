import re


def parse_chat_record(record):
    # 使用正则表达式提取发言者、时间和内容
    # 玖尔巴奇 (2021-05-27 22:37:05):我来啦！
    speaker = record.split(" ")[0]
    time = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", record)
    if time:
        time = time.group()
    else:
        time = None
    content = record.split(":")[-1]
    if speaker and time and content:
        return speaker, time, content
    else:
        return None


def parse_chat_records(filename):
    parsed_records = []
    with open(filename, "r",encoding='utf-8') as file:
        for line in file:
            parsed_record = parse_chat_record(line.strip())
            if parsed_record:
                parsed_records.append(parsed_record)
    return parsed_records


# 读取聊天记录
filename = "chat.txt"
records = parse_chat_records(filename)
# 制作数据集，json格式，{"content":玖尔巴奇content,"summary":及🐔content}`"}
import json

dataset = []
# 找到先玖尔巴奇说，后及🐔说的pair
for i in range(len(records) - 1):
    if records[i][0] == "玖尔巴奇" and records[i + 1][0] == '及🐔':
        # 如果任何一个人的记录只有[表情]，[视频/语音通话]，[图片]，则跳过
        if records[i][2] in ["[表情]", "[视频/语音通话]", "[图片]"] or records[i + 1][2] in [
            "[表情]",
            "[视频/语音通话]",
            "[图片]",
        ]:
            continue
        # dataset.append({"content":records[i][2],"summary":records[i + 1][2]})
        dataset.append(
            {
                "conversations": [
                    {"role": "system", "content": "你好，我是及🐔，我是一个聊天机器人，我喜欢聊天，你可以和我聊天哦！"},
                    {"role": "user", "content": records[i][2]},
                    {"role": "assistant", "content": records[i + 1][2]},
                ]
            }
        )
# 保存数据集
with open("dataset.json", "w",encoding='utf-8') as file:
    json.dump(dataset, file, ensure_ascii=False, indent=4)
# 划分训练集和测试集1:99
import random

random.shuffle(dataset)
testset = dataset[: int(len(dataset) * 0.01)]
trainset = dataset[int(len(dataset) * 0.01) :]
# 保存训练集和测试集
with open("train.json", "w",encoding='utf-8') as file:
    json.dump(trainset, file, ensure_ascii=False, indent=4)
with open("dev.json", "w",encoding='utf-8') as file:
    json.dump(testset, file, ensure_ascii=False, indent=4)
