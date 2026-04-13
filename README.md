# 中国大陆手机号前7位归属地查询工具

基于 Google 官方 `phonenumbers` 库，提供两个脚本：

- `phone_extract.py`：批量提取中国手机号前7位（号段前缀）到“运营商 + 属地”的映射关系，并输出为 `phone_location_table.yaml`
- `phone_query.py`：加载映射表后，交互式查询用户输入的7位号段

---

## 目录结构

```text
.
├── 86_zh                          # 号码与IP属地映射表原始文件
├── phone_extract.py
├── phone_query.py
├── phone_location_table.yaml      # 提取后生成
├── phone_location_table.pkl       # 查询脚本自动生成缓存
└── README.md
```

---

## 环境要求

- Python 3.10+
- pip

依赖：
- phonenumbers
- pyyaml

---

## 下载项目

### 方式1：Git 克隆

```bash
git clone <你的仓库地址>
cd <仓库目录>
```

### 方式2：GitHub 网页下载

1. 打开你的 GitHub 仓库页面
2. 点击 `Code` -> `Download ZIP`
3. 解压后进入项目目录

---

## 安装依赖

```bash
pip install phonenumbers pyyaml
```

---

## 脚本说明

## 1) phone_extract.py

用途：
- 扫描 `1300000` 到 `1999999` 的7位号段
- 调用 `phonenumbers` 提取归属地和运营商
- 生成 `phone_location_table.yaml`

运行：

```bash
python phone_extract.py
```

指定解释器运行（Windows 示例）：

```powershell
C:/Users/<UserName>/AppData/Local/Programs/Python/Python310/python.exe D:/your_workspace/phone_extract.py
```

输出：
- `phone_location_table.yaml`（主数据文件）

说明：
- 全量提取耗时较长，脚本会打印进度信息。

## 2) phone_query.py

用途：
- 启动后监听用户输入
- 输入7位号段（例如 `1300010`）
- 返回对应运营商和属地信息

运行：

```bash
python phone_query.py
```

指定解释器运行（Windows 示例）：

```powershell
C:/Users/<UserName>/AppData/Local/Programs/Python/Python310/python.exe D:/your_workspace/phone_query.py
```

交互示例：

```text
[*]正在加载 YAML 映射表（首次可能较慢）...
[*]正在建立本地缓存...
[*]手机号前7位查询已启动。
[*]请输入7位手机号前缀（示例: 1300010），输入 q 或 quit 退出。
> 1300010
号段: 1300010
运营商: 中国联通
IP属地: 北京市
> q
[*]已退出查询。
```

说明：
- 首次加载 YAML 可能较慢，属于正常现象。
- 程序会自动生成 `phone_location_table.pkl` 缓存，后续启动更快。

---

## 推荐使用流程

1. 先通过逆向获取映射表文件（如86_zh）
2. 先运行 `phone_extract.py` 生成或更新 `phone_location_table.yaml`
3. 再运行 `phone_query.py` 进行交互查询

---

## 常见问题 - Q&A

### Q1：程序看起来“没启动”
通常不是崩溃，而是在首次解析大型 YAML 文件。

处理建议：
- 等待首次加载完成
- 确认目录下已生成 `phone_location_table.pkl`
- 后续启动会优先走缓存，速度明显提升

### Q2：提示找不到 `phone_location_table.yaml`
请先运行：

```bash
python phone_extract.py
```

### Q3：输入后提示格式错误
`phone_query.py` 只接受 **7位纯数字**（如 `1380013`）且接受格式仅为 **3位运营商号码 + 4位地区号码**，暂不支持查询其他格式的号码。

---


## 相关文章
    中国大陆手机号分析：https://www.cnblogs.com/slayedxx/p/19844865
    从手机内部提取电话号码与IP属地映射表：https://www.cnblogs.com/slayedxx/p/19858201

---


