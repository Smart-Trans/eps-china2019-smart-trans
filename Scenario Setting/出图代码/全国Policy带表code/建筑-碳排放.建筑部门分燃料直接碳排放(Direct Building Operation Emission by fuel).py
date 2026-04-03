import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in [2023, 2030, 2040, 2050, 2060]]
    processed_data = pd.DataFrame(index=year_columns)

    sectors = {
        "biomass": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*biomass.*CO2",
        "electricity": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*electricity.*CO2",
        "hard coal": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*hard coal.*CO2",
        "heat": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*heat.*CO2",
        "LPG propane or butane": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*LPG propane or butane.*CO2",
        "natural gas": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*natural gas.*CO2",
        "petroleum": "Direct Buildings Pollutant Emissions.*(urban residential|rural residential|commercial).*petroleum.*CO2"
    }

    for sector_key, pattern in sectors.items():
        # 排除含有 'BAU' 的行
        sector_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains('BAU', regex=True)]

        processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 10 ** -10
    processed_data=processed_data.reindex(columns=['biomass','hard coal','petroleum','natural gas','LPG propane or butane','heat','electricity'])
    return processed_data



def plot_sector_energy_consumption(processed_data, output_folder, language):
    # 在英文图表中进行单位转换
    if language == 'en':
        processed_data *= 10 ** -2

        # 为了在英文图表中显示英文标签，我们需要在此处定义sector_labels
    sector_labels = {
        "biomass": "Biomass" if language == 'en' else "生物质能",
        "electricity": "Electricity" if language == 'en' else "电力",
        "hard coal": "Hard Coal" if language == 'en' else "煤炭",
        "heat": "Heat" if language == 'en' else "热力",
        "LPG propane or butane": "LPG Propane/Butane" if language == 'en' else "液化石油气",
        "natural gas": "Natural Gas" if language == 'en' else "天然气",
        "petroleum": "Petroleum" if language == 'en' else "柴油"
    }
    ncols={'en':4,'cn':4}
    labels = []
    titles = {'en': "Direct Building Operation Emission by Fuel", 'cn': '建筑部门分燃料直接碳排放'}
    ylabels = {'en': 'Mt CO2', 'cn': '万吨CO2'}

    colors = {
        "biomass": "#00b050",
        "electricity": "#f1bb18",
        "hard coal": "#969696",
        "heat": "#c01b00",
        "LPG propane or butane": "#087bf1",
        "natural gas": "#c01b00",
        "petroleum": "#000000"
        }

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=[str(year) for year in [2023, 2030, 2040, 2050, 2060]])
    bottom = np.zeros(len(processed_data.index))
    yrange = 0
    for sector in processed_data.columns:
        plt.bar(processed_data.index, processed_data[sector], bottom=bottom, color=colors[sector], label=sector_labels[sector],edgecolor='none')
        yrange = max(yrange,max(bottom+processed_data[sector]))
        label = sector_labels[sector]
        labels.append(label)
        tabletoshow[label] = list(processed_data[sector])
        bottom += processed_data[sector].values
        

    plt.xticks(rotation=0)
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    plt.legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    # 设置坐标轴和刻度颜色为黑色，以及刻度的位置
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    if language =='cn':
        plt.ylim(0,50000)
    else:
        plt.ylim(0,500)
    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    selected_rows = tabletoshow.transpose().round(1)
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

    output_path = f"{output_folder}/建筑-碳排放：建筑部门分燃料直接碳排放{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language], fontsize=18)
    output_path = f"{output_folder}/建筑-碳排放：建筑部门分燃料直接碳排放{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "D:\\实习\\EPS\\EPS数据\\省级\\内蒙data.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\内蒙Policy\\"
    processed_data = read_and_prepare_data(file_path)


    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
