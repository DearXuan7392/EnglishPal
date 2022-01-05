#! /usr/bin/python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

from Login import *
from Article import *
import Yaml

app = Flask(__name__)
app.secret_key = 'lunch.time!'

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def get_random_image(path):
    '''
    返回随机图
    :param path: 图片文件(JPEG格式)，不包含后缀名
    :return:
    '''
    img_path = random.choice(glob.glob(os.path.join(path, '*.jpg')))

    return img_path[img_path.rfind('/static'):]


def get_random_ads():
    '''
    返回随机广告
    :return: 一个广告(包含HTML标签)
    '''
    ads = random.choice(['个性化分析精准提升', '你的专有单词本', '智能捕捉阅读弱点，针对性提高你的阅读水平'])
    return ads + '。 <a href="/signup">试试</a>吧！'


def appears_in_test(word, d):
    '''
    如果字符串里没有指定的单词，则返回逗号加单词
    :param word: 指定单词
    :param d: 字符串
    :return: 逗号加单词
    '''
    if not word in d:
        return ''
    else:
        return ','.join(d[word])


def get_time():
    '''
    获取当前时间
    :return: 当前时间
    '''
    return datetime.now().strftime('%Y%m%d%H%M')  # upper to minutes


def get_flashed_messages_if_any():
    '''
    在用户界面显示黄色提示信息
    :return: 包含HTML标签的提示信息
    '''
    messages = get_flashed_messages()
    s = ''
    for message in messages:
        s += '<div class="alert alert-warning" role="alert">'
        s += f'Congratulations! {message}'
        s += '</div>'
    return s


@app.route("/<username>/reset", methods=['GET', 'POST'])
def user_reset(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回页面内容
    '''
    if request.method == 'GET':
        session['articleID'] = None
        return redirect(url_for('userpage', username=username))
    else:
        return 'Under construction'


@app.route("/mark", methods=['GET', 'POST'])
def mark_word():
    '''
    标记单词
    :return: 重定位到主界面
    '''
    if request.method == 'POST':
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, 1))
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return redirect(url_for('mainpage'))
    else: # 不回应GET请求
        return 'Under construction'


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    '''
    根据GET或POST方法来返回不同的主界面
    :return: 主界面
    '''
    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        # save history
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return render_template('mainpage_post.html', lst=lst, yml=Yaml.yml)

    elif request.method == 'GET':  # when we load a html page
        random_ads = get_random_ads()
        number_of_essays = total_number_of_essays()
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        d_len = len(d)
        lst = sort_in_descending_order(pickle_idea.dict2lst(d))
        return render_template('mainpage_get.html', random_ads=random_ads, number_of_essays=number_of_essays,
                               d_len=d_len, lst=lst, yml=Yaml.yml)


@app.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    '''
    标记单词
    :param username: 用户名
    :return: 重定位到用户界面
    '''
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        # 提交标记的单词
        d = load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
        return redirect(url_for('userpage', username=username))
    else:
        return 'Under construction'


@app.route("/<username>/<word>/unfamiliar", methods=['GET', 'POST'])
def unfamiliar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.unfamiliar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return redirect(url_for('userpage', username=username))


@app.route("/<username>/<word>/familiar", methods=['GET', 'POST'])
def familiar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.familiar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return redirect(url_for('userpage', username=username))


@app.route("/<username>/<word>/del", methods=['GET', 'POST'])
def deleteword(username, word):
    '''
    删除单词
    :param username: 用户名
    :param word: 单词
    :return: 重定位到用户界面
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea2.deleteRecord(user_freq_record, word)
    flash(f'<strong>{word}</strong> is no longer in your word list.')
    return redirect(url_for('userpage', username=username))


@app.route("/<username>", methods=['GET', 'POST'])
def userpage(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回用户界面
    '''
    # 未登录，跳转到未登录界面
    if not session.get('logged_in'):
        return render_template('not_login.html')

    # 用户过期
    user_expiry_date = session.get('expiry_date')
    # if datetime.now().strftime('%Y%m%d') > user_expiry_date:
    #     return render_template('out_time.html')

    # 获取session里的用户名
    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)

    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        return render_template('userpage_post.html',username=username,lst = lst, yml=Yaml.yml)

    elif request.method == 'GET':  # when we load a html page
        d = load_freq_history(user_freq_record)
        lst = pickle_idea2.dict2lst(d)
        lst2 = []
        for t in lst:
            lst2.append((t[0], len(t[1])))
        lst3 = sort_in_descending_order(lst2)
        words = ''
        for x in lst3:
            words += x[0] + ' '
        return render_template('userpage_get.html',
                               username=username,
                               session=session,
                               flashed_messages=get_flashed_messages_if_any(),
                               today_article=get_today_article(user_freq_record, session['articleID']),
                               d_len=len(d),
                               lst3=lst3,
                               yml=Yaml.yml,
                               words=words)


### Sign-up, login, logout ###
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    '''
    注册
    :return: 根据注册是否成功返回不同界面
    '''
    if request.method == 'GET':
        # GET方法直接返回注册页面
        return render_template('signup.html')
    elif request.method == 'POST':
        # POST方法需判断是否注册成功，再根据结果返回不同的内容
        username = request.form['username']
        password = request.form['password']

        available = check_username_availability(username)
        if not available: # 用户名不可用
            flash('用户名 %s 已经被注册。' % (username))
            return render_template('signup.html')
        elif len(password.strip()) < 4: # 密码过短
            return '密码过于简单。'
        else: # 添加账户信息
            add_user(username, password)
            verified = verify_user(username, password)
            if verified:
                # 写入session
                session['logged_in'] = True
                session[username] = username
                session['username'] = username
                session['expiry_date'] = get_expiry_date(username)
                session['articleID'] = None
                return '<p>恭喜，你已成功注册， 你的用户名是 <a href="%s">%s</a>。</p>\
                <p><a href="/%s">开始使用</a> <a href="/">返回首页</a><p/>' % (username, username, username)
            else:
                return '用户名密码验证失败。'


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    登录
    :return: 根据登录是否成功返回不同页面
    '''
    if request.method == 'GET':
        # GET请求
        if not session.get('logged_in'):
            # 未登录，返回登录页面
            return render_template('login.html')
        else:
            # 已登录，提示信息并显示登出按钮
            return '你已登录 <a href="/%s">%s</a>。 登出点击<a href="/logout">这里</a>。' % (
                session['username'], session['username'])
    elif request.method == 'POST':
        # POST方法用于判断登录是否成功
        # check database and verify user
        username = request.form['username']
        password = request.form['password']
        verified = verify_user(username, password)
        if verified:
            # 登录成功，写入session
            session['logged_in'] = True
            session[username] = username
            session['username'] = username
            user_expiry_date = get_expiry_date(username)
            session['expiry_date'] = user_expiry_date
            session['articleID'] = None
            return redirect(url_for('userpage', username=username))
        else:
            return '无法通过验证。'


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    '''
    登出
    :return: 重定位到主界面
    '''
    # 将session标记为登出状态
    session['logged_in'] = False
    return redirect(url_for('mainpage'))


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    '''
    重设密码
    :return: 返回适当的页面
    '''
    # 下列方法用于防止未登录状态下的修改密码
    if not session.get('logged_in'):
        return render_template('login.html')
    username = session['username']
    if username == '':
        return redirect('/login')
    if request.method == 'GET':
        # GET请求返回修改密码页面
        return render_template('reset.html', username=session['username'], state='wait')
    else:
        # POST请求用于提交修改后信息
        old_psd = request.form['old-psd']
        new_psd = request.form['new-psd']
        flag = change_password(username, old_psd, new_psd) # flag表示是否修改成功
        if flag:
            session['logged_in'] = False
            return \
'''
<script>
alert('修改密码成功!!!请重新登录');
window.location.href="/login";
</script>

'''

        else:
            return \
'''
<script>
alert('修改密码失败!!!');
window.location.href="/reset";
</script>

'''


if __name__ == '__main__':
    '''
    运行程序
    '''
    # app.secret_key = os.urandom(16)
    # app.run(debug=False, port='6000')
    app.run(debug=True)
    # app.run(debug=True, port='6000')
    # app.run(host='0.0.0.0', debug=True, port='6000')
    # print(mod5('123'))
