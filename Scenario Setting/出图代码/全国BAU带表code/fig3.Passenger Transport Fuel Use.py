import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 设置绘图风格
sns.set(style='white', palette='muted')

def search(data,col,Str1,Str2="",Str3=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) &  data[col].str.contains(Str3)]

def Sum(data,col):
    return data[col].apply(pd.to_numeric,errors='coerce').fillna(0).sum()

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "electricity": "BAU Transportation Sector Fuel Used.*passenger.*electricity",
        "jet fuel": "BAU Transportation Sector Fuel Used.*passenger.*jet fuel",
        "LPG propane or butane": "BAU Transportation Sector Fuel Used.*passenger.*LPG propane or butane",
        "natural gas": "BAU Transportation Sector Fuel Used.*passenger.*natural gas",
        "petroleum diesel": "BAU Transportation Sector Fuel Used.*passenger.*petroleum diesel",
        "petroleum gasoline": "BAU Transportation Sector Fuel Used.*passenger.*petroleum gasoline"
    }

    for sector_key, pattern in sectors.items():
        print(f"Processing sector: {sector_key}")
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        print(f"Rows matching pattern '{pattern}':")
        print(sector_data['Time'])  # 输出匹配到的行的名称
        print(f"Data for {sector_key}:")
        print(sector_data.head())  # 打印部分数据以便检查
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 3.60087861438191E-12
    processed_data=processed_data.reindex(columns=['petroleum gasoline','petroleum diesel','jet fuel','natural gas','electricity','LPG propane or butane'])
    return processed_data


def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Passenger Transport Fuel Use', 'cn': '载客运输燃料消费'}
    ylabels = {'en': 'trillion btu', 'cn': '吨标煤'}
    if language=='cn':
        processed_data=processed_data
    colors = {
        "electricity": "#f1bb18",
        "jet fuel": "#c2dffd",
        "LPG propane or butane": "#087bf1",
        "natural gas": "#c01b00",
        "petroleum diesel": "#000000",
        "petroleum gasoline": "#969696"
    }

    # 中英文对照字典
    sector_labels = {
        'en': {
            'electricity': 'Electricity',
            'jet fuel': 'Jet Fuel',
            'LPG propane or butane': 'LPG Propane or Butane',
            'natural gas': 'Natural Gas',
            'petroleum diesel': 'Petroleum Diesel',
            'petroleum gasoline': 'Petroleum Gasoline'
        },
        'cn': {
            'electricity': '电力',
            'jet fuel': '航空煤油',
            'LPG propane or butane': '液化石油气',
            'natural gas': '天然气',
            'petroleum diesel': '柴油',
            'petroleum gasoline': '汽油'
        }
    }
    
    ncols = {'en': 3, 'cn': 3}

    if language == 'en':
        processed_data = (processed_data / 3.60087861438191E-12) * 0.000000000001

    # 用于堆叠图的累积值数组
    cumulative = np.zeros(len(processed_data.index))
    stack_baseline = np.zeros(len(processed_data.index))  # 初始化一个与累积值数组形状相同的数组

    fig, axs = plt.subplots(1, 2, figsize=(16, 10))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
      # 获取当前的Axes对象ax

    # 设置坐标轴的颜色
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')

    # 设置坐标轴单位
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    cumulative = np.zeros(len(processed_data.index))
    labels = []
    for sector in processed_data.columns:
        label = sector_labels[language][sector] if language in sector_labels and sector in sector_labels[language] else sector
        labels.append(label)
        sector_values = processed_data[sector].astype(float)
        axs[1].fill_between(processed_data.index.astype(float), cumulative, cumulative + sector_values,
                         color=colors[sector], label=label)
        tabletoshow[label] = list(sector_values)
        cumulative += sector_values.values
        stack_baseline = np.maximum(stack_baseline, cumulative)  # 更新stack_baseline为当前的累积值

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    # 调整图表布局
   
    

    axs[1].set_xlim(left=2023,right=2060)
    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 40000)
    else:
        plt.ylim(0,12000)

    axs[1].yaxis.set_label_coords(0.04, 1)  # 通过坐标来微调标签位置
    axs[1].legend(loc=8, bbox_to_anchor=(0.5, -0.4), ncol=ncols[language],edgecolor="white")
     
    selected_rows = tabletoshow.loc[xticks].transpose().round(1)
    sum_row = selected_rows.sum().values.round(2)
    selected_rows.loc['Total'] = sum_row
    labels.append('Total')
    axs[0].axis('off')
    table = axs[0].table(
    cellText=selected_rows.values,
    rowLabels=labels,
    colLabels=selected_rows.columns,
    loc='bottom',
    bbox=[0.2, -0.15, 0.9, 1.1])
    axs[0].text(0.8, 1.35, titles[language], va='top', ha='left', fontsize=20)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    cell_0_0 = table.get_celld()[(0, 0)]
    cell_height = cell_0_0.get_height()
    table.add_cell(0, -1,width = 0.05,height = cell_height, text=' ', loc='center')
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    output_path = f"{output_folder}\\图3：载客运输燃料消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}\\图3：载客运输燃料消费{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "D:\\实习\\EPS\\EPS数据\\省级\\内蒙data.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\内蒙BAU\\"
    processed_data = read_and_prepare_data(file_path)

    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
