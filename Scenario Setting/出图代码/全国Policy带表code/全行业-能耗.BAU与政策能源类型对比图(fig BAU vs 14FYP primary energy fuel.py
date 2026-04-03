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
    data['Time']=data['Time'].astype(str)

    # 定义能源分类
    coal_sources = ['hard coal', 'lignite']
    petroleum_sources = ['diesel', 'LPG', 'gasoline', 'fuel oil', 'jet fuel', 'crude oil', 'biofuel gasoline',
                         'biofuel diesel']
    natural_gas_sources = ['natural gas']  # 假设数据中天然气的表示方式为'natural gas'
    renewable_sources = ['wind', 'solar', 'hydro', 'biomass', 'nuclear', 'geothermal']

    BAU_sources= {
        "BAU Coal": coal_sources,
        "BAU Petroleum": petroleum_sources,
        "BAU Natural Gas": natural_gas_sources,
        "BAU Renewable": renewable_sources
    }
    policy_sources={
        "Policy Coal": coal_sources,
        "Policy Petroleum": petroleum_sources,
        "Policy Natural Gas": natural_gas_sources,
        "Policy Renewable": renewable_sources
        }

    Policy_plot_data = pd.DataFrame(index=year_columns)
    BAU_plot_data=pd.DataFrame(index=year_columns)
    #BAU数据
    for source_type, source_list in BAU_sources.items():
        source_sum = pd.Series(0, index=year_columns)
        non_energy_use_sum = pd.Series(0, index=year_columns)
        for source in source_list:
            primary_pattern = f"BAU Total Primary Energy Use.*{source}"
            primary_use = data[data['Time'].str.contains(primary_pattern, regex=True) & ~data['Time'].str.contains("Output")]
            source_sum += primary_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

            non_energy_pattern = f"BAU Industrial Fuel Use for Non Energy Purposes.*{source}"
            non_energy_use = data[data['Time'].str.contains(non_energy_pattern, regex=True)]
            non_energy_use_sum += non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

        net_consumption = (source_sum - non_energy_use_sum) * 1.0E-12
        BAU_plot_data[source_type] = net_consumption
    #Policy数据
    for source_type, source_list in policy_sources.items():
        source_sum = pd.Series(0, index=year_columns)
        non_energy_use_sum = pd.Series(0, index=year_columns)
        for source in source_list:
            primary_pattern = f"Total Primary Energy Use.*{source}"
            non_energy_pattern = f"Industrial Fuel Use for Non Energy Purposes.*{source}"
            # 排除含有 'BAU' 的行
            primary_use = data[data['Time'].str.contains(primary_pattern, regex=True) & ~data['Time'].str.contains('BAU', regex=True) & ~data['Time'].str.contains('Output', regex=True)]
            non_energy_use = data[data['Time'].str.contains(non_energy_pattern, regex=True) & ~data['Time'].str.contains('BAU', regex=True)]

            source_sum += primary_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
            non_energy_use_sum += non_energy_use[year_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum()

        net_consumption = (source_sum - non_energy_use_sum) * 1.0E-12
        Policy_plot_data[source_type] = net_consumption

    return BAU_plot_data, Policy_plot_data, year_columns

def plot_stacked_area_chart(BAU_plot_data,Policy_plot_data, year_columns, output_folder,language):
    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    x_years = np.array([int(year) for year in year_columns])
    if language=='cn':
        BAU_plot_data=BAU_plot_data / 10000 * 3.60087861438191
        Policy_plot_data=Policy_plot_data / 10000 * 3.60087861438191
    # Language-specific settings
    titles = {'en':'BAU vs CNS Primary Energy Use by Fuel','cn':'分品种一次能源消费对比'}
    ylabels = {'en':'trillion btu','cn':'亿吨标煤'}
    if language=='en':
        sector_labels = {
            'Policy Coal': 'CNS Coal',
            'Policy Petroleum': 'CNS Petroleum',
            'Policy Natural Gas': 'CNS Natural Gas',
            'Policy Renewable': 'CNS Renewable',
            'BAU Coal': 'BAU Coal',
            'BAU Petroleum':'BAU Petroleum' ,
            'BAU Natural Gas':'BAU Natural Gas' ,
            'BAU Renewable': 'BAU Renewable'
    }
    else:
        sector_labels = {
               'Policy Coal': 'CNS煤',
               'Policy Petroleum': 'CNS汽油',
               'Policy Natural Gas': 'CNS天然气',
               'Policy Renewable': 'CNS可再生能源',
               'BAU Coal': 'BAU煤',
               'BAU Petroleum':'BAU汽油' ,
               'BAU Natural Gas':'BAU天然气' ,
               'BAU Renewable': 'BAU可再生能源'
       }
    colors={
        'Policy Coal': '#969696',
        'Policy Petroleum': '#000000',
        'Policy Natural Gas': '#c01b00',
        'Policy Renewable': '#00b050',
        'BAU Coal': '#969696',
        'BAU Petroleum':'#000000' ,
        'BAU Natural Gas':'#c01b00' ,
        'BAU Renewable': '#00b050'
        }
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
    labels = []
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
        line.append(line_obj)
        yrange = max(yrange,max(Policy_stack_baseline + data2))
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
        plt.ylim(0,100)
    else:
        plt.ylim(0,225000)
    axs[1].legend( loc=8,bbox_to_anchor=(0.5,-0.4), ncol=4,edgecolor="white")
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


    output_path = f"{output_folder}/全行业-能耗：BAU与政策能源类型对比图无标题{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")

    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/全行业-能耗：BAU与政策能源类型对比图{language}.png"
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

