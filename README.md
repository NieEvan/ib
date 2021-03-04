#### IB 行情工具

这是一个接入 IB 行情，并进行实时指标计算与触发条件时提醒的项目。

#### 项目打开方式

1. 使用 PyCharm 打开项目目录, 右键单击 main 目录 【Mark as Sources Root】
2. 执行 main/main.py 文件

#### DB 打开方式

1. PyCharm 右边栏 【Database】-> 【+（New）】-> 【Data Source】 -> 【sqlite】 打开设置弹窗, File 选择 main/db/data.db，下方选择下载安装 driver, 点击 Test Connection 测试连接。
2. 连接成功后, 选择刚新建的 DB, schemas main -> kbars 表格 查看数据
