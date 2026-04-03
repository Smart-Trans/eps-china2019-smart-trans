import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 设置图表的绘制风格
sns.set(style='white', palette='muted')

custom_colors = ["#c01b00", "#8B7355", "#969696", "#f1bb18", "#620e7a", "#087bf1", "#00b050"]


def search(data, col, Str1, Str2="", Str3=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) & data[col].str.contains(Str3)]


def Sum(data, col):
    return data[col].apply(pd.to_numeric, errors='coerce').fillna(0).sum()


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]

    # 筛选“BAU Process Emissions after CCS”和“CO2”的行
    process_emissions_filter = data['Time'].str.contains("BAU Process Emissions after CCS") & data['Time'].str.contains(
        "CO2")
    process_emissions_data = data[process_emissions_filter]
    # 计算分类型和分组排放的总和(计算每一年的总和 填充缺失值)
    process_emissions_sum = process_emissions_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    # 筛选 BAU Total Pollutant Emissions by Sector[industry sector,CO2]
    industry_sector_filter = data['Time'].str.contains("BAU Total Pollutant Emissions by Sector") & data[
        'Time'].str.contains("industry sector") & data['Time'].str.contains("CO2")
    industry_sector_data = data[industry_sector_filter]

    # 计算 BAU Industrial Process
    bau_industrial_process = process_emissions_sum

    # 计算 BAU Industrial Fuel
    bau_industrial_fuel = industry_sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
        0).sum() - bau_industrial_process

    # 获取 BAU transport
    bau_transport_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "transport", "CO2")
    bau_transport = Sum(bau_transport_data, year_columns)
    # 获取 BAU electricity
    bau_electricity_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "electricity", "CO2")
    bau_electricity = Sum(bau_electricity_data, year_columns)

    # 获取 BAU residential bldg
    bau_residential_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "residential", "CO2")
    bau_residential = Sum(bau_residential_data, year_columns)

    # 获取 BAU residential bldg
    bau_commercial_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "commercial", "CO2")
    bau_commercial = Sum(bau_commercial_data, year_columns)
    bau_bldg = bau_residential + bau_commercial

    # 获取 BAU heating and H2
    bau_heat_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "heat", "CO2")
    bau_heat = Sum(bau_heat_data, year_columns)

    # 获取 BAU LULUCF
    bau_LULUCF_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "LULUCF", "CO2")
    bau_LULUCF = Sum(bau_LULUCF_data, year_columns)

    # 获取 geo_engineering
    bau_geo_data = search(data, 'Time', "BAU Total Pollutant Emissions by Sector", "geo", "CO2")
    bau_geo = Sum(bau_geo_data, year_columns)

    # 获取 District Heating
    bau_district_data = search(data, 'Time', "BAU District Heating Pollutant Emissions Summed Across Fuels", "CO2")
    bau_district = Sum(bau_district_data, year_columns)

    # 获取 Hydrogen
    bau_hydrogen_data = search(data, 'Time', "BAU Hydrogen Sector Pollutant Emissions", "CO2")
    bau_hydrogen = Sum(bau_hydrogen_data, year_columns)

    # 获取总排放
    bau_totalCO2_data = data[data['Time'] == "BAU Total CO2e Emissions"]
    bau_totalCO2 = Sum(bau_totalCO2_data, year_columns)

    # 加总排放
    bau_total = bau_industrial_process + bau_industrial_fuel + bau_electricity + bau_residential + bau_commercial + bau_heat + bau_LULUCF + bau_geo + bau_district + bau_hydrogen + bau_transport

    # 计算 Non CO2
    bau_NonCO2 = bau_totalCO2 - bau_total

    # 准备绘图数据
    plot_data = pd.DataFrame({
        'transportation sector': bau_transport.values * 1e-14,
        'BAU Industrial Fuel': bau_industrial_fuel.values * 1e-14,
        'BAU Industrial Process': bau_industrial_process.values * 1e-14,
        'electricity sector': bau_electricity.values * 1e-14,
        'heating and H2': bau_heat.values * 1e-14,
        'buildings sector': bau_bldg.values * 1e-14,
        'Non CO2': bau_NonCO2.values * 1e-14,
        'land use': bau_LULUCF.values * 1e-14
    }, index=year_columns)

    # 准备绘图数据

    return plot_data, year_columns


def plot_stacked_area_chart(plot_data, year_columns, output_folder, language='en'):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    x_years = np.array([int(year) for year in year_columns])
    stack_baseline = np.zeros(len(x_years))
    labels = []
    tabletoshow = pd.DataFrame(index=range(2023, 2061))

    # Language-specific settings
    titles = {'en': 'Net Greenhouse Gas Emission by Sector', 'cn': '温室气体直接净排放'}
    ylabels = {'en': 'Mt CO2e', 'cn': '排放量 (亿吨)'}
    sector_labels = {
        'en': {
            'BAU Industrial Process': 'Industrial Process',
            'BAU Industrial Fuel': 'Industrial Fuel',
            'transportation sector': 'Transportation',
            'electricity sector': 'Electricity',
            'buildings sector': 'Buildings',
            'heating and H2': 'Heating and H2',
            'Non CO2': 'Non CO2',
            'land use': 'LULUCF'
        },
        'cn': {
            'BAU Industrial Process': "工业过程",
            'BAU Industrial Fuel': "工业燃料",
            'transportation sector': "交通部门",
            'electricity sector': "电力部门",
            'buildings sector': "建筑部门",
            'heating and H2': "供热和氢能",
            'Non CO2': "非二温室气体",
            'land use': "土地利用"
        }
    }
    ncols = {'en': 4, 'cn': 4}

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.unicode_minus'] = False
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.rcParams['axes.facecolor'] = 'white'
        plot_data = plot_data * 100
    color_index = 0
    yrange = 0
    land_use_values = plot_data['land use']
    stack_baseline = land_use_values.copy()

    for label, data in plot_data.items():
        label1 = sector_labels[language][label]
        labels.append(label1)
        if label == 'land use':
            continue
        else:
            axs[1].fill_between(x_years, stack_baseline, stack_baseline + data,
                                label=label1, color=custom_colors[color_index % len(custom_colors)], edgecolor='none')
            stack_baseline += data
        tabletoshow[label1] = list(data)
        color_index += 1

    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    # Total_values=plot_data.sum(axis=1).values.round(2)
    # axs[1].plot(x_years,Total_values, color='black', linewidth=2, label='Total', linestyle='--')

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)

    # 设置坐标轴界限
    axs[1].set_xlim([min(x_years), max(x_years)])
    if language == 'en':
        plt.yticks(ticks=[-2500, 0, 2500, 5000, 7500, 10000, 12500, 15000, 17500],
                   labels=['-2500', '0', '2500', '5000', '7500', '10000', '12500', '15000', '17500'])
    else:
        plt.yticks(ticks=[-25, 0, 25, 50, 75, 100, 125, 150, 175],
                   labels=['-25', '0', '25', '50', '75', '100', '125', '150', '175'])
    axs[1].set_title(ylabels[language], loc="left", fontsize=10, x=-0.05)
    axs[1].yaxis.set_label_coords(0.1, 1.02)
    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060]
    plt.xticks(xticks)

    plt.legend(loc=8, ncol=ncols[language], bbox_to_anchor=(0.5, -0.4), edgecolor="white")

    # 调整图表布局
    if language == 'cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)

    land_use_values = plot_data['land use'].values
    years = list(range(2023, 2061))
    land_use_df = pd.DataFrame(land_use_values, columns=['Land Use'])
    land_use_df['Year'] = years
    land_use_df.set_index('Year', inplace=True)
    land_use = land_use_df.loc[xticks].values
    land_use = land_use.flatten()
    if language == 'en':
        selected_rows.loc['LULUCF'] = land_use
    else:
        selected_rows.loc['土地利用'] = land_use
    sum_row = selected_rows.sum().values.round(2)
    selected_rows.loc['Total'] = sum_row

    labels = list(selected_rows.index)
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
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-')
    for column in plot_data.columns:
        plot_data[column] = pd.to_numeric(plot_data[column], errors='coerce')
    total_values = plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    output_path = f"{output_folder}/全行业-碳排放：BAU温室气体净排放{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")

    plt.title(titles[language], size=18)
    output_path = f"{output_folder}/全行业-碳排放：BAU温室气体净排放{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "C:\\Users\\Mywljy\\Desktop\\全国data10.31.csv"
    # output_folder = "C:\\Users\\Mywljy\\Desktop\\"
    plot_data, year_columns = read_and_prepare_data(file_path)

    # Plot both English and Chinese versions
    plot_stacked_area_chart(plot_data, year_columns, output_folder, language='en')
    plot_stacked_area_chart(plot_data, year_columns, output_folder, language='cn')