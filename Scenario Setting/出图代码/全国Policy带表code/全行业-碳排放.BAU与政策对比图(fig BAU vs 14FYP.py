import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
# 设置图表的绘制风格
sns.set(style='white', palette='muted')

colors = ["#c01b00", "#000000", "#969696", "#f1bb18", "#620e7a", "#087bf1", "#004185", "#00b050"]

def search(data,col,Str1,Str2="",Str3=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) &  data[col].str.contains(Str3)]

def Sum(data,col):
    return data[col].apply(pd.to_numeric,errors='coerce').fillna(0).sum()

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in range(2023, 2061)]
    
    
    #筛选policy数据
    # 筛选“policy Process Emissions after CCS”和“CO2”的行
    policy_process_emissions_filter = data['Time'].str.contains("Process Emissions after CCS") & data['Time'].str.contains("CO2") & ~data['Time'].str.contains("BAU")
    policy_process_emissions_data = data[policy_process_emissions_filter]
    # 计算分类型和分组排放的总和(计算每一年的总和 填充缺失值)
    policy_process_emissions_sum = policy_process_emissions_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    # 筛选 policy Total Pollutant Emissions by Sector[industry sector,CO2]
    policy_industry_sector_data = data[data['Time']=="Total Pollutant Emissions by Sector[industry sector,CO2]"]
    policy_industry_sector=Sum(policy_industry_sector_data,year_columns)
    
    # 计算 policy Industrial Process
    policy_industrial_process = policy_process_emissions_sum

    # 计算 policy Industrial Fuel
    policy_industrial_fuel = policy_industry_sector - policy_industrial_process

    # 获取 policy transport
    policy_transport_data=data[data['Time']=="Total Pollutant Emissions by Sector[transportation sector,CO2]"]
    policy_transport=Sum(policy_transport_data,year_columns)
    # 获取 policy electricity
    policy_electricity_data=data[data['Time']=="Total Pollutant Emissions by Sector[electricity sector,CO2]"]
    policy_electricity=Sum(policy_electricity_data,year_columns)
    
    # 获取 policy residential Bldgs
    policy_residential_data=data[data['Time']=="Total Pollutant Emissions by Sector[residential buildings sector,CO2]"]
    policy_residential=Sum(policy_residential_data,year_columns)

     # 获取 policy residential Bldgs
    policy_commercial_data=data[data['Time']=="Total Pollutant Emissions by Sector[commercial buildings sector,CO2]"]
    policy_commercial=Sum(policy_commercial_data,year_columns)
     
     # 获取 policy heating and H2
    policy_heat_data=data[data['Time']=="Total Pollutant Emissions by Sector[district heat and hydrogen sector,CO2]"]
    policy_heat=Sum(policy_heat_data,year_columns)
    
    # 获取 policy LULUCF
    policy_LULUCF_data=data[data['Time']=="Total Pollutant Emissions by Sector[LULUCF sector,CO2]"]
    policy_LULUCF=Sum(policy_LULUCF_data,year_columns)
    
    # 获取 geo_engineering
    policy_geo_data=data[data['Time']=="Total Pollutant Emissions by Sector[geoengineering sector,CO2]"]
    policy_geo=Sum(policy_geo_data,year_columns)
    
    # 获取 District Heating
    policy_district_data=data[data['Time']=="District Heating Pollutant Emissions Summed Across Fuels[CO2]"]
    policy_district=Sum(policy_district_data,year_columns)
    
    # 获取 Hydrogen
    policy_hydrogen_data=data[data['Time'].str.contains("Hydrogen Sector Pollutant Emissions") & data['Time'].str.contains("CO2") & ~data['Time'].str.contains("BAU")]
    policy_hydrogen=Sum(policy_hydrogen_data,year_columns)
    
    # 获取总排放
    policy_totalCO2_data=data[data['Time']=="Total CO2e Emissions"]
    policy_totalCO2=Sum(policy_totalCO2_data,year_columns)
    
    #加总排放
    policy_total=policy_industrial_process+policy_industrial_fuel+policy_electricity+policy_residential+ policy_commercial+policy_heat+policy_LULUCF+policy_geo+ policy_district+ policy_hydrogen+ policy_transport
    
    # 计算 Non CO2
    policy_NonCO2=policy_totalCO2-policy_total
    
    
    # 准备绘图数据

    Policy_plot_data = pd.DataFrame({
        'policy transportation sector': policy_transport.values * 1e-14,
        'policy Industrial Fuel': policy_industrial_fuel.values * 1e-14,
        'policy Industrial Process': policy_industrial_process.values * 1e-14,
        'policy electricity sector': policy_electricity.values * 1e-14,
        'policy heating and H2':policy_heat.values * 1e-14,
        'policy Bldgs': policy_residential.values * 1e-14+policy_commercial.values * 1e-14,
        'policy Non CO2': policy_NonCO2.values * 1e-14
    }, index=year_columns)


    # 筛选“BAU Process Emissions after CCS”和“CO2”的行
    process_emissions_filter = data['Time'].str.contains("BAU Process Emissions after CCS") & data['Time'].str.contains("CO2")
    process_emissions_data = data[process_emissions_filter]
    # 计算分类型和分组排放的总和(计算每一年的总和 填充缺失值)
    process_emissions_sum = process_emissions_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

    # 筛选 BAU Total Pollutant Emissions by Sector[industry sector,CO2]
    industry_sector_filter = data['Time'].str.contains("BAU Total Pollutant Emissions by Sector") & data['Time'].str.contains("industry sector") & data['Time'].str.contains("CO2")
    industry_sector_data = data[industry_sector_filter]

    # 计算 BAU Industrial Process
    bau_industrial_process = process_emissions_sum

    # 计算 BAU Industrial Fuel
    bau_industrial_fuel = industry_sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() - bau_industrial_process

    # 获取 BAU transport
    bau_transport_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","transport","CO2")
    bau_transport=Sum(bau_transport_data,year_columns)
    # 获取 BAU electricity
    bau_electricity_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","electricity","CO2")
    bau_electricity=Sum(bau_electricity_data,year_columns)
    
    # 获取 BAU residential Bldgs
    bau_residential_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","residential","CO2")
    bau_residential=Sum(bau_residential_data,year_columns)

     # 获取 BAU residential Bldgs
    bau_commercial_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","commercial","CO2")
    bau_commercial=Sum(bau_commercial_data,year_columns)
     
     # 获取 BAU heating and H2
    bau_heat_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","heat","CO2")
    bau_heat=Sum(bau_heat_data,year_columns)
    
    # 获取 BAU LULUCF
    bau_LULUCF_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","LULUCF","CO2")
    bau_LULUCF=Sum(bau_LULUCF_data,year_columns)
    
    # 获取 geo_engineering
    bau_geo_data=search(data,'Time',"BAU Total Pollutant Emissions by Sector","geo","CO2")
    bau_geo=Sum(bau_geo_data,year_columns)
    
    # 获取 District Heating
    bau_district_data=search(data,'Time',"BAU District Heating Pollutant Emissions Summed Across Fuels","CO2")
    bau_district=Sum(bau_district_data,year_columns)
    
    # 获取 Hydrogen
    bau_hydrogen_data=search(data,'Time',"BAU Hydrogen Sector Pollutant Emissions","CO2")
    bau_hydrogen=Sum(bau_hydrogen_data,year_columns)
    
    # 获取总排放
    bau_totalCO2_data=data[data['Time']=="BAU Total CO2e Emissions"]
    bau_totalCO2=Sum(bau_totalCO2_data,year_columns)
    
    #加总排放
    bau_total=bau_industrial_process+bau_industrial_fuel+bau_electricity+bau_residential+ bau_commercial+bau_heat+bau_LULUCF+bau_geo+ bau_district+ bau_hydrogen+ bau_transport
    
    # 计算 Non CO2
    bau_NonCO2=bau_totalCO2-bau_total
    
    
    # 准备绘图数据
    BAU_plot_data = pd.DataFrame({
        'BAU transportation sector': bau_transport.values * 1e-14,
        'BAU Industrial Fuel': bau_industrial_fuel.values * 1e-14,
        'BAU Industrial Process': bau_industrial_process.values * 1e-14,
        'BAU electricity sector': bau_electricity.values * 1e-14,
        'BAU heating and H2':bau_heat.values * 1e-14,
        'BAU Bldgs': bau_residential.values * 1e-14+bau_commercial.values * 1e-14,
        'BAU Non CO2': bau_NonCO2.values * 1e-14
    }, index=year_columns)
    return BAU_plot_data, Policy_plot_data, year_columns

def plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    x_years = np.array([int(year) for year in year_columns])

    # Language-specific settings
    titles = 'BAU vs CNS Greenhouse Gas Direct Emission by Sector'
    ylabels = 'Mt CO2e'
    sector_labels = {
            'policy Industrial Process': 'CNS Indst Proc',
            'policy Industrial Fuel': 'CNS Indst Fuel',
            'policy transportation sector': 'CNS Trans',
            'policy electricity sector': 'CNS Elec',
            'policy Bldgs': 'CNS Bldgs',
            'policy heating and H2': 'CNS Heat&H2',
            'policy Non CO2': 'CNS Non CO2',
            'BAU Industrial Process': 'BAU Indst Proc',
            'BAU Industrial Fuel': 'BAU Indst Fuel',
            'BAU transportation sector':'BAU Trans' ,
            'BAU electricity sector':'BAU Elec' ,
            'BAU Bldgs': 'BAU Bldgs',
            'BAU heating and H2':'BAU Heat&H2',
            'BAU Non CO2':'BAU Non CO2' 
    }
    colors={
        'policy Industrial Process': '#969696',
        'policy Industrial Fuel': '#000000',
        'policy transportation sector': '#c01b00',
        'policy electricity sector': '#f1bb18',
        'policy Bldgs': '#087bf1',
        'policy heating and H2': '#620e7a',
        'policy Non CO2': '#00b050',
        'BAU Industrial Process': '#969696',
        'BAU Industrial Fuel': '#000000',
        'BAU transportation sector':'#c01b00' ,
        'BAU electricity sector':'#f1bb18' ,
        'BAU Bldgs': '#087bf1',
        'BAU heating and H2':'#620e7a',
        'BAU Non CO2':'#00b050' 
        }
    ncols = 7

    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.facecolor'] = 'white'

    BAU_stack_baseline = np.zeros(len(x_years))
    Policy_stack_baseline=np.zeros(len(x_years))
    line=[]
    fill=[]
    yrange = 0
    labels = []
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    # 使用自定义的稳重配色方案绘制BAU堆积图
    for (label1, data1), (label2, data2) in zip(BAU_plot_data.items(),Policy_plot_data.items()):
        label = sector_labels[label1]
        labels.append(label)
        fill_obj=axs[1].fill_between(x_years, BAU_stack_baseline, BAU_stack_baseline + data1, label=sector_labels[label1],
                        color=colors[label1],edgecolor=colors[label1],alpha=0.5)
        yrange = max(yrange,max(BAU_stack_baseline + data1))
        tabletoshow[label] = list(data1)
        fill.append(fill_obj)
        BAU_stack_baseline += data1
        line_obj,=axs[1].plot(x_years, Policy_stack_baseline + data2, label=sector_labels[label2],
                  color=colors[label2],linestyle="dashed")
        yrange = max(yrange,max(Policy_stack_baseline + data2))
        line.append(line_obj)
        Policy_stack_baseline += data2
            # 设置坐标轴和刻度颜色为黑色，以及刻度的位置
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black') 
    axs[1].spines['right'].set_color('black') 

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)
    legend1=line[0:4]
    legend2=fill[0:4]
    legend3=line[4:7]
    legend4=fill[4:7]
    first=axs[1].legend(handles=legend1, loc=8, bbox_to_anchor=(0.5, -0.2), ncol=4,edgecolor="white")
    axs[1].add_artist(first)
    second=axs[1].legend(handles=legend2, loc=8, bbox_to_anchor=(0.5, -0.3), ncol=4,edgecolor="white")
    axs[1].add_artist(second)
    third=axs[1].legend(handles=legend3, loc=8, bbox_to_anchor=(0.5, -0.4), ncol=4,edgecolor="white")
    axs[1].add_artist(third)
    axs[1].legend(handles=legend4, loc=8, bbox_to_anchor=(0.5, -0.5), ncol=4,edgecolor="white")
    # 设置坐标轴界限
    axs[1].set_xlim([2023,2060])
    axs[1].set_ylim(0,200)
            # 计算所有数据的最高点，并设置y轴上限为最高值的1.4倍
    axs[1].set_title(ylabels,loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.1, 1.02)  # 通过坐标来微调标签位置
    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)

    # 调整图表布局
    selected_rows = tabletoshow.loc[xticks].transpose().round(2)
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
    axs[0].text(1.1, 1, ylabels, va='top', ha='right', fontsize=10)
    for column in BAU_plot_data.columns:
        BAU_plot_data[column] = pd.to_numeric(BAU_plot_data[column], errors='coerce')
    total_values =BAU_plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    output_path = f"{output_folder}/全行业-碳排放.BAU与政策对比图无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles,size=18)
    output_path = f"{output_folder}/全行业-碳排放.BAU与政策对比图.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国Policy图\\High\\"
    BAU_plot_data,Policy_plot_data, year_columns = read_and_prepare_data(file_path)
   
    # Plot both English and Chinese versions
    plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder)