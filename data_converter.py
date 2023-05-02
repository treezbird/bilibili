# csv_converter.py
import os
import pandas as pd

def convert_csv(input_folder):
    output_folder = 'output/play_info'
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取并处理CSV文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, 'play_info.csv')

            # 读取CSV文件，只选取第一列和第三列
            df = pd.read_csv(input_path, usecols=[0, 2], header=None)

            # 对选取的列进行转换
            for col in [0, 2]:
                df[col] = df[col].apply(lambda x: float(x.replace('万', '')) * 10000 if '万' in str(x) else x)

            # 保存转换后的数据
            if not os.path.exists(output_path):
                df.to_csv(output_path, index=False, header=False)
            else:
                # 如果play_info.csv已经存在，则将新数据附加到文件中
                with open(output_path, 'a', newline='') as f:
                    df.to_csv(f, index=False, header=False)
    
    return output_folder
