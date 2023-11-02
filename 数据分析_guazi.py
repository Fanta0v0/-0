import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from wordcloud import WordCloud

# 读取CSV文件
file_name = "瓜子二手车广州数据.csv"
data = pd.read_csv(file_name, delimiter=",")


def danwei(kilometers_str):
    if '万公里' in kilometers_str:
        # 如果包含'万公里'，则将其转换为公里
        kilometers = float(kilometers_str.replace('万公里', '')) * 10000
    else:
        # 否则，假设已经是公里
        kilometers = float(kilometers_str.replace('公里', ''))
    return kilometers


# 使用函数将数据中的公里数统一为公里单位
data['公里数'] = data['公里数'].apply(danwei)

# 提取车辆型号前两个字符作为品牌
data['品牌'] = data['车辆型号'].apply(lambda x: x.split(' ')[0][:2])
# 计算每个品牌的数量
brand_counts = data['品牌'].value_counts()
# 生成词云图
wordcloud = WordCloud(font_path='simsun.ttc', width=800, height=400,
                      background_color='white').generate_from_frequencies(brand_counts)
# 显示词云图
plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.title("瓜子二手车广州数据 - 品牌词云")
plt.show()


#  绘制价格的分布曲线
plt.figure(figsize=(10, 6))
sns.kdeplot(data['价格（万元）'], fill=True)
plt.title('价格分布曲线')
plt.xlabel('价格（万元）')
plt.ylabel('密度')
plt.show()

#  绘制公里数的分布曲线
plt.figure(figsize=(10, 6))
sns.kdeplot(data['公里数'], fill=True)
plt.title('公里数分布曲线')
plt.xlabel('公里数（公里）')
plt.ylabel('密度')
plt.show()


# 计算每个车龄数量
car_age_counts = data['车龄（年）'].value_counts()
# 绘制车龄占比的饼图
plt.figure(figsize=(8, 8))
plt.pie(car_age_counts, labels=car_age_counts.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # 使饼图保持圆形
plt.title('车龄占比')
plt.show()


def plot(data_name, brand_name):
    # 提取车龄（年）和价格（万元）数据
    car_age = data_name['车龄（年）']
    price = data_name['价格（万元）']

    # 计算每个车龄下的平均价格
    average_price_by_age = data_name.groupby('车龄（年）')['价格（万元）'].mean().reset_index()

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='车龄（年）', y='价格（万元）', data=average_price_by_age, marker='o', color='blue', label='平均价格')
    plt.title(f'{brand_name} - 车龄与平均价格的关系')
    plt.xlabel('车龄（年）')
    plt.ylabel('平均价格（万元）')

    # 计算线性回归模型
    slope, intercept, r_value, p_value, std_err = stats.linregress(car_age, price)

    # 绘制线性回归线
    sns.lineplot(x=car_age, y=slope * car_age + intercept, color='red', label=f'线性回归线 (R={r_value:.2f})')

    # 设置X轴刻度为整数
    plt.xticks(list(average_price_by_age['车龄（年）']))

    plt.legend()
    plt.show()

    # 提取公里数和价格数据
    mileage = data_name['公里数']
    price = data_name['价格（万元）']

    # 绘制公里数与价格的散点图和线性回归线
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=mileage, y=price, color='blue', marker='o', label='散点图')
    plt.title(f'{brand_name} - 公里数与价格的关系')
    plt.xlabel('公里数')
    plt.ylabel('价格（万元）')

    # 计算公里数与价格的线性回归模型
    slope, intercept, r_value, p_value, std_err = stats.linregress(mileage, price)

    # 绘制线性回归线
    sns.lineplot(x=mileage, y=slope * mileage + intercept, color='red', label=f'线性回归线 (R={r_value:.2f})')

    plt.legend()
    plt.show()


# 创建一个包含所有品牌数据的数据框
brands = ['吉利', '大众', '奔驰', '奥迪', '宝马']
all_data = []
for brand in brands:
    file_name = f"瓜子二手车广州{brand}数据.csv"
    data = pd.read_csv(file_name, delimiter=",")
    data['公里数'] = data['公里数'].apply(danwei)
    plot(data, brand)
    data['品牌'] = brand
    all_data.append(data)


combined_data = pd.concat(all_data)

# 创建一个包含三个子图的图形
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 绘制价格分布的箱线图
sns.boxplot(ax=axes[0], x='品牌', y='价格（万元）', data=combined_data)
axes[0].set_title('不同品牌车辆的价格分布对比')
axes[0].set_xlabel('品牌')
axes[0].set_ylabel('价格（万元）')


# 绘制车龄分布的箱线图
sns.boxplot(ax=axes[1], x='品牌', y='车龄（年）', data=combined_data)
axes[1].set_title('不同品牌车辆的车龄分布对比')
axes[1].set_xlabel('品牌')
axes[1].set_ylabel('车龄（年）')

# 绘制公里数分布的箱线图
sns.boxplot(ax=axes[2], x='品牌', y='公里数', data=combined_data)
axes[2].set_title('不同品牌车辆的公里数分布对比')
axes[2].set_xlabel('品牌')
axes[2].set_ylabel('公里数')

# 调整子图之间的间距
plt.tight_layout()
plt.show()

