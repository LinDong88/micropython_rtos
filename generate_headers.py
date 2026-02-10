import subprocess
import sys
import os
import re
from pathlib import Path

# 配置基础路径（根据实际情况调整）
BASE_DIR = Path(__file__).parent # 假设脚本放在项目根目录的scripts目录下
PORTS_DIR = BASE_DIR / "ports/rtt/boards"
GENHDR_DIR = PORTS_DIR / "genhdr"
PY_DIR = BASE_DIR / "py"

print(PORTS_DIR)
def run_command(cmd, cwd=None):
    """执行命令并检查返回值"""
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}")

def generate_root_pointers():
    print("Generating root_pointers.h...")
    input_file = GENHDR_DIR / "qstr.i.last"
    output_file = GENHDR_DIR / "root_pointers.h"
    
    cmd = f"python make_root_pointers.py {input_file}"
    print('root_pointers input_file=',input_file)
    print('root_pointers output_file=',output_file)
    print('cmd=',cmd)
    print('PY_DIR=',PY_DIR)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PY_DIR)
    
    with open(output_file, "w") as f:
        f.write(result.stdout)

def generate_mpversion():
    print("Generating mpversion.h...")
    output_file = GENHDR_DIR / "mpversion.h"
    run_command(f"python makeversionhdr.py {output_file}", cwd=PY_DIR)

def process_qstr_split():
    print("Processing qstr split...")
    cmd = (
        f"python {PY_DIR}/makeqstrdefs.py split qstr "
        f"{GENHDR_DIR}/qstr.i.last {GENHDR_DIR}/qstr _"
    )
    run_command(cmd)

def process_qstr_cat():
    print("Processing qstr cat...")
    cmd = (
        f"python {PY_DIR}/makeqstrdefs.py cat qstr _ "
        f"{GENHDR_DIR}/qstr {GENHDR_DIR}/qstrdefs.collected.h"
    )
    run_command(cmd)


def generate_preprocessed_qstr():
    # 定义基础路径（根据实际情况调整）
    
    # 原始命令字符串
    cmd = (
        f"cat ../py/qstrdefs.h qstrdefsport.h ../ports/rtt/boards/genhdr/qstrdefs.collected.h "
        f"| sed 's/^Q(.*)/\"&\"/' "
        f"| gcc -E -I. -Ibuild -I.. -I../ports/rtt/boards -I../ports/rtt -Wall -Werror -Wextra "
        f"-Wno-unused-parameter -Wpointer-arith -std=gnu99 -Os -fdata-sections "
        f"-ffunction-sections -fno-asynchronous-unwind-tables - "
        f"| sed 's/^\\\"\\(Q(.*)\\)\\\"/\\1/' "
        f"> {GENHDR_DIR}/qstrdefs.preprocessed.h"
    )
    print("cmd = ",cmd)
    print("PY_DIR = ",PY_DIR)
    try:
        # 在genhdr目录执行命令
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            cwd=PY_DIR
        )
        print("✅ 命令执行成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败，错误码: {e.returncode}")
        raise
'''
def generate_preprocessed_qstr():
    print("Generating preprocessed qstr...")
    # 合并文件内容
    files = [
        PY_DIR / "qstrdefs.h",
        PORTS_DIR / "qstrdefsport.h",
        GENHDR_DIR / "qstrdefs.collected.h"
    ]
    
    combined = []
    for f in files:
        with open(f) as fd:
            combined.append(fd.read())
    
    # 第一次sed处理
    processed = re.sub(r'^Q\((.*)\)', r'"Q(\1)"', "\n".join(combined), flags=re.MULTILINE)
    
    # 调用gcc预处理
    gcc_cmd = [
        "gcc", "-E", "-I.", "-Ibuild", "-I..", f"-I{PORTS_DIR}/boards",
        "-Wall", "-Werror", "-Wextra", "-Wno-unused-parameter", "-Wpointer-arith",
        "-std=gnu99", "-Os", "-fdata-sections", "-ffunction-sections",
        "-fno-asynchronous-unwind-tables", "-"
    ]
    result = subprocess.run(
        gcc_cmd,
        input=processed,
        text=True,
        capture_output=True,
        cwd=GENHDR_DIR
    )
    
    # 第二次sed处理
    final_output = re.sub(r'^\"(Q\(.*\))\"', r'\1', result.stdout, flags=re.MULTILINE)
    
    with open(GENHDR_DIR / "qstrdefs.preprocessed.h", "w") as f:
        f.write(final_output)
'''
def generate_qstr_data():
    print("Generating qstrdefs.generated.h...")
    input_file = GENHDR_DIR / "qstrdefs.preprocessed.h"
    output_file = GENHDR_DIR / "qstrdefs.generated.h"
    print(f"python {PY_DIR}/makeqstrdata.py {input_file} > {output_file}")
    run_command(f"python {PY_DIR}/makeqstrdata.py {input_file} > {output_file}")

def generate_module_defs():
    print("Generating moduledefs.h...")
    input_file = GENHDR_DIR / "qstr.i.last"
    output_file = GENHDR_DIR / "moduledefs.h"
    run_command(f"python makemoduledefs.py {input_file} > {output_file}", cwd=PY_DIR)

def main():
    # 确保生成目录存在
    GENHDR_DIR.mkdir(parents=True, exist_ok=True)

    generate_root_pointers()
    generate_mpversion()
    process_qstr_split()
    process_qstr_cat()
    generate_preprocessed_qstr()
    generate_qstr_data()
    generate_module_defs()

    print("All files generated successfully!")

if __name__ == "__main__":
    main()