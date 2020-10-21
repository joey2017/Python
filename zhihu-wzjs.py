import requests
from requests.exceptions import RequestException
import json
import pymysql

url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=%E7%BD%91%E7%AB%99%E5%BB%BA%E8%AE%BE&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'
#print(req.paging)#获取结果直接返回的就是json串
#print(json.loads(req.text))#json转字典
#print(req.json())#获取结果就是字典,只有返回的是json串的话才能用req.json()
#print(type(req.json()))

def get_api_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
            'x-requested-with': 'fetch',
            'referer': 'https://www.zhihu.com/search?type=content&q=%E7%BD%91%E7%AB%99%E5%BB%BA%E8%AE%BE',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-ab-param': 'zr_intervene=0;top_test_4_liguangyi=1;se_col_boost=0;zw_sameq_sorce=999;li_sp_mqbk=0;zr_expslotpaid=1;li_car_meta=0;tp_zrec=0;pf_creator_card=1;pf_profile2_tab=0;zr_rec_answer_cp=open;li_yxzl_new_style_a=1;li_edu_page=old;li_catalog_card=1;li_paid_answer_exp=0;zr_sim3=0;tp_clubhyb=0;qap_question_author=0;tp_topic_style=0;tp_dingyue_video=0;qap_question_visitor= 0;zr_slotpaidexp=1;li_svip_tab_search=1;se_ffzx_jushen1=0;tsp_hotlist_ui=1;li_panswer_topic=0;li_video_section=0;pf_noti_entry_num=0;li_pl_xj=0;ls_video_commercial=0;li_vip_verti_search=0;tp_contents=2;pf_adjust=0',
            'x-ab-pb': 'CkK0CuwKYAvXCycKrAubC9wLAAxMC0IL5Ao+Cw8LOAslCpYLhgsSC+ALSwvPC5oLtQu5C/MLcgtSC9cKAQv0C1gL4QsSIQABAAAGAAIAAAAAAAAAAAUAAQAAAAsAAAAAAAEBAAAAAA==',
            'x-api-version': '3.0.91',
            'x-app-za': 'OS=Web',
            'x-zse-86': '1.0_a_202AU8oRtfgBFBB7tqgrrqkXtp2TN8YLxBS6U0c0Of',
            'x-zse-83': '3_2.0'
        }
        cookies = {'cookie': '_zap=81017a37-adbd-4af6-b90d-dc1386dadc50; d_c0="AFBQ0mOtXxGPTo6rPyhJJsfHV4D5RgBcJ6A=|1591258571"; _ga=GA1.2.2146732438.1591258575; _xsrf=31e6316c-1387-4868-af35-dbfb47425146; capsion_ticket="2|1:0|10:1603264071|14:capsion_ticket|44:OTFmOGExZGY5MjI5NDFiOGJjNTU3YzQ4OTgwMTIyMjA=|391e5e77a41e68906025f6e1def1c9ac29ae552939b8f3a97697994978864854"; SESSIONID=gWMSmV2ofdk8cY6cJ4cdi22sWHaREg1beIWWt2jG8p6; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1603211569,1603243396,1603264072,1603264081; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1603264269; KLBRSID=d1f07ca9b929274b65d830a00cbd719a|1603268332|1603264069'}
        response = requests.get(url = url,cookies = cookies, headers = headers)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        print(response.json())
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_api_data(json):
    """
    接口返回数据处理
    """
    is_last_page = json.paging.is_end
    next_page = json.paging.next
    results = json.data
    data=[]
    for i in range(results):
        if results.type == 'search_result':
            temp={}
            temp.title=results[i].highlight.title
            temp.description=results[i].highlight.description
            temp.vote_up_count=results[i].object.vote_up_count
            temp.comment_count=results[i].object.comment_count
            data.append(temp)

    print(data)

def connect_mysql():
    """
    连接数据库
    """
    # connect = pymysql.connect(      #连接数据库
    #     user = "root",
    #     password = "root",
    #     host = "127.0.0.1",
    #     db = "MYSQL",
    #     port = 3306,
    #     charset = ("utf8"),    #注意编码一定要设置，否则gbk你懂的
    #     use_unicode=True,
    #     )
    db = pymysql.connect('127.0.0.1','root','','zhihu')
    con = db.cursor()    #设置游标
    # con.execute('SET NAMES UTF8')
    con.execute("drop database douban")       #以下7行表示删除原有的数据库和其中的表，新建数据库和表
    con.execute("create database douban")
    con.execute("use douban")                 #使用douban这个数据库
    con.execute("drop table if exists t_doubantop")
    sql = '''create table t_doubantop(num BIGINT,name VARCHAR(40) NOT NULL,charactor VARCHAR(40),remark VARCHAR(40),score VARCHAR(20))'''
    con.execute(sql)    #sql中的字符表示创建一个表 对应的信息有   num  name  charactor  remark  score

def close_mysql(db):
    """
    关闭数据库连接
    """
    db.close()

def execute_mysql():
    """
    执行mysql增删改操作
    """
    db = pymysql.connect("localhost","testuser","test123","TESTDB" )
 
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
            LAST_NAME, AGE, SEX, INCOME)
            VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

    # SQL 插入语句
    # sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
    #    LAST_NAME, AGE, SEX, INCOME) \
    #    VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
    #    ('Mac', 'Mohan', 20, 'M', 2000)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

def query_mysql():
    """
    执行mysql查询操作
    """
    # 打开数据库连接
    db = pymysql.connect("localhost","testuser","test123","TESTDB" )
 
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
 
    # SQL 查询语句
    sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > %s" % (1000)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            fname = row[0]
            lname = row[1]
            age = row[2]
            sex = row[3]
            income = row[4]
            # 打印结果
            print ("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
                    (fname, lname, age, sex, income ))
    except:
        print ("Error: unable to fetch data")
 
    # 关闭数据库连接
    db.close()
response = get_api_data(url)
#print(response)
#json_data = json.loads(response)
#print(json_data)
exit
#parse_api_data(json_data)    
#print(get_api_data(url))
    