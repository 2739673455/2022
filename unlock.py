import os
import shutil
import subprocess

def get_all_files_include_subfolders(folder):
    result = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            result.append(file_path)
    return result

def copy_file(source_path, dst_file_path):
    shutil.copy2(source_path, dst_file_path)

def rename_file(source_path, dst_file_path, current_dir):
    unlock_path = current_dir + "\\Unlock.exe"
    arg = f'-sourcePath="{source_path}" -destPath="{dst_file_path}"'
    cmd = f'"{unlock_path}" {arg}'
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, encoding="utf-8")
    output = output.strip()
    if output:
        print(output)

def main():
    current_dir,self_name = os.path.split(__file__)
    all_files = get_all_files_include_subfolders(current_dir)
    for file_path in all_files:
        if file_path.endswith(self_name) or file_path.endswith("Unlock.exe"):
            continue
        dst_file_path = file_path + ".temp"
        copy_file(file_path, dst_file_path)
        try:
            os.remove(file_path)
        except OSError:
            print(f"文件 {file_path} 删除失败")
            continue
        rename_file(dst_file_path, file_path, current_dir)
    input("解密完成，按回车键退出")

if __name__ == "__main__":
    main()