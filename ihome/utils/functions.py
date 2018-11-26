
import random
import re

import redis

from utils.settings import DATABASES, REDIS


def is_graph(filename):
    res = r'.*\.(jpg|png|bmp|jpeg|emf|ico$)'
    result = re.fullmatch(res, filename)
    if result:
        return True
    else:
        return False


def is_card(card):
    re_card = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)'
    result = re.fullmatch(re_card, card)
    if result:
        return True
    else:
        return False


def is_name(name):
    re_name = r'^[\u4E00-\u9FA5]+$'
    result = re.fullmatch(re_name, name)
    if result:
        return True
    else:
        return False


def image_code():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    image_code = ''
    for _ in range(4):
        image_code += random.choice(s)
    return image_code


def get_mysql_url():
    default_database = DATABASES['default']
    return '{}+{}://{}:{}@{}:{}/{}'.format(default_database['DRIVER'],
                                           default_database['DH'],
                                           default_database['USER'],
                                           default_database['PASSWORD'],
                                           default_database['HOST'],
                                           default_database['PORT'],
                                           default_database['NAME'])


def get_redis_url():
    result = redis.Redis(host=REDIS['HOST'], port=REDIS['PORT'])
    return result