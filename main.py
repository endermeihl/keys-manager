#!/usr/bin/env python3
"""
Entry point for Key Manager - CLI with argparse for Streamlit integration
"""

import argparse
import sys
import io

# 强制使用 UTF-8 编码输出，解决 Windows 下 subprocess 捕获乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from keys_manager import KeyManager


def main():
    parser = argparse.ArgumentParser(
        description='密钥管理器 - 安全生成和管理加密密钥'
    )
    parser.add_argument('--action',
                        choices=['generate', 'list', 'view', 'delete'],
                        help='操作类型: generate(生成), list(列表), view(查看), delete(删除)')
    parser.add_argument('--purpose', help='密钥用途/标签')
    parser.add_argument('--password', help='加密/解密密码')
    parser.add_argument('--prefix', default='sk-', help='密钥前缀 (默认: sk-)')
    parser.add_argument('--storage', default='keys.enc', help='存储文件路径 (默认: keys.enc)')

    args = parser.parse_args()

    # 初始化
    km = KeyManager(storage_file=args.storage)

    # 如果没有指定 action，显示帮助
    if not args.action:
        print("=" * 50)
        print("[密钥管理器]")
        print("=" * 50)
        print("\n可用操作 (--action):")
        print("  generate  - 生成新密钥 (需要 --purpose, --password, 可选 --prefix)")
        print("  list      - 列出所有密钥用途")
        print("  view      - 查看密钥 (需要 --purpose, --password)")
        print("  delete    - 删除密钥 (需要 --purpose, --password)")
        print("\n当前存储的密钥:")
        purposes = km.list_purposes()
        if purposes:
            for p in purposes:
                print(f"  - {p}")
        else:
            print("  (暂无)")
        return

    try:
        # --- 列出所有密钥 ---
        if args.action == 'list':
            purposes = km.list_purposes()
            print("=" * 50)
            print("[已存储的密钥列表]")
            print("=" * 50)
            if not purposes:
                print("暂无存储的密钥")
            else:
                print(f"共 {len(purposes)} 个密钥:")
                for i, p in enumerate(purposes, 1):
                    print(f"  {i}. {p}")

        # --- 生成新密钥 ---
        elif args.action == 'generate':
            if not args.purpose:
                print("[错误] 生成密钥需要指定 --purpose")
                sys.exit(1)
            if not args.password:
                print("[错误] 生成密钥需要指定 --password")
                sys.exit(1)

            generated_key = km.generate_key(args.purpose, args.password, prefix=args.prefix)
            print("=" * 50)
            print("[密钥生成成功]")
            print("=" * 50)
            print(f"用途: {args.purpose}")
            print(f"前缀: {args.prefix}")
            print(f"密钥: {generated_key}")
            print("\n[注意] 请妥善保存此密钥，之后需要密码才能再次查看。")

        # --- 查看密钥 ---
        elif args.action == 'view':
            if not args.purpose:
                print("[错误] 查看密钥需要指定 --purpose")
                sys.exit(1)
            if not args.password:
                print("[错误] 查看密钥需要指定 --password")
                sys.exit(1)

            key = km.get_key(args.purpose, args.password)
            print("=" * 50)
            print("[密钥查询结果]")
            print("=" * 50)
            print(f"用途: {args.purpose}")
            print(f"密钥: {key}")

        # --- 删除密钥 ---
        elif args.action == 'delete':
            if not args.purpose:
                print("[错误] 删除密钥需要指定 --purpose")
                sys.exit(1)
            if not args.password:
                print("[错误] 删除密钥需要指定 --password")
                sys.exit(1)

            km.delete_key(args.purpose, args.password)
            print("=" * 50)
            print("[删除成功]")
            print("=" * 50)
            print(f"密钥 '{args.purpose}' 已被删除")

    except ValueError as e:
        print(f"[错误] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[系统错误] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
