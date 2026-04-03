
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
# 设置图表的绘制风格
sns.set(style='white', palette='muted')

colors = ["#c01b00", "#ad6600", "#969696", "#f1bb18", "#087bf1", "#004185", "#b07aa1", "#ff9da7"]

def search(data,col,Str1,Str2="",Str3=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) &  data[col].str.contains(Str3) & ~data[col].str.contains("BAU")]

def Sum(data,col):
    return data[col].apply(pd.to_numeric,errors='coerce').fillna(0).sum()

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in range(2023, 2061)]
    
    #########用电量数据
    transportation_electricity_data=search(data,'Time',"Transportation Sector Electricity Demand")
    transportation_electricity=Sum(transportation_electricity_data, year_columns)
    industrial_electricity_data=search(data,'Time',"Industrial Sector Electricity Demand")
    industrial_electricity=Sum(industrial_electricity_data,year_columns)
    hydro_electricity_data=search(data,'Time',"Hydrogen Sector Electricity Demand")
    hydro_electricity=Sum(hydro_electricity_data,year_columns)
    heat_electricity_data=search(data,'Time',"District Heat Electricity Demand")
    heat_electricity=Sum(heat_electricity_data,year_columns)
    build_electricity_data=search(data,'Time',"Buildings Sector Net Electricity Demand")
    build_electricity=Sum(build_electricity_data,year_columns)
    build_electricity.index=year_columns
    import_electricity_data=search(data,'Time',"Net Imports of Electricity")
    import_electricity=pd.Series([max(item,0) for item in -Sum(import_electricity_data,year_columns)])
    import_electricity.index=year_columns
    total_electricity=transportation_electricity+industrial_electricity+hydro_electricity+heat_electricity+build_electricity+import_electricity
    ###########交通数据获取
    #Direct
    Direct_transportation_data=data[data['Time']=="Total Pollutant Emissions by Sector[transportation sector,CO2]"]
    Direct_transportation=Sum(Direct_transportation_data,year_columns)
    
    #From Electricity
    Direct_electricity_data=data[data['Time']=="Total Pollutant Emissions by Sector[electricity sector,CO2]"]
    transportation_electricity_data=search(data,'Time',"Transportation Sector Electricity Demand")
    #计算交通用电量占比
    transportation_percent=Sum(transportation_electricity_data,year_columns) / total_electricity
    Electricity_transportation=Sum(Direct_electricity_data,year_columns) * transportation_percent
    
    #From Hydrogen
    Hydrogen_transportation=pd.Series(0,index=year_columns)
    
    #From District Heating
    Heating_transportation=pd.Series(0,index=year_columns)
    
    #indirect
    Indirect_transportation= Direct_transportation+Electricity_transportation+Hydrogen_transportation+Heating_transportation
    transport_DF=pd.DataFrame({
        'transportation':  Indirect_transportation * 1e-14
        })
    
    ###########居民建筑数据获取
    #Direct
    Direct_residential_data=data[data['Time']=="Total Pollutant Emissions by Sector[residential buildings sector,CO2]"]
    Direct_residential=Sum(Direct_residential_data,year_columns)
    
    #From Electricity
    residential_electricity_data=search(data,'Time',"Buildings Sector Net Electricity Demand","residential")
    #计算居民建筑用电量占比
    residential_percent=Sum(residential_electricity_data,year_columns) / total_electricity
    Electricity_residential=Sum(Direct_electricity_data,year_columns) * residential_percent
    
    #From Hydrogen
    Hydrogen_residential=pd.Series(0,index=year_columns)
    
    #From District Heating
    district_heating_data=search(data,'Time',"District Heating Pollutant Emissions Summed Across Fuels","CO2")
    district_heating=Sum(district_heating_data,year_columns)
    #供热量计算
    #industry
    industry_heating_data=search(data,'Time',"Industrial Fuel Use for Energy Purposes\[heat")
    industry_heating=Sum(industry_heating_data,year_columns)*3.60087861438191E-12
    #residential
    residential_heating_data=search(data,'Time',"Building Components Energy Use","residential","heat")
    residential_heating=Sum(residential_heating_data,year_columns)*3.60087861438191E-12
    #commercial
    commercial_heating_data=search(data,'Time',"Building Components Energy Use","commercial","heat")
    commercial_heating=Sum(commercial_heating_data,year_columns)*3.60087861438191E-12
    #total
    total_heating= industry_heating+ residential_heating+ commercial_heating
    residential_heating_percent=commercial_heating/(total_heating)
    Heating_residential= residential_heating_percent* district_heating
    
    #indirect
    Indirect_residential= Direct_residential+Electricity_residential+Hydrogen_residential+Heating_residential
    residential_DF=pd.DataFrame({
        'residential':  Indirect_residential * 1e-14
        })
    
    ###########公共建筑数据获取
    #Direct
    Direct_commercial_data=data[data['Time']=="Total Pollutant Emissions by Sector[commercial buildings sector,CO2]"]
    Direct_commercial=Sum(Direct_commercial_data,year_columns)
    
    #From Electricity
    commercial_electricity_data=search(data,'Time',"Buildings Sector Net Electricity Demand","commercial")
    #计算居民建筑用电量占比
    commercial_percent=Sum(commercial_electricity_data,year_columns) / total_electricity
    Electricity_commercial=Sum(Direct_electricity_data,year_columns) * commercial_percent
    
    #From Hydrogen
    Hydrogen_commercial=pd.Series(0,index=year_columns)
    
    #From District Heating
    commercial_heating_percent=commercial_heating/(total_heating)
    Heating_commercial= commercial_heating_percent* district_heating
    
    #indirect
    Indirect_commercial= Direct_commercial+Electricity_commercial+Hydrogen_commercial+Heating_commercial
    commercial_DF=pd.DataFrame({
        'commercial':  Indirect_commercial * 1e-14
        })
    
    ###########工业过程数据获取
    #Indirect
    indirect_process_data=search(data,'Time',"Process Emissions after CCS","CO2")
    Indirect_process=Sum(indirect_process_data,year_columns)
    process_DF=pd.DataFrame({
        'process':   Indirect_process * 1e-14
        })
    
    ###########工业燃料数据获取
    #Direct
    industry_data=data[data['Time']=="Total Pollutant Emissions by Sector[industry sector,CO2]"]
    industry=Sum(industry_data,year_columns)
    Direct_fuel=industry-Indirect_process
    
    #From Electricity
    fuel_electricity_data=search(data,'Time',"Industrial Sector Electricity Demand")
    #计算工业燃料用电量占比
    fuel_percent=Sum(fuel_electricity_data,year_columns) / total_electricity
    Electricity_fuel=Sum(Direct_electricity_data,year_columns) * fuel_percent
    
    #From Hydrogen
    Hydrogen_fuel=pd.Series(0,index=year_columns)
    
    #From District Heating
    industry_heating_percent=industry_heating/(total_heating)
    Heating_fuel= industry_heating_percent* district_heating
    
    #indirect
    Indirect_fuel= Direct_fuel+Electricity_fuel+Hydrogen_fuel+Heating_fuel
    fuel_DF=pd.DataFrame({
        'fuel':  Indirect_fuel * 1e-14
        })
    
    ###########外送电力数据获取
    #发电量
    Electricity_import_data=data[data['Time']=="Net Imports of Electricity"]
    Electricity_export=Sum(Electricity_import_data,year_columns)*-1
    Electricity_export= Electricity_export.clip(lower=0)
    Electricity_export_percent=Electricity_export/ total_electricity
    Indirect_export=Sum(Direct_electricity_data,year_columns) * Electricity_export_percent
    export_DF=pd.DataFrame({
        'export':   Indirect_export * 1e-14
        })
    
    # 准备绘图数据
    plot_data = pd.DataFrame({
        'transport': Indirect_transportation * 1e-14,
        'fuel': Indirect_fuel * 1e-14,
        'process': Indirect_process *1e-14,
        'export': Indirect_export * 1e-14,
        'residential': Indirect_residential * 1e-14,
        'commercial': Indirect_commercial * 1e-14
        })

    return plot_data, year_columns

def plot_stacked_area_chart(plot_data, year_columns, output_folder, language='en'):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    x_years = np.array([int(year) for year in year_columns])
    stack_baseline = np.zeros(len(x_years))
    labels = []
    tabletoshow = pd.DataFrame(index=range(2023,2061))

    # Language-specific settings
    titles = {'en': 'Scope 1+2 CO2 Emission by Sector', 'cn': '分部门二氧化碳间接排放（范围1+2）'}
    ylabels = {'en': 'Mt CO2', 'cn': '排放量 (亿吨)'}
    sector_labels = {
        'en': {
            'transport': 'Transportation',
            'fuel': 'Industrial Fuel',
            'process': 'Industrial Process',
            'export': 'Electricity Export',
            'residential': 'Residential Bldgs',
            'commercial': 'Commercial Bldgs'
        },
        'cn': {
           'transport': '交通部门',
           'fuel': '工业燃料',
           'process': '工业过程',
           'export': '外送电力',
           'residential': '居民建筑',
           'commercial': '公共建筑'
        }
    }
    ncols = {'en': 3, 'cn': 3}

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.facecolor'] = 'white'
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.rcParams['axes.facecolor'] = 'white'

    color_index = 0
    # 使用自定义的稳重配色方案绘制堆积图
    yrange = 0
    if language == 'en':
        for label, data in plot_data.items():
            label1 = sector_labels[language][label]
            labels.append(label1)
            axs[1].fill_between(x_years, stack_baseline, stack_baseline + data*100, label=sector_labels[language][label],
                        color=colors[color_index % len(colors)], edgecolor='none')
            yrange = max(yrange,max(stack_baseline + data*100))
            tabletoshow[label1] = list(data*100)
            stack_baseline += data*100
            color_index += 1
    else:
        for label, data in plot_data.items():
            label1 = sector_labels[language][label]
            labels.append(label1)
            axs[1].fill_between(x_years, stack_baseline, stack_baseline + data, label=sector_labels[language][label],
                        color=colors[color_index % len(colors)], edgecolor='none')
            yrange = max(yrange,max(stack_baseline + data))
            tabletoshow[label1] = list(data)
            stack_baseline += data
            color_index += 1


    # 设置坐标轴和刻度颜色为黑色，以及刻度的位置
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black') 
    axs[1].spines['right'].set_color('black') 

    axs[1].tick_params(axis='x', colors='black', direction='out', length=5, pad=2)
    axs[1].tick_params(axis='y', colors='black', direction='out', length=5, pad=2)

    # 设置坐标轴界限
    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    axs[1].set_xlim([min(x_years), max(x_years)])

    #plt.ylabel(ylabels[language],rotation=0, labelpad=20,loc="bottom")
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.1, 1.02)  # 通过坐标来微调标签位置
    
    # 确定y轴最大值
    # yticks=range(0,14,2)
    # plt.yticks(yticks)
    if language == 'cn':
        plt.ylim(0 , 150)

    else:
        plt.ylim(0 , 15000)
    plt.legend(loc=8, ncol=ncols[language],bbox_to_anchor=(0.5, -0.4),edgecolor="white")

    # 调整图表布局
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
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
    if language=='en':
        plot_data=plot_data*100
    for column in plot_data.columns:
        plot_data[column] = pd.to_numeric(plot_data[column], errors='coerce')
    total_values = plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
         

    output_path = f"{output_folder}/全行业-碳排放：分部门二氧化碳间接排放（范围1+2）{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/全行业-碳排放：分部门二氧化碳间接排放（范围1+2）{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "D:\\实习\\EPS\\EPS数据\\省级\\内蒙data.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\内蒙Policy\\"
    plot_data, year_columns = read_and_prepare_data(file_path)

    # Plot both English and Chinese versions
    plot_stacked_area_chart(plot_data, year_columns, output_folder, language='en')
    plot_stacked_area_chart(plot_data, year_columns, output_folder, language='cn')
