#!/bin/bash

# 要查找的环境名称
ENV_NAME="daily_cf_tracker"

# 获取 conda 环境列表，并查找目标环境
# conda info --envs 输出格式示例：
# base                  *  /opt/anaconda3
# daily_cf_tracker         /opt/anaconda3/envs/daily_cf_tracker
#
# 使用 awk：寻找第二列（路径）并输出，忽略包含 '#' 的行，匹配环境名后输出路径
win_path=$(conda info --envs | awk -v name="$ENV_NAME" '$1 == name {print $NF; exit}')
env_path=$(cygpath -u "$win_path")

if [ -z "${env_path}" ]; then
    echo "错误: 未找到名为 '$ENV_NAME' 的 conda 环境." >&2
    exit 1
else
    echo "找到了 conda 环境位置: ${env_path}"
fi

# 尝试删除已有服务
nssm remove DailyCFTracker confirm

proj_path=$(pwd)

if [ -z "${proj_path}" ]; then
    echo "错误: 未能获取当前项目位置." >&2
    exit 1
else
    echo "找到了当前位置: ${proj_path}"
fi

nssm install DailyCFTracker "${env_path}/python.exe" "app.py"
nssm set DailyCFTracker AppDirectory "${proj_path}"
nssm set DailyCFTracker Start SERVICE_AUTO_START
nssm set DailyCFTracker AppStdout "${proj_path}/service.log"
nssm set DailyCFTracker AppStderr "${proj_path}/service_error.log"
