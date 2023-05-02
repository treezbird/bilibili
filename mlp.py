import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

def influence_evaluation(new_video_play_count, new_video_danmaku_count):
    class InfluenceMLP(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(InfluenceMLP, self).__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, output_size)

        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x

    def normalize_data(data, mean, std):
        std[std == 0] = 1
        return (data - mean) / std

    # 从CSV文件中读取数据
    video_data = pd.read_csv('output/play_info/play_info.csv', header=None)

    # 检查数据中的NaN值
    print("检查数据中的NaN值：")
    print(video_data.isnull().any())

    # 统计数据的描述
    print("统计数据的描述：")
    print(video_data.describe())

    # 转换为张量
    video_data = torch.tensor(video_data.values, dtype=torch.float32)

    # 计算数据均值和标准差，并标准化数据
    mean = torch.mean(video_data, dim=0)
    std = torch.std(video_data, dim=0)
    normalized_video_data = normalize_data(video_data, mean, std)

    # 计算目标数据：每个视频的影响力比重
    total_play_count = torch.sum(video_data[:, 0]).float()
    target_data = (video_data[:, 0] / total_play_count).reshape(-1, 1)

    # 创建神经网络实例，定义损失函数和优化器
    input_size = 2
    hidden_size = 32
    output_size = 1

    model = InfluenceMLP(input_size, hidden_size, output_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 训练神经网络
    epochs = 500

    for epoch in range(epochs):
        # 前向传播
        outputs = model(normalized_video_data)
        loss = criterion(outputs, target_data)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 输出损失值
        if (epoch+1) % 50 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

    def predict_influence(model, play_count, danmaku_count, mean, std):
        input_data = torch.tensor([[play_count, danmaku_count]], dtype=torch.float32)
        normalized_input_data = normalize_data(input_data, mean, std)
        output = model(normalized_input_data)
        return output.item()

    # 预测一个新视频的影响力比重
    influence_weight = predict_influence(model, new_video_play_count, new_video_danmaku_count, mean, std)
    print("该视频的影响力比重为:", influence_weight)

    return influence_weight