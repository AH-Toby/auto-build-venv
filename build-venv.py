# -*- coding:utf-8 -*-
import os
import shutil
import subprocess  # 单开进程包

VENV_DIR = 'venv'  # 虚拟环境名称
REQUIREMENTS_DIR = 'requirements.txt'  # 虚拟环境中需要安装的包


class VirtualEnviroment(object):
    """创建虚拟环境的类"""

    def __init__(self):
        self.venv_dir = None  # 虚拟环境位置
        self.requirements_dir = None  # 文本位置
        self.python = None  # python命令
        self.pip = None  # pip命令
        self.pex = None  # pex命令

    def create_venv(self):
        """创建虚拟环境包"""
        self.venv_dir = os.path.join(os.path.curdir, VENV_DIR)
        # 定位到虚拟环境./venv 当前位置下
        self.requirements_dir = os.path.join(os.path.curdir, REQUIREMENTS_DIR)
        # 定位到requirement.txt文件 ./requirement 当前位置下

        if os.path.exists(self.venv_dir):  # 判断当前目录下是否存在虚拟文件夹
            # 已经存在,删除虚拟文件夹
            shutil.rmtree(self.venv_dir)  # 删除虚拟文件夹以及其下所有的文件

        print("Creating virtual environment..")
        subprocess.Popen(["python3", "-m", "virtualenv", "-p", "/export/apps/python/python3.6", VENV_DIR],
                         stderr=subprocess.STDOUT).wait()

        # 运行python3 -m virtualenv -p "/export/apps/python/python3.6" 'venv'  创建python3的虚拟环境
        # subprocess.Popen()  一个进程
        # stderr=subprocess.STDOUT  表示无论进程运行成功还是失败都按照标准输出
        # .wait() 一直等待进程结束

        self.pip = os.path.join(self.venv_dir, 'bin/pip')  # 定位到venv虚拟环境下pip包的位置
        self.pex = os.path.join(self.venv_dir, 'bin/pex')
        self.python = os.path.join(self.venv_dir, 'bin/python')

    def install_packages(self):
        """安装需要的包"""
        print("Installing packages..")
        subprocess.Popen([self.pip, "install", "-r", self.requirements_dir], stderr=subprocess.STDOUT).wait()
        # 运行 pip install -r requirements.txt
        subprocess.Popen([self.pip, "install", "-e", os.path.curdir], stderr=subprocess.STDOUT).wait()
        # 运行 pip install -e . 从本地安装pip

    def create_symlink(self):
        """连接外部创建连接,连接内部venv环境"""
        print("Creating symlink..")
        if not os.path.islink('./activate'):
            print("Creating `activate`..")
            os.symlink(os.path.join(self.venv_dir, 'bin', 'activate'), 'activate')
            # 建立与虚拟环境的连接

if __name__ == '__main__':
    venv = VirtualEnviroment()
    venv.create_venv()
    venv.install_packages()
    venv.create_symlink()
