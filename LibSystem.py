#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author : 蔡楷 / Kyle
import Packages.DBInit as DBInit
import Packages.prettytable as pretty_table
import sqlite3
import base64
import time
from os import path


# 数据库初始化函数
# 若不存在数据库文件，则执行初始化程序
def check_db():
    global connect
    global c
    if not path.exists("LibSystem.db"):
        DBInit.create_table()
        connect = sqlite3.connect("LibSystem.db")
        c = connect.cursor()
    else:
        connect = sqlite3.connect("LibSystem.db")
        c = connect.cursor()
        print("--------------------------------")
        print("         数据库载入成功！        ")
        print("--------------------------------")
    return connect, c


# 登录函数
def login():
    global c
    print("---------图书馆管理系统---------")
    while True:
        print("1. 登录\n2. 注册\n3. 查询用户列表\n4. 退出")
        print("--------------------------------")
        choice = input("请输入序号：")
        if choice == '1':
            user_id = input("请输入您的 ID：")
            # fetchone 获得一个元组，一直执行可获取下一个结果，直至查不到时返回 None
            data = c.execute("select ReaderPassword from Reader where ReaderID='%s'" % user_id).fetchone()
            if data:
                # 通过 .encode() 将其由 Str 变成 Byte（Base64 只能加解密 Byte）
                # 将用户输入的密码进行 Base64 加密，获得：b'base64编码内容'
                # 使用 .decode("utf-8") 去掉b和单引号，以便与数据库中的密码进行对比
                user_password = input("请输入您的密码：").encode()
                user_password = base64.b64encode(user_password).decode("utf-8")
                if user_password == data[0]:
                    print("--------------------------------")
                    print("            登录成功！          ")
                else:
                    print("--------------------------------")
                    print("            密码错误！           ")
                    print("--------------------------------")
                    time.sleep(0.5)
                    continue
            else:
                print("--------------------------------")
                print("            ID 错误！           ")
                print("--------------------------------")
                time.sleep(0.5)
                continue
            return user_id
        elif choice == "2":
            register()
        elif choice == '3':
            print("--------------------------------")
            print("用户列表：")
            c.execute("SELECT ReaderID, ReaderName, ReaderCollege, ReaderNumber from Reader")
            # 使用 PrettyTable 获取数据，并更改表头后进行打印
            list_table = pretty_table.from_db_cursor(c)
            list_table.field_names = ["ID", "姓名", "学院", "学号"]
            print(list_table)
            print("| 管理员默认密码：admin；用户默认密码：123456 |")
            print("+------+--------+----------------+------------+")
            continue
        elif choice == '4':
            quite()
        else:
            print("--------------------------------")
            print("            输入错误！          ")
            print("--------------------------------")
            time.sleep(0.5)


# 用户注册函数
def register():
    global connect
    global c
    print("--------------------------------")
    reader_name = input("请输入您的姓名：")
    reader_password = input("请输入您的密码：").encode()
    reader_password = base64.b64encode(reader_password).decode("utf-8")
    reader_college = input("请输入您的学院：")
    reader_number = input("请输入您的学号：")
    print("--------------------------------")
    c.execute("INSERT INTO Reader (ReaderName, ReaderPassword, ReaderCollege, ReaderNumber) VALUES ('%s','%s','%s',"
              "'%s')" % (reader_name, reader_password, reader_college, reader_number))
    connect.commit()
    print("         用户创建成功！          ")
    print("--------------------------------")
    time.sleep(0.5)


# 用户选单界面
# 使用 while 与 break 实现输入错误程序不退出的功能
def user_ui(user_id):
    global connect
    global c
    name = c.execute("SELECT ReaderName from Reader where ReaderID='%s'" % user_id).fetchone()
    print("--------------------------------")
    print("欢迎您，{}！".format(name[0]))
    print("1. 图书借阅\n2. 图书归还\n3. 修改密码\n4. 退出")
    print("--------------------------------")
    choice = input("请输入序号：")
    while True:
        if choice == "1":
            c.execute("select * from Book")
            book_table = pretty_table.from_db_cursor(c)
            book_table.field_names = ["ID", "书名", "作者", "出版社", "价格", "出版日期", "分类", "馆藏数"]
            print(book_table)
            book_id = input("请输入您要借阅的图书 ID（输入0返回上一级）：")
            if book_id == "0":
                break
            else:
                # 检测输入的图书 ID 是否正确
                check_id = c.execute("select BookID from Book where BookID='%s'" % book_id).fetchone()
                if not check_id:
                    print("--------------------------------")
                    print("         您输入的ID有误！        ")
                    time.sleep(0.5)
                    break
                else:
                    pass
                check_borrow = c.execute(
                    "select BookID from Borrow where ReaderID='%s' AND BookID='%s'" % (user_id, book_id)).fetchone()
                if check_borrow:
                    # 禁止多次借阅相同书籍
                    print("--------------------------------")
                    print("       抱歉，您已借阅此书！       ")
                    time.sleep(0.5)
                    break
                else:
                    pass
            book_state = c.execute("select BookState from Book where BookID='%s'" % book_id).fetchone()
            book_state = book_state[0]
            if book_state == 0:
                # 馆藏数为 0 时禁止借阅
                print("--------------------------------")
                print("         抱歉，暂无此书！        ")
                time.sleep(0.5)
                break
            else:
                book_state = book_state - 1
            book_name = c.execute("select BookName from Book where BookID='%s'" % book_id).fetchone()
            book_name = book_name[0]
            # 使用 time 获得系统当前日期作为借阅日期，格式为：年-月-日
            borrow_date = time.strftime("%Y-%m-%d", time.localtime())
            c.execute("INSERT INTO Borrow (ReaderID, BookID, BookName, BorrowDate) VALUES ('%s','%s','%s','%s')" % (
                user_id, book_id, book_name, borrow_date))
            c.execute("UPDATE Book SET BookState='%s' where BookID='%s'" % (book_state, book_id))
            connect.commit()
            print("--------------------------------")
            print("          成功借阅该书。         ")
            time.sleep(0.5)
            break
        elif choice == "2":
            # 非管理员还书需要密码
            admin = False
            book_return(user_id, admin)
            break
        elif choice == "3":
            password_change(user_id)
            break
        elif choice == "4":
            quite()
        else:
            print("--------------------------------")
            print("       输入有误，请重新输入！    ")
            time.sleep(0.5)
            break


# 管理员选单界面
def admin_ui(user_id):
    global connect
    global c
    print("--------------------------------")
    print("欢迎您，管理员！")
    print("1. 读者信息\n2. 图书信息\n3. 借阅信息\n4. 修改密码\n5. 退出")
    print("--------------------------------")
    choice = input("请输入序号：")
    while True:
        if choice == "1":
            c.execute("SELECT ReaderID, ReaderName, ReaderCollege, ReaderNumber from Reader")
            reader_table = pretty_table.from_db_cursor(c)
            reader_table.field_names = ["ID", "姓名", "学院", "学号"]
            print(reader_table)
            select = input("请输入读者 ID 删除用户并归还所有借阅的书（输入0返回上一级）：")
            if select == "0":
                break
            elif select == "1000":
                # 禁止删除管理员账号
                print("--------------------------------")
                print("       不能删除管理员账户！      ")
                time.sleep(0.5)
                break
            else:
                pass
            user_delete(select)
            break
        elif choice == "2":
            c.execute("select * from Book")
            book_table = pretty_table.from_db_cursor(c)
            book_table.field_names = ["ID", "书名", "作者", "出版社", "价格", "出版日期", "分类", "馆藏数"]
            print(book_table)
            print("1. 删除图书\n2. 添加图书\n3. 返回上一级")
            print("--------------------------------")
            sub_choice = input("请输入序号：")
            if sub_choice == "1":
                delete_book()
                break
            elif sub_choice == "2":
                add_book()
                break
            elif sub_choice == "3":
                break
            else:
                print("--------------------------------")
                print("            输入有误！          ")
                time.sleep(0.5)
                break
        elif choice == "3":
            c.execute("SELECT ReaderID, BookID, BookName, BorrowDate from Borrow")
            borrow_table = pretty_table.from_db_cursor(c)
            borrow_table.field_names = ["读者ID", "图书ID", "书名", "借阅时间"]
            print(borrow_table)
            user_id = input("请输入要归还图书的读者 ID（输入0返回上一级）：")
            if user_id == "0":
                break
            else:
                pass
            # 管理员替读者还书时不需要密码
            admin = True
            book_return(user_id, admin)
        elif choice == "4":
            password_change(user_id)
            break
        elif choice == "5":
            quite()
        else:
            print("--------------------------------")
            print("      输入有误，请重新输入！     ")
            time.sleep(0.5)
            break


# 密码更改函数
def password_change(user_id):
    print("--------------------------------")
    user_password = input("请输入原密码：").encode()
    user_password = base64.b64encode(user_password).decode("utf-8")
    password = c.execute("SELECT ReaderPassword from Reader where ReaderID='%s'" % user_id).fetchone()
    if user_password == password[0]:
        user_password = input("请输入新密码：").encode()
        user_password = base64.b64encode(user_password).decode("utf-8")
        c.execute("UPDATE Reader SET ReaderPassword='%s' where ReaderID='%s'" % (user_password, user_id))
        connect.commit()
        print("--------------------------------")
        print("   密码已成功修改，请重新登录！   ")
        quite()
    else:
        print("--------------------------------")
        print("      原密码错误，密码未更改！    ")
        time.sleep(0.5)


# 图书归还函数
def book_return(user_id, admin):
    global connect
    global c
    c.execute("SELECT BookID, BookName, BorrowDate from Borrow where ReaderID='%s'" % user_id)
    borrow_table = pretty_table.from_db_cursor(c)
    borrow_table.field_names = ["ID", "书名", "借阅时间"]
    check_borrow = c.execute("SELECT BookID, BookName, BorrowDate from Borrow where ReaderID='%s'" % user_id).fetchone()
    if check_borrow:
        password = c.execute("SELECT ReaderPassword from Reader where ReaderID='%s'" % user_id).fetchone()
        print(borrow_table)
        book_id = input("请输入要归还的图书 ID（输入0返回上一级）：")
        if book_id == "0":
            return
        else:
            pass
        # 判断用户是否为管理员，若不是则要求输入密码，反之跳过。
        if admin is False:
            user_password = input("请输入密码：").encode()
            user_password = base64.b64encode(user_password).decode("utf-8")
        else:
            user_password = False
        book_state = c.execute("SELECT BookState from Book where BookID='%s'" % book_id).fetchone()
        book_state = book_state[0] + 1
        if user_password == password[0] or user_password is False:
            c.execute("DELETE from Borrow where BookID='%s' AND ReaderID='%s'" % (book_id, user_id))
            c.execute("UPDATE Book SET BookState='%s' where BookID='%s'" % (book_state, book_id))
            connect.commit()
            print("--------------------------------")
            print("           已归还图书。          ")
            time.sleep(0.5)
        else:
            print("--------------------------------")
            print("      密码错误，图书未归还！     ")
            time.sleep(0.5)
    else:
        print("--------------------------------")
        print("        暂无已借阅的书籍。       ")
        time.sleep(0.5)


# 图书删除函数
def delete_book():
    global connect
    global c
    book_id = input("请输入图书 ID：")
    # 删除 Borrow 和 Book 里相应的行
    c.execute("DELETE from Borrow where BookID='%s'" % book_id)
    c.execute("DELETE from Book where BookID='%s'" % book_id)
    connect.commit()
    print("--------------------------------")
    print("           已删除此书。          ")
    time.sleep(0.5)


# 图书添加函数
def add_book():
    global connect
    global c
    print("--------------------------------")
    book_name = input("请输入书本名称（输入0取消添加书本）：")
    if book_name == "0":
        return
    else:
        pass
    book_author = input("请输入作者：")
    book_publisher = input("请输入出版社：")
    book_price = input("请输入单价（精确到一位小数）：")
    book_date = input("请输入出版日期（如2020-06-24）：")
    book_type = input("请输入书本类型：")
    book_state = input("请输入数量：")
    print("--------------------------------")
    c.execute(
        "INSERT INTO Book (BookName, BookAuthor, BookPublisher, BookPrice, BookDate, BookType, BookState) VALUES ("
        "'%s','%s','%s','%s','%s','%s','%s')" % (
            book_name, book_author, book_publisher, book_price, book_date, book_type, book_state))
    connect.commit()
    print("           已添加此书。          ")
    time.sleep(0.5)


# 用户删除函数
def user_delete(user_id):
    global connect
    global c
    admin_password = c.execute("SELECT ReaderPassword from Reader where ReaderID='1000'").fetchone()
    print("--------------------------------")
    password = input("请输入管理员密码：").encode()
    password = base64.b64encode(password).decode("utf-8")
    if password == admin_password[0]:
        book_id = c.execute("SELECT BookID from Borrow where ReaderID='%s'" % user_id).fetchall()
        # fetchall 返回多个元组，因而需要使用 for 循环遍历每一个元组
        for i in book_id:
            book_state = c.execute("SELECT BookState from Book where BookID='%s'" % i[0]).fetchone()
            book_state = book_state[0] + 1
            c.execute("DELETE from Borrow where BookID='%s' AND ReaderID='%s'" % (i[0], user_id))
            c.execute("UPDATE Book SET BookState='%s' where BookID='%s'" % (book_state, i[0]))
        c.execute("DELETE from Reader where ReaderID='%s'" % user_id)
        connect.commit()
        print("--------------------------------")
        print("           用户已删除！          ")
        time.sleep(0.5)
    else:
        print("--------------------------------")
        print("         管理员密码错误！        ")
        time.sleep(0.5)


# 退出程序函数
def quite():
    global connect
    # 断开数据库连接
    connect.close()
    print("--------------------------------")
    print("       感谢您的使用，再见！      ")
    print("--------------------------------")
    exit()


# 主程序
# 使用 while 与 break 配合实现输入出错后将用户带回选单界面
if __name__ == '__main__':
    connect, c = check_db()
    person = login()
    while True:
        if person == "1000":
            admin_ui(person)
        else:
            user_ui(person)
