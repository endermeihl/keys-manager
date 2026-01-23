# Keys Manager

一个安全的密钥管理工具，用于生成、存储和管理加密密钥。

## 功能特性

- **安全密钥生成**：生成 24 位高强度随机密钥（包含大小写字母、数字和特殊字符）
- **加密存储**：使用 PBKDF2 + Fernet 对称加密算法保护密钥
- **密码保护**：所有敏感操作需要密码验证
- **分类管理**：通过用途标签管理多个密钥

## 安装依赖

```bash
pip install cryptography
```

## 使用方法

### 方式一：交互式 CLI（推荐）

使用 `cli.py`，密码通过安全方式输入（不显示在屏幕上）：

```bash
# 生成新密钥
python cli.py generate --purpose "API Key"

# 列出所有密钥用途
python cli.py list

# 查看指定密钥
python cli.py view --purpose "API Key"

# 删除密钥
python cli.py delete --purpose "API Key"
```

### 方式二：命令行参数（适合脚本集成）

使用 `main.py`，通过参数传递密码：

```bash
# 查看帮助
python main.py

# 生成新密钥
python main.py --action generate --purpose "API Key" --password "your_password"

# 列出所有密钥用途
python main.py --action list

# 查看指定密钥
python main.py --action view --purpose "API Key" --password "your_password"

# 删除密钥
python main.py --action delete --purpose "API Key" --password "your_password"
```

### 可选参数

- `--storage`：指定存储文件路径（默认：`keys.enc`）

## 存储文件

密钥以加密形式存储在 `keys.enc` 文件中（JSON 格式）。该文件包含：
- 加密盐值（salt）
- 加密后的密钥数据

## 安全说明

1. 请使用强密码保护您的密钥
2. 妥善保管 `keys.enc` 文件
3. 密钥生成后请立即保存，遗忘密码将无法恢复
4. 使用交互式 CLI 可避免密码出现在命令行历史中

## 项目结构

```
keys-manager/
├── keys_manager.py   # 核心加密管理模块
├── cli.py            # 交互式命令行界面
├── main.py           # 参数式命令行入口
├── keys.enc          # 加密存储文件（运行后生成）
└── README.md
```
