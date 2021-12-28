import psycopg2
from psycopg2 import errors
import time
import sys

def RandRow(table_name):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()
	n =input('Input how much random you need ')
	if(table_name=='cashier'):
		curso_r.execute(f"WITH table_m AS(INSERT INTO cashier SELECT chr(trunc(65+random()*500)::int), chr(trunc(65 + random()*500)::int),chr(trunc(65 + random()*500)::int) FROM generate_series(1,{n}) RETURNING type_of_discount)INSERT INTO discount SELECT type_of_discount FROM table_m")
	elif(table_name=='discount'):
		curso_r.execute(f"WITH table_m AS(INSERT INTO discount SELECT chr(trunc(65+random()*500)::int), chr(trunc(65 + random()*500)::int) FROM generate_series(1,{n}) RETURNING type_of_discount)INSERT INTO cashier SELECT type_of_discount FROM table_m")
	elif(table_name=='film'):
		curso_r.execute(f"WITH table_m AS(INSERT INTO film SELECT chr(trunc(65+random()*500)::int), chr(trunc(65 + random()*500)::int) FROM generate_series(1,{n}) RETURNING film_title)INSERT INTO viewer SELECT film_title FROM table_m")
	elif(table_name=='viewer'):
		curso_r.execute(f"WITH table_m AS(INSERT INTO viewer SELECT chr(trunc(65+random()*500)::int), chr(trunc(65 + random()*500)::int) FROM generate_series(1,{n}) RETURNING film_title)INSERT INTO film SELECT film_title FROM table_m")
	curso_r.close()
	con.close()

def SoloUpd(name1,column):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	old_name=input('Enter old name --> ')
	new_name = input('Enter new name --> ')
	try:
		db_command = "UPDATE " + name1 + " SET " + column + " =  '" + new_name + "' WHERE " + column + " = '"+ old_name + "'"
		curso_r.execute(db_command)
	except psycopg2.Error as err:
		print(err.pgcode)
		print(f'WARNING:Error {err}')
	curso_r.close()
	con.close()



def DoubleUpd(name1,name2,column):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	old_value=input('Enter old name --> ')
	new_value = input('Enter new name --> ')
	try:
		db_command = "WITH " + name1 + " AS (UPDATE " + name1 + " SET " + column + " = '" + new_value + "' WHERE " + column + " = '"+ old_value + "')" + " UPDATE " + name2 + " SET " + column + " = '" + new_value + "' WHERE " + column + " = '"+ old_value + "'"
	except psycopg2.Error as err:
		print(err.pgcode)
		print(f'WARNING:Error {err}')
	curso_r.execute(db_command)
	curso_r.close()
	con.close()



def Update(table_name):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	column_name=input('Enter column name --> ')
	ColumnInformation(table_name,column_name)
	if(((table_name=='cashier')or(table_name=='discount'))and(column_name=='type_of_discount')):
		try:
			DoubleUpd('cashier','discount','type_of_discount')
		except psycopg2.Error as err:
			print(err.pgcode)
			print(f'WARNING:Error {err}')
	elif(((table_name=='film')or(table_name=='viewer'))and(column_name=='film_title')):
		try:
			DoubleUpd('film','viewer','film_title')
		except psycopg2.Error as err:
			print(err.pgcode)
			print(f'WARNING:Error {err}')
	else:
		try:
			SoloUpd(table_name,column_name)
		except psycopg2.Error as err:
			print(err.pgcode)
			print(f'WARNING:Error {err}')
	curso_r.close()
	con.close()


def Delete(table_name):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	column=input('Enter column --> ')
	ColumnInformation(table_name,column)
	row=input('Enter row info --> ')
	if(table_name=='discount'):
		#ColumnInformation('cashier','type_of_discount')
		db_command = "WITH dad AS(DELETE FROM discount WHERE " + column + " = '"+ row + "')DELETE FROM cashier WHERE type_of_discount = '"+ row + "'"
		curso_r.execute(db_command)
	elif(table_name=='cashier'):
		#ColumnInformation('discount','type_of_discount')
		db_command = "WITH ada AS(DELETE FROM cashier WHERE " + column + " = '"+ row + "')DELETE FROM discount WHERE type_of_discount = '"+ row + "'"
		curso_r.execute(db_command)
	elif(table_name=='film'):
		#ColumnInformation('viewer','film_title')
		db_command = "WITH asd AS(DELETE FROM film WHERE " + column + " = '"+ row + "')DELETE FROM viewer WHERE film_title = '"+ row + "'"
		curso_r.execute(db_command)
	else:
		#ColumnInformation('film','film_title')
		db_command = "WITH dsa AS(DELETE FROM viewer WHERE " + column + " = '"+ row + "')DELETE FROM film WHERE film_title = '"+ row + "'"
		curso_r.execute(db_command)
	curso_r.close()
	con.close()


def Add(table_name):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	count=0
	mass=[]
	NULL_value = '[null]'
	if(table_name=='cashier'):
		print("Enter 3 value -->")
		while(count<3):
			value=input()
			mass.append(value)
			count+=1
		table_name2 = 'discount'
		db_command = "WITH " + table_name + " AS " + "( INSERT INTO " + table_name + " VALUES ('" + mass[0] + "','" + mass[1] + "','" + mass[2] + "'))"+ "INSERT INTO " + table_name2 + " VALUES ('" + mass[2] + "')"
		curso_r.execute(db_command)
	elif(table_name == 'discount'):
		print("Enter 2 value -->")
		while(count<2):
			value=input()
			mass.append(value)
			count+=1
		table_name2 = 'cashier'
		db_command = "WITH " + table_name + " AS " + "( INSERT INTO " + table_name + " VALUES ('" + mass[0] + "','" + mass[1] + "'))"+ "INSERT INTO " + table_name2 + " VALUES ('" + NULL_value + "','" + NULL_value + "','" + mass[0] + "')"
		curso_r.execute(db_command)
	elif(table_name == 'film'): 
		print("Enter 2 value -->")
		while(count<2):
			value=input()
			mass.append(value)
			count+=1
		table_name2 = 'viewer'
		db_command = "WITH " + table_name + " AS " + "( INSERT INTO " + table_name + " VALUES ('" + mass[0] + "','" + mass[1] + "'))"+ "INSERT INTO " + table_name2 + " VALUES ('" + NULL_value + "','" + mass[0] + "')"
		curso_r.execute(db_command)  
	else:
		print("Enter 2 value -->")
		while(count<2):
			key=input()
			mass.append(key)
			count+=1
		table_name2='film'
		db_command = "WITH " + table_name + " AS " + "( INSERT INTO " + table_name + " VALUES ('" + mass[0] + "','" + mass[1] + "'))"+ "INSERT INTO " + table_name2 + " VALUES ('" + mass[1] + "')"
		curso_r.execute(db_command)
	curso_r.close()
	con.close()



def Search():
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()

	n = input("Input quantity of attributes to search by >>> ")
	n = int(n)
	column=[]
	for h in range(0,n):
		column.append(str(input(f"Input name of the attribute number {h+1} to search by >>> ")))
	print(column)
	tables = []
	types = []
	if n == 2:
		curso_names_str = f"SELECT table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE information_schema.columns.column_name LIKE '{column[0]}' INTERSECT ALL SELECT table_name FROM information_schema.columns WHERE information_schema.columns.column_name LIKE '{column[1]}'"
	else:
		curso_names_str = "SELECT table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE information_schema.columns.column_name LIKE '{}'".format(column[0])
	print("\ncol_names_str:", curso_names_str)
	curso_r.execute(curso_names_str)
	curso_names = (curso_r.fetchall())
	for tup in curso_names:
		tables += [tup[0]]
	if 'film/cashier' in tables:
		tables.remove('film/cashier')
		print(tables)
	for s in range(0,len(column)):
		for k in range(0,len(tables)):
			curso_r.execute(f"SELECT data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='{tables[k]}' AND column_name ='{column[s]}'")
			type=(curso_r.fetchall())
			for j in type:
				types+=[j[0]]
	print(types)
	if n == 1:
		if len(tables) == 1:
			if types[0] == 'character varying':
				i_char = input(f"Input string for {column[0]} to search by >>> ")
				search_time = time.time()
				curso_r.execute(f"SELECT * FROM {tables[0]} WHERE {column[0]} LIKE '{i_char}'")
				print(curso_r.fetchall())
				print("Time for search is: %s sec" %(time.time() - search_time))
		elif len(tables) == 2:
			if types[0] == 'character varying':
				i_char = input(f"Input string for {column[0]} to search by >>> ")
				search_time = time.time()
				curso_r.execute(f"SELECT {column[0]} FROM {tables[0]} WHERE {column[0]} LIKE '{i_char}' UNION ALL SELECT {column[0]} FROM {tables[1]} WHERE {column[0]} LIKE '{i_char}'")
				print(curso_r.fetchall())
				print("Time for search is: %s sec" %(time.time() - search_time))
           
	elif n == 2:
		if len(tables) == 1:
			if types[0] == 'character varying' and types[1] == 'character varying':
				i_char = input(f"Input string for {column[0]} to search by >>> ")
				o_char = input(f"Input string for {column[1]} to search by >>> ")
				search_time = time.time()
				curso_r.execute(f"SELECT * FROM {tables[0]} WHERE {column[0]} LIKE '{i_char}' AND {column[1]} LIKE '{o_char}' ")
				print(curso_r.fetchall())
				print("Time for search is: %s sec" %(time.time() - search_time))
	curso_r.close()
	con.close()            


def ColumnInformation(table_name,column_name):
	con = psycopg2.connect(
  	  database="MyData", 
  	  user="postgres", 
  	  password="", 
      host="localhost", 
  	  port="5432"
	)
	con.set_session(autocommit=True)
	curso_r=con.cursor()
	curso_r.execute(f"SELECT {column_name} FROM {table_name}")
	print(curso_r.fetchall())
	curso_r.close()
	con.close()