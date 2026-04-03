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
    # 读取数据，处理警告信息
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    year_columns = [str(year) for year in range(2023, 2061)]
    data['Time'] = data['Time'].fillna('')

    BAU_sources = {
        "BAU HDVs": "BAU Transportation Pollutant Emissions Disaggregated.*HDVs.*CO2.*freight",
        "BAU rail": "BAU Transportation Pollutant Emissions Disaggregated.*rail.*CO2.*freight",
        "BAU LDVs": "BAU Transportation Pollutant Emissions Disaggregated.*LDVs.*CO2.*freight"
    }
    policy_sources = {
        "Policy HDVs": "Transportation Pollutant Emissions Disaggregated.*HDVs.*CO2.*freight",
        "Policy rail": "Transportation Pollutant Emissions Disaggregated.*rail.*CO2.*freight",
        "Policy LDVs": "Transportation Pollutant Emissions Disaggregated.*LDVs.*CO2.*freight"
    }
    
    Policy_plot_data = pd.DataFrame(index=year_columns)
    BAU_plot_data=pd.DataFrame(index=year_columns)
    #BAU数据
    for source_type, pattern in BAU_sources.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        BAU_plot_data[source_type]=Sum(sector_data,year_columns) * 1.0E-10

    #Policy数据
    for source_type, pattern in policy_sources.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains("BAU", regex=True)]
        Policy_plot_data[source_type]=Sum(sector_data,year_columns) * 1.0E-10

    return BAU_plot_data, Policy_plot_data, year_columns

def plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,language):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    x_years = np.array([int(year) for year in year_columns])

    # Language-specific settings
    if language=='en':
     titles = 'BAU vs CNS Freight CO2 Emission'
    else:
     titles = "货运二氧化碳排放量对比"
    ylabels = {'cn':"万吨CO2",'en':"Mt CO2"}
    if language=='cn':
     sector_labels = {
            "BAU HDVs": "BAU载货重型车",
            "BAU rail": "BAU载货铁路机车",
            "BAU LDVs": "BAU载货轻型车",
            "Policy HDVs": "CNS载货重型车",
            "Policy rail": "CNS载货铁路机车",
            "Policy LDVs": "CNS载货轻型车"
            }
    else:
     sector_labels = {
            "BAU HDVs": "BAU Freight HDVs",
            "BAU rail": "BAU Freight Rail",
            "BAU LDVs": "BAU Freight LDVs",
            "Policy HDVs": "CNS Freight HDVs",
            "Policy rail": "CNS Freight Rail",
            "Policy LDVs": "CNS Freight LDVs"
    }
    colors={
            "BAU HDVs": "#000000",
            "BAU rail": "#00b050",
            "BAU LDVs": "#f593e0",
            "Policy HDVs": "#000000",
            "Policy rail": "#00b050",
            "Policy LDVs": "#f593e0"
        }
    if language=='cn':
     plt.rcParams['font.sans-serif'] = ['SimHei']
     plt.rcParams['axes.facecolor'] = 'white'
    else:
     plt.rcParams['font.sans-serif'] = ['Times New Romen']
     plt.rcParams['axes.facecolor'] = 'white'
    if language=='en':
      BAU_plot_data=BAU_plot_data/100
      Policy_plot_data=Policy_plot_data/100
    else:
      BAU_plot_data=BAU_plot_data
      Policy_plot_data=Policy_plot_data
    BAU_stack_baseline = np.zeros(len(x_years))
    Policy_stack_baseline=np.zeros(len(x_years))
    line=[]
    fill=[]
    # 使用自定义的稳重配色方案绘制BAU堆积图
    yrange = 0
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    labels = []
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
    '''
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
    '''
    # 设置坐标轴界限
    axs[1].set_xlim([2023,2060])
            # 计算所有数据的最高点，并设置y轴上限为最高值的1.4倍
    max_value = Policy_stack_baseline.max()

    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.1, 1.02)  # 通过坐标来微调标签位置
    if language =='cn':
        plt.ylim(0,100000)
    else:
        plt.ylim(0,1000)

    axs[1].legend( loc=8,bbox_to_anchor=(0.5,-0.4), ncol=3,edgecolor="white")
    # 调整图表布局

    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
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
    axs[0].text(1.1, 1, ylabels[language], va='top', ha='right', fontsize=10)
    for column in BAU_plot_data.columns:
        BAU_plot_data[column] = pd.to_numeric(BAU_plot_data[column], errors='coerce')
    total_values = BAU_plot_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=1, left=0)
    output_path = f"{output_folder}/交通-碳排放.载货碳排放BAU与政策对比图无标题{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.title(titles,size=18)
    output_path = f"{output_folder}/交通-碳排放.载货碳排放BAU与政策对比图{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    #file_path = "D:\\实习\\EPS\\EPS数据\\省级\\内蒙data.csv"
    #output_folder = "C:\\Users\\Mywljy\\Desktop\\内蒙Policy\\"
    BAU_plot_data,Policy_plot_data, year_columns = read_and_prepare_data(file_path)
   
    # Plot both English and Chinese versions
    plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,'cn')
    plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,'en')