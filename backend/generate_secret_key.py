"""
生成新的 Django SECRET_KEY
运行此脚本生成一个新的安全密钥用于生产环境
"""

import secrets
import string

def generate_secret_key(length=50):
    """生成一个随机的 SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("\n" + "="*60)
    print("🔑 新的 SECRET_KEY 已生成:")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("📝 请将此密钥添加到:")
    print("   1. backend/.env 文件中: SECRET_KEY=<上面的密钥>")
    print("   2. 或服务器环境变量中")
    print("="*60)
    print("\n⚠️  警告: 请妥善保管此密钥，不要提交到 Git！\n")
