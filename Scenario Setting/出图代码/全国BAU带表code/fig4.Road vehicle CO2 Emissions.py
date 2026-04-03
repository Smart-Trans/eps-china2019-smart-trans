import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "LDVs passenger": "BAU Transportation Pollutant Emissions Disaggregated.*LDVs.*CO2.*passenger.",
        "LDVs freight": "BAU Transportation Pollutant Emissions Disaggregated.*LDVs.*CO2.*freight.",
        "HDVs passenger": "BAU Transportation Pollutant Emissions Disaggregated.*HDVs.*CO2.*passenger.",
        "HDVs freight": "BAU Transportation Pollutant Emissions Disaggregated.*HDVs.*CO2.*freight."
    }

    for sector_key, pattern in sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 10 ** -10
    processed_data=processed_data.reindex(columns=['LDVs freight','HDVs passenger','HDVs freight','LDVs passenger'])
    return processed_data


def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Road Vehicle CO2 Emission', 'cn': '道路汽车二氧化碳排放'}
    ylabels = {'en': 'Mt CO2', 'cn': '亿吨CO2'}

    if language == 'en':
        processed_data = processed_data / 100
    else:
        processed_data = processed_data / 10000

    colors = {
        "LDVs passenger": "#969696",
        "LDVs freight": "#f593e0",
        "HDVs passenger": "#f1bb18",
        "HDVs freight": "#000000"
    }

    sector_labels = {
        "LDVs passenger": {"en": "LDVs Passenger", "cn": "轻型载客车"},
        "LDVs freight": {"en": "LDVs Freight", "cn": "轻型载货车"},
        "HDVs passenger": {"en": "HDVs Passenger", "cn": "重型载客车"},
        "HDVs freight": {"en": "HDVs Freight", "cn": "重型载货车"}
    }

    ncols = {"en": 4, "cn": 4}
    fig, axs = plt.subplots(1, 2, figsize=(16, 5))
    tabletoshow = pd.DataFrame(index=range(2023, 2061))

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    else:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    cumulative = np.zeros(len(processed_data.index))
    labels = []

    for sector in processed_data.columns:
        label = sector_labels[sector][language]
        labels.append(label)
        sector_values = processed_data[sector].astype(float)
        axs[1].fill_between(processed_data.index.astype(float), cumulative, cumulative + sector_values,
                            color=colors[sector], label=label)
        tabletoshow[label] = list(sector_values)
        cumulative += sector_values.values

    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])
    axs[1].set_xlim(left=2023, right=2060)

    # 设置坐标轴颜色为黑色
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')

    # 设置绘图从坐标轴原点开始
    plt.autoscale(axis='y')
    if language=='cn':
        plt.ylim(0, 14)
    else:
        plt.ylim(0,1400)
    axs[1].set_title(ylabels[language], loc="left", fontsize=10, x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1.01)
    axs[1].legend(loc=8, bbox_to_anchor=(0.5, -0.4), ncol=ncols[language], edgecolor="white")

    # 创建显示的数据表
    if language == 'cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)

    # 计算总和行，并添加到 selected_rows 中
    sum_row = selected_rows.sum().values.round(2)
    selected_rows.loc['Total'] = sum_row
    labels.append('Total')  # 添加 'sum' 到 labels

    axs[0].axis('off')

    # 更新 labels，确保其与 selected_rows 的行数相等
    labels = [sector_labels[sector][language] for sector in processed_data.columns] + ['sum']

    # 创建表格
    table = axs[0].table(
        cellText=selected_rows.values,
        rowLabels=labels,
        colLabels=selected_rows.columns,
        loc='bottom',
        bbox=[0.2, -0.15, 0.9, 1.1]
    )

    axs[0].text(0.8, 1.35, titles[language], va='top', ha='left', fontsize=20)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    cell_0_0 = table.get_celld()[(0, 0)]
    cell_height = cell_0_0.get_height()
    table.add_cell(0, -1, width=0.05, height=cell_height, text=' ', loc='center')
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    output_path = f"{output_folder}/图4：道路汽车二氧化碳排放{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    plt.title(titles[language], size=18)
    output_path = f"{output_folder}/图4：道路汽车二氧化碳排放{language}.png"
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
