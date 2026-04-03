import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import re
import string
# 设置绘图风格
sns.set(style='white', palette='muted')


def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in range(2023, 2061)]
    CO2processed_data = pd.DataFrame(index=year_columns)
    Pprocessed_data = pd.DataFrame(index=year_columns)
    sectors=[
        "Agricultural",
        "Iron and Steel",
        "Petrochem & Coke",
        "Non-metallic Mineral",
        "Chemicals",
        "Mining and Washing of Coal",
        "Construction",
        "Industry Overall",
        "Rubber and Plastics Products"
        ]
    CO2_sectors = {
        "Agricultural": "Industrial Sector Pollutant Emissions.*agriculture.*CO2",
        "Iron and Steel": "Industrial Sector Pollutant Emissions.*iron and steel.*CO2",
        "Petrochem & Coke": "Industrial Sector Pollutant Emissions.*petroleum and coke.*CO2",
        "Non-metallic Mineral": "Industrial Sector Pollutant Emissions.*cement and other nonmetallic minerals.*CO2",
        "Chemicals": "Industrial Sector Pollutant Emissions.*chemicals.*CO2",
        "Mining and Washing of Coal": "Industrial Sector Pollutant Emissions.*coal mining.*CO2",
        "Construction": "Industrial Sector Pollutant Emissions.*construction.*CO2",
        "Rubber and Plastics Products": "Industrial Sector Pollutant Emissions.*rubber and plastic products.*CO2"
    }
    
    #计算工业非氢部门
    industryCO2_data=data[data['Time'].str.contains("Industrial Sector Pollutant Emissions") & data['Time'].str.contains("CO2") & ~data['Time'].str.contains("BAU") & ~data['Time'].str.contains("agriculture")]
    industryCO2=industryCO2_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
        0).sum() * 10 ** -10
    CO2processed_data["Industry Overall"]=industryCO2
    #得到分行业二氧化碳排放
    for sector_key, pattern in CO2_sectors.items():
        # 确保行不包含“BAU”
        sector_data = data[data['Time'].str.contains(pattern, regex=True) & ~data['Time'].str.contains("BAU")]
        CO2processed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 10 ** -10
    #计算分行业增加值
    #筛选工业各行业代码
    code=[]
    for y in industryCO2_data['Time']:
        x=re.findall(r'\[(.*?),', y)
        code=code+x
    trans_table = str.maketrans('', '', string.ascii_lowercase + ' ')
    code=[item.translate(trans_table) for item in code]
    P_sectors={
        "Agricultural": "BAU Value Added by ISIC Code by Year.*01T03",
        "Iron and Steel": "BAU Value Added by ISIC Code by Year.*241",
        "Petrochem & Coke": "BAU Value Added by ISIC Code by Year.*19",
        "Non-metallic Mineral": "BAU Value Added by ISIC Code by Year.*239",
        "Chemicals": "BAU Value Added by ISIC Code by Year.*20",
        "Mining and Washing of Coal": "BAU Value Added by ISIC Code by Year.*05",
        "Construction": "BAU Value Added by ISIC Code by Year.*41T43",
        "Rubber and Plastics Products": "BAU Value Added by ISIC Code by Year.*22"
        }
    for sector_key, pattern in P_sectors.items():
        sector_data = data[data['Time'].str.contains(pattern, regex=True)]
        Pprocessed_data[sector_key] = sector_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
            0).sum() * 6.5196001920818 *1E-8
    #计算工业非氢部门
    
    pattern='|'.join(str(num) for num in code)
    industryP_data=data[data['Time'].str.contains("BAU Value Added by ISIC Code by Year") & data['Time'].str.contains(pattern)]
    industryP=industryP_data[year_columns].apply(pd.to_numeric, errors='coerce').fillna(
        0).sum() * 6.5196001920818 *1E-8
    Pprocessed_data['Industry Overall']=industryP
    
    #求行业二氧化碳排放强度
    processed_data=pd.DataFrame(index=year_columns)
    for sector in sectors:
        processed_data[sector]=CO2processed_data[sector]/Pprocessed_data[sector]
    
    
    return processed_data


def plot_sector_CO2_intensity(processed_data, output_folder, language):
    if language=='en':
        processed_data=processed_data* 6.5196001920818 *100
    titles = {'en': 'CO2 Emissions Intensity by Industrial Sector', 'cn': '行业二氧化碳排放强度'}
    ylabels = {'en': 'tCO2/millionUSD', 'cn': '吨CO2/万元'}

    colors = {
        "Agricultural": "#04ffaf",
        "Iron and Steel": "#004185",
        "Petrochem & Coke": "#000000",
        "Non-metallic Mineral": "#c2dffd",
        "Chemicals": "#f1bb18",
        "Mining and Washing of Coal": "#969696",
        "Construction": "#6E8000",
        "Industry Overall": "#740000",
        "Rubber and Plastics Products": "#ff00ff"
    }

    # 中英文对照字典
    sector_labels_cn = {
        "Agricultural": "农林牧渔业",
        "Iron and Steel": "黑色金属冶炼",
        "Petrochem & Coke": "石油、煤炭加工业",
        "Non-metallic Mineral": "非金属矿物制品",
        "Chemicals": "化学工业",
        "Mining and Washing of Coal": "煤炭开采洗选",
        "Construction": "建筑业",
        "Industry Overall": "工业（除电热氢）",
        "Rubber and Plastics Products": "橡胶及塑料制品"
    }
    ncols={
        "cn":3,
        "en":3
        }

    fig, axs = plt.subplots(1, 2, figsize=(16, 7))
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    labels = []
    if language=='cn':
      for sector in processed_data.columns:
        if sector not in ['Agricultural','Construction','Rubber and Plastics Products']:
            label = sector_labels_cn[sector] if language == 'cn' else sector
            labels.append(label)
            sector_values = processed_data[sector].astype(float)
            plt.plot(processed_data.index.astype(float), processed_data[sector],
                             color=colors[sector], label=label,linewidth=2)
            tabletoshow[label] = list(processed_data[sector])
    if language=='en':
       for sector in processed_data.columns:
         if sector not in ['Agricultural','Construction','Mining and Washing of Coal']:
            label = sector
            labels.append(label)
            sector_values = processed_data[sector].astype(float)
            plt.plot(processed_data.index.astype(float), processed_data[sector],
                              color=colors[sector], label=label,linewidth=2)
            tabletoshow[label] = list(processed_data[sector])

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
    xticks = [2023, 2025, 2030, 2035, 2040, 2045, 2050,2055,2060]
    axs[1].set_xticks(xticks)
    axs[1].set_xticklabels([str(year) for year in xticks])  # 修正在这里
    axs[1].set_xlim(left=2023, right=2060)
    # 设置坐标轴颜色为黑色
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black')
    axs[1].spines['right'].set_color('black')
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')
    # 设置绘图从坐标轴原点开始

 

    plt.xlim(left=2023, right=2060)
    # 设置y轴上限为原数据绘图最高值的1.4倍
    max_value = processed_data.sum(axis=1).max()
    plt.autoscale(axis = 'y')
    y_min, y_max = plt.ylim()
    if language == 'cn':
        plt.ylim(0 , 16)
    else:
        plt.ylim(0, 10000)
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.05, 1)  # 通过坐标来微调标签位置
    axs[1].legend(loc=8,bbox_to_anchor=(0.5,-0.4), ncol=ncols[language],edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().round(2)
    else:
        selected_rows = tabletoshow.loc[xticks].transpose().round(1)

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
    if language == 'en':
        select_data = processed_data.drop(columns=['Agricultural', 'Construction', 'Mining and Washing of Coal'])
    else:
        select_data = processed_data.drop(columns=['Agricultural', 'Construction', 'Rubber and Plastics Products'])
    print(select_data)
    total_values = select_data.sum(axis=1)
    max_year = total_values.idxmax()
    max_value = total_values.max()
    #axs[0].text(0.5, -0.3, f"year: {max_year},max: {max_value:.2f}", va='center', ha='center', fontsize=12)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)
    output_path = f"{output_folder}/工业-碳排放：行业二氧化碳排放强度{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")

    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/工业-碳排放：行业二氧化碳排放强度{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\High Scenario.csv"
    # output_folder = "D:\\eps\\全国Policy图\\High\\"
    processed_data = read_and_prepare_data(file_path)

    plot_sector_CO2_intensity(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_CO2_intensity(processed_data, output_folder, 'en')  # 英文版图表
