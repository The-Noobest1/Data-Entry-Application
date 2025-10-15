import sys
import os
import subprocess

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

from tkinter import *
from tkinter import ttk ,messagebox,filedialog
from tkcalendar import Calendar ,DateEntry
from datetime import datetime
from sql import Database
from itertools import chain
import re
import ttkthemes 
from PIL import Image, ImageTk


db = Database(host='localhost', user='root', password='1234')  #when this class is called the __init__ (constructor) take its parameter and run



page=Tk() 
# page.configure(background="red")  

page.geometry("1280x630+0+0")
page.state('zoomed')
page.title("shop management")
page.iconbitmap(bitmap="./icons/boxicon.ico")

ttkthemes.ThemedStyle(master=page,theme="winxpblue")
# most acceptable
#clearlooks 
#elegance
#radiance  
#scidblue,scidgrey
#winxpblue
style=ttk.Style()
# style.theme_use('clam')
style.configure('TFrame',background="#dad5b8" )  # Frame background color
style.configure('TLabel',foreground="#191815",anchor='center' , font=('Arial', 14))  # Label background, foreground, font
style.configure('TLabelframe.Label',foreground="#191815", font=('Arial', 14))  # Label background, foreground, font
style.configure('TEntry', fieldbackground="#ececec" ,font=('Arial', 11))  # Entry field background and font
style.configure('TCombobox',fieldbackground="#ececec" ,  font=("Arial Bold", 20))  # Combobox field background and font
style.configure('TButton',foreground="#19170a", font=('Arial Bold', 11))  # Button colors and font
style.configure('TSpinbox', fieldbackground="#ececec" ,font=('Arial Bold', 11))  # Spinbox field background and font
style.configure('Treeview',fieldbackground='#ffffff',foreground="#1e1e1c", font=('Simplified Arabic Bold',13),rowheight=30)  # Spinbox field background and font
style.configure('Treeview.Heading',background="#ece7ca",font=('Simplified Arabic Bold',12))
style.map('Treeview',fieldbackground='#ece9d8')
style.map('TButton', background=[('active','red'), ("!active", "blue")])


string_pattern_compiled=re.compile(r"^[\u0600-\u06FF]+(\s[\u0600-\u06FF]+)*$")
intger_pattern_compiled=re.compile(r"^[0-9]+$")


password_var=StringVar()


envoy=StringVar()
company=StringVar()
product_name=StringVar()
amount=StringVar()
measure=StringVar()
cost_per_one=DoubleVar()              
The_pay_id=IntVar()
state=StringVar() 
date=StringVar()
transaction_id_search=IntVar()
#---discount_entry_in_main_window
discount_details=IntVar()
#---discount_entry_in_it's_own_window
discount_amount=StringVar()
discount_way=StringVar()
transaction_id_II=StringVar()


#----- searching varibles-----------
start_date=StringVar()
end_date=StringVar()
search_name_var=StringVar()
search_transaction_id=IntVar()
category_combobox=StringVar()
search_id=IntVar()

# second_window_money_transaction
client_1=StringVar()  #for both tables
the_whole_amount=IntVar()
the_single_paid_amount=IntVar()                   #intvar()  default is 0
the_returned_amount=IntVar()                  #stringvar()  default is
state_2=StringVar()  
transaction=IntVar()
non_auto_date=StringVar()

#----- searching variables----------- 
transaction_id=IntVar()

# third_windpw_categorys
category=StringVar()
quantity=DoubleVar()
measure_3=StringVar()
price_2=DoubleVar()
non_auto_date_third=StringVar()



#------------

customers=StringVar()
companies=StringVar()

#---------------

payroll_name=StringVar()
payroll_amount=StringVar()
#-------
the_started_amount=StringVar()
#-------
returned_categoy=StringVar()
returned_quantity=StringVar()
returned_cost=StringVar()
#-------
other_name=StringVar()
other_amount=StringVar()

#==========واجهة الإدخال==========
seller_frame = ttk.Frame(page)
seller_frame.place(width=340, height=637)

seller_title = ttk.Label(seller_frame, text="تفاصيل الفاتورة")
seller_title.place(x=150, y=1)

transaction_id_count_label=ttk.Label(seller_frame,text=f"{db.last_transaction_id()}:عدد الفواتير",font=('Arial', 11))
transaction_id_count_label.place(x=4,y=460)

envoy_label = ttk.Label(seller_frame, text=" العميل ")
envoy_label.place(x=4, y=39)
envoy_input = ttk.Combobox(seller_frame, textvariable=envoy, font=("Arial Bold", 11))
envoy_input['values'] = db.combobox_values_first_from_forth_customer_company("CUSTOMER_DETAILS")
envoy_input.place(x=120, y=40, width=200, height=25)

company_label = ttk.Label(seller_frame, text="اسم الشركة")
company_label.place(x=4, y=79)
company_input = ttk.Combobox(seller_frame, textvariable=company, font=("Arial Bold", 11))
company_input['values'] = db.combobox_values_first_from_forth_customer_company("COMPANY_DETAILS")
company_input.place(x=120, y=80, width=200, height=25)

product_name_label = ttk.Label(seller_frame, text="اسم المنتج")
product_name_label.place(x=4, y=119)
product_name_input = ttk.Combobox(seller_frame, textvariable=product_name, font=("Arial Bold", 11))
product_name_input['values'] = db.category_combobox()
product_name_input.place(x=120, y=120, width=200, height=25)

def auto_measure_select(event):
     selected_measure=db.select_measure(product_name.get())
     measure.set(selected_measure)

amount_label = ttk.Label(seller_frame, text="الكمية")
amount_label.place(x=4, y=159)
amount_input = ttk.Entry(seller_frame, textvariable=amount, font=("Arial Bold", 11))
amount_input.place(x=120, y=160, width=200, height=25)

measure_label = ttk.Label(seller_frame, text="النوع")
measure_label.place(x=4, y=199)
measure_input = ttk.Combobox(seller_frame, textvariable=measure, font=("Arial Bold", 11))
measure_input['values'] = db.comboxbox_measure()
measure_input.place(x=120, y=200, width=200, height=25)

cost_per_one_label = ttk.Label(seller_frame, text="سعر الواحدة")
cost_per_one_label.place(x=4, y=239)
cost_per_one_input = ttk.Entry(seller_frame, textvariable=cost_per_one, font=("Arial Bold", 11))
cost_per_one_input.place(x=120, y=240, width=200, height=25)

The_pay_id_label = ttk.Label(seller_frame, text="فاتورة")
The_pay_id_label.place(x=4, y=279)
The_pay_id_input = ttk.Entry(seller_frame, textvariable=The_pay_id, font=("Arial Bold", 11))
The_pay_id_input.place(x=120, y=280, width=200, height=25)

state_label = ttk.Label(seller_frame, text="الدفع")
state_label.place(x=4, y=319)
state_input = ttk.Combobox(seller_frame, textvariable=state, font=("Arial Bold", 11))
state_input['values'] = ("قيد", "تم")
state_input.place(x=120, y=320, width=200, height=25)

date_label = ttk.Label(seller_frame, text="التاريخ")
date_label.place(x=4, y=359)
date_input = DateEntry(seller_frame, textvariable=date, font=("Arial Bold", 11), date_pattern="mm/dd/y")
date_input.place(x=120, y=360, width=200, height=25)

discount_details_label = ttk.Label(seller_frame, text="خصم")
discount_details_label.place(x=145, y=400)
discount_details_input = ttk.Entry(seller_frame, textvariable=discount_details, font=("Arial Bold", 11))
discount_details_input.place(x=180, y=400, width=60, height=25)

transaction_id_search_label = ttk.Label(seller_frame, text=f"معرف الفاتورة")
transaction_id_search_label.place(x=6, y=400)
transaction_id_search.set((db.last_transaction_id()+1))
transaction_id_search_input = ttk.Spinbox(seller_frame,textvariable=transaction_id_search,from_=1, to=1000000, font=("Arial Bold", 11))
transaction_id_search_input.place(x=6, y=430, width=60, height=28)

#------main_window_staticis------
main_statistics_label_frame=ttk.Labelframe(seller_frame,text="إحصائيات",labelanchor='n',relief='groove',takefocus=0)
main_statistics_label_frame.place(x=5,y=530,width=200,height=100)

sum_cost_label=ttk.Label(main_statistics_label_frame,text=f":إجمالى",font=('Arial', 14))
sum_cost_label.place(x=130,y=8)

sum_cost=ttk.Label(main_statistics_label_frame,text=f"0",font=('Arial', 14))
sum_cost.place(x=30,y=8)

#-------main_table_category_table_id's_error_detection-------
square=Canvas(seller_frame,background="white")
square.place(x=6,y=500,width=15,height=15)
circle=square.create_oval(12,12,2,2,fill="green",state='normal')    #__x0:width __y0:height  __x1:x  __y1:y
color_state=1

def error_detect():
      if db.id_error_dedection():
            global color_state 
            match color_state:
                  case 1:
                        square.itemconfig(circle,fill="red",state='normal')
                  case 0:
                        square.itemconfig(circle,state='hidden')
                  
            color_state= not color_state           
            page.after(800,error_detect)
      else:
            square.itemconfig(circle,fill="green",state='normal')


#===========menu_functions====================
def backup():

      def back_up_command_line():
            #mysqldump responsible to back_up the database 
            dump_cmd = f'mysqldump -u root -p"{password_var.get()}"  WORKSHOP > {back_up_file_path}.sql'

            try:      
            # Execute the  command in cmd
                  subprocess.run(dump_cmd, shell=True, check=True)
                  messagebox.showinfo("successful back_up",f"{back_up_file_path}") 
            except subprocess.CalledProcessError as e:
                  messagebox.showerror("failed back_up",f"Error occurred during backup: {e}")   
            password_window.destroy()      

      if not os.path.isdir('./database_back_up'):
            os.mkdir('./database_back_up')

      date=datetime.now().strftime("%d-%m-%Y_%H_%M")
      back_up_file=f"back_up_{date}"
      back_up_file_path=os.path.join("./database_back_up",back_up_file)

      password_window=Toplevel(page)
      password_window.geometry("200x200")
      password_window.title("password")

      password_frame=Frame(password_window,bg='#8f8e8e')
      password_frame.place(width=200,height=200)

      password_label=Label(password_frame,text="enter password")
      password_label.place(x=55,y=40,width=120,height=25)

      password_entry=Entry(password_frame,textvariable=password_var)
      password_entry.place(x=60,y=80,width=100,height=20)

      sumbit_button=Button(password_frame,text="إرسال",command=back_up_command_line)
      sumbit_button.place(x=60,y=140,width=80,height=20)
      

#------global_function------
def photo_resizing(path):
      global image   
      original_image =Image.open(fr"{path}")
      resized_image = original_image.resize((25, 25), Image.Resampling.LANCZOS)  
      image = ImageTk.PhotoImage(resized_image)
      return image

#===========main_window_functions=============

def getdata(event):
      selected_row=showing_table.focus()               
      data=showing_table.item(selected_row)
      global column
      column=data["values"]

      try:    #translate dict to list   take values and transfer it to the list                  #column4[2]=str(column4[2]).replace('2','43')
         if float(column[4])>=0: # not minus integer   # SuS amogus --> .isdigit() <-- another solution 
           amount.set("+"+str(column[4]))  # "" preserve the same format   ''don't preserve the same format  print("+2") print ('+2')
         elif float(column[4])<0:
           amount.set(column[4])
         envoy.set(column[1])
         company.set(column[2])
         product_name.set(column[3])   # put colunm values to entrys
         measure.set(column[5])
         cost_per_one.set(column[6])
         The_pay_id.set(column[8])
         state.set(column[9])
         date.set(column[10])
      except IndexError:   
            pass
            return
      except ValueError:
           messagebox.showerror("ValueError","check the inputs")
           amount.get()
           return

def is_float(amout_string):
      try:
            float(amout_string[1:])
            return True
      except :
            return False 
      
def is_date(date_string):
      try:
            datetime.strptime(date_string,"%m/%d/%Y")  
            return True
      except Exception :
            return False    
           
def ensure_insert(action):
      if The_pay_id.get()!=transaction_id_search.get():
            response=messagebox.askokcancel(f"{action} warning","transaction_id not equal")
            return response
      else:
            return True      #search what func return without else 

def add():
      if ensure_insert("add")==True:

                  if   (envoy.get()!="" and company.get()=="" and amount.get()[0]=="-" and amount.get()!="" and (amount.get()[1:].isdigit() or is_float(amount.get()))) or (envoy.get()=="" and company.get()!="" and amount.get()!="" and amount.get()[0]=="+" and (amount.get()[1:].isdigit() or is_float())):
                                    
                                    if   product_name.get()!="":
                                                
                                                if measure.get()!="":
                                                            
                                                            if   cost_per_one.get()!="" : #<------  check_float_function
                                                                  
                                                                        if   The_pay_id.get()!="" and The_pay_id.get().is_integer():
                                                                              
                                                                                    if   date.get()!="" and is_date(date.get()):

                                                                                          if company.get()!="" and envoy.get()=="":
                                                                                                state_var="تم"
                                                                                          else:
                                                                                                state_var=state.get()

                                                                                          db.insertion(envoy.get(),company.get(),product_name.get(),amount.get(),measure.get(),cost_per_one.get(),The_pay_id.get(),state_var,date.get(),discount_details.get())
                                                                                          clear()
                                                                                          displayall_transaction_id()    
                                                                                          dynamic_screen()
                                                                                          error_detect()

                                                                                    else: 
                                                                                          messagebox.showwarning("value_error","check the date") 
                                                                                          return
                                                                        else: 
                                                                              messagebox.showwarning("value_error","check transaction_id value") 
                                                                              return
                                                            else: 
                                                                  messagebox.showwarning("value_error","check the cost value") 
                                                                  return
                                                else:
                                                      messagebox.showwarning("value_error","enter/check measure type")
                                    else: 
                                          messagebox.showwarning("value_error","enter/check product_name")                         
                                          return      #name_input=envoy                # company_input=company        #etc      #with get() only
                  else: 
                        messagebox.showwarning("value_error","You must enter either a customer or a company")
                        return
      else:
            return      


def updateing():
      if ensure_insert("update")==True:
                  
                  if   (envoy.get()!="" and company.get()=="" and amount.get()[0]=="-" and amount.get()!="" and (amount.get()[1:].isdigit() or is_float(amount.get()))) or (envoy.get()=="" and company.get()!="" and amount.get()[0]=="+" and amount.get()!="" and (amount.get()[1:].isdigit() or is_float())):
                                    
                                    if   product_name.get()!="":
                                                
                                                if measure.get()!="":
                                                            
                                                            if   cost_per_one.get()!="" : #<------  check_float_function
                                                                  
                                                                        if   The_pay_id.get()!="" and The_pay_id.get().is_integer():
                                                                              
                                                                                    if   date.get()!="" and is_date(date.get()):

                                                                                          if company.get()!="" and envoy.get()=="":
                                                                                                state_var="تم"
                                                                                          else:
                                                                                                state_var=state.get()
                                                                                          
                                                                                          db.update_third_table_AND_first_table(envoy.get(),company.get(),product_name.get(),amount.get(),measure.get(),cost_per_one.get(),The_pay_id.get(),state_var,date.get(),column[0])
                                                                                          clear()
                                                                                          displayall_transaction_id()   
                                                                                          error_detect()  
                                                                                          
                                                                                    else: 
                                                                                          messagebox.showwarning("value_error","check the date") 
                                                                                          return
                                                                        else: 
                                                                              messagebox.showwarning("value_error","check transaction_id value") 
                                                                              return
                                                            else: 
                                                                  messagebox.showwarning("value_error","check the cost value") 
                                                                  return
                                                else:
                                                      messagebox.showwarning("value_error","enter/check measure type")
                                    else: 
                                          messagebox.showwarning("value_error","enter/check product_name")                         
                                          return      #name_input=envoy                # company_input=company        #etc      #with get() only
                  else: 
                        messagebox.showwarning("value_error","You must enter either a customer or a company or check +/-")
                        return
      else:
            return

def clear():
      envoy.set("")
      company.set("")
      product_name.set("")       # clear entrys(textvariable) values
      amount.set("") 
      measure.set("")
      cost_per_one.set("")
      The_pay_id.set("")
      state.set("")
      date.set("")
      discount_details.set(0)


def delete():
      if ensure_insert("delete")==True:
            db.remove(column[0])
            clear()
            displayall_transaction_id()
            dynamic_screen()
            error_detect()
      else:
            return      

def  displayall():
      showing_table.delete(*showing_table.get_children())    
      for row in db.fetced():
            showing_table.insert("",END,values=row)    

def  displayall_transaction_id():
      showing_table.delete(*showing_table.get_children())    
      for row in db.transactions(transaction_id_search.get()):
            showing_table.insert("",END,values=row)  
      global sum_cost
      sum_cost.config(text=f"{(db.sum_category_cost(transaction_id_search.get())):.2f}")
            
def dynamic_screen():
      global transaction_id_count_label
      transaction_id_count_label.config(text=f"{db.last_transaction_id()}:عدد الفواتير")

#---------------- feature_functions -----------------
            
#-----refresh-----
            
def refresh():

      global product_name_input
      product_name_input.config(values=db.category_combobox())

      global envoy_input
      envoy_input.config(values=db.combobox_values_first_from_forth_customer_company("CUSTOMER_DETAILS"))

      global company_input
      company_input.config(values=db.combobox_values_first_from_forth_customer_company("COMPANY_DETAILS"))

      global measure_input
      measure_input.config(values=db.comboxbox_measure())

      displayall()
      product_name_input.bind("<<ComboboxSelected>>",auto_measure_select)

#---------main_searching_window---------
def pop_all_searching_functions_window():
      global child_window_searching
      child_window_searching=Toplevel(page)
      child_window_searching.geometry("150x250")          
      child_window_searching.title("Searching_By")

      child_window_searching_frame=ttk.Frame(child_window_searching)
      child_window_searching_frame.place(width=400,height=300)

      search_id_button=ttk.Button(child_window_searching_frame,text="بحث بالعملية",command=pop_up_search_id_window,takefocus=0)
      search_id_button.place(x=20,y=20,width=100,height=40)

      search_transaction_id_button=ttk.Button(child_window_searching_frame,text="بحث برقم الفاتورة",command=search_transaction_id_func,takefocus=0)
      search_transaction_id_button.place(x=20,y=100,width=100,height=40)

      search_name_button=ttk.Button(child_window_searching_frame,text="بحث بالإسم",command=pop_up_search_name_window,takefocus=0)
      search_name_button.place(x=20,y=180,width=100,height=40)

#-----search_by_id----- 
def search_id_func():
      if search_id.get()!="" and search_id.get().is_integer():
            rows=db.searching_id(search_id.get())            
            showing_table.delete(*showing_table.get_children())
            for row in rows:
                  showing_table.insert("",END,values=row)  
      else:
            messagebox.showwarning("خطأ في الفاتورة","تأكد من كتابة رقم الفاتورة صحيحا")            

#-----search_by_transaction_id----- 
def search_transaction_id_func():
      if search_transaction_id.get()!="" and search_transaction_id.get().is_integer():
            rows=db.searching_transaction_id(search_transaction_id.get())            
            showing_table.delete(*showing_table.get_children())
            for row in rows:
                  showing_table.insert("",END,values=row)  
      else:
            messagebox.showwarning("خطأ في المعرف","صحيحا (id)تأكد من كتابة رقم المعرف ")  
#-----search_by_name-----      
def search_name_func():
      if  is_date(start_date.get()) and  is_date(end_date.get()):
            rows=db.searching_name(search_name_var.get(),start_date.get(),end_date.get(),category_combobox.get()) 
            showing_table.delete(*showing_table.get_children()) 
            for row in rows:
                  showing_table.insert("",END,values=row)   
      else:
            messagebox.showwarning("خطأ في التاريخ","تأكد من كتابة التاريخ في الخانتين")             


def pop_up_search_id_window():
      child_window_id=Toplevel(child_window_searching)
      child_window_id.geometry("170x200+160+360")
      child_window_id.title("search_window")

      child_window_frame_search_id=ttk.Frame(child_window_id)
      child_window_frame_search_id.place(width=400,height=400)

      label_id=ttk.Label(child_window_frame_search_id,text="معرف العملية")
      label_id.place(x=40,y=50)
      search_input_id=ttk.Spinbox(child_window_frame_search_id,textvariable=search_id,from_=1,to=1000000)
      search_input_id.place(x=60,y=80,width=40,height=28)

      button_id=ttk.Button(child_window_frame_search_id,text="إرسال",command=search_id_func)
      button_id.place(x=20,y=125,width=120,height=25) 


def pop_up_search_transaction_id_window():
      child_window_transaction_id=Toplevel(child_window_searching)
      child_window_transaction_id.geometry("170x200+160+360")
      child_window_transaction_id.title("search_window")

      child_window_frame_search_transaction_id=ttk.Frame(child_window_transaction_id)
      child_window_frame_search_transaction_id.place(width=400,height=400)

      label_transaction_id=ttk.Label(child_window_frame_search_transaction_id,text="(id)رقم المعرف")
      label_transaction_id.place(x=40,y=50)
      search_input_transaction_id=ttk.Spinbox(child_window_frame_search_transaction_id,textvariable=search_transaction_id,from_=1,to=1000000)
      search_input_transaction_id.place(x=60,y=80,width=40,height=28)

      button_transaction_id=ttk.Button(child_window_frame_search_transaction_id,text="إرسال",command=search_transaction_id)
      button_transaction_id.place(x=20,y=125,width=120,height=25) 

def pop_up_search_name_window():
      child_window_name=Toplevel(child_window_searching)
      child_window_name.geometry("400x400")
      child_window_name.title("search_window")

      child_window_frame_search_name=ttk.Frame(child_window_name)
      child_window_frame_search_name.place(width=400,height=400)

      label_name_var=ttk.Label(child_window_frame_search_name,text="الإسم")
      label_name_var.place(x=240,y=50)
      search_input_name_var=ttk.Combobox(child_window_frame_search_name,textvariable=search_name_var,values=db.combobox_values(), font=("Arial Bold", 11))
      search_input_name_var.place(x=80,y=50,width=150,height=25)

      label_start_time=ttk.Label(child_window_frame_search_name,text="Start Time")
      label_start_time.place(x=240,y=100)
      search_input_start_time=DateEntry(child_window_frame_search_name,textvariable=start_date,date_pattern="mm/dd/y")
      search_input_start_time.place(x=80,y=100,width=150,height=25)

      label_end_time=ttk.Label(child_window_frame_search_name,text="End Time")
      label_end_time.place(x=240,y=150)
      search_input_end_time=DateEntry(child_window_frame_search_name,textvariable=end_date,date_pattern="mm/dd/y")
      search_input_end_time.place(x=80,y=150,width=150,height=25)

      label_categorys=ttk.Label(child_window_frame_search_name,text="category")
      label_categorys.place(x=240,y=200)
      search_input_category=ttk.Combobox(child_window_frame_search_name,textvariable=category_combobox,values=db.combobox_values_categorys(), font=("Arial Bold", 11))
      search_input_category.place(x=80,y=200,width=150,height=25)

      button_name=ttk.Button(child_window_frame_search_name,text="إرسال",command=search_name_func)
      button_name.place(x=150,y=290,width=120,height=25) 



      
def search_sorting_func(sorting_option):
      if sorting_option=="ابحث بإستخدام الشركة":
            option="company"
      elif sorting_option=="ابحث بإستخدام الموزع":
            option="envoy"   
      showing_table.delete(*showing_table.get_children())
      for row in db.search_sorting_fetch(option):
            showing_table.insert("",END,values=row)  



#==============================second_window_functions(money_transaction)==============================
      
class statistic_sum():
      def __init__(self,parent_frame):
            self.child_window_frame=parent_frame
      def statistic_frame(self,label_text,label_func,window_name="money_debts_detail"):
            self.statistics_label_frame=ttk.Labelframe(self.child_window_frame,text="إحصائيات",labelanchor='n',relief='groove',takefocus=0)
            self.statistics_label_frame.place(x=10,y=420,width=280,height=170)
            #   
            self.v1_label=ttk.Label(self.statistics_label_frame,text=f"{label_text[0]}")
            self.v1_label.place(x=150,y=10)

            self.v1=ttk.Label(self.statistics_label_frame,text=f"{(label_func[0]):.2f}",foreground="#090907")
            self.v1.place(x=10,y=10)
            #
            self.v2_label=ttk.Label(self.statistics_label_frame,text=f"{label_text[1]}",font=("Arial",14))
            self.v2_label.place(x=155,y=40)

            self.v2=ttk.Label(self.statistics_label_frame,text=f"{(label_func[1]):.2f}",foreground="#090907")
            self.v2.place(x=10,y=40)
            #
            self.v3_label=ttk.Label(self.statistics_label_frame,text=f"{label_text[2]}")
            self.v3_label.place(x=180,y=70)

            self.v3=ttk.Label(self.statistics_label_frame,text=f"{(label_func[2]):.2f}",foreground="#090907")
            self.v3.place(x=10,y=70)

            self.refresh_statistic_button=ttk.Button(self.statistics_label_frame,image=image_1,command=lambda:self.refresh_statistics_label(label_func,window_name),takefocus=0)#
            self.refresh_statistic_button.place(x=120,y=100,width=35,height=35)

            match window_name:
                  case "category_details":
                        self.statistics_label_frame.place(x=10,y=420,width=300,height=200)
                        self.v1_label.place(x=170,y=10)
                        self.v2_label.place(x=175,y=40)
                        self.v3_label.place(x=170,y=70)

                        self.v4_label=ttk.Label(self.statistics_label_frame,text=f"{label_text[3]}")
                        self.v4_label.place(x=170,y=100)

                        self.v4=ttk.Label(self.statistics_label_frame,text=f"{(label_func[3]):.2f}",foreground="#090907")
                        self.v4.place(x=10,y=100)

                        self.refresh_statistic_button.place(x=125,y=135,width=35,height=35)
                  case "default":
                        self.v4=None      
                        
            return self.statistics_label_frame,self.v1,self.v2,self.v3,self.v4,self.refresh_statistic_button  
#------money_details_statictis------- # try loop when button clicked call statistic_frame in refresh_statistics_label but if label exist
      def refresh_statistics_label(self,label_func,window_name):
            
            self.v1.config(text=f"{(label_func[0]):.2f}",foreground="#090907")
            self.v2.config(text=f"{(label_func[1]):.2f}",foreground="#090907")
            self.v3.config(text=f"{(label_func[2]):.2f}",foreground="#090907")
            match window_name:
                  case "category_details":
                        self.v4.config(text=f"{(label_func[3]):.2f}",foreground="#090907")
                  

      def dynamic_refresh_statistics_label(self,label_func,window_name):

            self.v1.config(text=f"{(label_func[0]):.2f}",foreground="#090907")
            self.v2.config(text=f"{(label_func[1]):.2f}",foreground="#090907")
            self.v3.config(text=f"{(label_func[2]):.2f}",foreground="#090907")
            match window_name:
                  case "category_details":
                        self.v4.config(text=f"{(label_func[3]):.2f}",foreground="#090907")
            
#==============================first_table========================================
class Money_details(statistic_sum):
      def __init__(self,parent,parent_frame):
            self.child_window=parent
            self.child_window_frame=parent_frame
            self.pop_up_transactions_first_table()
      #----------------------first_table_function-------------------------

      def getdata_sec(self):
            selected_row_1=self.showing_table_1.focus()               
            data_1=self.showing_table_1.item(selected_row_1)
            self.column_1=data_1["values"]

            client_1.set(self.column_1[0])


      def add_sec(self):
            if client_1.get() == "":
                  messagebox.showwarning("value_error","ENTER ALL ENTRYS")
                  return      
            else:db.insertion_sec_1(client_1.get())   
            self.clear_sec()
            self.displayall_sec()
      
      def update_sec(self):
            if client_1.get() == "":
                  messagebox.showwarning("value_error","ENTER ALL ENTRYS")
                  return
            else:db.update_sec_1(client_1.get(),self.column_1[0])
            self.clear_sec()
            self.displayall_sec()


      def clear_sec(self):
            client_1.set("")


      def delete_sec(self):
            db.remove_sec_1(self.column_1[0])
            self.clear_sec()
            self.displayall_sec()


      def  displayall_sec(self):
            self.showing_table_1.delete(*self.showing_table_1.get_children())    
            for row_1 in db.fetced_sec_1():
                  self.showing_table_1.insert("",END,values=row_1)   





#----------------------second_table_function-------------------------


      def getdata_sec_2(self):
            selected_row_2=self.showing_table_2.focus()               
            data_2=self.showing_table_2.item(selected_row_2)
            self.column2=data_2["values"]

            the_whole_amount.set(self.column2[2])
            the_single_paid_amount.set(self.column2[4])
            the_returned_amount.set(self.column2[5])   # put colunm values to entrys
            non_auto_date.set(self.column2[7])    
            transaction.set(self.column2[8])

      def add_sec_2(self): 
            option={'parent':self.child_window}
            def listing_finished_id():
                  the_list=list()
                  for row_2 in db.fetced_sec_2(self.column_1[0]): # can change it for better performance
                        if  row_2[6]=="تم":
                              the_list.append(row_2[8])            # listing the completed transaction_id
                        else:
                              continue
                  return the_list
            the_list=listing_finished_id()

            if len(self.showing_table_2.get_children())==0 :
                  sum_value=0
                  the_returned_amount.set(0)
                  the_whole_amount_last=the_whole_amount.get()
            elif len(self.showing_table_2.get_children())!=0:
                  last_row=self.showing_table_2.get_children()[-1]   #last_row
                  item=self.showing_table_2.item(last_row)["values"]    #last_row_column's_values

                  if item[-1]  in the_list:  # mean it is "تم"                                                
                        sum_value=0                                                #!!!!!!!!!!!!!!!!!!!!!! seperate them with search if i want to modify transaction i can search for it's id 
                        the_returned_amount.set(0)                       ###!!!!! useless
                        the_whole_amount_last=the_whole_amount.get() 
                  else:
                        try:  # you set focus (as click in the row)
                              self.showing_table_2.focus_set(last_row)
                              sum_value=db.fetced_sum_sec_2(self.column_1[0],self.column2[8])[0]
                        except: # if you want to write in entrys
                              sum_value=db.fetced_sum_sec_2(self.column_1[0],transaction.get())[0]
                        the_whole_amount_last=int(item[2])    #whole amount (before supstract it from returned *if exists*) = the previous whole amount
            the_sum_paid_value=sum_value+the_single_paid_amount.get()                             # sum the paid amount


            if  the_whole_amount_last != "" : 

                  if the_single_paid_amount.get() != "" :

                        if the_returned_amount.get() != "" :

                              if non_auto_date.get() !="" :

                                    if transaction.get() !=""  :

                                          if transaction.get() in the_list:
                                                
                                                messagebox.showwarning("value_error","This Transaction_id has finished ,use another Transaction_id ",**option) 
                                                return  
                                          else: 
                                                state_2.set("قيد")
                                                the_whole_amount_sub=the_whole_amount_last-the_returned_amount.get()

                                                if the_whole_amount_sub==the_sum_paid_value:
                                                      state_2.set("تم")
                                                      try:
                                                            db.update_details_state_from_money_details(self.column_1[0],self.column2[8])
                                                      except:
                                                            db.update_details_state_from_money_details(self.column_1[0],transaction.get())
                                                elif the_whole_amount_sub<the_sum_paid_value:
                                                      messagebox.showwarning("value_error"," check the the_whole_cost and the_paid_cost",**option) 
                                                      return
                                                db.insertion_sec_2(self.column_1[0],the_whole_amount_sub,the_sum_paid_value,the_single_paid_amount.get(),the_returned_amount.get(),state_2.get(),non_auto_date.get(),transaction.get())   
                                                self.clear_sec_2()       
                                                self.searching_money_transaction_id()       
                                    else:
                                          messagebox.showwarning("value_error","check the transaction_id",**option)
                                          return
                              else:
                                    messagebox.showwarning("value_error","check the date",**option)
                                    return            
                        else:
                              messagebox.showwarning("value_error","check the returned_amount",**option)
                              return
                  else:
                        messagebox.showwarning("value_error","check the paid_amount",**option)
                        return           
            else:
                  messagebox.showwarning("value_error","check the whole_amount",**option)
                  return

      def  clear_sec_2(self):
            the_whole_amount.set("")       # clear entrys(textvariable) values
            the_single_paid_amount.set("") 
            the_returned_amount.set("")
            state_2.set("")
            non_auto_date.set("")

      def  delete_sec_2(self):
            db.remove_sec_2(self.column2[0])
            self.clear_sec_2()
            self.searching_money_transaction_id()

      def  displayall_sec_2(self):
            self.showing_table_2.delete(*self.showing_table_2.get_children())    
            for row_2 in db.fetced_sec_2(self.column_1[0]):
                  self.showing_table_2.insert("",END,values=row_2) 


#-------second_table_feature_functions-------
            
      def  getdata_and_display(self):
            self.getdata_sec()
            self.displayall_sec_2()
            self.dynamic_main_money_functions=(db.dynamic_main_money_sum(self.column_1[0])[0],db.dynamic_main_money_sum(self.column_1[0])[1],db.dynamic_main_money_sum(self.column_1[0])[2])

      def  back_to_previous_table(self):
            self.showing_table_2.destroy() 
            self.pop_up_transactions_first_table()   


      def searching_money_transaction_id(self):
            self.showing_table_2.delete(*self.showing_table_2.get_children())
            for row_2 in db.searching_money_transcation_id(self.column_1[0],transaction_id.get()):
                  self.showing_table_2.insert("",END,values=row_2) 
            self.showing_table_2.bind("<ButtonRelease-1>",lambda e:self.getdata_sec_2()) 


      

      #------------------- first_table -------------------#

      def pop_up_transactions_first_table(self):
                  
            for widget in self.child_window_frame.winfo_children():
                  widget.destroy()

            self.child_window.geometry("500x630+30+18")  #main window
            self.child_window.title("الحسابات")
            
            #-------

            self.child_window_frame=ttk.Frame(self.child_window)   #right_side frame
            self.child_window_frame.place(width=300,height=630)

            client_label=ttk.Label(self.child_window_frame,text="اسم العميل ")
            client_label.place(x=4,y=30)
            client_input=ttk.Combobox(self.child_window_frame,textvariable=client_1,values=db.combobox_values_first_from_forth_customer_company("CUSTOMER_DETAILS")) 
            client_input.place(x=100,y=40,width=180,height=24)

            submit_button=ttk.Button(self.child_window_frame,text="حفظ",command=self.add_sec,takefocus=0)
            submit_button.place(x=90,y=280,width=120,height=40)

            update_button=ttk.Button(self.child_window_frame,text="تعديل",command=self.update_sec,takefocus=0)
            update_button.place(x=20,y=340,width=120,height=40)

            delete_button=ttk.Button(self.child_window_frame,text="حذف",command=self.delete_sec,takefocus=0)
            delete_button.place(x=160,y=340,width=120,height=40)
            #------statistics_frame------#
            
            main_money_labels=(" : إجمالى المديونية"," : إجمالى المدفوع",": المتبقى")
            main_money_functions=(db.main_money_debts_sum()[0],db.main_money_debts_sum()[1],db.main_money_debts_sum()[2])
            self.statistics_label_frame,self.v1,self.v2,self.v3,self.v4,self.refresh_statistic_button=statistic_sum(self.child_window_frame).statistic_frame(main_money_labels,main_money_functions,"default")
            
            #--------
            data_tables_1 =ttk.Frame(self.child_window)
            data_tables_1.place(x=300,y=1,width=200,height=630)  #table_frame

            scroll_1=Scrollbar(data_tables_1)
            scroll_1.pack(side=RIGHT,fill=Y)

            self.showing_table_1=ttk.Treeview(data_tables_1,columns=(1),height=630,takefocus=0,yscrollcommand=scroll_1.set)

            self.showing_table_1.heading("1",text="اسم العميل")
            self.showing_table_1.column("1",anchor=CENTER,width=180)

            self.showing_table_1['show']= 'headings'
            self.showing_table_1.bind("<ButtonRelease-1>",lambda e:self.getdata_sec())
            self.showing_table_1.bind("<Double-Button-1>",lambda e:self.transaction_second_table_part_one())
            self.showing_table_1.pack()
            
            scroll_1.config(command=self.showing_table_1.yview)

            self.displayall_sec()

      #==============================second_table_part_one======================================== 

      def transaction_second_table_part_one(self):
            self.statistics_label_frame.place_forget()
            for widget in self.child_window_frame.winfo_children():
                  if widget not in self.statistics_label_frame.winfo_children() and widget!=self.statistics_label_frame:
                        widget.destroy()
            
            self.child_window.geometry("1272x630+0+0")
            self.child_window.resizable(0,0)

            transaction_search_button=ttk.Spinbox(self.child_window_frame,textvariable=transaction_id,from_=1,to=1000000,font=('Arial Bold', 11))
            transaction_search_button.place(x=140,y=247,width=60,height=24)

            search_button=ttk.Button(self.child_window_frame,text="ابحث بالمجموعة",command=self.transaction_second_table_part_two,takefocus=0)
            search_button.place(x=20,y=240,width=100,height=40)

            data_tables_2 =ttk.Frame(self.child_window)
            data_tables_2.place(x=500,y=1,width=771,height=630)

            scroll_2=Scrollbar(data_tables_2)
            scroll_2.pack(side=RIGHT,fill=Y)
            
            self.showing_table_2=ttk.Treeview(data_tables_2,columns=(1,2,3,4,5,6,7,8,9),height=630,takefocus=0,yscrollcommand=scroll_2.set)

            self.showing_table_2.heading("1",text="id")
            self.showing_table_2.column("1",anchor=CENTER,width=40)

            self.showing_table_2.heading("2",text="الموزع")
            self.showing_table_2.column("2",anchor=CENTER,width=170)

            self.showing_table_2.heading("3",text="المبلغ الكلى")
            self.showing_table_2.column("3",anchor=CENTER,width=90)

            self.showing_table_2.heading("4",text="مجموع المبالغ")                 
            self.showing_table_2.column("4",anchor=CENTER,width=90)           #sum of all column must = width of table   
            
            self.showing_table_2.heading("5",text="المبلغ المدفوع")
            self.showing_table_2.column("5",anchor=CENTER,width=92)
            
            self.showing_table_2.heading("6",text="المرتجع")
            self.showing_table_2.column("6",anchor=CENTER,width=60)

            self.showing_table_2.heading("7",text="الحالة")
            self.showing_table_2.column("7",anchor=CENTER,width=50)
            
            self.showing_table_2.heading("8",text="التاريخ")
            self.showing_table_2.column("8",anchor=CENTER,width=100)
            
            self.showing_table_2.heading("9",text="مجموعة")
            self.showing_table_2.column("9",anchor=CENTER,width=60)

            self.showing_table_2['show']= 'headings'

            self.showing_table_1.bind("<ButtonRelease-1>",lambda e:self.getdata_and_display())
            self.showing_table_1.unbind("<Double-Button-1>")

            self.showing_table_2.pack()
            
            scroll_2.config(command=self.showing_table_2.yview)

            self.displayall_sec_2()
            
      #==============================second_table_part_two========================================

      def transaction_second_table_part_two(self):
            self.statistics_label_frame.place(x=10,y=440,width=280,height=180)
            for widget in self.child_window_frame.winfo_children():
                  if widget!=self.statistics_label_frame:
                        widget.destroy()
            for  labelframe_child in self.statistics_label_frame.winfo_children():
                  if labelframe_child==self.refresh_statistic_button:
                        labelframe_child.destroy()

            self.child_window.geometry("1272x630+0+0")
            
            dynamic_main_money_functions=(db.dynamic_main_money_sum(self.column_1[0])[0],db.dynamic_main_money_sum(self.column_1[0])[1],db.dynamic_main_money_sum(self.column_1[0])[2])
            self.dynamic_refresh_statistics_label(dynamic_main_money_functions,"default")
            
            total_amount_label=ttk.Label(self.child_window_frame,text="المبلغ الكلى")
            total_amount_label.place(x=4,y=39)
            total_amount_input=ttk.Entry(self.child_window_frame,textvariable=the_whole_amount)
            total_amount_input.place(x=100,y=40,width=180,height=24)

            paid_amount_label=ttk.Label(self.child_window_frame,text="المبلغ المدفوع",)
            paid_amount_label.place(x=4,y=79)
            paid_amount_input=ttk.Entry(self.child_window_frame,textvariable=the_single_paid_amount)
            paid_amount_input.place(x=100,y=80,width=180,height=24)

            returned_amount_label=ttk.Label(self.child_window_frame,text="المرتجع")
            returned_amount_label.place(x=4,y=119)
            returned_amount_input=ttk.Entry(self.child_window_frame,textvariable=the_returned_amount)
            returned_amount_input.place(x=100,y=120,width=180,height=24)

            date_label=ttk.Label(self.child_window_frame,text="التاريخ")
            date_label.place(x=4,y=159)
            date_input=DateEntry(self.child_window_frame,textvariable=non_auto_date,date_pattern="mm/dd/y")
            date_input.place(x=100,y=160,width=180,height=24)
            
            transaction_label=ttk.Label(self.child_window_frame,text="المجموعة")
            transaction_label.place(x=4,y=199)
            transaction_button=ttk.Entry(self.child_window_frame,textvariable=transaction)
            transaction_button.place(x=100,y=200,width=180,height=24)

            submit_button=ttk.Button(self.child_window_frame,text="حفظ",command=self.add_sec_2,takefocus=0)              #after submit clear all data in entrys
            submit_button.place(x=170,y=240,width=120,height=40)

            delete_button=ttk.Button(self.child_window_frame,text="حذف",command=self.delete_sec_2,takefocus=0)
            delete_button.place(x=20,y=240,width=120,height=40)
            
            search_button=ttk.Button(self.child_window_frame,text="فتح",command=self.searching_money_transaction_id,takefocus=0)
            search_button.place(x=200,y=346,width=30,height=30)
            transaction_search_button=ttk.Spinbox(self.child_window_frame,textvariable=transaction_id,from_=1,to=1000000,font=('Arial Bold', 11))
            transaction_search_button.place(x=140,y=347,width=60,height=28)

            refresh_button=ttk.Button(self.child_window_frame,image=image_1,command=self.displayall_sec_2,takefocus=0)
            refresh_button.place(x=255,y=1,width=35,height=35)

            path_2=r"./icons/back.png"
            image_2=photo_resizing(path_2)
            back_button=ttk.Button(self.child_window_frame,image=image_2,command=self.back_to_previous_table,takefocus=0)
            back_button.place(x=10,y=1,width=35,height=35)

            self.showing_table_1.bind("<ButtonRelease-1>",lambda e:(self.getdata_and_display(),self.dynamic_refresh_statistics_label(self.dynamic_main_money_functions,"default")))
            self.searching_money_transaction_id()


#==============fisrt_table_functions==================

#================================(category_window)=================================
#================  table_one  ==============           #make class contian this 
class Category_window(statistic_sum):
      def __init__(self,parent,parent_frame):
            self.child_window_third=parent
            self.child_window_third_frame=parent_frame
            self.pop_up_categorys_window()

      def getdata_third(self):
       selected_row_3=self.showing_table_3.focus()               #select focused row 
       data_3=self.showing_table_3.item(selected_row_3)          #get the selected row items and put it into dict
       self.column3=data_3["values"]                          
       
       category.set(self.column3[0])
       quantity.set(self.column3[1]) # put colunm values to entrys
       measure_3.set(self.column3[2])
       price_2.set(self.column3[3])
       non_auto_date_third.set(self.column3[5])    
      
      def add_third(self):
            option={'parent':self.child_window_third}

            if category.get()!="" :

                  if quantity.get()!=""  :

                        if measure_3.get()!="" and  measure_3.get().isalpha():

                              if price_2.get()!="" :

                                    if non_auto_date_third.get() != "":

                                          db.insertion_third_table(category.get(),quantity.get(),measure_3.get(),price_2.get(),non_auto_date_third.get())   
                                          self.clear_third()
                                          self.displayall_third()

                                    else:
                                          messagebox.showwarning("value_error","check the date",**option)
                                          return
                              else:
                                    messagebox.showwarning("value_error","check the price",**option)
                                    return                
                        else:
                              messagebox.showwarning("value_error","enter/check measure",**option)
                              return   
                  else: 
                        messagebox.showwarning("value_error","check the quantity",**option)
                        return                   
            else: 
                  messagebox.showwarning("value_error","check the  category",**option)
                  return               

      def  update_third(self):
            option={'parent':self.child_window_third}
            if category.get() != "" :  

                  if quantity.get()!=""  :   

                        if measure_3.get()!="" and measure_3.get().isalpha():

                              if price_2.get() != "" :

                                    if non_auto_date_third.get() != "":

                                          db.update_category_in_all_tables(category.get(),quantity.get(),measure_3.get(),price_2.get(),non_auto_date_third.get(),self.column3[0])
                                          self.clear_third()
                                          self.displayall_third()

                                    else:
                                          messagebox.showwarning("value_error","check the date",**option)
                                          return
                              else:
                                    messagebox.showwarning("value_error","check the price",**option)
                                    return  
                        else:
                              messagebox.showwarning("value_error","enter/check measure",**option)          
                              return          
                  else: 
                        messagebox.showwarning("value_error","check the quantity",**option)
                        return                   
            else: 
                  messagebox.showwarning("value_error","check the  category",**option)
                  return       

      def clear_third(self):
            category.set("")
            quantity.set("")
            measure_3.set("")
            price_2.set("")       # clear entrys(textvariable) values
            non_auto_date_third.set("") 

      def  delete_third(self):
            db.remove_third(category.get())
            self.clear_third()
            self.displayall_third()


      def  displayall_third(self):
            self.showing_table_3.delete(*self.showing_table_3.get_children())    
            for row_3 in db.fetced_third_table():
                  category_foreign=row_3[0]
                  quantity_income,quantity_income_cost,quantity_outcome,quantity_outcome_cost=db.suming(category_foreign)       
                  self.showing_table_3.insert("",END,values=(row_3[0],row_3[1],row_3[2],row_3[3],row_3[4],row_3[5],quantity_income,quantity_income_cost,quantity_outcome,quantity_outcome_cost)) 

      #================table_second_functions======================

      def  displayall_third_part_two(self):
            self.showing_table_3_part_two.delete(*self.showing_table_3_part_two.get_children())    
            for row_3 in db.search_category(self.column3[0]):
                  self.showing_table_3_part_two.insert("", END, values=row_3)


      def order(self,event):
            if self.showing_table_3_part_two.identify_region(event.x,event.y)=='heading' and (self.showing_table_3_part_two.identify_column(event.x)=="#2" or self.showing_table_3_part_two.identify_column(event.x)=="#3"):
                  self.showing_table_3_part_two.delete(*self.showing_table_3_part_two.get_children())
                  for row in db.ordering(self.column3[0]):
                        self.showing_table_3_part_two.insert("",END,values=row)
            else:return 



      def pop_up_categorys_window(self): # fifth_window,fifth_window_frame
            
            for widget in self.child_window_third_frame.winfo_children():
                  widget.destroy()

            self.child_window_third.resizable(1,1)
            self.child_window_third.geometry("850x360")
            self.child_window_third.state('zoomed')
            self.child_window_third.title("الأصناف")
            self.child_window_third_frame.place(width=330,height=656)

            category_label=ttk.Label(self.child_window_third_frame,text="الصنف")
            category_label.place(x=4,y=30)
            category_input=ttk.Entry(self.child_window_third_frame,textvariable=category)
            category_input.place(x=120,y=40,width=200,height=25)

            amount_num_label=ttk.Label(self.child_window_third_frame,text="العدد")
            amount_num_label.place(x=4,y=70)
            amount_num_input=ttk.Entry(self.child_window_third_frame,textvariable=quantity)
            amount_num_input.place(x=120,y=80,width=200,height=25)

            measure_3_label=ttk.Label(self.child_window_third_frame,text="النوع")
            measure_3_label.place(x=4,y=110)
            measure_3_input=ttk.Entry(self.child_window_third_frame,textvariable=measure_3)
            measure_3_input.place(x=120,y=120,width=200,height=25)

            the_whole_price=ttk.Label(self.child_window_third_frame,text="سعر الصنف")
            the_whole_price.place(x=4,y=150)
            the_whole_price_input=ttk.Entry(self.child_window_third_frame,textvariable=price_2)
            the_whole_price_input.place(x=120,y=160,width=200,height=25)

            date_label=ttk.Label(self.child_window_third_frame,text="التاريخ")
            date_label.place(x=4,y=190)
            date_input=DateEntry(self.child_window_third_frame,textvariable=non_auto_date_third,date_pattern="mm/dd/y")
            date_input.place(x=120,y=200,width=200,height=25)


            submit_button=ttk.Button(self.child_window_third_frame,text="حفظ",command=self.add_third,takefocus=0)     # ,command=add_third        #after submit clear all data in entrys
            submit_button.place(x=100,y=280,width=120,height=40)
      
            update_button=ttk.Button(self.child_window_third_frame,text="تعديل",command=self.update_third,takefocus=0)#
            update_button.place(x=30,y=340,width=120,height=40)

            delete_button=ttk.Button(self.child_window_third_frame,text="حذف",command=self.delete_third,takefocus=0) #
            delete_button.place(x=190,y=340,width=120,height=40)

            #######-statistics_frame-#######
            
            main_money_labels=(" : إجمالي مخزن"," : إجمالي الوارد",": إجمالي الصادر",": إجمالي(م)الحالى")
            main_money_functions=(db.sum_category_storage_cost(),db.sum_category_entered_cost(),db.sum_category_out_cost(),db.sum_category_current_cost())
            self.statistics_label_frame,self.v1,self.v2,self.v3,self.v4,self.refresh_statistic_button=statistic_sum(self.child_window_third_frame).statistic_frame(main_money_labels,main_money_functions,"category_details")



            #----------category_1_table----------#

            data_tables_3 =ttk.Frame(self.child_window_third)
            data_tables_3.place(x=330,y=1,width=950,height=353)

            scroll_3=Scrollbar(data_tables_3)
            scroll_3.pack(side=RIGHT,fill=Y)

            self.showing_table_3=ttk.Treeview(data_tables_3,columns=(1,2,3,4,5,6,7,8,9,10),height=348,takefocus=0,yscrollcommand=scroll_3.set)
      
            self.showing_table_3.heading("1",text="اسم الصنف")
            self.showing_table_3.column("1",anchor=CENTER,width=183)
            
            self.showing_table_3.heading("2",text="(م)كمية")
            self.showing_table_3.column("2",anchor=CENTER,width=50)

            self.showing_table_3.heading("3",text="النوع")
            self.showing_table_3.column("3",anchor=CENTER,width=80)

            self.showing_table_3.heading("4",text="سعر الواحد")
            self.showing_table_3.column("4",anchor=CENTER,width=80)
            
            self.showing_table_3.heading("5",text="(م)السعرالكلى")
            self.showing_table_3.column("5",anchor=CENTER,width=90)
      
            self.showing_table_3.heading("6",text="التاريخ")
            self.showing_table_3.column("6",anchor=CENTER,width=90)

            self.showing_table_3.heading("7",text="الوارد")
            self.showing_table_3.column("7",anchor=CENTER,width=100)

            self.showing_table_3.heading("8",text="سعر الوارد")
            self.showing_table_3.column("8",anchor=CENTER,width=80)

            self.showing_table_3.heading("9",text="الصادر")
            self.showing_table_3.column("9",anchor=CENTER,width=100)

            self.showing_table_3.heading("10",text="سعر الصادر")
            self.showing_table_3.column("10",anchor=CENTER,width=80)
            
            self.showing_table_3['show']= 'headings'
            scroll_3.config(command=self.showing_table_3.yview)
            
            self.showing_table_3.bind("<ButtonRelease-1>",lambda e:self.getdata_third())
            self.showing_table_3.bind("<Double-Button-1>",lambda e:self.category_changes())
            
            self.showing_table_3.pack()

            self.displayall_third()

            

      #=================  table_three  ====================== 
            
      def category_changes(self): # child_fifth
            self.child_window_third.geometry("1280x720")    

            data_tables_3_part_two =ttk.Frame(self.child_window_third)
            data_tables_3_part_two.place(x=330,y=348,width=950,height=308)

            scroll_3_part_two=Scrollbar(data_tables_3_part_two)
            scroll_3_part_two.pack(side=RIGHT,fill=Y)
            
            self.showing_table_3_part_two=ttk.Treeview(data_tables_3_part_two,columns=(1,2,3,4,5,6,7,8),height=308,takefocus=0,yscrollcommand=scroll_3_part_two.set)
            
            self.showing_table_3_part_two.heading("1",text="id")
            self.showing_table_3_part_two.column("1",anchor=CENTER,width=60)

            self.showing_table_3_part_two.heading("2",text="الصنف")
            self.showing_table_3_part_two.column("2",anchor=CENTER,width=220)

            self.showing_table_3_part_two.heading("3",text="الوارد")
            self.showing_table_3_part_two.column("3",anchor=CENTER,width=80)

            self.showing_table_3_part_two.heading("4",text="سعر الوارد")
            self.showing_table_3_part_two.column("4",anchor=CENTER,width=120)
      
            self.showing_table_3_part_two.heading("5",text="صادر")
            self.showing_table_3_part_two.column("5",anchor=CENTER,width=80)
            
            self.showing_table_3_part_two.heading("6",text="سعر الصادر")
            self.showing_table_3_part_two.column("6",anchor=CENTER,width=120)

            self.showing_table_3_part_two.heading("7",text="النوع")
            self.showing_table_3_part_two.column("7",anchor=CENTER,width=150)

            self.showing_table_3_part_two.heading("8",text="التاريخ")
            self.showing_table_3_part_two.column("8",anchor=CENTER,width=100)

            self.showing_table_3_part_two['show']= 'headings'
            scroll_3_part_two.config(command=self.showing_table_3_part_two.yview)

            self.showing_table_3_part_two.pack()
            self.showing_table_3_part_two.bind("<ButtonRelease-1>",lambda event:self.order(event))
            self.displayall_third_part_two()

 
#===============================================================================================================================
       
class other_windows:
#Class Variables -->ClassName.variable_name
#Instance Variables -->self.variable_name
#if class called and it contain __init__ method it will create instance(clone) not original
#if you don't want to create instance you can pass the variable you want to any function(arguments) this will edit the original variable           
# if variable declared inside class you can't use it inside the class_functions until you put it inside __init__ constructor 
# self call all class methods and variables and method_variable_with_self  like -->  self.variable
# lambda has no name    lambda argument:the_code  normal function  def name(argument):the_code       
# lambda used when you want to call event_function with argument      
# when bind (the_event will pass to the function as argument)
      def __init__(self):  #exeuted when class called   
            self.child_fifth=Toplevel(page)
            self.child_fifth.geometry("520x200+60+60")
            self.child_fifth.title("الإحصائات")
            self.child_fifth.resizable(0,0)
            self.option={'parent':self.child_fifth}

            self.child_fifth_frame=ttk.Frame(self.child_fifth)
            self.child_fifth_frame.place(width=520,height=400)

            category_button=ttk.Button(self.child_fifth_frame, text="الأصناف",command=lambda:Category_window(self.child_fifth,self.child_fifth_frame)) #pass child_fifth,child_fifth_frame to category_table
            category_button.place(x=20,y=20, width=100, height=40)
            
            transaction_button=ttk.Button(self.child_fifth_frame, text="المديونية",command=lambda:Money_details(self.child_fifth,self.child_fifth_frame)) #pass child_fifth,child_fifth_frame to money_transaction_table
            transaction_button.place(x=160,y=20, width=100, height=40)

            customer_button=ttk.Button(self.child_fifth_frame,text="العملاء",command=self.customer_entered)
            customer_button.place(x=20,y=80,width=100,height=40)

            company_button=ttk.Button(self.child_fifth_frame,text="الشركات",command=self.companie_entered)
            company_button.place(x=160,y=80,width=100,height=40)

            payroll_button=ttk.Button(self.child_fifth_frame,text="الرواتب",command=self.payroll)
            payroll_button.place(x=20,y=140,width=100,height=40)

            started_money_button=ttk.Button(self.child_fifth_frame,text="رأس المال",command=self.started_money)
            started_money_button.place(x=160,y=140,width=100,height=40)

            overall_button=ttk.Button(self.child_fifth_frame,text="الحسابات",command=self.statistics)
            overall_button.place(x=280,y=20,width=100,height=40)

            returned_items_button=ttk.Button(self.child_fifth_frame,text="المرتجع",command=self.returned_items)
            returned_items_button.place(x=400,y=20,width=100,height=40)

            other_button=ttk.Button(self.child_fifth_frame,text="مصروفات أخري",command=self.other_money)
            other_button.place(x=280,y=80,width=100,height=40)

            discount_button=ttk.Button(self.child_fifth_frame,text="الخصومات",command=self.discount_win)
            discount_button.place(x=280,y=140,width=100,height=40)
            
      def getdata_5(self,table_num):
            selected_row_5=self.showing_table_5.focus()   #return row identifier
            data_5=self.showing_table_5.item(selected_row_5)       # return row values(items) and some options 
            self.column_5=data_5["values"]                      # choseing the values only
            match table_num:
                  case 1:
                        payroll_name.set(self.column_5[0])
                        payroll_amount.set(self.column_5[1])
                  case 2:
                        the_started_amount.set(self.column_5[0]) 
                  case 3:
                        customers.set(self.column_5[0])
                  case 4:     
                        companies.set(self.column_5[0])
                  case 5:
                        other_name.set(self.column_5[1])  
                        other_amount.set(self.column_5[2])      
                  case 6:
                        returned_categoy.set(self.column_5[1]) 
                        returned_quantity.set(self.column_5[2]) 
                        returned_cost.set(self.column_5[3])
                  case 7:
                        discount_amount.set(self.column_5[0])
                        discount_way.set(self.column_5[1])
                        transaction_id_II.set(self.column_5[2])      

      def add_update_fifth_table(self,table_num,action):
            match table_num:
                  case 1:
                        if string_pattern_compiled.match(payroll_name.get()):
                              if (payroll_name.get() not in db.payroll_name_handle()):
                                    if intger_pattern_compiled.match(payroll_amount.get()):
                                          if action=="add":
                                                db.insertation_fifth_table("PAYROLL",payroll_name.get(),payroll_amount.get(),None)
                                          elif action=="update":     
                                                db.updateing_fifth_table("PAYROLL",payroll_name.get(),payroll_amount.get(),self.column_5[0],None)
                                          self.displaying_fifth_table("PAYROLL")    
                                    else:
                                          messagebox.showwarning("خطأ في كتابة المبلغ","تأكد من عدم وجود فراغات",**self.option)   
                              else:
                                    messagebox.showwarning("خطأ في كتابة الإسم","الإسم مكرر",**self.option)
                        else:
                              messagebox.showwarning("خطأ في كتابة الإسم","تأكد من عدم وجود فراغات في بدايةأو نهاية الإسم",**self.option)  
                  case 2:
                        if intger_pattern_compiled.match(the_started_amount.get()):
                              if db.start_money_count==0:
                                    if action=="add":
                                          db.insertation_fifth_table("MAIN_MONEY",the_started_amount.get(),None,None)
                                    elif action=="update": 
                                          db.updateing_fifth_table("MAIN_MONEY",the_started_amount.get(),None,None,None)
                                    self.displaying_fifth_table("MAIN_MONEY")
                              else:
                                    messagebox.showwarning("اكثر من رأس مال","ادخل رأس المال مرة واحدة فقط",**self.option)              
                        else:
                              messagebox.showwarning("خطأ في كتابة رأس المال","مسموح بالأرقام فقط ",**self.option) 
                  case 3:              
                        if string_pattern_compiled.match(customers.get()):
                              if action=="add":
                                    db.insertation_fifth_table("CUSTOMER_DETAILS",customers.get(),None,None)  
                              elif action=="update":
                                    db.updateing_fifth_table("CUSTOMER_DETAILS",customers.get(),self.column_5[1],self.column_5[0],None)
                              self.displaying_fifth_table("CUSTOMER_DETAILS")       
                        else:
                              messagebox.showwarning("Value_Error","CHECK Customer")
                  case 4:
                        if string_pattern_compiled.match(companies.get()):
                              if action=="add":
                                    db.insertation_fifth_table("COMPANY_DETAILS",companies.get(),None,None)
                              elif action=="update":
                                    db.updateing_fifth_table("COMPANY_DETAILS",companies.get(),self.column_5[1],self.column_5[0],None)
                              self.displaying_fifth_table("COMPANY_DETAILS")       
                        else:
                              messagebox.showwarning("Value_Error","CHECK Company")   
                  case 5:
                        if string_pattern_compiled.match(other_name.get()):
                              if intger_pattern_compiled.match(other_amount.get()):
                                    if action=="add":
                                                db.insertation_fifth_table("OTHER_MONEY",other_name.get(),other_amount.get(),None)
                                    elif action=="update":
                                                db.updateing_fifth_table("OTHER_MONEY",other_name.get(),other_amount.get(),self.column_5[0])  
                                    self.displaying_fifth_table("OTHER_MONEY")
                              else:
                                   messagebox.showwarning("خطأ فى الإسم","(لا تستخدم فراغات فى بداية اونهاية الإسم)تأكد من الإسم")            
                        else:
                              messagebox.showwarning("خطأ فى المال","(مسموح الأرقام فقط)تأكد من المبلغ")        
                  case 6:
                        if returned_categoy.get().isalnum(): #delete this and the make list above the reason is that the returned category may contain numbers and character
                              if intger_pattern_compiled.match(returned_quantity.get()):
                                    if intger_pattern_compiled.match(returned_cost.get()):
                                          if action=="add":
                                                db.insertation_fifth_table("RETURNED",returned_categoy.get(),returned_quantity.get(),returned_cost.get())
                                          elif action=="update":
                                                db.updateing_fifth_table("RETURNED",returned_categoy.get(),returned_quantity.get(),returned_cost.get(),self.column_5[0])
                                          self.displaying_fifth_table("RETURNED")
                                    else:
                                          messagebox.showwarning("خطأ فى اسم المنتج","تأكد من الصنف")    
                              else:
                                    messagebox.showwarning("خطأ فى كتابة الكمية","تأكد من عدم وجود فراغات")                 
                        else:
                              messagebox.showwarning("خطأ فى كتابة السعر","تأكد من عدم وجود فراغات")       
                  case 7:
                        if intger_pattern_compiled.match(discount_amount.get()):
                              if discount_way.get()==("+") or discount_way.get()==("-"):
                                    if intger_pattern_compiled.match(transaction_id_II.get()):
                                          if action=="add":
                                                db.insertation_fifth_table("DISCOUNT",discount_amount.get(),discount_way.get(),transaction_id_II.get())                         
                                          elif action=="update":
                                                db.updateing_fifth_table("DISCOUNT",discount_amount.get(),discount_way.get(),transaction_id_II.get(),self.column_5[2])
                                          self.displaying_fifth_table("DISCOUNT") 
                                    else:
                                         messagebox.showwarning("تأكد من الخصم","(لا فراغات)يجب ان تكون المدخلات ارقام")       
                              else:
                                    messagebox.showwarning("تأكد من الإشارة","+/- اتجاه الخصم يجب ان يكون ")       
                        else:
                              messagebox.showwarning("تأكد من معرف الفاتورة","(لا فراغات)يجب ان تكون المدخلات ارقام")                                        
            self.clear_fifth_table(table_num)
                        
      def clear_fifth_table(self,table_num):
            match table_num:
                  case 1:
                        payroll_name.set("")
                        payroll_amount.set(0)
                  case 2:
                        the_started_amount.set(0)
                  case 3:
                        customers.set("")     
                  case 4:
                        companies.set("")  
                  case 5:
                        other_name.set("")
                        other_amount.set("")        
                  case 6:
                        returned_categoy.set("") 
                        returned_cost.set(0)
                        returned_quantity.set(0)
                  case 7:
                        discount_amount.set("")
                        discount_way.set("")
                        transaction_id_II.set("")

      def delete_fifth_table(self,table_num):
            match table_num:
                  case 1:
                        db.remove_fifth_table("PAYROLL",self.column_5[0],None)
                        self.displaying_fifth_table("PAYROLL")
                  case 2:
                        db.remove_fifth_table("MAIN_MONEY",None,None)
                        self.displaying_fifth_table("MAIN_MONEY") 
                  case 3:       
                        db.remove_fifth_table("CUSTOMER_DETAILS",None,self.column_5[1])
                        self.displaying_fifth_table("CUSTOMER_DETAILS") 
                  case 4:
                        db.remove_fifth_table("COMPANY_DETAILS",None,self.column_5[1])
                        self.displaying_fifth_table("COMPANY_DETAILS") 
                  case 5:
                        db.remove_fifth_table("OTHER_MONEY",None,self.column_5[0])
                        self.displaying_fifth_table("OTHER_MONEY")
                  case 6:
                        db.remove_fifth_table("RETURNED",None,self.column_5[0])   
                        self.displaying_fifth_table("RETURNED") 
                  case 7:
                        db.remove_fifth_table("DISCOUNT",None,self.column_5[2])         
                        self.displaying_fifth_table("DISCOUNT") 
            self.clear_fifth_table(table_num)
            
      def displaying_fifth_table(self,table):
            self.showing_table_5.delete(*self.showing_table_5.get_children())
            for row in db.fetced_fifth_table(table):
                  self.showing_table_5.insert("",END,values=row)

#-----------------------------


      def payroll(self):
              
            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("550x350+40+40")
            self.child_fifth.title("الرواتب")
            self.child_fifth_frame.place(width=280,height=350)


            worker_label=ttk.Label(self.child_fifth_frame,text="الإسم")
            worker_label.place(x=4,y=40)
            worker_input=ttk.Entry(self.child_fifth_frame,textvariable=payroll_name)
            worker_input.place(x=90,y=40,width=180,height=25)

            the_payroll_label=ttk.Label(self.child_fifth_frame,text="المرتب")
            the_payroll_label.place(x=4,y=100)
            the_payroll_input=ttk.Entry(self.child_fifth_frame,textvariable=payroll_amount)
            the_payroll_input.place(x=90,y=100,width=100,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(1,"add"),takefocus=0)  
            submit_button.place(x=100,y=180,width=90,height=40)

            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(1,"update"),takefocus=0)
            update_button.place(x=40,y=240,width=90,height=40)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(1),takefocus=0)
            delete_button.place(x=160,y=240,width=90,height=40)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=280,width=270,height=351)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="الإسم")
            self.showing_table_5.column("1",anchor=CENTER,width=170)

            self.showing_table_5.heading("2",text="المرتب")
            self.showing_table_5.column("2",anchor=CENTER,width=83)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda e:self.getdata_5(1))
            self.displaying_fifth_table("PAYROLL")


      def started_money(self):
            for widget in self.child_fifth_frame.winfo_children():
                 widget.destroy()

            self.child_fifth.geometry("490x250+80+80")
            self.child_fifth.title("رأس المال")
            self.child_fifth_frame.place(width=300,height=250)

            the_started_amount_label=ttk.Label(self.child_fifth_frame,text="رأس المال")
            the_started_amount_label.place(x=4,y=50)
            the_started_amount_input=ttk.Entry(self.child_fifth_frame,textvariable=the_started_amount)
            the_started_amount_input.place(x=90,y=50,width=120,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(2,"add"),takefocus=0)  
            submit_button.place(x=110,y=110,width=90,height=30)

            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(2,"update"),takefocus=0)
            update_button.place(x=30,y=170,width=90,height=30)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(2),takefocus=0)
            delete_button.place(x=190,y=170,width=90,height=30)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=300,width=190,height=250)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="رأس المال")
            self.showing_table_5.column("1",anchor=CENTER,width=173)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda event:self.getdata_5(2))
            self.displaying_fifth_table("MAIN_MONEY")

      def customer_entered(self):


            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("550x360+40+40")
            self.child_fifth.title("العملاء المسجلين") #!!!!!!!!!!!!!!!!!
            self.child_fifth.resizable(False,False)
            self.child_fifth_frame.place(width=300,height=360)


            customer_label=ttk.Label(self.child_fifth_frame,text="العميل")#!!!!!!!!!!!!!!!!!
            customer_label.place(x=4,y=40)

            customer_input=ttk.Entry(self.child_fifth_frame,textvariable=customers)    #!!!!!!!!!!!!!!!!!
            customer_input.place(x=80,y=40,width=200,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(3,"add"),takefocus=0)  
            submit_button.place(x=100,y=160,width=90,height=40)
      
            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(3,"update"),takefocus=0)
            update_button.place(x=30,y=220,width=90,height=40)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(3),takefocus=0)
            delete_button.place(x=190,y=220,width=90,height=40)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=300,width=250,height=360)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="العميل")
            self.showing_table_5.column("1",anchor=CENTER,width=150)

            self.showing_table_5.heading("2",text="الكود")
            self.showing_table_5.column("2",anchor=CENTER,width=83)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda event:self.getdata_5(3))
            self.displaying_fifth_table("CUSTOMER_DETAILS")
            
      def companie_entered(self):
            

            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()
      
            self.child_fifth.geometry("550x360+40+40")
            self.child_fifth.title("الشركات المسجلة")
            self.child_fifth.resizable(False,False)

            self.child_fifth_frame.place(width=300,height=360)
            company_label=ttk.Label(self.child_fifth_frame,text="الشركة")#!!!!!!!!!!!!!!!!!
            company_label.place(x=4,y=40)

            company_input=ttk.Entry(self.child_fifth_frame,textvariable=companies)
            company_input.place(x=80,y=40,width=200,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(4,"add"),takefocus=0)  
            submit_button.place(x=100,y=160,width=90,height=40)
      
            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(4,"update"),takefocus=0)
            update_button.place(x=30,y=220,width=90,height=40)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(4),takefocus=0)
            delete_button.place(x=190,y=220,width=90,height=40)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=300,width=250,height=360)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="الشركة")
            self.showing_table_5.column("1",anchor=CENTER,width=150)

            self.showing_table_5.heading("2",text="الكود")
            self.showing_table_5.column("2",anchor=CENTER,width=83)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda event:self.getdata_5(4))
            self.displaying_fifth_table("COMPANY_DETAILS")

      def other_money(self):

            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("650x450+40+40")
            self.child_fifth.title("المصروفات الأخري")
            self.child_fifth_frame.place(width=300,height=450)

            worker_label=ttk.Label(self.child_fifth_frame,text="الوصف")
            worker_label.place(x=4,y=40)
            worker_input=ttk.Entry(self.child_fifth_frame,textvariable=other_name)
            worker_input.place(x=100,y=40,width=160,height=25)

            the_quantity_label=ttk.Label(self.child_fifth_frame,text="السعر")
            the_quantity_label.place(x=4,y=100)
            the_quantity_input=ttk.Entry(self.child_fifth_frame,textvariable=other_amount)
            the_quantity_input.place(x=100,y=100,width=160,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(5,"add"),takefocus=0)  
            submit_button.place(x=100,y=280,width=90,height=40)

            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(5,"update"),takefocus=0)
            update_button.place(x=30,y=340,width=90,height=40)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(5),takefocus=0)
            delete_button.place(x=190,y=340,width=90,height=40)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=300,width=350,height=450)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2,3),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="id")
            self.showing_table_5.column("1",anchor=CENTER,width=60)

            self.showing_table_5.heading("2",text="الوصف")
            self.showing_table_5.column("2",anchor=CENTER,width=190)

            self.showing_table_5.heading("3",text="السعر")
            self.showing_table_5.column("3",anchor=CENTER,width=83)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda e:self.getdata_5(5))
            self.displaying_fifth_table("OTHER_MONEY")


      def returned_items(self):

            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("740x400+40+40")
            self.child_fifth.title("المرتجع")
            self.child_fifth_frame.place(width=300,height=400)


            worker_label=ttk.Label(self.child_fifth_frame,text="إسم الصنف")
            worker_label.place(x=4,y=40)
            worker_input=ttk.Combobox(self.child_fifth_frame,textvariable=returned_categoy)
            worker_input['values']=db.category_combobox()
            worker_input.place(x=100,y=40,width=180,height=25)
            
            the_quantity_label=ttk.Label(self.child_fifth_frame,text="الكمية")
            the_quantity_label.place(x=4,y=100)
            the_quantity_input=ttk.Entry(self.child_fifth_frame,textvariable=returned_quantity)
            the_quantity_input.place(x=100,y=100,width=180,height=25)

            the_cost_label=ttk.Label(self.child_fifth_frame,text="السعر")
            the_cost_label.place(x=4,y=160)
            the_cost_input=ttk.Entry(self.child_fifth_frame,textvariable=returned_cost)
            the_cost_input.place(x=100,y=160,width=180,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(6,"add"),takefocus=0)  
            submit_button.place(x=90,y=260,width=100,height=40)

            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(6,"update"),takefocus=0)
            update_button.place(x=20,y=320,width=100,height=40)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(6),takefocus=0)
            delete_button.place(x=180,y=320,width=100,height=40)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=300,width=440,height=400)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2,3,4),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="id")
            self.showing_table_5.column("1",anchor=CENTER,width=60)

            self.showing_table_5.heading("2",text="إسم الصنف")
            self.showing_table_5.column("2",anchor=CENTER,width=200)

            self.showing_table_5.heading("3",text="الكمية")
            self.showing_table_5.column("3",anchor=CENTER,width=80)

            self.showing_table_5.heading("4",text="السعر(ك)")
            self.showing_table_5.column("4",anchor=CENTER,width=83)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda e:self.getdata_5(6))
            worker_input.bind("<Button-1>",lambda e:worker_input.config(values=db.category_suggestion(worker_input.get())))
            self.displaying_fifth_table("RETURNED")

      def discount_win(self):

            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("420x300+40+40")
            self.child_fifth.title("الخصومات")
            self.child_fifth_frame.place(width=230,height=300)

            worker_label=ttk.Label(self.child_fifth_frame,text="الخصم")
            worker_label.place(x=4,y=30)
            worker_input=ttk.Entry(self.child_fifth_frame,textvariable=discount_amount)
            worker_input.place(x=80,y=30,width=100,height=25)

            the_quantity_label=ttk.Label(self.child_fifth_frame,text="الإتجاة")
            the_quantity_label.place(x=4,y=90)
            the_quantity_input=ttk.Combobox(self.child_fifth_frame,textvariable=discount_way,values=("+","-"))
            the_quantity_input.place(x=80,y=90,width=100,height=25)

            the_cost_label=ttk.Label(self.child_fifth_frame,text=" الفاتورة")
            the_cost_label.place(x=4,y=150)
            the_cost_input=ttk.Entry(self.child_fifth_frame,textvariable=transaction_id_II)
            the_cost_input.place(x=80,y=150,width=100,height=25)

            submit_button=ttk.Button(self.child_fifth_frame,text="حفظ",command=lambda:self.add_update_fifth_table(7,"add"),takefocus=0)  
            submit_button.place(x=60,y=200,width=90,height=35)

            update_button=ttk.Button(self.child_fifth_frame,text="تعديل",command=lambda:self.add_update_fifth_table(7,"update"),takefocus=0)
            update_button.place(x=10,y=240,width=90,height=35)

            delete_button=ttk.Button(self.child_fifth_frame,text="حذف",command=lambda:self.delete_fifth_table(7),takefocus=0)
            delete_button.place(x=120,y=240,width=90,height=35)

            data_tables_5=ttk.Frame(self.child_fifth)
            data_tables_5.place(x=230,width=190,height=301)

            scroll_5=Scrollbar(data_tables_5)
            scroll_5.pack(side=RIGHT,fill=Y)

            self.showing_table_5=ttk.Treeview(data_tables_5,column=(1,2,3),height=14,takefocus=0,yscrollcommand=scroll_5.set)

            self.showing_table_5.heading("1",text="الخصم")
            self.showing_table_5.column("1",anchor=CENTER,width=60)

            self.showing_table_5.heading("2",text="اتجاة")
            self.showing_table_5.column("2",anchor=CENTER,width=60)

            self.showing_table_5.heading("3",text="الفاتورة")
            self.showing_table_5.column("3",anchor=CENTER,width=60)

            self.showing_table_5['show']= 'headings'
            self.showing_table_5.pack()
            scroll_5.config(command=self.showing_table_5.yview)

            self.showing_table_5.bind("<ButtonRelease-1>",lambda e:self.getdata_5(7))
            self.displaying_fifth_table("DISCOUNT")


      

      def refreshs(self):
            self.refresh_statistic_button.invoke()
            self.refresh_statistic_button_1.invoke()
            self.payroll_sum.config(text=f"{db.payroll_money_sum()}:المرتبات")
            self.payroll_sum.config(text=f"{db.main_money_sum()}:رأس المال")
            self.payroll_sum.config(text=f"{db.other_money_sum()}:مصاريف أخري")
            self.payroll_sum.config(text=f"{db.sum_of_all()}:المكسب")

      def statistics(self):
            for widget in self.child_fifth_frame.winfo_children():
                  widget.destroy()

            self.child_fifth.geometry("700x350+80+80")
            self.child_fifth.title("الإحصائات")
            self.child_fifth_frame.place(x=0,y=0,width=350,height=200)
            self.child_fifth_frame_2=ttk.Frame(self.child_fifth)
            self.child_fifth_frame_2.place(x=350,y=0,width=350,height=200)
            self.child_fifth_frame_3=ttk.Frame(self.child_fifth)
            self.child_fifth_frame_3.place(x=0,y=200,width=700,height=150)
            
            main_money_labels=(" : إجمالى المديونية"," : إجمالى المدفوع",": المتبقى")
            main_money_functions=(db.main_money_debts_sum()[0],db.main_money_debts_sum()[1],db.main_money_debts_sum()[2])
            self.statistics_label_frame,self.v1,self.v2,self.v3,self.v4,self.refresh_statistic_button=statistic_sum(self.child_fifth_frame).statistic_frame(main_money_labels,main_money_functions,"default")
            self.statistics_label_frame.pack(side='top',fill='both',expand=True)   
            self.v1.config(relief='groove',border=3)
            self.v2.config(relief='groove',border=3)
            self.v3.config(relief='groove',border=3)
            self.refresh_statistic_button.place_forget()

            main_money_labels=(" : إجمالي مخزن"," : إجمالي الوارد",": إجمالي الصادر",": إجمالي(م)الحالى")
            main_money_functions=(db.sum_category_storage_cost(),db.sum_category_entered_cost(),db.sum_category_out_cost(),db.sum_category_current_cost())
            self.statistics_label_frame_1,self.v1_1,self.v2_1,self.v3_1,self.v4_1,self.refresh_statistic_button_1=statistic_sum(self.child_fifth_frame_2).statistic_frame(main_money_labels,main_money_functions,"category_details")
            self.statistics_label_frame_1.pack(side='top',fill='both',expand=True) 
            self.v1_1.config(relief='groove',border=3)
            self.v2_1.config(relief='groove',border=3)
            self.v3_1.config(relief='groove',border=3)
            self.v4_1.config(relief='groove',border=3)
            self.refresh_statistic_button_1.place_forget()

                  
            self.stastisctic_label_frame_bottom=ttk.Labelframe(self.child_fifth_frame_3,text="إحصائيات",labelanchor='n',relief='groove',takefocus=0)
            self.stastisctic_label_frame_bottom.pack(side='bottom',fill='both',expand=True)
  
            self.payroll_sum=ttk.Label(self.stastisctic_label_frame_bottom,text=f"{db.payroll_money_sum()}:المرتبات")
            self.payroll_sum.place(x=20,y=15)

            self.main_sum=ttk.Label(self.stastisctic_label_frame_bottom,text=f"{db.main_money_sum()}:رأس المال")
            self.main_sum.place(x=150,y=45)

            self.other_sum=ttk.Label(self.stastisctic_label_frame_bottom,text=f"{db.other_money_sum()}:مصاريف أخري")
            self.other_sum.place(x=280,y=15)

            self.sum_of_sum=ttk.Label(self.stastisctic_label_frame_bottom,text=f"{db.sum_of_all()}:المكسب")
            self.sum_of_sum.place(x=150,y=85)

            self.main_resfresh_button=ttk.Button(self.stastisctic_label_frame_bottom,command=refresh)
            self.main_resfresh_button.place(x=630,y=40,width=50,height=35)

      

#-------------------------------main_window_functions----------------------------------

#======== main_window_buttons ======== 
menubar=Menu(page,type='menubar')     #make menubar background

file=Menu(menubar,tearoff=False)         
menubar.add_cascade(label='file',menu=file)      # add horizentel buttons
file.add_command(label ='Save', command =backup)      # add (menu)option to horizentel buttons 
file.add_separator()
file.add_command(label ='Exit', command = page.destroy)



submit_button = ttk.Button(seller_frame, text="حفظ",command=add)#lambda:checking_stock("add")
submit_button.place(x=160, y=430, width=110, height=40)

update_button = ttk.Button(seller_frame, text="تعديل",command=updateing)#lambda:checking_stock("update")
update_button.place(x=95, y=480, width=110, height=40)

delete_button = ttk.Button(seller_frame, text="حذف",command=delete)#lambda:checking_stock("delete")
delete_button.place(x=220, y=480, width=110, height=40)

transaction_id_search_button = ttk.Button(seller_frame, text="فتح",command=displayall_transaction_id)
transaction_id_search_button.place(x=66, y=429, width=30, height=30)

searching_button = ttk.Button(seller_frame, text="البحث",command=pop_all_searching_functions_window)
searching_button.place(x=230, y=530, width=90, height=40)

sorting_option=StringVar()
sorting_option_all={"","ابحث بإستخدام الشركة","ابحث بإستخدام الموزع"}
sorting_search_button=ttk.OptionMenu(seller_frame,sorting_option,*sorting_option_all,command=search_sorting_func)
sorting_search_button.place(x=6,y=4)

path_1=r"./icons/sync.png"
image_1=photo_resizing(path_1)

refresh_button = ttk.Button(seller_frame,image=image_1,command=refresh)
refresh_button.place(x=295, y=1, width=35, height=35)

others_button = ttk.Button(seller_frame, text="أخرى",command=other_windows)
others_button.place(x=230, y=590, width=100, height=40)
#======= main_window_data-table =======

data_tables =ttk.Frame(page)
data_tables.place(x=340,width=940,height=637) #table width     --1

scroll=Scrollbar(data_tables)
scroll.pack(side=RIGHT,fill=Y) 

showing_table=ttk.Treeview(data_tables,columns=(1,2,3,4,5,6,7,8,9,10,11),takefocus=0,yscrollcommand=scroll.set,show='headings') #table hight

showing_table.heading("1",text="id")
showing_table.column("1",anchor=W,width=40)

showing_table.heading("2",text=" العميل")
showing_table.column("2",anchor=CENTER,width=130)

showing_table.heading("3",text=" الشركة")
showing_table.column("3",anchor=CENTER,width=130)

showing_table.heading("4",text="اسم الصنف")                 
showing_table.column("4",anchor=CENTER,width=180)           #sum of all column must = width of table   --1
 
showing_table.heading("5",text="كمية")
showing_table.column("5",anchor=CENTER,width=60)

showing_table.heading("6",text="النوع")
showing_table.column("6",anchor=CENTER,width=60)

showing_table.heading("7",text="سعر الواحدة")
showing_table.column("7",anchor=CENTER,width=70)

showing_table.heading("8",text="السعر الكلى")
showing_table.column("8",anchor=CENTER,width=80)

showing_table.heading("9",text="فاتورة")
showing_table.column("9",anchor=CENTER,width=40)

showing_table.heading("10",text="الدفع")
showing_table.column("10",anchor=CENTER,width=30)

showing_table.heading("11",text="التاريخ")
showing_table.column("11",anchor=CENTER,width=100)  # scroll size is 19

scroll.config(command=showing_table.yview)        
showing_table.pack(fill=BOTH, expand=True)
page.config(menu = menubar)

showing_table.bind("<ButtonRelease-1>",getdata)

product_name_input.bind("<<ComboboxSelected>>",auto_measure_select)

displayall()
error_detect()
page.mainloop()

