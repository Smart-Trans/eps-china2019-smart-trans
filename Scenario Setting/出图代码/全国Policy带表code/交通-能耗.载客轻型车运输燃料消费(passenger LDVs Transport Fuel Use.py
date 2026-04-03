import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# 设置绘图风格
sns.set(style='white', palette='muted')

def search(data,col,Str1,Str2="",Str3="",Str4=""):
    return data[data[col].str.contains(Str1) & data[col].str.contains(Str2) &  data[col].str.contains(Str3) &  data[col].str.contains(Str4) & ~data[col].str.contains("BAU") & ~data[col].str.contains("Year")]

def Sum(data,col):
    return data[col].apply(pd.to_numeric,errors='coerce').fillna(0).sum()

def read_and_prepare_data(file_path):
    data = pd.read_csv(file_path, dtype={'Time': str}, on_bad_lines='warn')
    data['Time']=data['Time'].astype(str)
    year_columns = [str(year) for year in range(2023, 2061)]
    processed_data = pd.DataFrame(index=year_columns)
    
    biofuel_diesel_data=search(data,'Time',"Transportation Sector Fuel Used","biofuel diesel","LDVs","passenger")
    biofuel_diesel=Sum(biofuel_diesel_data,year_columns)
    
    biofuel_gasoline_data=search(data,'Time',"Transportation Sector Fuel Used","biofuel gasoline","LDVs","passenger")
    biofuel_gasoline=Sum(biofuel_gasoline_data,year_columns)
    
    electricity_data=search(data,'Time',"Transportation Sector Fuel Used","electricity","LDVs","passenger")
    electricity=Sum(electricity_data,year_columns)
    
    hydrogen_data=data[data['Time'].str.contains("Transportation Sector Fuel Used") & data['Time'].str.contains("LDVs") & data['Time'].str.contains("passenger") & data['Time'].str.contains("hydrogen tf") & ~data['Time'].str.contains("BAU") & ~data['Time'].str.contains("Year")]
    hydrogen=Sum(hydrogen_data,year_columns)
    
    jet_fuel_data=search(data,'Time',"Transportation Sector Fuel Used","jet fuel","LDVs","passenger")
    jet_fuel=Sum(jet_fuel_data,year_columns)
    
    LPG_data=search(data,'Time',"Transportation Sector Fuel Used","LPG propane or butane","LDVs","passenger")
    lpg=Sum(LPG_data,year_columns)
    
    natural_gas_data=search(data,'Time',"Transportation Sector Fuel Used","natural gas tf","LDVs","passenger")
    natural_gas=Sum(natural_gas_data,year_columns)
    
    petroleum_diesel_data=search(data,'Time',"Transportation Sector Fuel Used","petroleum diesel","LDVs","passenger")
    petroleum_diesel=Sum(petroleum_diesel_data,year_columns)
    
    petroleum_gasoline_data=search(data,'Time',"Transportation Sector Fuel Used","petroleum gasoline","LDVs","passenger")
    petroleum_gasoline=Sum(petroleum_gasoline_data,year_columns)
    
    processed_data=pd.DataFrame({
        "biofuel diesel": biofuel_diesel * 3.60087861438191E-12,
        "biofuel gasoline": biofuel_gasoline * 3.60087861438191E-12,
        "electricity": electricity * 3.60087861438191E-12,
        "hydrogen": hydrogen * 3.60087861438191E-12,
        "jet fuel": jet_fuel * 3.60087861438191E-12,
        "natural gas": natural_gas * 3.60087861438191E-12,
        "petroleum diesel": petroleum_diesel * 3.60087861438191E-12,
        "petroleum gasoline": petroleum_gasoline * 3.60087861438191E-12
        })
    processed_data=processed_data.reindex(columns=['petroleum gasoline','petroleum diesel','jet fuel','natural gas','electricity','hydrogen','biofuel diesel','biofuel gasoline'])
    return processed_data



def plot_sector_energy_consumption(processed_data, output_folder, language):
    titles = {'en': 'Passenger LDVs Transport Fuel', 'cn': '载客轻型车运输燃料消费'}
    ylabels = {'en': 'trillion btu', 'cn': '万吨标煤'}
    fig, axs = plt.subplots(1, 2, figsize=(16, 10))
    if language=='cn':
        processed_data=processed_data
    colors = {
        "biofuel diesel": "#00b050",
        "biofuel gasoline": "#04ffaf",
        "electricity": "#f1bb18",
        "hydrogen": "#620e7a",
        "jet fuel": "#c2dffd",
        "natural gas": "#c01b00",
        "petroleum diesel": "#000000",
        "petroleum gasoline": "#969696",
        "LPG propane or butane": "#087bf1",
        "heavy or residual fuel oil":"#ad6600"
    }

    # 中英文对照字典
    sector_labels = {
        "biofuel diesel": {"en": "Biofuel Diesel", "cn": "生物柴油"},
        "biofuel gasoline": {"en": "Biofuel Gasoline", "cn": "生物汽油"},
        "electricity": {"en": "Electricity", "cn": "电力"},
        "hydrogen": {"en": "Hydrogen", "cn": "氢能"},
        "jet fuel": {"en": "Jet Fuel", "cn": "航空煤油"},
        "natural gas": {"en": "Natural Gas", "cn": "天然气"},
        "petroleum diesel": {"en": "Petroleum Diesel", "cn": "柴油"},
        "petroleum gasoline": {"en": "Petroleum Gasoline", "cn": "汽油"},
        "LPG propane or butane": {"en": "LPG propane or butane", "cn": "燃料油、残渣油"},
        "heavy or residual fuel oil":{"en": "heavy or residual fuel oil", "cn": "液化石油气"}
    }
    
    ncols = {'en': 4, 'cn': 4}
    tabletoshow = pd.DataFrame(index=range(2023,2061))
    if language == 'en':
        # Apply unit conversion for English chart
        processed_data = (processed_data / 3.60087861438191E-12) * 1.0E-12
        cumulative = np.zeros(len(processed_data.index))
        # 计算每个部门在所有年份的总和，并根据这个总和排序
        labels = []
        for sector in processed_data.columns:
            label = sector_labels[sector][language]
            labels.append(label)
            sector_values = processed_data.loc[:, sector].astype(float)
            axs[1].fill_between(processed_data.index, cumulative, cumulative + sector_values, color=colors[sector],
                             label=label)
            tabletoshow[label] = list(sector_values)
            cumulative += sector_values.values

    
    
    cumulative = np.zeros(len(processed_data.index))
    labels = []
    for sector in processed_data.columns:
        if sector not in ['Agricultural', 'Construction']:
            label = sector_labels[sector][language]
            labels.append(label)
            sector_values = processed_data[sector].astype(float)
            axs[1].fill_between(processed_data.index.astype(float), cumulative, cumulative + sector_values,
                             color=colors[sector], label=label)
            tabletoshow[label] = list(sector_values)
            cumulative += sector_values.values
            

    if language == 'cn':
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 确保中文字符显示正确
    if language == 'en':
        plt.rcParams['font.sans-serif'] = ['Times New Roman']

    # 设置坐标轴颜色为黑色
    axs[1].spines['bottom'].set_color('black')
    axs[1].spines['left'].set_color('black')
    axs[1].spines['top'].set_color('black') 
    axs[1].spines['right'].set_color('black')
    
    axs[1].tick_params(axis='x', colors='black')
    axs[1].tick_params(axis='y', colors='black')

    xticks=[2023,2025,2030,2035,2040,2045,2050,2055,2060]
    plt.xticks(xticks)
    plt.subplots_adjust(top=0.7, bottom=0.3, right=0.95, left=0.05)

    # 设置坐标轴单位
    axs[1].set_title(ylabels[language],loc="left",fontsize=10,x=-0.05)
    axs[1].yaxis.set_label_coords(0.035, 1.01)  # 通过坐标来微调标签位置
    # 设置绘图从坐标轴原点开始
    plt.autoscale(axis = 'y')
    y_min, y_max = plt.ylim()
    if language =='cn':
        plt.ylim(0,26000)
    else:
        plt.ylim(0,7000)


    plt.xlim(left=2023, right=2060)
    # 设置y轴上限为原数据绘图最高值的1.4倍
    axs[1].legend(loc=8, ncol=ncols[language],bbox_to_anchor=(0.5, -0.4),edgecolor="white")
    if language=='cn':
        selected_rows = tabletoshow.loc[xticks].transpose().astype(int)
        sum_row = selected_rows.sum().values.round(1)
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
    
    output_path = f"{output_folder}/交通-能耗：载客轻型车运输燃料消费{language}无标题.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"{titles[language]} chart saved to: {output_path}")
    
    plt.title(titles[language],size=18)
    output_path = f"{output_folder}/交通-能耗：载客轻型车运输燃料消费{language}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{titles[language]} chart saved to: {output_path}")

if __name__ == "__main__":
    file_path = os.environ.get('INPUT_CSV_PATH', 'default.csv')
    output_folder = os.environ.get('OUTPUT_FOLDER_PATH', '.')
    # file_path = "D:\\eps\\eps-china2022-smart-trans-main\\policy\\default.csv"
    # output_folder = "D:\\eps\\全国Policy图\\"
    processed_data = read_and_prepare_data(file_path)

    plot_sector_energy_consumption(processed_data, output_folder, 'cn')  # 中文版图表
    plot_sector_energy_consumption(processed_data, output_folder, 'en')  # 英文版图表
