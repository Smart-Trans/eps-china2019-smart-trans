import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

sns.set(style='white', palette='muted')


def search(data, col, Str1, Str2="", Str3="", Str4=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) & data[col].str.contains(Str3) & data[
        col].str.contains(Str4) & ~data[col].str.contains("BAU") & ~data[col].str.contains("Year")]


def Sum(data, col):
    return data[col].apply(pd.to_numeric, errors='coerce').fillna(0).sum()


def read_and_prepare_data(file_path):
    try:
        data = pd.read_csv(file_path, on_bad_lines='warn', low_memory=False)
        data['Time'] = data['Time'].astype(str)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

    year_columns = [str(year) for year in range(2023, 2061)]
    sectors = {
        "transportation sector": "Transportation Sector",
        "electricity sector": "Electricity Sector",
        "residential buildings sector": "Residential Buildings Sector",
        "commercial buildings sector": "Commercial Buildings Sector",
        "industry sector": "Industry Sector",
        "district heat and hydrogen sector": "District Heat and Hydrogen Sector"
    }
    renewable_sources = ['wind', 'solar', 'hydro', 'biomass', 'nuclear', 'geothermal']
    processed_data = pd.DataFrame(index=year_columns)

    # 计算各部门能耗
    for sector, label in sectors.items():
        sector_pattern = f"Total Primary Fuel Use by Sector.*{sector}"
        sector_data = data[data['Time'].str.contains(sector_pattern, regex=True) & ~data['Time'].str.contains("BAU")]
        sector_sum = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 1.0E-12
        processed_data[label] = sector_sum

    # 调整电力部门数据，加入可再生能源
    extra_energy = pd.Series(0, index=year_columns)
    for source in renewable_sources:
        energy_use = data[
            data['Time'].str.contains(f"Total Primary Energy Use.*{source}", regex=True) & ~data['Time'].str.contains(
                "BAU") & ~data['Time'].str.contains("Output")]
        non_energy_use = data[
            data['Time'].str.contains(f"Industrial Fuel Use for Non Energy Purposes.*{source}", regex=True) & ~data[
                'Time'].str.contains("BAU")]
        extra_energy += (energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() -
                         non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()) * 1.0E-12
    processed_data["Electricity Sector"] += extra_energy

    # 计算非燃料使用，排除特定行
    exclusions = [
        "coal mining 05,hard coal if",
        "refined petroleum and coke 19,hard coal if",
        "refined petroleum and coke 19,crude oil if"
    ]
    non_energy_use = data[~data['Time'].str.contains('|'.join(exclusions), regex=True) & data['Time'].str.contains(
        "Industrial Fuel Use for Non Energy Purposes", regex=True) & ~data['Time'].str.contains("BAU")]
    non_energy_total = non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
        0).sum() * 1.0E-12
    processed_data["Nonenergy Use"] = non_energy_total

    # 从工业部门减去非燃料使用的总和
    non_energy_use_for_industry = data[
        data['Time'].str.contains("Industrial Fuel Use for Non Energy Purposes", regex=True) & ~data[
            'Time'].str.contains("BAU")]
    non_energy_total_for_industry = non_energy_use_for_industry[year_columns].apply(pd.to_numeric,
                                                                                    errors='coerce').fillna(
        0).sum() * 1.0E-12
    processed_data["Industry Sector"] -= non_energy_total_for_industry
    processed_data = processed_data.reindex(
        columns=['Transportation Sector', 'Industry Sector', 'Nonenergy Use', 'Electricity Sector',
                 'Residential Buildings Sector', 'Commercial Buildings Sector', 'District Heat and Hydrogen Sector'])
    return processed_data


def plot_energy_consumption(processed_data, output_folder, language):
    labels = []
    if language == 'cn':
        processed_data = processed_data / 10000
    titles = {'en': 'Primary Energy Use by Sector', 'cn': '分部门一次能源消费量'}
    ylabels = {'en': 'trillion btu', 'cn': '亿吨标煤'}
    ncols = {'en': 3, 'cn': 4}
    if language == 'cn':
        processed_data.columns = ['交通部门', '工业燃料', '非燃料使用', '电力部门', '居民建筑', '公共建筑',
                                  '供热与氢能']
        processed_data = processed_data * 3.60087861438191

    fig, axs = plt.subplots(1, 2, figsize=(18, 5))
    tabletoshow = pd.DataFrame(index=range(2023, 2061))

    plt.rcParams['font.sans-serif'] = ['SimHei'] if language == 'cn' else ['Times New Roman']
    # 深沉饱和度高的科研配色方案
    colors = ["#c01b00", "#7C7C7C", "#A5A5A5", "#f1bb18", "#087bf1", "#004185", "#620e7a"]
    # 绘制堆积面积图，应用自定义的颜色方案
    processed_data = processed_data.astype(float)
    bottom_array = np.zeros(len(processed_data))
    for column, color in zip(processed_data.columns, colors):
        axs[1].fill_between(processed_data.index.astype(int), bottom_array, bottom_array + processed_data[column],
                            label=column, color=color, edgecolor='none')

        tabletoshow[column] = list(processed_data[column])
        bottom_array += processed_data[column]

    # 设置坐标轴的颜色和可见性
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    axs[1].set_xlim(left=2023, right=2060)  # 明确设置x轴范围以确保从原点开始

    # 设置y轴上限为原数据绘图最高值的1.2倍
    plt.autoscale(axis='y')
    if language =='cn':
        plt.ylim(0,100)
    else:
        plt.ylim(0,300000)

    # 设置x轴显示的年份
    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])

    axs[1].set_title(ylabels[language], loc="left", fontsize=10, x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1)

    axs[1].legend(loc=8, ncol=ncols[language], bbox_to_anchor=(0.5, -0.4), edgecolor="white")
    if language == 'cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(1)
    sum_row = selected_rows.sum().values.round(2)
    selected_rows.loc['Total'] = sum_row
    labels.append('Total')
    labels = [processed_data.columns[i] for i in range(len(processed_data.columns))] + ['sum']
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
    table.add_cell(0, -1, width=0.05, height=cell_height, text=' ', loc='center')
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    for column in processed_data.columns:
        processed_data[column] = pd.to_numeric(processed_data[column], errors='coerce')
    total_values = processed_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    output_path = f"{output_folder}/全行业-能耗：分部门一次能源消费量{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"图表已保存至: {output_path}")

    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/全行业-能耗：分部门一次能源消费量{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"图表已保存至: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "C:\\Users\\Mywljy\\Desktop\\data.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\"
    processed_data = read_and_prepare_data(file_path)
    if processed_data is not None:
        plot_energy_consumption(processed_data, output_folder, 'en')
        plot_energy_consumption(processed_data, output_folder, 'cn')
