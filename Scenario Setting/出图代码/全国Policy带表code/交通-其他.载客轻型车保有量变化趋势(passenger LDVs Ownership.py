import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

sns.set(style='white', palette='muted')

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    start_year_sectors = {
        "Gasoline": "SYVbT Start Year Vehicles by Technology.*LDVs.*gasoline vehicle.",
        "Diesel": "SYVbT Start Year Vehicles by Technology.*LDVs.*diesel vehicle.",
        "Natural Gas": "SYVbT Start Year Vehicles by Technology.*LDVs.*natural gas vehicle.",
        "LPG": "SYVbT Start Year Vehicles by Technology.*LDVs.*LPG vehicle.",
        "PHV": "SYVbT Start Year Vehicles by Technology.*LDVs.*plugin hybrid vehicle.",
        "BEV": "SYVbT Start Year Vehicles by Technology.*LDVs.*battery electric vehicle.",
        "Hydrogen": "SYVbT Start Year Vehicles by Technology.*LDVs.*hydrogen vehicle."
    }

    bau_sectors = {
        "Gasoline": "Vehicles.*LDVs.*passenger.*gasoline vehicle.",
        "Diesel": "Vehicles.*LDVs.*passenger.*diesel vehicle.",
        "Natural Gas": "Vehicles.*LDVs.*passenger.*natural gas vehicle.",
        "LPG": "Vehicles.*LDVs.*passenger.*LPG vehicle.",
        "PHV": "Vehicles.*LDVs.*passenger.*plugin hybrid vehicle.",
        "BEV": "Vehicles.*LDVs.*passenger.*battery electric vehicle.",
        "Hydrogen": "Vehicles.*LDVs.*passenger.*hydrogen vehicle."
    }

    processed_data = pd.DataFrame(columns=['Start Year'] + [str(year) for year in range(2023, 2061)])

    # 处理开始年份数据，并确保排除包含“BAU”
    for sector, pattern in start_year_sectors.items():
        start_year_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains("BAU") & ~data['Time'].str.contains("freight")]

        if not start_year_data.empty:
            processed_data.at[sector, 'Start Year'] = start_year_data.iloc[:, 1].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    # 处理BAU年份数据，并确保排除包含“BAU”
    for sector, pattern in bau_sectors.items():
        bau_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains("BAU") & ~data['Time'].str.contains("Output") & ~data['Time'].str.contains("Retir") & ~data['Time'].str.contains("Year") & ~data['Time'].str.contains("Change") & ~data['Time'].str.contains("New") & ~data['Time'].str.contains("Amount") & ~data['Time'].str.contains("freight")]
        if not bau_data.empty:
            for year in range(2023, 2061):
                processed_data.at[sector, str(year)] = bau_data[str(year)].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    processed_data = processed_data.apply(pd.to_numeric, errors='coerce').fillna(0)

    return processed_data


def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {
        'en': "Passenger LDVs Ownership",
        'cn': '载客轻型车保有量变化趋势'
    }
    ylabels = {
        'en': r"$x10^{8}$ Vehicle",
        'cn': r"$x10^{8}$ 台"
    }
    
    ncols={'cn':4,'en':4}

    sector_labels_cn = {
        "Gasoline": "汽油",
        "Diesel": "柴油",
        "Natural Gas": "天然气",
        "LPG": "液化石油气",
        "PHV": "插电混合",
        "BEV": "纯电动",
        "Hydrogen": "燃料电池"
    }
    
    colors={
        "Gasoline": "#969696",
        "Diesel": "#000000",
        "Natural Gas": "#c01b00",
        "LPG": "#087bf1",
        "PHV": "#00b050",
        "BEV": "#f1bb18",
        "Hydrogen": "#620e7a"
        }

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    else:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    data_for_plotting = processed_data.T
    years_to_plot = ['Start Year']+[f"{year}" for year in range(2023,2061)]
    data_for_plotting = data_for_plotting.loc[years_to_plot]
    data_for_plotting= data_for_plotting/1.0E8

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=years_to_plot)
    labels = []
    bottom = np.zeros(len(data_for_plotting))
    for sector in processed_data.index:
        axs[1].fill_between(data_for_plotting.index, bottom, bottom + data_for_plotting[sector], color=colors[sector],label=sector_labels_cn[sector] if language == 'cn' else sector)
        label = sector_labels_cn[sector] if language == 'cn' else sector
        labels.append(label)
        tabletoshow[label] = list(data_for_plotting[sector])
        bottom += data_for_plotting[sector].values

    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')

    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    plt.xticks(['Start Year','2025','2030','2035','2040','2045','2050','2055','2060'])
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    axs[1].legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[['Start Year','2025','2030','2035','2040','2045','2050','2055','2060']].transpose().round(2)
    else:
        selected_rows = tabletoshow.loc[['Start Year','2025','2030','2035','2040','2045','2050','2055','2060']].transpose().round(2)
    sum_row = selected_rows.sum().values.round(2)
    selected_rows.loc['Total'] = sum_row
    labels.append('Total')
    axs[0].axis('off')
    table = axs[0].table(
    cellText=selected_rows.values,
    rowLabels=labels,
    colLabels=['Start\nYear','2025','2030','2035','2040','2045','2050','2055','2060'],
    loc='bottom',
    bbox=[0.2, -0.15, 0.9, 1.1])
    axs[0].text(0.8, 1.35, titles[language], va='top', ha='left', fontsize=20)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    cell_0_0 = table.get_celld()[(0, 0)]
    cell_height = cell_0_0.get_height()
    table.add_cell(0, -1,width = 0.05,height = cell_height, text=' ', loc='center')
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    for column in data_for_plotting.columns:
        data_for_plotting[column] = pd.to_numeric(data_for_plotting[column], errors='coerce')
    total_values = data_for_plotting.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.autoscale(axis = 'y')
    if language =='cn':
        plt.ylim(0,6)
    else:
        plt.ylim(0,6)


    plt.xlim(left=0,right=38)

    output_path = f"{output_folder}/交通-其他：载客轻型车保有量变化趋势{language}无标题.png"
    #plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    
    plt.title(titles[language], size=18)
    output_path = f"{output_folder}/交通-其他：载客轻型车保有量变化趋势{language}.png"
    #plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\eps-china2022-smart-trans-main\\policy\\default.csv"
    # output_folder = "D:\\eps\\全国Policy图\\"
    
    processed_data = read_and_prepare_data(file_path)

    # Generate and save charts for both languages
    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
