import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
sns.set(style='white', palette='muted')

# Define sectors with different patterns for 'Start Year' and subsequent years
start_year_sectors = {
    "Gasoline": "SYVbT Start Year Vehicles by Technology.*HDVs.*gasoline vehicle.",
    "Diesel": "SYVbT Start Year Vehicles by Technology.*HDVs.*diesel vehicle.",
    "Natural Gas": "SYVbT Start Year Vehicles by Technology.*HDVs.*natural gas vehicle.",
    "LPG": "SYVbT Start Year Vehicles by Technology.*HDVs.*LPG vehicle.",
    "PHV": "SYVbT Start Year Vehicles by Technology.*HDVs.*plugin hybrid vehicle.",
    "BEV": "SYVbT Start Year Vehicles by Technology.*HDVs.*battery electric vehicle.",
    "Hydrogen": "SYVbT Start Year Vehicles by Technology.*HDVs.*hydrogen vehicle."
}

bau_sectors = {
    "Gasoline": "BAU Vehicles.*HDVs.*gasoline vehicle.",
    "Diesel": "BAU Vehicles.*HDVs.*diesel vehicle.",
    "Natural Gas": "BAU Vehicles.*HDVs.*natural gas vehicle.",
    "LPG": "BAU Vehicles.*HDVs.*LPG vehicle.",
    "PHV": "BAU Vehicles.*HDVs.*plugin hybrid vehicle.",
    "BEV": "BAU Vehicles.*HDVs.*battery electric vehicle.",
    "Hydrogen": "BAU Vehicles.*HDVs.*hydrogen vehicle."
}


def read_and_prepare_data(file_path):
    try:
        data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    except pd.errors.ParserError as e:
        print(f"Error reading the CSV file: {e}")
        return None

    year_columns = [str(year) for year in [2023, 2030, 2040, 2050, 2060]]
    processed_data = pd.DataFrame(index=['Start Year'] + year_columns)

    # Retrieve 'Start Year' data
    for sector_key, pattern in start_year_sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data.at['Start Year', sector_key] = sector_data['2023'].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum()

    # Retrieve data for all other years
    for sector_key, pattern in bau_sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        for year in year_columns:
            processed_data.at[year, sector_key] = sector_data[year].apply(pd.to_numeric, errors='coerce').fillna(
                0).sum()

    # Convert units to millions
    processed_data *= 1e-4
    return processed_data, bau_sectors


def plot_sector_energy_consumption(processed_data, output_folder):
    titles = "Heavy Duty Vehicles"
    ylabels = r"x$10^{4}$"

    colors = ["#969696", "#000000", "#c01b00", "#087bf1", "#00b050", "#f1bb18", "#620e7a", "#ff9da7"]
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    bottom = np.zeros(len(processed_data.index))
    tabletoshow = pd.DataFrame(index=['Start Year',2023, 2030, 2040, 2050, 2060])
    x_positions = np.arange(len(processed_data.index))
    labels = []
    for sector_key, color in zip(bau_sectors.keys(), colors):
        plt.bar(
            x_positions,
            processed_data[sector_key],
            bottom=bottom,
            color=color,
            label=sector_key,
            width=0.8,
            edgecolor = 'none'
        )
        label = sector_key
        labels.append(label)
        tabletoshow[label] = list(processed_data[sector_key])
        bottom += processed_data[sector_key]

    plt.xticks(x_positions, ['Start Year'] + [str(year) for year in [2023, 2030, 2040, 2050, 2060]], rotation=0)
    plt.xlabel('Year')
    axs[1].set_title(ylabels,loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.04, 1)  # 通过坐标来微调标签位置

    plt.legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=4,edgecolor="white")

    plt.autoscale(axis = 'y')
    y_min, y_max = plt.ylim()
    plt.ylim(0 , 4000)
    selected_rows = tabletoshow.transpose().round(2)
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
    axs[0].text(0.8, 1.35, titles, va='top', ha='left', fontsize=20)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    cell_0_0 = table.get_celld()[(0, 0)]
    cell_height = cell_0_0.get_height()
    table.add_cell(0, -1,width = 0.05,height = cell_height, text=' ', loc='center')
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05,wspace = 0.2)

    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    # yticks=range(0,80,10)
    # plt.yticks(yticks) 
    output_path = f"{output_folder}/HDVs无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles,size=18)
    output_path = f"{output_folder}/HDVs.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国BAU图\\"

    # 读取并处理数据
    processed_data, bau_sectors = read_and_prepare_data(file_path)

    # 如果processed_data不是None，则绘制图表
    if processed_data is not None:
        plot_sector_energy_consumption(processed_data, output_folder)
