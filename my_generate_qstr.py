import subprocess
import argparse
import os


default_includes=['.', 'build', '..', 
                  'ports/rtt/',
                  'ports/rtt/modules/',
                  'ports/rtt/boards/',
                  'ports/rtt/modules/machine',
                  'extmod/',
                  'shared/runtime',
                  'shared/timeutils',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/toolchain/riscv64-unknown-elf/include',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel/rt-thread/include',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel/rt-thread/components/legacy',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel/rt-thread/components/drivers/include',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel/rt-thread/components/finsh',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/kernel/rt-thread/components/drivers/audio',
                  'C:/Users/LR/Downloads/luban-lite-master-wx/luban-lite-master/bsp/artinchip/include/drv'
                  ]
default_source_dirs=['py',
                     'ports/rtt/',
                     'ports/rtt/modules/machine/',
                     'ports/rtt/modules/modmachine.c',
                     'shared/readline',
                     'shared/runtime/interrupt_char.c',
                     ]
# 'E:/RK1808/luban-lite-master/bsp/artinchip\include\drv'
def find_c_files(directories):
    """递归查找指定目录中的所有.c文件"""
    c_files = []
    for dir_path in directories:
        if not os.path.exists(dir_path):
            continue
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.c'):
                    full_path = os.path.join(root, file)
                    c_files.append(full_path)
    return c_files

def build_command(args):
    """构建要执行的命令列表"""
    # 处理包含路径
    include_flags = [f'-I{path}' for path in args.includes]
    
    # 收集源文件
    source_files = args.sources.copy()
    if args.source_dirs:
        source_files += find_c_files(args.source_dirs)
    
    # 构建基本命令
    # 去掉了-Werror
    cmd = [
        'python', args.script_path,
        'pp', 'gcc', '-E', 'output', args.output_file,
        'cflags',
        *include_flags,
        '-Wall', '-Wextra',
        '-Wno-unused-parameter', '-Wpointer-arith',
        '-std=gnu99', '-Os',
        '-fdata-sections', '-ffunction-sections',
        '-fno-asynchronous-unwind-tables', '-DNO_QSTR',
        'cxxflags', '-DNO_QSTR',
        'sources',
        *source_files
    ]
    
    return cmd

def main():
    parser = argparse.ArgumentParser(description='生成qstr定义')
    parser.add_argument('--script-path', default='py/makeqstrdefs.py',
                      help='makeqstrdefs.py脚本路径')
    parser.add_argument('--output-file', default='ports/rtt/boards/genhdr/qstr.i.last',
                      help='输出文件路径')
    parser.add_argument('--includes', nargs='+', default=default_includes,
                      help='包含目录列表（自动添加-I前缀）')
    parser.add_argument('--source-dirs', nargs='+', default=default_source_dirs,
                      help='要扫描的源代码目录（自动收集.c文件）')
    parser.add_argument('--sources', nargs='+', default=['py/mpstate.c'],
                      help='要包含的源代码文件（可指定多个）')
    
    args = parser.parse_args()

    # 构建并执行命令
    command = build_command(args)
    print("执行命令:", ' '.join(command))
    
    try:
        subprocess.run(command, check=True)
        print("命令执行成功")
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误码: {e.returncode}")
        exit(1)

if __name__ == '__main__':
    main()