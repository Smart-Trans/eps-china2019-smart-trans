import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
# 设置绘图风格
sns.set(style='white', palette='muted')
colors = ["#4e79a7", "#4e79a7", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7"]
def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')

    year_columns = [str(year) for year in range(2023, 2061)]

    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "Transportation": "BAU Total Energy Use by Sector.*transportation",
        "Residential": "BAU Total Energy Use by Sector.*residential",
        "Commercial": "BAU Total Energy Use by Sector.*commercial",
    }

    for sector_key, pattern in sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 3.60087861438191E-12

#工业燃料计算
    industry_pattern = "BAU Total Energy Use by Sector.*industry"
    industry_data = data[data['Time'].str.contains(industry_pattern, regex=True)]
    industry_sum = industry_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
#非燃料使用
    non_energy_pattern = "BAU Industrial Fuel Use for Non Energy Purposes"
    non_energy_data = data[data['Time'].str.contains(non_energy_pattern, regex=True)]
    non_energy_sum = non_energy_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    processed_data["Industry"] = (industry_sum - non_energy_sum) * 3.60087861438191E-12

    exclusions_patterns = [
        "BAU Industrial Fuel Use for Non Energy Purposes\[coal mining 05,hard coal if\]",
        "BAU Industrial Fuel Use for Non Energy Purposes\[refined petroleum and coke 19,hard coal if\]",
        "BAU Industrial Fuel Use for Non Energy Purposes\[refined petroleum and coke 19,crude oil if\]"
    ]
    non_energy_exclusive_data = non_energy_data[~non_energy_data['Time'].str.contains('|'.join(exclusions_patterns), regex=True)]
    non_energy_exclusive_sum = non_energy_exclusive_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    processed_data["Nonenergy Use"] = non_energy_exclusive_sum * 3.60087861438191E-12

    for col in processed_data.columns:
        processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce').fillna(0)
    processed_data=processed_data.reindex(columns=['Transportation','Industry','Nonenergy Use','Residential','Commercial'])
    return processed_data

def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Final Energy Consumption by Sector', 'cn': '终端能源消费量'}
    ylabels = {'en': 'Trillion btu', 'cn': '亿吨标煤'}
    if language=='cn':
        processed_data=processed_data/10000

    colors = {
        "Transportation": "#c01b00",
        "Residential": "#087bf1",
        "Commercial": "#004185",
        "Industry": "#7C7C7C",
        "Nonenergy Use": "#A5A5A5"
    }

    # 中英文图例名称映射
    sector_names_cn = {
        "Transportation": "交通部门",
        "Residential": "居民建筑",
        "Commercial": "公共建筑",
        "Industry": "工业燃料",
        "Nonenergy Use": "非燃料使用"
    }
    ncols={
        'cn':5,'en':5
        }
    if language == 'en':
       processed_data=processed_data/3.60087861438191
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    cumulative = pd.Series(0, index=processed_data.index)
    processed_data=processed_data.astype(float)
    labels = []
    for sector in processed_data.columns:
        label = sector_names_cn[sector] if language == 'cn' else sector
        labels.append(label)
        axs[1].fill_between(processed_data.index.astype(float), cumulative, cumulative + processed_data[sector], color=colors[sector], label=label)
        cumulative += processed_data[sector]
        tabletoshow[label] = list(processed_data[sector])

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050,2055,2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])  # 修正在这里
    axs[1].set_xlim(left=2023, right=2060)
    # 设置坐标轴颜色为黑色
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')
    # 设置绘图从坐标轴原点开始
    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 70)
    else:
        plt.ylim(0,200000)
    plt.xlim(left=2023, right=2060)



    #plt.title(titles[language], fontsize=18)
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1.02)  # 通过坐标来微调标签位置
    axs[1].legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
        sum_row = selected_rows.sum().values.round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(1)
        sum_row = selected_rows.sum().values.round(1)
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
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    output_path = f"{output_folder}/图5：终端能源消费量{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    plt.title(titles[language], size=18)
    output_path = f"{output_folder}/图5：终端能源消费量{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国BAU图\\"
    processed_data = read_and_prepare_data(file_path)
    
    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表


