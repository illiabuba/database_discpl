import psycopg2
from psycopg2 import errors
from model import * 
from view import *



cashier_v = ['data1','cash_registrater_number','type_of_discount']
discount_v = ['type_of_discount','size_of_discount']
film_v = ['tilm_title','duration']
viewer_v = ['data','film_title']

def UserRequest():

    user_message=input('Enter command --> ')
    if(user_message=='4'):
    	try:
            if(user_message=='4'):
                Search()
                sys.exit() 
    	except psycopg2.Error as err:
    		print(err.pgcode)
    		print(f'WARNING:Error {err}') 		
    table=input('Enter table name --> ')
    if((table =='film')or(table=='viewer')):
        print('Film and Viewer connection 1:N , changes in the "film_title" column , touch both tables -->')
        print(f'Film column --> {film_v}')
        print(f'Viewer column --> {viewer_v}')
        try:
            if(user_message=='3'):
                Update(table)
            elif(user_message=='1'):
                Add(table)
            elif(user_message=='2'):
                Delete(table)
            elif(user_message=='5'):
                RandRow(table)
            elif(user_message != '5'or'4'or'3'or'2'or'1'):
                print("Error: wrong command, it has to be from 1 to 5") 
                sys.exit() 
        except psycopg2.Error as err:
            print(err.pgcode)
            print(f'WARNING:Error {err}')
    elif((table=='cashier')or(table=='discount')):
        print('Cashier and Discount connection 1:N , changes in the "type_of_discount" column , touch both tables -->')
        print(f'Cashier column --> {cashier_v}')
        print(f'Discount column --> {discount_v}')
        try:
            if(user_message=='3'):
                Update(table)
            elif(user_message=="1"):
                Add(table)
            elif(user_message=='2'):
                Delete(table)
            elif(user_message=='5'):
                RandRow(table)
            elif(user_message != '5'or'4'or'3'or'2'or'1'):
                print("Error: wrong command, it has to be from 1 to 5")  
                sys.exit() 
        except psycopg2.Error as err:
            print(err.pgcode)
            print(f'WARNING:Error {err}')
    else:
        print('Error: wrong table name') 

Menu()  
UserRequest()

