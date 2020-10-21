#_*_coding:utf-8_*_

import pymysql
import xlwt
from datetime import datetime

def get_data(sql):

    # 创建数据库连接.
    conn = pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='tpadmin',port=3306,charset='utf8')
    # 创建游标
    cur = conn.cursor()
    # 执行查询，
    cur.execute(sql)
    # 由于查询语句仅会返回受影响的记录条数并不会返回数据库中实际的值，所以此处需要fetchall()来获取所有内容。
    result = cur.fetchall()
    #关闭游标
    cur.close()
    #关闭数据库连接
    conn.close
    # 返给结果给函数调用者。
    return result

    
def write_data_to_excel(name,sql):

    # 将sql作为参数传递调用get_data并将结果赋值给result,(result为一个嵌套元组)
    result = get_data(sql)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2016-8-9
    today_date = datetime.date(today)
    # 遍历result中的没个元素。
    for i in range(len(result)):
        #对result的每个子元素作遍历，
        for j in range(len(result[i])):
            #将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i,j,result[i][j])
    # 以传递的name+当前日期作为excel名称保存。
    wbk.save(name+str(today_date)+'.xls')

# 如果该文件不是被import,则执行下面代码。
if __name__ == '__main__':
    #定义一个字典，key为对应的数据类型也用作excel命名，value为查询语句
    db_dict = {'category':'select * from category'}
    # 遍历字典每个元素的key和value。
    for k,v in db_dict.items():
        # 用字典的每个key和value调用write_data_to_excel函数。
        write_data_to_excel(k,v)
