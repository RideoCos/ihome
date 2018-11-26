
import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 上传static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# media路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')

# upload上传路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')

DATABASES = {
    'default': {
        'DRIVER': 'mysql',
        'DH': 'pymysql',
        'NAME': 'ihome',
        'USER': 'root',
        'PASSWORD': 'RideoCos921',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

REDIS = {
    'HOST': 'localhost',
    'PORT': 6379
}