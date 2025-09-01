import mysql.connector
import datetime
from itertools import chain
from tkinter import messagebox

class Database:      
    def __init__(self, host, user, password):
        self.con = mysql.connector.connect(    
            user=user,
            password=password,
        )
        self.cur = self.con.cursor()      
        self.host=host
        self.user=user
        self.password=password
        self.cur.execute("USE WORKSHOP")

################# first_table functions ################################################################################################
    



    def insertion(self,envoy,company,product_name,amount,measure,cost_per_one,The_pay_id,state,date,discount):

        calenedar_date = datetime.datetime.strptime(date,"%m/%d/%Y")
        calenedar_date_formatted=calenedar_date.strftime("%m/%d/%Y")

        self.cur.execute("START TRANSACTION")
        try:
            if amount.startswith("+"):
                cost_for_all = cost_per_one * float(amount)
                self.cur.execute(f"INSERT INTO DETAILS VALUES (NOT NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (envoy, company, product_name, amount, measure, cost_per_one, cost_for_all,The_pay_id,state,calenedar_date_formatted)) 
                self.cur.execute(f"INSERT INTO CATEGORY_CHANGES (category_foreign,quantity_income,quantity_income_cost,measure,non_auto_date_third,quantity_outcome,quantity_outcome_cost) VALUES (%s,%s,%s,%s,%s,0,0)",
                            (product_name,amount,cost_for_all,measure,calenedar_date_formatted) )  
                if discount!=0 and discount.is_integer():
                    self.cur.execute(f"INSERT INTO DISCOUNT VALUES(%s,%s,%s)",
                                    (discount,"+",The_pay_id)) 
                self.con.commit()
            elif amount.startswith("-"):               
                cost_for_all = cost_per_one * float(amount.strip('-'))
                self.cur.execute(f"INSERT INTO DETAILS VALUES (NOT NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (envoy, company, product_name, amount, measure, cost_per_one, cost_for_all,The_pay_id,state,calenedar_date_formatted))
                amount=amount.strip("-")  
                self.cur.execute(f"INSERT INTO CATEGORY_CHANGES (category_foreign,quantity_outcome,quantity_outcome_cost,measure,non_auto_date_third,quantity_income,quantity_income_cost) VALUES (%s,%s,%s,%s,%s,0,0)",
                     
                            (product_name,amount,cost_for_all,measure,calenedar_date_formatted) )
                if discount!=0 and discount.is_integer():
                    self.cur.execute(f"INSERT INTO DISCOUNT VALUES(%s,%s,%s)",
                                    (discount,"-",The_pay_id))  
                self.con.commit()   
        except  Exception  as error :
            self.con.rollback()
            messagebox.showerror("Database Error",f"{error}")  


    def update_third_table_AND_first_table(self,envoy,company,product_name,amount,measure,cost_per_one,The_pay_id,state,date,id):
        calenedar_date = datetime.datetime.strptime(date,"%m/%d/%Y")
        calenedar_date_formatted=calenedar_date.strftime("%m/%d/%Y") 

        self.cur.execute("START TRANSACTION")        #mean any querys under it will be one session and querys will not execute physically until all querys is executed without errors ( recommended to use it with error_handling(try.expect.finally))  
        try:
            if amount.startswith("+"):
                    the_whole_price=float(amount) * cost_per_one

                    self.cur.execute(f"UPDATE DETAILS SET envoy=%s,company=%s,product_name=%s,amount=%s,measure=%s,cost_per_one=%s,cost_for_all=%s,transaction_id=%s,state=%s,time=%s where id=%s " ,                                      # |
                            (envoy,company,product_name,amount,measure,cost_per_one,the_whole_price,The_pay_id,state,date,id))                                                                                                      # |-----> ALL THIS QUERYS  ARE IN ONE SESSION 
                    self.cur.execute(f"UPDATE CATEGORY_CHANGES SET category_foreign=%s,quantity_income=%s,quantity_income_cost=%s,measure=%s,non_auto_date_third=%s,quantity_outcome=0,quantity_outcome_cost=0 WHERE id=%s ",    # |----->
                            (product_name,amount,the_whole_price,measure,calenedar_date_formatted,id) )  #AND category_foreign IN (SELECT category FROM CATEGORY)                                                             # |
                    self.con.commit()        #foreign key mean (child of) referer to primary key (if primary key not exists the child will not exists)   
            
            elif amount.startswith("-"):
                    the_whole_price=float(amount.strip('-')) * cost_per_one

                    self.cur.execute(f"UPDATE DETAILS SET envoy=%s,company=%s,product_name=%s,amount=%s,measure=%s,cost_per_one=%s,cost_for_all=%s,transaction_id=%s,state=%s,time=%s where id=%s " ,
                            (envoy,company,product_name,amount,measure,cost_per_one,the_whole_price,The_pay_id,state,date,id))
                    amount=amount.strip("-")  
                    self.cur.execute(f"UPDATE CATEGORY_CHANGES SET category_foreign=%s,quantity_outcome=%s,quantity_outcome_cost=%s,measure=%s,non_auto_date_third=%s,quantity_income=0,quantity_income_cost=0 WHERE id=%s ",
                            (product_name,amount,the_whole_price,measure,calenedar_date_formatted,id) )#AND category_foreign IN (SELECT category FROM CATEGORY) 
                    self.con.commit()
        except Exception as error:
                self.con.rollback()
                messagebox.showerror("Database Error",f"{error}")


    def fetced(self):
        self.cur.execute("SELECT * FROM DETAILS ORDER BY Transaction_id,id,time") 
        rows=self.cur.fetchall()
        return rows   
    
    def remove(self,id):
        self.cur.execute("START TRANSACTION")
        try:
            self.cur.execute(f"DELETE FROM DETAILS WHERE id=%s",(id,))   #comma  because sql expects parameters as a tuple only
            self.cur.execute(f"DELETE FROM CATEGORY_CHANGES WHERE id=%s",(id,))  
            self.con.commit()
        except Exception as error:
            self.con.rollback()
            messagebox.showerror("Database Error",f"{error}")   

    def transactions(self,Transaction_id):
        self.cur.execute(f"SELECT * FROM DETAILS WHERE Transaction_id=%s ORDER BY Transaction_id,id,time",(Transaction_id,)) 
        rows=self.cur.fetchall()
        return rows   

    def searching_id(self,id):
        self.cur.execute("SELECT * FROM DETAILS WHERE id=%s ",
                         (id,))
        rows=self.cur.fetchall()
        return rows
    
    def searching_transaction_id(self,pay_id):
        self.cur.execute("SELECT * FROM DETAILS WHERE transaction_id=%s",
                         (pay_id))
        rows=self.cur.fetchall()
        return rows

    def searching_name(self,name,START_DATE,END_DATE,category):
        main_query=""
        param=[]

        if name!="":
           main_query+="SELECT * FROM DETAILS WHERE (envoy=%s or company=%s) "
           param.append(name)
           param.append(name)
        if category!="":
            if name=="":
                main_query+="SELECT * FROM DETAILS WHERE product_name=%s "
                param.append(category)

            elif name!="":
                main_query+="AND product_name=%s "
                param.append(category)    


        if START_DATE!="" and END_DATE!="":
            
            #_____________________________________________
            start_date = datetime.datetime.strptime(START_DATE, "%m/%d/%Y")   # Convert the start and end dates to datetime objects
            end_date = datetime.datetime.strptime(END_DATE, "%m/%d/%Y")
    
            # end_date += datetime.timedelta(days=1)           # Add one day to the start date     ======= if you want to make operation with  dates  you must first convert it to datetime objects
                   # ^^^^^^  ADD   Subtract --->  -=    etc                                                                   ^^^^^^^^^^^^    ^^^^^^^^        ^^^^^^^^^^^^^^         ^^^^^^^^^^^^
            # ____________________________________________
            start_date_formatted = start_date.strftime("%m/%d/%Y")      # Convert back to strings in the required format
            end_date_formatted = end_date.strftime("%m/%d/%Y")

            if name=="" and category=="":
                main_query+="SELECT * FROM DETAILS WHERE (time BETWEEN %s AND %s) "

            if name!="" or category!="":
                main_query+="AND (time BETWEEN %s AND %s) "
            param.append(start_date_formatted)
            param.append(end_date_formatted)
   
        main_query+="ORDER BY time,Transaction_id,id"
        self.cur.execute(main_query,param)
        rows=self.cur.fetchall()
        return rows
 


    def search_sorting_fetch(self,option):
        self.cur.execute(f"SELECT * FROM DETAILS WHERE {option}!='' ORDER BY time,Transaction_id,id")
        rows=self.cur.fetchall()
        return rows

    def order_by_time(self):
        self.cur.execute("SELECT * FROM DETAILS ORDER BY time ASC")
        rows=self.cur.fetchall()
        return rows
     



    def combobox_values(self):
        self.cur.execute("SELECT DISTINCT envoy,company FROM DETAILS")    
        rows=self.cur.fetchall()
        value_list=list()
        for row in rows:
            if row[0]=='' :
                 value_list.append(row[1])
            elif row[1]=='' :
                 value_list.append(row[0])
        return value_list
    
    def comboxbox_measure(self):
        self.cur.execute("SELECT DISTINCT measure FROM CATEGORY")
        rows=self.cur.fetchall()
        return rows
        
    def combobox_values_categorys(self):
        self.cur.execute("SELECT DISTINCT product_name FROM DETAILS")    
        rows=self.cur.fetchall()
        values_tuple=tuple(chain.from_iterable(rows))
        return values_tuple


    def last_transaction_id(self):
        self.cur.execute("SELECT IFNULL(MAX(Transaction_id),0) FROM DETAILS")
        row=self.cur.fetchone()
        return row[0]
    
    def sum_category_cost(self,transction_id):
        self.cur.execute(f"SELECT IFNULL(SUM(cost_for_all),0) FROM DETAILS WHERE Transaction_id=%s",
                         (transction_id,))
        row=self.cur.fetchone()
        return row[0]
    
    def select_measure(self,product_name):
        self.cur.execute(f"SELECT measure FROM CATEGORY WHERE category=%s",
                         (product_name,))
        row=self.cur.fetchone()
        return row[0]

    def stock_check(self,product_name):
        self.cur.execute("START TRANSACTION")
        self.cur.execute(F"""SELECT
                                CASE
                                   WHEN IFNULL(CATEGORY.quantity,0)+IFNULL(SUM(CATEGORY_CHANGES.quantity_income),0)>=IFNULL(SUM(CATEGORY_CHANGES.quantity_outcome),0) THEN 0
                                   ELSE 1
                                END AS RESULT
                             FROM CATEGORY_CHANGES
                             LEFT JOIN CATEGORY ON CATEGORY.category = CATEGORY_CHANGES.category_foreign 
                             WHERE CATEGORY_CHANGES.category_foreign=%s 
                         """,(product_name,))
        result=self.cur.fetchall() #amogus
        return result[0]
    
    def category_combobox(self):
        self.cur.execute(f"SELECT category FROM CATEGORY")
        rows=self.cur.fetchall()
        values_tuple=tuple(chain.from_iterable(rows))
        return values_tuple
    
    def category_suggestion(self,input_char):
        self.cur.execute(F"SELECT category FROM CATEGORY WHERE category LIKE '%{input_char}%'")
        rows=self.cur.fetchall()
        values_tuple=tuple(chain.from_iterable(rows))
        return values_tuple

##################money_transaction_first_table_functions###################################################################################################
    def insertion_sec_1(self,client):
        self.cur.execute(f"INSERT INTO MONEYDETAILS_CUSTOMERS VALUES (%s)",
                         (client,))
        self.con.commit()

    def fetced_sec_1(self):
        self.cur.execute("SELECT * FROM MONEYDETAILS_CUSTOMERS ") 
        rows=self.cur.fetchall()
        return rows

    def update_sec_1(self,client_new,client_old):
        self.cur.execute(f"UPDATE MONEYDETAILS_CUSTOMERS SET customer=%s WHERE customer=%s",
                         (client_new,client_old))
        self.con.commit()

    def remove_sec_1(self,client):
        self.cur.execute(f"DELETE FROM MONEYDETAILS_CUSTOMERS WHERE customer=%s",(client,))  
        self.con.commit()

    def searching_money_transcation_id(self,client,transation_id):
        self.cur.execute(f"SELECT * FROM MONEYDETAILS WHERE client=%s AND transation_id=%s ORDER BY the_paid_amount",(client,transation_id))
        rows=self.cur.fetchall()
        return rows

#--------------- money_transaction_second_table-------------------
    def insertion_sec_2(self,client,the_whole_amount,the_sum_paid_amount,the_single_paid_amount,the_returned_amount,stat,non_auto_date,transation_id):
        calenedar_date = datetime.datetime.strptime(non_auto_date,"%m/%d/%Y")
        calenedar_date_formatted=calenedar_date.strftime("%m/%d/%Y")
        
        self.cur.execute(f"INSERT INTO MONEYDETAILS VALUES (NOT NULL,%s,%s,%s,%s,%s,%s,%s,%s) ",
                 (client,the_whole_amount,the_sum_paid_amount,the_single_paid_amount,the_returned_amount,stat,calenedar_date_formatted,transation_id))
        self.con.commit()

    def fetced_sum_sec_2(self,column2,transation_id):
        self.cur.execute(f"SELECT SUM(the_single_paid_amount) FROM MONEYDETAILS WHERE client=%s AND transation_id=%s ORDER BY transation_id,the_paid_amount",(column2,transation_id)) 
        sum_value=self.cur.fetchall() #  [(value_1,),(value_2,),(value_3,),(value_4,),(value_5,)]   [0][0],[1][0],etc
        sum_value_tuple=list(chain.from_iterable(sum_value))
        if sum_value_tuple[0] == None:
            sum_value_tuple.pop()
            sum_value_tuple.append(0)
        return sum_value_tuple

    def fetced_sec_2(self,column2):
        self.cur.execute(f"SELECT * FROM MONEYDETAILS WHERE client=%s ORDER BY transation_id,the_paid_amount",(column2,)) 
        rows=self.cur.fetchall()        
        return rows

    def update_details_state_from_money_details(self,envoy,transaction_id):
        self.cur.execute("START TRANSACTION")
        self.cur.execute(F"UPDATE DETAILS SET state='تم'  WHERE envoy=%s AND transaction_id=%s AND state='قيد' ",
                         (envoy,transaction_id))
        self.con.commit()                 

    def remove_sec_2(self,id):
        self.cur.execute(f"DELETE FROM MONEYDETAILS WHERE id=%s",(id,))  
        self.con.commit()


    
#################category_table_functions##################################################################################################

    def insertion_third_table(self,category,quantity,measure_3,cost,non_auto_date_third):
        calenedar_date = datetime.datetime.strptime(non_auto_date_third,"%m/%d/%Y")
        calenedar_date_formatted=calenedar_date.strftime("%m/%d/%Y")
        the_whole_cost=(quantity)*(cost)
        try:
            self.cur.execute(f"INSERT INTO CATEGORY VALUES (%s,%s,%s,%s,%s,%s)",
                    (category,quantity,measure_3,cost,the_whole_cost,calenedar_date_formatted))
            self.con.commit()  
        except Exception:
            self.con.rollback()
            messagebox.showwarning("خطأ في الإدخال","الصنف موجود بالفعل")    

    def fetced_third_table(self):
        self.cur.execute("SELECT * FROM CATEGORY")
        rows=self.cur.fetchall()
        return rows


    def remove_third(self,category):
        try:
            self.cur.execute(f"DELETE FROM CATEGORY WHERE category=%s",(category,))  
            self.con.commit()
        except Exception:
            self.con.rollback()
            messagebox.showwarning("عملية مرفوضة","توجد عمليات لهذا الصنف")        

    def update_category_in_all_tables(self,category_new,quantity,measure_3,cost,date,category_old):
        
        self.cur.execute("START TRANSACTION")
        try:
            the_whole_cost=(quantity)*(cost)
            self.cur.execute(f"SET  SESSION foreign_key_checks=OFF")
            self.cur.execute(f"UPDATE CATEGORY SET category=%s,quantity=%s,measure=%s,cost=%s,the_whole_cost=%s,non_auto_date_third=%s WHERE category=%s",
                            (category_new,quantity,measure_3,cost,the_whole_cost,date,category_old))      
            
            self.cur.execute(f"UPDATE DETAILS SET product_name=%s WHERE product_name=%s",
                            (category_new,category_old))
            
            self.cur.execute(f"UPDATE CATEGORY_CHANGES SET category_foreign=%s WHERE category_foreign=%s",
                            (category_new,category_old))
            self.cur.execute(f"SET  SESSION foreign_key_checks=ON ")
            self.con.commit()
        except:
            self.con.rollback()
            messagebox.showerror("parent_error","check categorys parent/child or their id")

    def suming(self,category_foreign):
        self.cur.execute(f"SELECT quantity_income,quantity_income_cost,quantity_outcome,quantity_outcome_cost  FROM CATEGORY_CHANGES WHERE category_foreign=%s",(category_foreign,))
        rows=self.cur.fetchall() 
    
     # it will return tuple of all values of what we selected [(value,), (value,), (value,), (value,)]
        quantity_income= sum(float(row[0]) for row in rows)
        quantity_income_cost= sum(float(row[1]) for row in rows)
        quantity_outcome= sum(float(row[2]) for row in rows)
        quantity_outcome_cost= sum(float(row[3]) for row in rows)
        
        return quantity_income,quantity_income_cost,quantity_outcome,quantity_outcome_cost

    def search_category(self,column3):
        self.cur.execute(f"SELECT * FROM CATEGORY_CHANGES WHERE category_foreign=%s ORDER BY non_auto_date_third,id",(column3,))
        rows=self.cur.fetchall()
        return rows                                

    
    def ordering(self,column4):
        self.cur.execute(f"SELECT * FROM CATEGORY_CHANGES WHERE category_foreign=%s ORDER BY quantity_income,quantity_income_cost",(column4,))
        rows=self.cur.fetchall()
        return rows

#-------------------payroll_table_AND_started_money_table---------------------
    

    def insertation_fifth_table(self,table,v1,v2,v3):
        try:
            match table:



        

                case "PAYROLL":
                    self.cur.execute(f"INSERT INTO PAYROLL VALUES(%s,%s)", 
                                (v1,v2))
                case "MAIN_MONEY":
                    self.cur.execute(f"INSERT INTO MAIN_MONEY VALUES(%s)", 
                                (v1,))
                case "CUSTOMER_DETAILS":
                    self.cur.execute(f"INSERT INTO CUSTOMER_DETAILS VALUES(%s,NOT NULL)",
                                (v1,)) 
                case "COMPANY_DETAILS":
                    self.cur.execute(f"INSERT INTO COMPANY_DETAILS VALUES(%s,NOT NULL)",
                                (v1,))     
                case "OTHER_MONEY":
                    self.cur.execute(f"INSERT INTO OTHER_MONEY VALUES(NOT NULL,%s,%s)",
                        (v1,v2))   
                case "RETURNED":
                    self.cur.execute(f"INSERT INTO RETURNED VALUES(NOT NULL,%s,%s,%s)",
                        (v1,v2,v3))
                case "DISCOUNT":
                    self.cur.execute(f"INSERT INTO DISCOUNT VALUES(%s,%s,%s)",
                        (v1,v2,v3))    

            self.con.commit()
        except Exception as error:
            self.con.rollback()
            messagebox.showerror("Database Error",f"{error}")   

    def updateing_fifth_table(self,table,v1,v2,v3,v4):   
        try:
            match table:

                case "PAYROLL":
                    self.cur.execute(f"UPDATE PAYROLL SET worker=%s,payroll=%s WHERE worker=%s", # payroll_table
                                (v1,v2,v3))   
                
                case "MAIN_MONEY":
                    self.cur.execute(f"UPDATE MAIN_MONEY SET amount=%s", #started_money_table
                                (v1,))   
                
                case "CUSTOMER_DETAILS":    

                    self.cur.execute("START TRANSACTION")

                    self.cur.execute("SET SESSION foreign_key_checks=OFF")    # 0 ==   1 == ON
                    self.cur.execute(f"UPDATE CUSTOMER_DETAILS SET customer=%s WHERE customer_id=%s ",
                                    (v1,v2))
                    self.cur.execute(f"UPDATE DETAILS SET envoy=%s WHERE envoy=%s",
                                    (v1,v3))
                    self.cur.execute(f"UPDATE MONEYDETAILS_CUSTOMERS SET customer=%s WHERE customer=%s",
                                    (v1,v3))
                    self.cur.execute(f"UPDATE MONEYDETAILS SET client=%s WHERE client=%s",
                                    (v1,v3))
                    self.cur.execute("SET SESSION foreign_key_checks=ON")

                case "COMPANY_DETAILS":    

                    self.cur.execute("START TRANSACTION")

                    self.cur.execute("SET SESSION foreign_key_checks=OFF")    # 0 ==   1 == ON
                    self.cur.execute(f"UPDATE COMPANY_DETAILS SET companies=%s WHERE company_id=%s",
                                    (v1,v2))
                    self.cur.execute(f"UPDATE DETAILS SET company=%s WHERE company=%s",
                                    (v1,v3))
                    self.cur.execute("SET SESSION foreign_key_checks=ON")
                
                case "OTHER_MONEY":
                    self.cur.execute(f"UPDATE OTHER_MONEY SET name=%s,amount=%s WHERE id=%s",
                         (v1,v2,v3))

                case "RETURNED":
                    self.cur.execute(F"UPDATE RETURNED SET name=%s,quantitiy=%s,cost=%s WHERE id=%s",
                         (v1,v2,v3,v4))    
                case "DISCOUNT":
                    self.cur.execute(f"UPDATE DISCOUNT SET discount=%s,discount_way=%s,transaction_id_II=%s WHERE transaction_id_II=%s",
                         (v1,v2,v3,v4))

            self.con.commit()     
        except Exception as error:
            self.con.rollback()    
            messagebox.showerror("Database Error",f"{error}") 

    def fetced_fifth_table(self,table):
        
        self.cur.execute(f"SELECT * FROM {table}")   
        rows=self.cur.fetchall()

        if table in ["PAYROLL","MAIN_MONEY","RETURNED","OTHER_MONEY","DISCOUNT"]:
            return rows
        elif table in ["CUSTOMER_DETAILS","COMPANY_DETAILS"]:
            return rows[1:]  
        
    def remove_fifth_table(self,table,worker,id):
     
        if table=="PAYROLL":
            self.cur.execute(f"DELETE FROM PAYROLL WHERE worker=%s", 
                            (worker,))
        elif table== "MAIN_MONEY":
            self.cur.execute(f"DELETE FROM MAIN_MONEY") 

        elif table=="CUSTOMER_DETAILS":
            self.cur.execute(f"DELETE FROM CUSTOMER_DETAILS WHERE customer_id=%s",
                         (id,))    
        elif table=="COMPANY_DETAILS": 
            self.cur.execute(f"DELETE FROM COMPANY_DETAILS WHERE company_id=%s",
                         (id,))
        elif table=="OTHER_MONEY":
            self.cur.execute(f"DELETE FROM OTHER_MONEY WHERE id=%s",
                         (id))   
        elif table=="RETURNED":
            self.cur.execute(f"DELETE FROM RETURNED WHERE id=%s",
                         (id,))    
        elif table=="DISCOUNT":
            self.cur.execute(f"DELETE FROM DISCOUNT WHERE transaction_id_II=%s",
                         (id,))    
        self.con.commit()
    #global_function
    def combobox_values_first_from_forth_customer_company(self,table):
            if table=="CUSTOMER_DETAILS":
                self.cur.execute("SELECT * FROM CUSTOMER_DETAILS ORDER BY customer ASC")  #WHERE (customer_id>1)
            elif table=="COMPANY_DETAILS":
                self.cur.execute("SELECT * FROM COMPANY_DETAILS ORDER BY companies ASC")
            rows=self.cur.fetchall()
            values_list=list()
            for row in rows:                           # first id is conserved for blank input !!!!!!
                values_list.append(row[0])
            return values_list

#---------------DISCOUNT_TABLE-----------------



    
#------------------statistic_window----------------
    
    #----------------category_suming_function----------------
    def sum_category_storage_cost(self):
            self.cur.execute("SELECT IFNULL(SUM(the_whole_cost),0) FROM CATEGORY")
            category_sum=self.cur.fetchone()
            return category_sum[0]
    
    def sum_category_entered_cost(self):
            self.cur.execute("SELECT IFNULL(SUM(quantity_income_cost),0) FROM CATEGORY_CHANGES")
            category_sum=self.cur.fetchone()
            return category_sum[0]
    
    def sum_category_out_cost(self):
            self.cur.execute("SELECT IFNULL(SUM(quantity_outcome_cost),0) FROM CATEGORY_CHANGES")
            category_sum=self.cur.fetchone()
            return category_sum[0]
    
    def sum_category_current_cost(self):
        return (self.sum_category_storage_cost())+(self.sum_category_entered_cost())-(self.sum_category_out_cost())
    
#-----------money_details_debts----------------
    def main_money_debts_sum(self):
        self.cur.execute("""SELECT IFNULL(SUM(SEPERATED_whole_price),0) 
                        FROM (
                        SELECT MAX(the_whole_amount) AS SEPERATED_whole_price 
                        FROM MONEYDETAILS
                        GROUP BY transation_id,client )
                        AS SubQueryAlias
                        """)
        whole_debt_sum=self.cur.fetchone() 
        self.cur.execute("SELECT IFNULL(SUM(the_single_paid_amount),0) FROM MONEYDETAILS")
        single_debt_sum=self.cur.fetchone()
        remain_money=float(whole_debt_sum[0]-single_debt_sum[0])

        return whole_debt_sum[0],single_debt_sum[0],remain_money

    def dynamic_main_money_sum(self,client):
        self.cur.execute(f"""SELECT SUM(SEPERATED_whole_price) 
                FROM (
                SELECT MAX(the_whole_amount) AS SEPERATED_whole_price 
                FROM MONEYDETAILS
                WHERE client=%s
                GROUP BY transation_id )
                AS SubQueryAlias
                """,(client,))
        dynamic_whole_debt_sum=self.cur.fetchone()
        self.cur.execute(f"SELECT SUM(the_single_paid_amount) FROM MONEYDETAILS WHERE client=%s",(client,))
        dynamic_single_debt_sum=self.cur.fetchone()
        if dynamic_whole_debt_sum[0]!=None and  dynamic_single_debt_sum[0]!=None:
            dynamic_remain_money=float(dynamic_whole_debt_sum[0]-dynamic_single_debt_sum[0])
            return dynamic_whole_debt_sum[0],dynamic_single_debt_sum[0],dynamic_remain_money
        else:
            return 0,0,0

         
    def payroll_money_sum(self):
        self.cur.execute("SELECT SUM(payroll) FROM PAYROLL")
        sum_row=self.cur.fetchone()
        return sum_row[0]
    
    def main_money_sum(self):
        self.cur.execute("SELECT SUM(amount) FROM MAIN_MONEY")
        sum_row=self.cur.fetchone()
        return sum_row[0] 
    
    def other_money_sum(self):
        self.cur.execute("SELECT SUM(amount) FROM OTHER_MONEY")
        sum_row=self.cur.fetchone()
        return sum_row[0] 
    
    def sum_of_all(self):
        self.cur.execute("""SELECT SUM(all_records) 
                            FROM(
                            SELECT payroll AS all_records FROM PAYROLL
                            UNION ALL
                            SELECT amount AS all_records FROM MAIN_MONEY
                            UNION ALL 
                            SELECT amount AS all_records FROM OTHER_MONEY)
                            AS SUBQUARY""")
        sum_row=self.cur.fetchone()
        return sum_row[0] 

    def id_error_dedection(self):
        self.cur.execute("SELECT SUM(DETAILS.id) FROM DETAILS INNER JOIN CATEGORY_CHANGES ON DETAILS.id=CATEGORY_CHANGES.id AND DETAILS.product_name=CATEGORY_CHANGES.category_foreign ")
        joined_rows=self.cur.fetchone()
        self.cur.execute("SELECT SUM(id) FROM DETAILS")
        all_rows_details=self.cur.fetchone()
        self.cur.execute("SELECT SUM(id) FROM CATEGORY_CHANGES")
        all_rows_category=self.cur.fetchone()
        if joined_rows==all_rows_details and joined_rows==all_rows_category:
            return 0
        else:
            return 1

#payroll_function_error_handlling
    def payroll_name_handle(self):
        self.cur.execute("SELECT worker FROM PAYROLL")
        rows=self.cur.fetchall()
        values_tuple=tuple(chain.from_iterable(rows))
        return values_tuple
    
    def start_money_count(self):
        self.cur.execute("SELECT COUNT(amount) FROM MAIN_MONEY")
        rows=self.cur.fetchone()
        return rows
