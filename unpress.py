#!/bin/python3
import os
import tarfile
import argparse

# 定义文件列表
fileList = ['etc/caddy',
            'etc/config',
            'etc/openclash',
            'etc/samba',
            'etc/ssh',
            'etc/ppp',

            'etc/netdata/netdata.conf',
            'etc/adguardhome.yaml',
            'etc/shadow',
            'etc/init.d/caddy'
            ]

# 解压压缩包到当前目录
def extractTar(file):
    with tarfile.open(file, 'r:gz') as tar:
        tar.extractall()


# 移除除了文件列表中指定的文件和目录之外的文件
def removeFilesExcept(fileList, directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        skipRoot = False
        for filePath in fileList:           
            if root == filePath or root.startswith(filePath):
                skipRoot = True
                break

        if skipRoot:
            continue

        files_to_remove = [file for file in files if os.path.join(root, file) not in fileList]
        dirs_to_remove = [dir for dir in dirs if os.path.join(root, dir) not in fileList]

        for file in files_to_remove:
            filePath = os.path.join(root, file)
            os.remove(filePath)

        for dir in dirs_to_remove:
            dirPath = os.path.join(root, dir)
            if not os.listdir(dirPath):
                os.rmdir(dirPath)

# 设置命令行参数
parser = argparse.ArgumentParser(description='Extract and clean files from a tar archive')
parser.add_argument('tarFile', type=str, help='Path to the tar.gz file')
args = parser.parse_args()

# 解析命令行参数
tarFile = args.tarFile

# 解压指定的压缩包
extractTar(tarFile)

# 移除除了文件列表中指定的文件之外的文件
removeFilesExcept(fileList, 'etc')
