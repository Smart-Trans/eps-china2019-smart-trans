import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style='white', palette='muted')

# Define sectors with different patterns for 'Start Year' and subsequent years
start_year_sectors = {
    "Coal": "SYC Start Year Electricity Generation Capacity.*(hard coal|lignite es).",
    "Natural Gas": "SYC Start Year Electricity Generation Capacity.*(natural gas|natural gas peaker es).",
    "Hydro": "SYC Start Year Electricity Generation Capacity.*hydro",
    "Wind": "SYC Start Year Electricity Generation Capacity.*(onshore wind|offshore wind).",
    "Solar": "SYC Start Year Electricity Generation Capacity.*(solar PV|solar thermal).",
    "Other": "SYC Start Year Electricity Generation Capacity.*(geothermal|biomass es|municipal solid waste).",
    "Pumped Hydro": "BPHC BAU Pumped Hydro Capacity"
}

bau_sectors = {
    "Coal": "Electricity Generation Capacity.*(hard coal|lignite es).",
    "Natural Gas": "Electricity Generation Capacity.*(natural gas|natural gas peaker es)",
    "Hydro": "Electricity Generation Capacity.*hydro",
    "Wind": "Electricity Generation Capacity.*(onshore wind|offshore wind)",
    "Solar": "Electricity Generation Capacity.*(solar PV|solar thermal)",
    "Other": "Electricity Generation Capacity.*(geothermal|biomass es|municipal solid waste)",
    "Pumped Hydro": "BPHC BAU Pumped Hydro Capacity",
    "Battery Storage" : "Grid Battery Storage Capacity in MWh",
    "Demand Response" : "This Year Demand Response Capacity"
}
##如果需要调整数据 则运行此行
def adjust_data(data):
    # selection
    if '2065' in data.columns:
        data_filter=data['2065'].notna()
        colnames=[f"{i}" for i in range(2023,2061)]
        rcolnames=[f"{i}" for i in range(2033,2071)]
        for i,j in zip(colnames,rcolnames):
            data.loc[data_filter,i]=data.loc[data_filter,j]
        drop_colnames=[f"{i}" for i in range(2061,2072)]
        data=data.drop(drop_colnames,axis=1,inplace=True)    
        
def read_and_prepare_data(file_path):
    try:
        data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
        print("data done")
    except pd.errors.ParserError as e:
        print(f"Error reading the CSV file: {e}")
        return None, None
    adjust_data(data)
    data['Time']=data['Time'].astype(str)
    data.fillna(0)
    selected_years = ['2023', '2030', '2040', '2050', '2060']
    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=['Start Year'] + selected_years)

    # Retrieve 'Start Year' data for all sectors
    for sector_key, pattern in start_year_sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]

        processed_data.at['Start Year', sector_key] = sector_data['2023'].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    # Retrieve data for selected years for all sectors
    for sector_key, pattern in bau_sectors.items():
        if sector_key != 'Pumped Hydro' and sector_key !='Battery Storage' and sector_key !='Demand Response' :  # Skip 'Pumped Hydro' here
            sector_data = data[data['Time'].str.contains(pattern, regex=True) &~data['Time'].str.contains("BAU")&~data['Time'].str.contains("Change") &~data['Time'].str.contains("Output") &~data['Time'].str.contains("Surviving") &~data['Time'].str.contains("Shifted") &~data['Time'].str.contains("Year") &~data['Time'].str.contains("Distributed") &~data['Time'].str.contains("before")]
            for year in selected_years:
                processed_data.at[year, sector_key] = sector_data[year].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

           # Special handling for 'Pumped Hydro' for selected years
        if sector_key=='Pumped Hydro':
          pumped_hydro_pattern = bau_sectors['Pumped Hydro']
          pumped_hydro_data = data[data['Time'].str.contains(pumped_hydro_pattern, regex=True)]
          for i, year in enumerate(selected_years):
            processed_data.at[year, 'Pumped Hydro'] = pumped_hydro_data.iloc[:, 11 + i].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
        if sector_key=='Battery Storage':
          battery_storage_pattern=bau_sectors['Battery Storage']
          battery_storage_data=data[data['Time'].str.contains(battery_storage_pattern, regex=True) & ~data['Time'].str.contains("BAU")]
          for year in selected_years:
            processed_data.at[year, sector_key] = battery_storage_data[year].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
            
        if sector_key=='Demand Response':
          demand_response_pattern=bau_sectors['Demand Response']
          demand_response_data=data[data['Time'].str.contains(demand_response_pattern, regex=True) &~data['Time'].str.contains("BAU")]
          for year in selected_years:
            processed_data.at[year, sector_key] = demand_response_data[year].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
    # Convert units to millions
    processed_data *= 0.001
    return processed_data, bau_sectors



def plot_sector_energy_consumption(processed_data, output_folder, language, legend_titles):
    titles = {'en': 'Electricity Generation Capacity', 'cn': '分品种装机容量'}
    ylabels = {'en': 'GW', 'cn': '吉瓦'}

    colors ={
    "Coal": "#969696",
    "Natural Gas": "#c01b00",
    "Hydro": "#620e7a",
    "Wind": "#c2dffd",
    "Solar": "#f1bb18",
    "Other": "#ff00ff",
    "Pumped Hydro": "#004185",
    "Battery Storage" : "#087bf1",
    "Demand Response" : "#00b050"
        }
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=['Start Year'] +[2023, 2030, 2040, 2050, 2060])
    bottom = np.zeros(len(processed_data.index))
    ncols={'en':4,'cn':4}

    x_positions = np.arange(len(processed_data.index))

    # Set initial values for Battery Storage and Demand Response to 0
    processed_data.at['Start Year', 'Battery Storage'] = 0
    processed_data.at['Start Year', 'Demand Response'] = 0

    # Set initial value for Pumped Hydro to the same as BAU 2023 data
    processed_data.at['Start Year', 'Pumped Hydro'] = processed_data.at['2023', 'Pumped Hydro']
    labels = []
    for sector_key, color in zip(bau_sectors.keys(), colors):
        label = legend_titles.get(sector_key, sector_key)
        labels.append(label)
        axs[1].bar(
            x_positions,
            processed_data[sector_key],
            bottom=bottom,
            color=colors[sector_key],
            label=legend_titles.get(sector_key, sector_key),
            edgecolor = 'none'
        )
        tabletoshow[label] = list(processed_data[sector_key])
        
        bottom += processed_data[sector_key]
    plt.xticks(x_positions, ['Start Year'] + [str(year) for year in [2023, 2030, 2040, 2050, 2060]], rotation=0)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)

    # Set font properties based on language
    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
        font_name = 'SimHei'
    else:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        font_name = 'Times New Roman'

    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.04, 1)  # Adjust label position

    axs[1].legend(bbox_to_anchor=(0.5, -0.4), loc=8,edgecolor="white",ncol=ncols[language])
    # 设置坐标轴和刻度颜色为黑色，以及刻度的位置
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    max_value = processed_data.sum(axis=1).max()
    plt.autoscale(axis = 'y')
    if language =='cn':
        plt.ylim(0,12000)
    else:
        plt.ylim(0,12000)
    selected_rows = tabletoshow.loc[['Start Year'] +[2023, 2030, 2040, 2050, 2060]].transpose().round(1)
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
    # 设置坐标轴颜色为黑色


    
    output_path = f"{output_folder}/其他：装机量{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    
    plt.title(titles[language], size=18, fontname=font_name)
    output_path = f"{output_folder}/其他：装机量{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\Low Scenario.csv"
    # output_folder = "D:\\eps\\全国Policy图\\Low\\"
    processed_data, bau_sectors = read_and_prepare_data(file_path)

    if processed_data is not None:
        legend_titles_en = {
            "Coal": "Coal",
            "Natural Gas":"Natural Gas",
            "Hydro":"Hydro",
            "Wind":"Wind",
            "Solar":"Solar",
            "Other":"Other",
            "Pumped Hydro":"Pumped Hydro",
            "Battery Storage":"Battery Storage",
            "Demand Response":"Demand Response"
        }
        legend_titles_cn = {
            "Coal": "燃煤",
            "Natural Gas":"燃气",
            "Hydro":"水电",
            "Wind":"风能",
            "Solar":"太阳能",
            "Other":"生物质及其他",
            "Pumped Hydro":"抽水蓄能",
            "Battery Storage":"电化学储能",
            "Demand Response":"需求响应"
        }
        # Generate charts for both English and Chinese
        plot_sector_energy_consumption(processed_data, output_folder, 'en', legend_titles_en)
        plot_sector_energy_consumption(processed_data, output_folder, 'cn', legend_titles_cn)