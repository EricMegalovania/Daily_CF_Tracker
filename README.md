第一次使用

```bash
git checkout -b daily_cf_tracker
```

更新仓库

```bash
git checkout main               # 切换到主分支
git pull origin main            # 拉取原仓库的最新修改
git checkout daily_cf_tracker   # 切回你的分析分支
git merge main                  # 将最新代码合并进来
```

运行网站

```bash
conda env create -f environment.yaml
python app.py
```

注册为服务

```bash
sudo nssm install CFDailyTracker "C:\ProgramData\miniconda3\envs\daily_cf_tracker\python.exe" "app.py"
sudo nssm set CFDailyTracker AppDirectory "D:\A_devcpp\Daily_CF_Problems\tracker"
sudo nssm set CFDailyTracker Start SERVICE_AUTO_START
sudo nssm set CFDailyTracker AppStdout "D:\A_devcpp\Daily_CF_Problems\tracker\service.log"
sudo nssm set CFDailyTracker AppStderr "D:\A_devcpp\Daily_CF_Problems\tracker\service_error.log"
```

常用管理命令

| 操作 | 命令 |
|------|------|
| 启动 | `sudo nssm start DailyCFTracker` |
| 停止 | `sudo nssm stop DailyCFTracker` |
| 重启 | `sudo nssm restart DailyCFTracker` |
| 查看状态 | `sudo nssm status DailyCFTracker` |
| 删除服务 | `sudo nssm remove DailyCFTracker confirm` |
| 修改配置 | `sudo nssm edit DailyCFTracker`（打开 GUI） |