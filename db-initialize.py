import mysql.connector

class Database:      
    def __init__(self,host, user, password):
        con = mysql.connector.connect(    
        host=host,
        user=user,
        password=password
        )
        cur = con.cursor()      

        cur.execute("CREATE DATABASE IF NOT EXISTS WORKSHOP")
        con.commit()
        cur.execute("USE WORKSHOP")





        sql_quary7="""
        CREATE TABLE  CUSTOMER_DETAILS(
        customer VARCHAR(255) ,     
        customer_id INT NOT NULL AUTO_INCREMENT UNIQUE,
        PRIMARY KEY(customer)
        )"""
        cur.execute(sql_quary7)
        con.commit() 
       
        sql_quary8="""
        CREATE TABLE COMPANY_DETAILS(
        companies varchar(255),
        company_id INT NOT NULL AUTO_INCREMENT UNIQUE,
        PRIMARY KEY(companies)  
        )"""
        cur.execute(sql_quary8)
        con.commit() 

        sql_quary1= """
        CREATE TABLE IF NOT EXISTS DETAILS(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        envoy VARCHAR(255) ,
        company VARCHAR(255)  ,
        product_name VARCHAR(255),
        amount  VARCHAR(255),  
        measure VARCHAR(255),
        cost_per_one FLOAT,
        cost_for_all FLOAT,
        transaction_id INT,
        state VARCHAR(255),  
        time  VARCHAR(255),  
        FOREIGN KEY (envoy) REFERENCES CUSTOMER_DETAILS(customer),
        FOREIGN KEY (company) REFERENCES COMPANY_DETAILS(companies)
        )
        """
        cur.execute(sql_quary1)
        con.commit()


#trigger-operations

        sql_quary3="""
        CREATE TABLE IF NOT EXISTS MONEYDETAILS_CUSTOMERS(
        customer VARCHAR(255) Primary Key
        )
         """
        cur.execute(sql_quary3)
        con.commit() 


        sql_quary2=""" 
        CREATE TABLE IF NOT EXISTS MONEYDETAILS(
        id INT Primary Key,
        client VARCHAR(255) ,
        the_whole_amount INT,
        the_paid_amount INT,
        the_single_paid_amount INT,
        the_returned_amount INT DEFAULT '0' ,
        stat VARCHAR(255),
        non_auto_date VARCHAR(255),
        transation_id INT,
        FOREIGN KEY (client) REFERENCES MONEYDETAILS_CUSTOMERS(customer)
        ) 
         """
        cur.execute(sql_quary2) 
        con.commit()         





        sql_quary4="""
        CREATE TABLE IF NOT EXISTS CATEGORY(
        category VARCHAR(255) Primary Key,
        quantity FLOAT,
        measure VARCHAR(255),
        cost FLOAT,
        the_whole_cost FLOAT,
        non_auto_date_third VARCHAR(255)
        )
         """
        cur.execute(sql_quary4)
        con.commit() 



        sql_quary5="""
        CREATE TABLE CATEGORY_CHANGES(
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        category_foreign VARCHAR(255),
        quantity_income FLOAT,
        quantity_income_cost FLOAT,
        quantity_outcome FLOAT,
        quantity_outcome_cost FLOAT,
        measure VARCHAR(255),
        non_auto_date_third VARCHAR(255),
        FOREIGN KEY (category_foreign) REFERENCES CATEGORY(category)
        )
         """
        cur.execute(sql_quary5)
        con.commit()


#deprecated
        # sql_quary6="""
        # CREATE TABLE IF NOT EXISTS CATEGORY_RECENT(
        # category_recent VARCHAR(255) PRIMARY KEY,
        # quantity_entered FLOAT,
        # quantity_entered_cost FLOAT,
        # quantity_out FLOAT,
        # quantity_out_cost FLOAT
        # )
        #  """
        # cur.execute(sql_quary6)
        # con.commit() 


        sql_quary9="""
        CREATE TABLE PAYROLL(
        worker varchar(255),
        payroll INT,
        PRIMARY KEY (worker)
        )"""
        cur.execute(sql_quary9)
        con.commit()
        

        sql_quary10="""
        CREATE TABLE MAIN_MONEY(
        amount INT
        )"""
        cur.execute(sql_quary10)
        con.commit()

        sql_quary11="""
        CREATE TABLE OTHER_MONEY(
        id INT NOT NULL AUTO_INCREMENT UNIQUE,
        name varchar(255),
        amount INT
        )"""
        cur.execute(sql_quary11)
        con.commit()


        sql_quary12="""
        CREATE TABLE RETURNED(
        id INT NOT NULL AUTO_INCREMENT UNIQUE,
        name VARCHAR(225),
        quantitiy INT,
        cost INT
        )"""
        cur.execute(sql_quary12)
        con.commit()
        
        sql_quary13="""
        CREATE TABLE IF NOT EXISTS DISCOUNT(
        discount INT,
        discount_way varchar(255),
        transaction_id_II INT PRIMARY KEY
        )"""
        cur.execute(sql_quary13)
        con.commit()





        cur.execute("""
                        CREATE TRIGGER AUTO_INSERT_MONEY_DETAILS 
                        AFTER INSERT ON DETAILS
                        FOR EACH ROW
                        BEGIN
                                DECLARE total_amount INT;
                                SET total_amount= (SELECT SUM(cost_for_all) FROM DETAILS WHERE envoy=NEW.envoy AND transaction_id=NEW.transaction_id AND state="قيد");
                                IF NEW.state="قيد" 
                                     THEN
                                       IF NOT EXISTS (SELECT 1 FROM MONEYDETAILS_CUSTOMERS WHERE customer=NEW.envoy)
                                           THEN
                                                INSERT INTO MONEYDETAILS_CUSTOMERS VALUES(NEW.envoy);   
                                       END IF;
        
                                       IF EXISTS (SELECT 1 FROM MONEYDETAILS WHERE client=NEW.envoy AND transation_id=NEW.transaction_id) 
                                             THEN
                                                  UPDATE MONEYDETAILS SET the_whole_amount=total_amount WHERE client=NEW.envoy AND transation_id=NEW.transaction_id;
                                       ELSE
                                            INSERT INTO MONEYDETAILS VALUES(NOT NULL,NEW.envoy,total_amount,0,0,0,"قيد",NEW.time,NEW.transaction_id);         
                                       END IF;
                                END IF;
                        END;
                        """)
        con.commit()

        cur.execute("""
                        CREATE TRIGGER AUTO_UPDATE_MONEY_DETAILS 
                        AFTER UPDATE ON DETAILS
                        FOR EACH ROW
                        BEGIN
                                DECLARE total_amount INT;
                                SET total_amount= (SELECT SUM(cost_for_all) FROM DETAILS WHERE envoy=NEW.envoy AND transaction_id=NEW.transaction_id AND state="قيد");
                                IF NEW.state="قيد" 
                                     THEN
                                       IF NOT EXISTS (SELECT 1 FROM MONEYDETAILS_CUSTOMERS WHERE customer=NEW.envoy)
                                           THEN
                                                INSERT INTO MONEYDETAILS_CUSTOMERS VALUES(NEW.envoy);   
                                       END IF;
                                       IF EXISTS (SELECT 1 FROM MONEYDETAILS WHERE client=NEW.envoy AND transation_id=NEW.transaction_id ) 
                                             THEN
                                                  UPDATE MONEYDETAILS SET the_whole_amount=total_amount WHERE client=NEW.envoy AND transation_id=NEW.transaction_id;
                                       ELSE
                                            INSERT INTO MONEYDETAILS VALUES(NOT NULL,NEW.envoy,total_amount,0,0,0,"قيد",NEW.time,NEW.transaction_id);         
                                       END IF;
                                ELSEIF NEW.state = "تم" 
                                    THEN
                                        IF OLD.state = "قيد"
                                                THEN       
                                              IF NOT EXISTS (SELECT 1 FROM DETAILS WHERE envoy=NEW.envoy AND transaction_id=NEW.transaction_id AND state="قيد")  
                                                THEN
                                                     DELETE FROM  MONEYDETAILS WHERE client=NEW.envoy AND transation_id=NEW.transaction_id;
                                              ELSE 
                                                  UPDATE MONEYDETAILS SET the_whole_amount=total_amount WHERE client=NEW.envoy AND transation_id=NEW.transaction_id;  
                                              END IF;
                                              IF NOT EXISTS (SELECT 1 FROM MONEYDETAILS WHERE client=NEW.envoy)  
                                                  THEN
                                                      DELETE FROM  MONEYDETAILS_CUSTOMERS WHERE customer=NEW.envoy;
                                              END IF;
                                        END IF;
                                END IF;
                        END;
                        """)
        con.commit()

        cur.execute("""
                        CREATE TRIGGER AUTO_DELETE_MONEY_DETAILS 
                        AFTER DELETE ON DETAILS
                        FOR EACH ROW
                        BEGIN
                              DECLARE total_amount INT;
                              SET total_amount= (SELECT SUM(cost_for_all) FROM DETAILS WHERE envoy=OLD.envoy AND transaction_id=OLD.transaction_id AND state="قيد");
                              IF OLD.state="قيد" 
                                  THEN
                                      IF total_amount IS NULL  THEN
                                            DELETE FROM MONEYDETAILS WHERE client=OLD.envoy AND transation_id=OLD.transaction_id;
                            
                                      ELSE 
                                            UPDATE MONEYDETAILS SET the_whole_amount=total_amount WHERE client=OLD.envoy AND transation_id=OLD.transaction_id;
                                      END IF;
                                      IF total_amount IS NULL  THEN
                                             DELETE FROM  MONEYDETAILS_CUSTOMERS WHERE customer=OLD.envoy;
                                      END IF;      
                              END IF;
                        END;
                        """)
        con.commit()


        
Database(host='localhost', user='root', password='1234')
    
