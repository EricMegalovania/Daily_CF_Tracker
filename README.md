第一次使用前, 设置本地的仓库地址

```bash
# 在 .env 里填写本地克隆的仓库地址
conda env create -f environment.yaml
```

后续可以用如下命令来更新

```bash
conda env update -f environment.yaml --prune
```

运行网站

```bash
conda activate daily_cf_tracker
python app.py
```

注册为服务

```bash
sudo bash install.sh  # 需要安装 gsudo 这个命令, 在 Git Bash 中运行
```

常用管理命令

| 操作 | 命令 |
|------|------|
| 启动 | `nssm start DailyCFTracker` |
| 停止 | `nssm stop DailyCFTracker` |
| 重启 | `nssm restart DailyCFTracker` |
| 查看状态 | `nssm status DailyCFTracker` |
| 删除服务 | `nssm remove DailyCFTracker confirm` |
| 修改配置 | `nssm edit DailyCFTracker`（打开 GUI） |