import os
import glob
import pandas as pd

input_folder = 'output/title_detail'
output_file = 'output/id.csv'

# 获取文件夹中的所有CSV文件
csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

# 初始化一个空的列表来存储所有ID
id_list = []

# 遍历所有CSV文件
for file in csv_files:
    # 读取CSV文件
    df = pd.read_csv(file)
    
    # 获取第六列（假设为ID）
    id_column = df.iloc[:, 5]
    
    # 将ID列添加到ID列表中
    id_list.extend(id_column)

# 将ID列表转换为DataFrame
id_dataframe = pd.DataFrame({'ID': id_list})

# 将结果DataFrame保存为CSV文件
id_dataframe.to_csv(output_file, index=False)
