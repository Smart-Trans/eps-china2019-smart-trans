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
        "Biofuel Diesel": "BAU Transportation Sector Fuel Used.*LDVs.*passenger.*biofuel diesel",
        "Biofuel Gasoline": "BAU Transportation Sector Fuel Used.*LDVs.*passenger.*biofuel gasoline",
        "Electricity": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*electricity",
        #"Heavy or Residual Fuel Oil": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*heavy or residual fuel oil",
        "Hydrogen": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*hydrogen*",
        "Jet Fuel": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*jet fuel",
        #"LPG Propane or Butane": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*LPG propane or butane",
        "Natural Gas": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*natural gas",
        "Petroleum Diesel": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*petroleum diesel",
        "Petroleum Gasoline": "BAU Transportation Sector Fuel Used.*LDVs.*freight.*petroleum gasoline"
    }

    for sector_key, pattern in sectors.items():
        print(f"Processing sector: {sector_key}")
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        print(f"Rows matching pattern '{pattern}':")
        print(sector_data['Time'])  # 输出匹配到的行的名称
        print(f"Data for {sector_key}:")
        print(sector_data.head())  # 打印部分数据以便检查
        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 3.60087861438191E-12
    processed_data=processed_data.reindex(columns=['Petroleum Gasoline','Petroleum Diesel','Jet Fuel','Natural Gas','Electricity','Hydrogen','Biofuel Diesel','Biofuel Gasoline'])
    return processed_data

def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Freight LDVs Transport Fuel', 'cn': '载货轻型车运输燃料消费'}
    ylabels = {'en': 'trillion btu', 'cn': '万吨标煤'}

    colors = {
        "Biofuel Diesel": "#00b050",
        "Biofuel Gasoline": "#04ffaf",
        "Electricity": "#f1bb18",
        "Heavy or Residual Fuel Oil": "#ad6600",
        "Hydrogen": "#620e7a",
        "Jet Fuel": "#c2dffd",
        "LPG Propane or Butane": "#087bf1",
        "Natural Gas": "#c01b00",
        "Petroleum Diesel": "#000000",
        "Petroleum Gasoline": "#969696"
    }

    # 中英文对照字典
    sector_labels_cn = {
        "Biofuel Diesel": "生物柴油",
        "Biofuel Gasoline": "生物汽油",
        "Electricity": "电力",
        "Heavy or Residual Fuel Oil": "燃料油、残渣油",
        "Hydrogen": "氢能",
        "Jet Fuel": "航空煤油",
        "LPG Propane or Butane": "液化石油气",
        "Natural Gas": "天然气",
        "Petroleum Diesel":"柴油",
        "Petroleum Gasoline": "汽油"
    }
    
    ncols={
        "en": 4,
        "cn": 4
        }
    fig, axs = plt.subplots(1, 2, figsize=(16, 10))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    if language == 'en':
        # Apply unit conversion for English chart
        processed_data = (processed_data / 3.60087861438191E-12) * 1E-12
        cumulative = np.zeros(len(processed_data.index))
        # 计算每个部门在所有年份的总和，并根据这个总和排序
        sector_sums = processed_data.sum()
        sorted_sectors = sector_sums.sort_values(ascending=False).index
        labels = []
        for sector in sorted_sectors:
            label = sector_labels_cn[sector] if language == 'cn' else sector
            labels.append(label)
            sector_values = processed_data.loc[:, sector].astype(float)
            axs[1].fill_between(processed_data.index, cumulative, cumulative + sector_values, color=colors[sector],
                             label=label)
            tabletoshow[label] = list(sector_values.values)
            cumulative += sector_values.values


    
    
    cumulative = np.zeros(len(processed_data.index))
    labels = []
    for sector in processed_data.columns:
        if sector not in ['Agricultural','Construction']:
            label = sector_labels_cn[sector] if language == 'cn' else sector
            labels.append(label)
            sector_values = processed_data[sector].astype(float)
            axs[1].fill_between(processed_data.index.astype(float), cumulative, cumulative + sector_values,
                             color=colors[sector], label=label)
            tabletoshow[label] = list(sector_values.values)
            cumulative += sector_values.values

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 确保中文字符显示正确
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
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
        plt.ylim(0, 16000)
    else:
        plt.ylim(0,5000)


    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    plt.xlim(left=2023, right=2060)
    # 设置y轴上限为原数据绘图最高值的1.2倍
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.035, 1.01)  # 通过坐标来微调标签位置
    axs[1].legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")

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
    output_path = f"{output_folder}/图4：载货轻型车运输燃料消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/图4：载货轻型车运输燃料消费{language}.png"
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
