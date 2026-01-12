# Keys Manager

一个安全的密钥管理工具，用于生成、存储和管理加密密钥。

## 功能特性

1. **生成密钥**: 通过命令行生成24位安全密钥并加密保存到本地，生成时需要标记密钥作用
2. **密码保护查看**: 只能通过命令行输入密码进行查看密钥
3. **列出密钥用途**: 可以不需要密码查看有哪些作用的密钥
4. **单个密钥查询**: 一次只能通过密码和作用查询一个密钥
5. **删除密钥**: 可以通过密码删除密钥（不支持修改密钥）

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 生成新密钥

```bash
python cli.py generate --purpose "API密钥"
```

系统会提示输入密码（输入两次确认）。密钥生成后会显示一次，请妥善保存。

### 列出所有密钥用途

无需密码即可查看所有已存储的密钥用途：

```bash
python cli.py list
```

### 查看指定密钥

需要提供密码和密钥用途：

```bash
python cli.py view --purpose "API密钥"
```

系统会提示输入密码。

### 删除密钥

需要提供密码确认删除：

```bash
python cli.py delete --purpose "API密钥"
```

系统会提示输入密码并要求确认删除操作。

## 安全说明

- 所有密钥使用 Fernet (对称加密) 进行加密存储
- 主密码通过 PBKDF2 进行密钥派生 (100,000 次迭代)
- 密钥长度为 24 个字符，包含大小写字母、数字和特殊字符
- 加密后的密钥存储在 `keys.enc` 文件中
- 忘记密码将无法恢复密钥

## 示例

```bash
# 生成一个用于 GitHub API 的密钥
$ python cli.py generate --purpose "GitHub API"
Enter password to encrypt the key: 
Confirm password: 
✓ Key generated successfully!
Purpose: GitHub API
Key (24 characters): aB3$xY9#mK2@pL5^qR8*

# 列出所有密钥用途
$ python cli.py list
Stored key purposes (1):
  - GitHub API

# 查看密钥
$ python cli.py view --purpose "GitHub API"
Enter password: 
✓ Key retrieved successfully!
Purpose: GitHub API
Key: aB3$xY9#mK2@pL5^qR8*

# 删除密钥
$ python cli.py delete --purpose "GitHub API"
Enter password to delete the key: 
Are you sure you want to delete the key 'GitHub API'? (yes/no): yes
✓ Key 'GitHub API' deleted successfully!
```

## 许可证

MIT License
