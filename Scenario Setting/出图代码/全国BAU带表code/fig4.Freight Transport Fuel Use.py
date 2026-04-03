import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
# 设置绘图风格
sns.set(style='white', palette='muted')

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "electricity": "BAU Transportation Sector Fuel Used.*freight.*electricity",
        "heavy or residual fuel oil": "BAU Transportation Sector Fuel Used.*freight.*heavy or residual fuel oil",
        "hydrogen": "BAU Transportation Sector Fuel Used.*freight.*hydrogen*",
        "jet fuel": "BAU Transportation Sector Fuel Used.*freight.*jet fuel",
        "LPG propane or butane": "BAU Transportation Sector Fuel Used.*freight.*LPG propane or butane",
        "natural gas": "BAU Transportation Sector Fuel Used.*freight.*natural gas",
        "petroleum diesel": "BAU Transportation Sector Fuel Used.*freight.*petroleum diesel",
        "petroleum gasoline": "BAU Transportation Sector Fuel Used.*freight.*petroleum gasoline"
    }

    for sector_key, pattern in sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 3.60087861438191E-12
    processed_data=processed_data.reindex(columns=['petroleum gasoline','petroleum diesel','jet fuel','natural gas','electricity','hydrogen','heavy or residual fuel oil','LPG propane or butane'])
    return processed_data

def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Freight Transport Fuel Use', 'cn': '载货运输燃料消费'}
    ylabels = {'en': 'trillion btu', 'cn': '吨标煤'}
    if language=='en':
        processed_data=processed_data/3.60087861438191
    else:
        processed_data=processed_data
    # 中英文对照字典
    sector_labels = {
        "electricity": {"en": "Electricity", "cn": "电力"},
        "heavy or residual fuel oil": {"en": "Heavy or Residual Fuel Oil", "cn": "燃料油、残渣油"},
        "hydrogen": {"en": "Hydrogen", "cn": "氢能"},
        "jet fuel": {"en": "Jet Fuel", "cn": "航空煤油"},
        "LPG propane or butane": {"en": "LPG Propane or Butane", "cn": "液化石油气"},
        "natural gas": {"en": "Natural Gas", "cn": "天然气"},
        "petroleum diesel": {"en": "Petroleum Diesel", "cn": "柴油"},
        "petroleum gasoline": {"en": "Petroleum Gasoline", "cn": "汽油"}
    }

    colors = {
        "electricity": "#f1bb18",
        "heavy or residual fuel oil": "#ad6600",
        "hydrogen": "#620e7a",
        "jet fuel": "#c2dffd",
        "LPG propane or butane": "#087bf1",
        "natural gas": "#c01b00",
        "petroleum diesel": "#000000",
        "petroleum gasoline": "#969696"
    }
    
    ncols={
        "cn": 4,
        "en": 4
        
        }

    fig, axs = plt.subplots(1, 2, figsize=(16, 5))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    

    plt.rcParams['font.sans-serif'] = ['SimHei'] if language == 'cn' else ['Times New Roman']

    # 绘制堆积面积图，应用颜色方案
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

    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050,2055, 2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])
    axs[1].set_xlim(left=2023, right=2060)  # 明确设置x轴范围以确保从原点开始
    plt.autoscale(axis = 'y')
    if language=='cn':
        plt.ylim(0, 100000)
    else:
        plt.ylim(0,30000)


    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    
    axs[1].legend(loc=8, bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    labels = [sector_labels[sector][language] for sector in processed_data.columns]
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().astype(int)
        sum_row = selected_rows.sum().values.astype(int)
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
    axs[1].yaxis.set_label_coords(0.035, 1.01)  # 通过坐标来微调标签位置
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    output_path = f"{output_folder}/图4：载货运输燃料消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/图4：载货运输燃料消费{language}.png"
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
