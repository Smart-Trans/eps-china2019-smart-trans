import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)

    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "Industrial": "Industrial Fuel Use for Energy Purposes.*heat.",
        "Urban Residential": "Building Components Energy Use.*urban residential.*heat.",
        "Rural Residential": "Building Components Energy Use.*rural residential.*heat.",
        "Commercial": "Building Components Energy Use.*commercial.*heat."
    }

    for sector_key, pattern in sectors.items():
        # 确保数据行不包含“BAU”
        sector_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains('BAU') & ~data['Time'].str.contains('Output') & ~data['Time'].str.contains('Perc') & ~data['Time'].str.contains('before')]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 3.60087861438191E-12

    return processed_data



def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'District Heating Demand', 'cn': '分部门集中供热需求'}
    ylabels = {'en': 'trillion btu', 'cn': '万吨标煤'}

    colors = {
        "Industrial": "#9467bd",
        "Urban Residential": "#969696",
        "Rural Residential": "#00b050",
        "Commercial": "#004185"
    }

    sector_labels_cn = {
        "Industrial": "工业部门",
        "Urban Residential": "城镇居民",
        "Rural Residential": "乡村居民",
        "Commercial": "公共建筑"

    }
    
    ncols={'cn':4,'en':4}

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    cumulative = np.zeros(len(processed_data.index))

    if language == 'en':
        # Apply unit conversion for English chart
        processed_data_en = processed_data.copy()
        processed_data_en = processed_data_en /3.60087861438191
        plot_data = processed_data_en
    else:
        plot_data = processed_data

    # 计算每个部门在所有年份的总和，并根据这个总和排序
    sector_sums = plot_data.sum()
    sorted_sectors = sector_sums.sort_values(ascending=False).index

    labels = []
    for sector in sorted_sectors:
        label = sector_labels_cn[sector] if language == 'cn' else sector
        labels.append(label)
        sector_values = plot_data[sector].astype(float)
        axs[1].fill_between(plot_data.index.astype(float), cumulative, cumulative + sector_values, color=colors[sector],
                         label=label)
        tabletoshow[label] = list(sector_values)
        cumulative += sector_values.values

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])  # 修正在这里
    axs[1].set_xlim(left=2023, right=2060)
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')
    # 设置绘图从坐标轴原点开始
    plt.autoscale(axis = 'y')
    y_min, y_max = plt.ylim()
    if language =='cn':
        plt.ylim(0,60000)
    else:
        plt.ylim(0,20000)


    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1.0)  # 通过坐标来微调标签位置
    axs[1].legend( loc=8, bbox_to_anchor=(0.5, -0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().astype(int)
        sum_row = selected_rows.sum().values.round(1)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
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
    for column in plot_data.columns:
        plot_data[column] = pd.to_numeric(plot_data[column], errors='coerce')
    total_values = plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    output_path = f"{output_folder}/全行业-能耗：分部门集中供热需求量{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/全行业-能耗：分部门集中供热需求量{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")
if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国Policy图\\High\\"

    processed_data = read_and_prepare_data(file_path)

    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
