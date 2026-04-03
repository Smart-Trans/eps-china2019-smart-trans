import subprocess
import os
from tqdm import tqdm

def run_python_scripts(directory, input_csv_path, output_folder_path):
    python_command = "python"
    # 获取当前脚本的绝对路径并转换为文件名
    current_script = os.path.basename(__name__)
    env = os.environ.copy()
    env["INPUT_CSV_PATH"] = input_csv_path
    env["OUTPUT_FOLDER_PATH"] = output_folder_path

    # 列出目录下的所有.py文件，除了当前执行的脚本
    scripts = [file for file in os.listdir(directory) if file.endswith(".py") and file != current_script]

    for filename in tqdm(scripts, desc="Running scripts"):
        filepath = os.path.join(directory, filename)
        print(f"开始处理脚本：{filename}")
        try:
            # 执行脚本，并设置环境变量
            result = subprocess.run([python_command, filepath], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
            # 如果脚本执行成功，打印输出
            print(f"脚本 {filename} 执行完成。输出：\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            # 如果脚本执行失败，打印错误信息
            print(f"执行脚本 {filepath} 时出错：\n{e.stderr}")
        except subprocess.TimeoutExpired as e:
            # 如果脚本执行超时，打印超时信息
            print(f"脚本 {filepath} 在 {e.timeout} 秒后超时。")

if __name__ == "__main__":
    directory = "C:\\Users\\zhlx3\\Desktop\\何逸群\\实习生\\马媛\\2024.11.28 NCSC出图代码\\全国Policy带表code"
    input_csv_path = "C:\\Users\\zhlx3\\Desktop\\何逸群\\何逸群\\省级EPS\\smart-trans 省级\\eps-china2022-smart-trans\\MostRecentRun.csv"
    output_folder_path = "C:\\Users\\zhlx3\\Desktop\\何逸群\\实习生\\马媛\\2024.11.28 NCSC出图代码\\渐进转型CNS"
    run_python_scripts(directory, input_csv_path, output_folder_path)
