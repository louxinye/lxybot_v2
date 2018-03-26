# -*- coding: utf-8 -*-
import pymysql


# 添加、删除、更新操作
def action(sql):
	db = pymysql.connect("localhost", "root", "123456", "osu")
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		db.commit()
		success = 1
	except:
		db.rollback()
		success = 0
		print('error!')
	db.close()
	return success


# 查询操作,会返回结果
def select(sql):
	db = pymysql.connect("localhost", "root", "123456", "osu")
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
	except ValueError:
		results = -1
	db.close()
	return results