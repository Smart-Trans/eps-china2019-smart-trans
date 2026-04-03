import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
# 设置绘图风格为深色网格，使用柔和的色调
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    # 读取数据，处理警告信息
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]

    # 定义能源分类
    coal_sources = ['hard coal', 'lignite']
    petroleum_sources = ['diesel', 'LPG', 'gasoline', 'fuel oil', 'jet fuel', 'crude oil', 'biofuel gasoline',
                         'biofuel diesel']
    natural_gas_sources = ['natural gas']  # 假设数据中天然气的表示方式为'natural gas'
    renewable_sources = ['wind', 'solar', 'hydro', 'biomass', 'nuclear', 'geothermal']

    sources = {
        "Coal": coal_sources,
        "Petroleum": petroleum_sources,
        "Natural Gas": natural_gas_sources,
        "Renewable": renewable_sources
    }

    processed_data = pd.DataFrame(index=year_columns)

    for source_type, source_list in sources.items():
        source_sum = pd.Series(0, index=year_columns)
        non_energy_use_sum = pd.Series(0, index=year_columns)
        for source in source_list:
            primary_pattern = f"BAU Total Primary Energy Use.*{source}"
            primary_use = data[data['Time'].str.contains(primary_pattern, regex=True) &~data['Time'].str.contains("Output")]
            # print(primary_use.head)
            # print(primary_use.tail)
            source_sum += primary_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

            non_energy_pattern = f"BAU Industrial Fuel Use for Non Energy Purposes.*{source}"
            non_energy_use = data[data['Time'].str.contains(non_energy_pattern, regex=True)]
            # print(non_energy_use.head)
            # print(non_energy_use.tail)
            non_energy_use_sum += non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

        net_consumption = (source_sum - non_energy_use_sum) * 1.0E-12
        processed_data[source_type] = net_consumption

    return processed_data


def plot_energy_consumption(processed_data, output_folder, language):
    if language=='cn':
        processed_data=processed_data/10000
    titles = {
        'en': 'Total Primary Energy Use by Fuel',
        'cn': '分品种一次能源消费量'
    }
    ylabels = {
        'en': 'trillion btu',
        'cn': '亿吨标煤'
    }

    # 为每个能源种类设置一个颜色
    colors = {
        "Coal": "#969696",
        "Petroleum": "#000000",
        "Natural Gas": "#c01b00",
        "Renewable": "#00b050"
    }
    
    ncols={
        "cn":4,
        "en":4
        }

    # 根据语言设置字体
    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        processed_data=processed_data* 3.60087861438191
    else:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))

    # 指定颜色并绘图
    processed_data=processed_data.astype(float)
    bottom_array = np.zeros(len(processed_data))
    for column in processed_data.columns:
        axs[1].fill_between(processed_data.index.astype(int), bottom_array, bottom_array + processed_data[column], label=column, color=colors[column], edgecolor='none')

        tabletoshow[column] = list(processed_data[column])
        bottom_array += processed_data[column]
    # ax = processed_data.plot(kind='area', stacked=True, color=[colors[col] for col in processed_data.columns], ax=ax)
    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    axs[1].set_xlim([2023,2060])
    # 设置标题和轴标签的字体属性

    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1)  # 通过坐标来微调标签位置

    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    
    # 根据语言设置图例
    if language == 'cn':
        labels = ['煤炭', '油品', '天然气', '可再生能源']
    else:
        labels = ['Coal', 'Petroleum', 'Natural Gas', 'Renewable']

    handles, _ = axs[1].get_legend_handles_labels()
    axs[1].legend(handles, labels, loc=8,
              bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
        sum_row = selected_rows.sum().values.round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().astype(int)
        sum_row = selected_rows.sum().values.astype(int)
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
    # 设置y轴上限为原数据绘图最高值的1.2倍
    max_value = processed_data.sum(axis=1).max()
    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 100)
    else:
        plt.ylim(0,300000)


    # 保存图表
    output_path = f"{output_folder}/图4：分品种一次能源消费量{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/图4：分品种一次能源消费量{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "D:\\实习\\EPS\\EPS数据\\全国\\11.13全国快速BAU.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\快速BAU\\"

    # 正确接收返回值
    plot_data = read_and_prepare_data(file_path)

    # 绘制并保存中文版图表
    plot_energy_consumption(plot_data, output_folder, 'cn')
    # 绘制并保存英文版图表
    plot_energy_consumption(plot_data, output_folder, 'en')
