#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author : 蔡楷 / Kyle
import sqlite3


def create_table():
    print("--------------------------------")
    print(" 未检测到数据库文件，正在初始化... ")
    connect = sqlite3.connect("LibSystem.db")
    c = connect.cursor()
    # 新建三个表单 Book, Reader, Borrow 分别存储书本信息、读者信息和借阅信息
    c.execute('''CREATE TABLE Book(
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookName TEXT,
    BookAuthor TEXT,
    BookPublisher TEXT,
    BookPrice FLOAT,
    BookDate TEXT,
    BookType TEXT,
    BookState INTEGER
    );''')
    c.execute('''CREATE TABLE Reader(
    ReaderID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReaderName TEXT,
    ReaderPassword TEXT,
    ReaderCollege TEXT,
    ReaderNumber TEXT
    );''')
    c.execute('''CREATE TABLE Borrow(
    BorrowID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReaderID INTEGER,
    BookID INTEGER,
    BookName TEXT,
    BorrowDate TEXT
    );''')
    # 新建一个对应表单内容的元组并使用 for 循环进行写入
    books = ((1, u"数据结构与算法分析", u"冯舜玺", u"机械工业出版社", 35.00, u"2004-01-01", u"计算机",  5),
             (2, u"流畅的Python", u"安道 / 吴珂", u"人民邮电出版社", 139.00, u"2017-05-15", u"计算机", 10),
             (3, u"你当像鸟飞往你的山", u"任爱红", u"南海出版公司", 59.00, u"2019-10-20", u"教育", 5),
             (4, u"天才基本法", u"长洱", u"江苏凤凰文艺出版社", 78.00, u"2019-07-01", u"成长", 7),
             (5, u"鸟瞰古文明", u"[法] 让-克劳德·戈尔万", u"湖南美术出版社", 128.00, u"2019-10-01", u"历史", 5),
             (6, u"了不起的我", u"陈海贤", u"台海出版社", 69.00, u"2019-10-23", u"心理学", 3),
             (7, u"失败者的春秋", u"刘勃", u"百花文艺出版社", 9.90, u"2019-06-01", u"历史", 8),
             (8, u"牛津高阶英汉双解词典(第四版)", u"李北达", u"商务印书馆", 88.00, u"1997-08-01", u"工具书", 5))
    for r in books:
        c.execute("INSERT INTO Book VALUES (?,?,?,?,?,?,?,?)", r)
    readers = ((1000, u"Admin", u"YWRtaW4=", u"新闻与传播学院", u"2019000000"),
               (1001, u"陈一", u"MTIzNDU2", u"新闻与传播学院", u"2019000001"),
               (1002, u"王二", u"MTIzNDU2", u"计算机学院", u"2019000002"),
               (1003, u"张三", u"MTIzNDU2", u"艺术学院", u"2019000003"),
               (1004, u"李四", u"MTIzNDU2", u"文学院", u"2019000004"),
               (1005, u"周五", u"MTIzNDU2", u"文学院", u"2019000005"),
               (1006, u"黄六", u"MTIzNDU2", u"文学院", u"2019000006"),
               (1007, u"霸天", u"MTIzNDU2", u"体育学院", u"2019000008"))
    for r in readers:
        c.execute("INSERT INTO Reader VALUES (?,?,?,?,?)", r)
    borrows = ((1, 1001, 1, u"数据结构与算法分析", u"2018-01-05"),
               (2, 1001, 2, u"流畅的Python", u"2018-04-07"),
               (3, 1002, 3, u"你当像鸟飞往你的山", u"2018-12-05"),
               (4, 1003, 5, u"鸟瞰古文明", u"2018-12-25"),
               (5, 1004, 4, u"天才基本法", u"2019-03-02"),
               (6, 1004, 2, u"流畅的Python", u"2019-05-07"),
               (7, 1003, 7, u"失败者的春秋", u"2019-11-07"),
               (8, 1006, 8, u"牛津高阶英汉双解词典(第四版)", u"2020-02-13"),
               (9, 1007, 2, u"流畅的Python", u"2020-03-14"),
               (10, 1008, 8, u"牛津高阶英汉双解词典(第四版)", u"2020-06-18"))
    for r in borrows:
        c.execute("INSERT INTO Borrow VALUES (?,?,?,?,?)", r)
    connect.commit()
    print("--------------------------------")
    print("        数据库初始化成功！       ")
    print("--------------------------------")
    # 断开数据库连接
    connect.close()


if __name__ == '__main__':
    create_table()
