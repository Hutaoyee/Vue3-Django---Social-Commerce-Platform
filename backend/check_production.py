"""
Django 生产环境配置检查脚本
运行此脚本检查生产环境配置是否安全
"""

import os
import sys
from pathlib import Path

def check_settings():
    """检查 Django 设置"""
    issues = []
    warnings = []
    
    # 导入设置
    sys.path.insert(0, str(Path(__file__).parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    import django
    django.setup()
    
    from django.conf import settings
    
    print("🔍 检查 Django 生产环境配置...\n")
    
    # 1. 检查 DEBUG
    if settings.DEBUG:
        issues.append("❌ DEBUG = True (必须设置为 False)")
    else:
        print("✅ DEBUG = False")
    
    # 2. 检查 SECRET_KEY
    if 'django-insecure' in settings.SECRET_KEY:
        issues.append("❌ SECRET_KEY 使用默认值 (必须更改)")
    else:
        print("✅ SECRET_KEY 已修改")
    
    # 3. 检查 ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == []:
        issues.append("❌ ALLOWED_HOSTS 为空 (必须配置)")
    else:
        print(f"✅ ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    
    # 4. 检查数据库密码
    db_password = settings.DATABASES['default'].get('PASSWORD', '')
    if not db_password or db_password == 'afmysql123321':
        warnings.append("⚠️  数据库密码可能不安全")
    else:
        print("✅ 数据库密码已配置")
    
    # 5. 检查 CORS
    if getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False):
        warnings.append("⚠️  CORS_ALLOW_ALL_ORIGINS = True (生产环境应指定具体域名)")
    else:
        print("✅ CORS 配置正确")
    
    # 6. 检查静态文件
    if not settings.STATIC_ROOT:
        warnings.append("⚠️  STATIC_ROOT 未配置")
    else:
        print(f"✅ STATIC_ROOT = {settings.STATIC_ROOT}")
    
    # 7. 检查安全设置
    security_settings = {
        'SECURE_SSL_REDIRECT': False,
        'SESSION_COOKIE_SECURE': False,
        'CSRF_COOKIE_SECURE': False,
        'SECURE_BROWSER_XSS_FILTER': True,
        'SECURE_CONTENT_TYPE_NOSNIFF': True,
        'X_FRAME_OPTIONS': 'DENY',
    }
    
    for setting, expected in security_settings.items():
        value = getattr(settings, setting, None)
        if value != expected and setting.startswith('SECURE_'):
            warnings.append(f"⚠️  {setting} 未启用 (HTTPS 环境建议启用)")
    
    # 输出结果
    print("\n" + "="*50)
    if issues:
        print("🚨 严重问题:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("✅ 所有检查通过!")
    
    print("="*50)
    
    return len(issues) == 0

if __name__ == '__main__':
    try:
        success = check_settings()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        sys.exit(1)
