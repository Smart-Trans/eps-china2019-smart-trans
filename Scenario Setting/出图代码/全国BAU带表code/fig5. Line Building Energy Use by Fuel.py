import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023,2061)]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "biomass": "BAU Building Components Energy Use.*biomass.",
        "electricity": "BAU Building Components Energy Use.*electricity.",
        "hard coal": "BAU Building Components Energy Use.*hard coal.",
        "heat": "BAU Building Components Energy Use.*heat bf.",
        "LPG propane or butane": "BAU Building Components Energy Use.*LPG propane or butane.",
        "natural gas": "BAU Building Components Energy Use.*natural gas.",
        "petroleum diesel": "BAU Building Components Energy Use.*petroleum diesel."

    }
    #"biomass": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*biomass.",
    #"electricity": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*electricity.",
    #"hard coal": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*hard coal.",
    #"heat": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*heat.",
    #"LPG propane or butane": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*LPG propane or butane.",
    #"natural gas": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*natural gas.",
    #"petroleum": "BAU Building Components Energy Use.*(urban residential|rural residential|commercial).*petroleum."
    for sector_key, pattern in sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 3.60087861438191E-12
    processed_data=processed_data.reindex(columns=['biomass','hard coal','petroleum diesel','natural gas','LPG propane or butane','heat','electricity'])
    return processed_data


def plot_sector_energy_consumption(processed_data, output_folder, language):
    # 在英文图表中进行单位转换
    if language == 'en':
        processed_data *= (1E-12 / 3.60087861438191E-12)
    else:
        processed_data=processed_data

        # 为了在英文图表中显示英文标签，我们需要在此处定义sector_labels
    sector_labels = {
        "biomass": "Biomass" if language == 'en' else "生物质能",
        "electricity": "Electricity" if language == 'en' else "电力",
        "hard coal": "Hard Coal" if language == 'en' else "煤炭",
        "heat": "Heat" if language == 'en' else "热力",
        "LPG propane or butane": "LPG Propane/Butane" if language == 'en' else "液化石油气",
        "natural gas": "Natural Gas" if language == 'en' else "天然气",
        "petroleum diesel": "Petroleum" if language == 'en' else "石油"
    }

    titles = {'en': "Building Energy Use by Fuel", 'cn': '建筑部门分品种能源消费'}
    ylabels = {'en': 'trillion btu', 'cn': '万吨标煤'}
    ncols = {'en': 4,'cn': 4}

    colors = {
        "biomass": '#00b050',
        "electricity": '#f1bb18',
        "hard coal": '#969696',
        "heat": '#620e7a',
        "LPG propane or butane": '#087bf1',
        "natural gas": '#c01b00',
        "petroleum diesel": '#000000'
        }

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    bottom = np.zeros(len(processed_data.index))

    for sector in sector_labels.keys():
        axs[1].fill_between(processed_data.index.astype(int), bottom, processed_data[sector]+bottom, color=colors[sector], label=sector_labels[sector])

        tabletoshow[sector] = list(processed_data[sector])
        bottom += processed_data[sector].values

    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    labels = [sector_labels[sector] for sector in processed_data.columns] 
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1)  # 通过坐标来微调标签位置
    axs[1].legend(loc=8, bbox_to_anchor=(0.5, -0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().astype(int)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
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
    # 设置坐标轴和刻度颜色为黑色，以及刻度的位置
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')

    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 160000)
    else:
        plt.ylim(0,50000)


    axs[1].set_xlim(left=2023,right=2060)

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)

    output_path = f"{output_folder}/图5：折线图建筑部门分品种能源消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/图5：折线图建筑部门分品种能源消费{language}.png"
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
