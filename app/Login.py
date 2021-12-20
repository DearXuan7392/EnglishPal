import hashlib
from datetime import datetime

from UseSqlite import InsertQuery, RecordQuery

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def verify_user(username, password):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    password = mod5(username + password)
    rq.instructions_with_parameters("SELECT * FROM user WHERE name=? AND password=?", (username, password))
    rq.do_with_parameters()
    result = rq.get_results()
    return result != []


def add_user(username, password):
    start_date = datetime.now().strftime('%Y%m%d')
    expiry_date = '20211230'
    password = mod5(username + password)
    rq = InsertQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("INSERT INTO user Values ('%s', '%s', '%s', '%s')" % (username, password, start_date, expiry_date))
    rq.do()


def check_username_availability(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("SELECT * FROM user WHERE name='%s'" % (username))
    rq.do()
    result = rq.get_results()
    return result == []


def change_password(username, old_psd, new_psd):
    if not verify_user(username, old_psd):  # 旧密码错误
        return False
    password = mod5(username + new_psd)
    rq = InsertQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("UPDATE user SET password = '%s' WHERE name = '%s'" % (password, username))
    rq.do()
    return True


def get_expiry_date(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("SELECT expiry_date FROM user WHERE name='%s'" % (username))
    rq.do()
    result = rq.get_results()
    if len(result) > 0:
        return result[0]['expiry_date']
    else:
        return '20191024'


def mod5(str):
    return str
    h = hashlib.md5(str.encode(encoding='utf-8'))
    return h.hexdigest()