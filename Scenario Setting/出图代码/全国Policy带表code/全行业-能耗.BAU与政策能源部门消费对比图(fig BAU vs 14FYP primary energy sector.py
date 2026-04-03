import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
# 设置图表的绘制风格
sns.set(style='white', palette='muted')

def search(data,col,Str1,Str2="",Str3=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) &  data[col].str.contains(Str3)]

def Sum(data,col):
    return data[col].apply(pd.to_numeric,errors='coerce').fillna(0).sum()

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in range(2023, 2061)]
    policy_sectors = {
        "transportation sector": "Policy Transportation Sector",
        "electricity sector": "Policy Electricity Sector",
        "residential buildings sector": "Policy Residential Buildings Sector",
        "commercial buildings sector": "Policy Commercial Buildings Sector",
        "industry sector": "Policy Industry Sector",
        "district heat and hydrogen sector": "Policy District Heat and Hydrogen Sector"
    }
    bau_sectors = {
        "transportation sector": "BAU Transportation Sector",
        "electricity sector": "BAU Electricity Sector",
        "residential buildings sector": "BAU Residential Buildings Sector",
        "commercial buildings sector": "BAU Commercial Buildings Sector",
        "industry sector": "BAU Industry Sector",
        "district heat and hydrogen sector": "BAU District Heat and Hydrogen Sector"
        }
    renewable_sources = ['wind', 'solar', 'hydro', 'biomass', 'nuclear', 'geothermal']
    Policy_plot_data = pd.DataFrame(index=year_columns)
    BAU_plot_data = pd.DataFrame(index=year_columns)
    #筛选policy数据
    for sector, label in policy_sectors.items():
        sector_pattern = f"Total Primary Fuel Use by Sector\\[{sector}"
        sector_data = data[data['Time'].str.contains(sector_pattern, regex=True) & ~data['Time'].str.contains("BAU")]
        sector_sum = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 1.0E-12
        Policy_plot_data[label] = sector_sum

    # 调整电力部门数据，加入可再生能源
    extra_energy = pd.Series(0, index=year_columns)
    for source in renewable_sources:
        energy_use = data[data['Time'].str.contains(f"Total Primary Energy Use.*{source}", regex=True) & ~data['Time'].str.contains("BAU") & ~data['Time'].str.contains("Output")]
        non_energy_use = data[data['Time'].str.contains(f"Industrial Fuel Use for Non Energy Purposes.*{source}", regex=True) & ~data['Time'].str.contains("BAU")]
        extra_energy += (energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() -
                         non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()) * 1.0E-12
    Policy_plot_data["Policy Electricity Sector"] += extra_energy

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
    Policy_plot_data["Policy Nonenergy Use"] = non_energy_total

    # 从工业部门减去非燃料使用的总和
    non_energy_use_for_industry = data[
        data['Time'].str.contains("Industrial Fuel Use for Non Energy Purposes", regex=True) & ~data['Time'].str.contains("BAU")]
    non_energy_total_for_industry = non_energy_use_for_industry[year_columns].apply(pd.to_numeric,errors='coerce').fillna(0).sum() * 1.0E-12
    Policy_plot_data["Policy Industry Sector"] -= non_energy_total_for_industry
    
    
    # 计算各部门能耗
    for sector, label in bau_sectors.items():
        sector_pattern = f"BAU Total Primary Fuel Use by Sector\\[{sector}"
        sector_data = data[data['Time'].str.contains(sector_pattern, regex=True)]
        sector_sum = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() * 1.0E-12
        BAU_plot_data[label] = sector_sum

    # 调整电力部门数据，加入可再生能源
    extra_energy = pd.Series(0, index=year_columns)
    for source in renewable_sources:
        energy_use = data[data['Time'].str.contains(f"BAU Total Primary Energy Use.*{source}", regex=True)]
        non_energy_use = data[data['Time'].str.contains(f"BAU Industrial Fuel Use for Non Energy Purposes.*{source}", regex=True)]
        extra_energy += (energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum() -
                         non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()) * 1.0E-12
    BAU_plot_data["BAU Electricity Sector"] += extra_energy

    # 计算非燃料使用，排除特定行
    exclusions = [
        "coal mining 05,hard coal if",
        "refined petroleum and coke 19,hard coal if",
        "refined petroleum and coke 19,crude oil if"
    ]
    non_energy_use = data[~data['Time'].str.contains('|'.join(exclusions), regex=True) & data['Time'].str.contains(
        "BAU Industrial Fuel Use for Non Energy Purposes", regex=True)]
    non_energy_total = non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
        0).sum() * 1.0E-12
    BAU_plot_data["BAU Nonenergy Use"] = non_energy_total

    # 从工业部门减去非燃料使用的总和
    non_energy_use_for_industry = data[
        data['Time'].str.contains("BAU Industrial Fuel Use for Non Energy Purposes", regex=True)]
    non_energy_total_for_industry = non_energy_use_for_industry[year_columns].apply(pd.to_numeric,
                                                                                    errors='coerce').fillna(
        0).sum() * 1.0E-12
    BAU_plot_data["BAU Industry Sector"] -= non_energy_total_for_industry

    return BAU_plot_data, Policy_plot_data, year_columns

def plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,language):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    labels = []
    x_years = np.array([int(year) for year in year_columns])
    if language=='cn':
        BAU_plot_data=BAU_plot_data / 10000 * 3.60087861438191 
        Policy_plot_data=Policy_plot_data / 10000 * 3.60087861438191 
    # Language-specific settings
    titles = {'en':'BAU vs CNS Primary Energy Use by Sector','cn':'分部门一次能源消费对比'}
    ylabels = {'en':'trillion btu','cn':'亿吨标煤'}
    if language=='en':
     sector_labels = {
            'Policy Industry Sector': 'CNS Indst Fuel',
            'Policy Transportation Sector': 'CNS Trans',
            'Policy Electricity Sector': 'CNS Elec',
            'Policy Residential Buildings Sector': 'CNS Res Bldgs',
            'Policy Commercial Buildings Sector': 'CNS Com Bldgs',
            'Policy District Heat and Hydrogen Sector': 'CNS Heat&H2',
            'Policy Nonenergy Use': 'CNS Nonenergy',
            'BAU Industry Sector': 'BAU Indst Fuel',
            'BAU Transportation Sector':'BAU Trans' ,
            'BAU Electricity Sector':'BAU Elec' ,
            'BAU Residential Buildings Sector': 'BAU Res Bldgs',
            'BAU Commercial Buildings Sector': 'BAU Com Bldgs',
            'BAU District Heat and Hydrogen Sector':'BAU Heat&H2',
            'BAU Nonenergy Use': 'BAU Nonenergy'
    }
    else:
     sector_labels = {
            'Policy Industry Sector': 'CNS工业燃料',
            'Policy Transportation Sector': 'CNS交通部门',
            'Policy Electricity Sector': 'CNS电力部门',
            'Policy Residential Buildings Sector': 'CNS居民建筑',
            'Policy Commercial Buildings Sector': 'CNS商业建筑',
            'Policy District Heat and Hydrogen Sector': 'CNS供热与氢能',
            'Policy Nonenergy Use': 'CNS非燃料使用',
            'BAU Industry Sector': 'BAU工业燃料',
            'BAU Transportation Sector':'BAU交通部门',
            'BAU Electricity Sector':'BAU电力部门',
            'BAU Residential Buildings Sector': 'BAU居民建筑',
            'BAU Commercial Buildings Sector': 'BAU商业建筑',
            'BAU District Heat and Hydrogen Sector':'BAU供热与氢能',
            'BAU Nonenergy Use': 'BAU非燃料使用'
    }
    colors={
        'Policy Industry Sector': '#000000',
        'Policy Transportation Sector': '#c01b00',
        'Policy Electricity Sector': '#f1bb18',
        'Policy Residential Buildings Sector': '#087bf1',
        'Policy Commercial Buildings Sector': '#004185',
        'Policy District Heat and Hydrogen Sector': '#620e7a',
        'Policy Nonenergy Use': '#c2dffd',
        'BAU Industry Sector': '#000000',
        'BAU Transportation Sector':'#c01b00' ,
        'BAU Electricity Sector':'#f1bb18' ,
        'BAU Residential Buildings Sector': '#087bf1',
        'BAU Commercial Buildings Sector': '#004185',
        'BAU District Heat and Hydrogen Sector':'#620e7a',
        'BAU Nonenergy Use':'#c2dffd' 
        }
    ncols = 7

    if language=='en':
     plt.rcParams['font.sans-serif'] = ['Times New Roman']
     plt.rcParams['axes.facecolor'] = 'white'
    else:
     plt.rcParams['font.sans-serif'] = ['SimHei']
     plt.rcParams['axes.facecolor'] = 'white'

    BAU_stack_baseline = np.zeros(len(x_years))
    Policy_stack_baseline=np.zeros(len(x_years))
    line=[]
    fill=[]
    BAU_stack_baseline = pd.to_numeric(BAU_stack_baseline, errors='coerce')
    # 使用自定义的稳重配色方案绘制BAU堆积图
    yrange = 0
    for (label1, data1), (label2, data2) in zip(BAU_plot_data.items(), Policy_plot_data.items()):
        data1 = pd.to_numeric(data1, errors='coerce')
        fill_obj=axs[1].fill_between(x_years, BAU_stack_baseline, BAU_stack_baseline + data1, label=sector_labels[label1],
                        color=colors[label1],edgecolor=colors[label1],alpha=0.5)
        label = sector_labels[label1]
        labels.append(label)
        tabletoshow[label] = list(data1)
        fill.append(fill_obj)
        yrange = max(yrange,max(BAU_stack_baseline + data1))
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
            # 计算所有数据的最高点，并设置y轴上限为最高值的1.4倍

    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.1, 1.02)  # 通过坐标来微调标签位置

    if language =='cn':
        plt.ylim(0,120)
    else:
        plt.ylim(0,300000)
    # 调整图表布局
    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
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
    for column in BAU_plot_data.columns:
        BAU_plot_data[column] = pd.to_numeric(BAU_plot_data[column], errors='coerce')
    total_values = BAU_plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)

    output_path = f"{output_folder}/全行业-能耗.BAU与政策能源部门消费对比图无标题{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/全行业-能耗.BAU与政策能源部门消费对比图{language}.png"
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
    plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,'cn')
    plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,'en')