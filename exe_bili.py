import requests
from bs4 import BeautifulSoup
import pandas as pd
from login_bili_no_detail import login_bili
#from login_bili import login_bili   #该代码将会获得所有视频的详细信息，涉及隐私，不予公开
from data_converter import convert_csv
from mlp import influence_evaluation


if __name__ == "__main__":
    search_keyword = "淄博烧烤"
    login_bili(search_keyword)

    # 转换数据
    convert_csv('output/title_detail')

    # 设置新视频的播放量和弹幕数
    new_video_play_count = 4865758
    new_video_danmaku_count = 7319
    
    # 运行影响力预测
    influence_weight = influence_evaluation(new_video_play_count, new_video_danmaku_count)

    # 所有视频总播放量
    df = pd.read_csv('output/play_info/play_info.csv')
    sum = df.iloc[:, 0].sum()
    print("所有视频总播放量为：", sum)

    # 所有视频总弹幕数
    df = pd.read_csv('output/play_info/play_info.csv')
    sum = df.iloc[:, 1].sum()
    print("所有视频总弹幕为：", sum)

    # 所有推举淄博烧烤美味视频总数
    df = pd.read_csv('price_unrelated.csv')
    sum = df.iloc[:, 1].sum()
    print("所有推举淄博烧烤美味视频总数为：", sum)

    # 所有推举淄博烧烤美味弹幕总数
    df = pd.read_csv('price_unrelated.csv')
    sum = df.iloc[:, 2].sum()
    print("所有推举淄博烧烤美味弹幕总数为：", sum)