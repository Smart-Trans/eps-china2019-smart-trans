import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')

sectors = {
    "heating": "BAU Building Components Energy Use.*heating.",
    "cooling and ventilation": "BAU Building Components Energy Use.*cooling and ventilation.",
    "lighting": "BAU Building Components Energy Use.*lighting.",
    "appliances": "BAU Building Components Energy Use.*appliance.",
    "other component": "BAU Building Components Energy Use.*other component."
}

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in [2023, 2030, 2040, 2050, 2060]]
    processed_data = pd.DataFrame(index=year_columns)

    for sector_key, pattern in sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 3.60087861438191E-12

    return processed_data

def plot_sector_energy_consumption(processed_data, output_folder, language):
    if language == 'en':
        # Adjust for English chart unit conversion
        processed_data *= (1E-12 / 3.60087861438191E-12)
    else:
        processed_data=processed_data

    titles = {'en': "Building Energy Use by Usage", 'cn': '建筑部门分途径能源消费'}
    ylabels = {'en': 'trillion btu', 'cn': '吨标煤'}

    sector_labels_en = {
        "heating": "Heating",
        "cooling and ventilation": "Cooling & Ventilation",
        "lighting": "Lighting",
        "appliances": "Appliances",
        "other component": "Other Component"
    }

    sector_labels_cn = {
        "heating": "供热",
        "cooling and ventilation": "制冷及通风",
        "lighting": "照明",
        "appliances": "生活电器",
        "other component": "其他部件"
    }
    ncols = {'cn':5,'en':5}

    colors = {
        "heating": "#c01b00",
        "cooling and ventilation": "#087bf1",
        "lighting": "#f1bb18",
        "appliances": "#00b050",
        "other component": "#000000"
        }
    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=[2023, 2030, 2040, 2050, 2060])
    bottom = np.zeros_like(processed_data.index.astype(float))

    sector_labels = sector_labels_en if language == 'en' else sector_labels_cn
    labels = []
    for sector_key in sectors.keys():
        axs[1].bar(
            processed_data.index,
            processed_data[sector_key],
            bottom=bottom,
            color=colors[sector_key],
            label=sector_labels[sector_key]
            ,edgecolor='none'# Set bar width here
        )
        labels.append(sector_labels[sector_key])
        tabletoshow[sector_labels[sector_key]] = list(processed_data[sector_key])
        bottom += processed_data[sector_key]
    
    plt.xticks(rotation=0)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].legend(loc=8, bbox_to_anchor=(0.5, -0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.transpose().round(2)
    else:
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
    axs[0].text(0.8, 1.35, titles[language], va='top', ha='left', fontsize=20)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    cell_0_0 = table.get_celld()[(0, 0)]
    cell_height = cell_0_0.get_height()
    table.add_cell(0, -1,width = 0.05,height = cell_height, text=' ', loc='center')
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 160000)
    else:
        plt.ylim(0,50000)
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)


    # axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    # axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    
    output_path = f"{output_folder}/图5：建筑部门分途径能源消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/图5：建筑部门分途径能源消费{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国BAU图\\"
    processed_data = read_and_prepare_data(file_path)
    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
