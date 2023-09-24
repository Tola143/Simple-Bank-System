from tkinter import *
from tkinter import ttk, Button
from time import *
import webbrowser
import datetime
import os
import sqlite3 as sql

# folder_receipt ="C:\\Users\ASUS\\OneDrive - kmutnb.ac.th\\Documents\\Python\\Assignment\\GUI\\Customer_Receipt\\{}.txt"
folder_receipt = os.path.join(os.path.dirname(__file__), "Customer_Receipt\\{}.txt")
url = 'https://www.facebook.com/litayong.kantola'
dbcon = sql.connect('customer_data.db')
cur = dbcon.cursor()

menu = {'                                   Milk Tea Category' : None,
        "1, Taiwan Milk Tea = 19B": 19,
        "2, Coffee Milk Tea = 19B": 19,
        "3, Cocoa Milk Tea = 19B": 19,
        "4, Taro Milk Tea = 24B": 24,
        "5, Lychee Milk Tea = 19B": 19,
        "6, Melon Milk Tea = 19B": 19,
        "7, Strawberry Milk Tea = 19B": 19,
        "8, Apple Milk Tea = 19B": 19,
        "9, Caramel Milk Tea = 19B": 19,
        "10, Vanilla Milk Tea = 19B": 19,
        "11, Honey Milk Tea = 19B": 19,

        '                                   Fresh Milk Category': None,
        "12, Fresh milk with Brown Sugar Sauce = 24B":24,
        "13, Fresh milk = 24B":24,
        "14, Caramel Fresh milk = 39B":39,
        "15, Honey Fresh milk = 34B":34,
        "16, Fresh milk  with Brown Sugar Pearl = 34B":34,

        '                                       Soda Category': None,
        "17, Strawberry Soda = 19B":19,
        "18, Sala Soda = 19B":19,
        "19, Sala Lemon Soda = 19B":19,
        "20, Lychee Soda = 19B":19,
        "21, Apple Soda = 19B":19,
        "22, Melon Soda = 19B":19,
        "23, Lemon Soda Soda = 19B":19
        }

def login():
    canvas.pack_forget()
    login_button.grid_forget()
    create_acc_button.grid_forget()

    password_entry.config(show='*')

    user_email_label.grid(row=1, column=0, pady=10)
    user_email_entry.grid(row=1, column=1, pady=10)
    password.grid(row=2, column=0, pady=10)
    password_entry.grid(row=2, column=1, pady=10)
    show_button.grid(row=2, column=2, pady=10)
    back_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
    start_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

def create_acc():
    canvas.pack_forget()
    login_button.grid_forget()
    create_acc_button.grid_forget()

    show_button.config(text='Hide')

    user_email_label.grid(row=1, column=0, pady=10)
    user_email_entry.grid(row=1, column=1, pady=10)
    password.grid(row=2, column=0, pady=10)
    password_entry.grid(row=2, column=1, pady=10)
    show_button.grid(row=2, column=2, pady=10)
    back_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
    create_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

def update():
    time_string = strftime('%I:%M:%S %p')
    time_label.config(text=time_string)

    day_string = strftime('%A')
    day_label.config(text=day_string)

    date_string = strftime('%B %d, %Y')
    date_label.config(text=date_string)

    canvas.after(1000,update)

global hide
hide = True
def show_hide(is_hide):
    global hide
    hide = is_hide
    if hide:
        password_entry.config(show='')
        hide = False
    else:
        password_entry.config(show='*')
        hide = True

def back():
    user_email_label.grid_forget()
    user_email_entry.grid_forget()
    password_entry.grid_forget()
    password.grid_forget()

    create_button.grid_forget()
    start_button.grid_forget()
    show_button.grid_forget()
    back_button.grid_forget()

    warning_label.grid_forget()

    greeting_label.grid(row=0, column=0, columnspan=2)
    login_button.grid(row=1, column=0, pady=20)
    create_acc_button.grid(row=1, column=1, pady=20)
    canvas.pack()

def start():
    cu_email = str(user_email_entry.get())
    cu_password = str(password_entry.get())
    sql = "SELECT* FROM customer WHERE cu_email=?"
    val = (cu_email,)
    cur.execute(sql,val)
    recorde = cur.fetchall()
    if cu_password == recorde[0][1]:
        print(recorde[0])
        user = str(user_email_entry.get())          # get user email(name) from entry.
        file_name = folder_receipt.format(user)     # user data in text file.
        if os.path.exists(file_name):
            with open(file_name, "r") as receipt:
                data_customer = receipt.readlines()
                for i in  range(len(data_customer)):
                    pro_history.insert(i,data_customer[i].strip())
        else:
            pro_history.insert(0,'NO DATA')         # show all user data in list box.

        dbcon.close()
        frame1.pack()
        frame2.pack(pady=10)
        frame.pack_forget()

    elif cu_password != recorde[0][1]:
        warning_label.grid(row=4, column=0, columnspan=2, pady=20)

def create():
    cu_email = str(user_email_entry.get())
    cu_password = str(password_entry.get())
    sql = """
         INSERT INTO customer(cu_email, cu_password)
         VALUES(?,?)
         """
    val = (cu_email,cu_password)
    cur.execute(sql,val)
    dbcon.commit()
    dbcon.close()

    frame.pack_forget()
    frame1.pack()
    frame2.pack(pady=10)

def enter(event):
    start()
    print(event.keysym)

def order():
    data = []
    date = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    order = ''
    amount = int(amount_entry.get())
    user = str(user_email_entry.get())
    file_name = folder_receipt.format(user)
    if os.path.exists(file_name):
        with open(file_name, "r") as receipt:
            data_customer = receipt.readlines()  # list data
            last = len(data_customer)  # get last data
            row = last + 1
            for i in milk_tea_category.curselection():
                name = milk_tea_category.get(i)
                price = menu.get(name)
                total = amount * price
                data.append(milk_tea_category.get(i))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(row, name, amount, total, date)
                order += text
                history.insert(i,text.strip())

            for j in fresh_milk_category.curselection():
                name = fresh_milk_category.get(j)
                price = menu.get(name)
                total = amount*price
                data.append(fresh_milk_category.get(j))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(row, name, amount, total, date)
                order += text
                history.insert(j, text.strip())

            for k in soda_category.curselection():
                name = soda_category.get(k)
                price = menu.get(name)
                total = amount * price
                data.append(soda_category.get(k))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(row, name, amount, total, date)
                order += text
                history.insert(k, text.strip())

        with open(file_name,'a') as reciept:
            reciept.write(order)

    else:
        with open(file_name, 'a') as reciept:
            for i in milk_tea_category.curselection():
                name = milk_tea_category.get(i)
                price = menu.get(name)
                total = amount * price
                data.append(milk_tea_category.get(i))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(1, name, amount, total, date)
                order += text
                history.insert(i, text.strip())

            for j in fresh_milk_category.curselection():
                name = fresh_milk_category.get(j)
                price = menu.get(name)
                total = amount * price
                data.append(fresh_milk_category.get(j))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(1, name, amount, total, date)
                order += text
                history.insert(j, text.strip())

            for k in soda_category.curselection():
                name = soda_category.get(k)
                price = menu.get(name)
                total = amount * price
                data.append(soda_category.get(k))
                text = 'NO:{} Item: {}  Amount: {} Total: {}B Date: {}\n'.format(1, name, amount, total, date)
                order += text
                history.insert(k, text.strip())

            reciept.write(order)

    for i in data:
        print(i)

def open_web(e):
    webbrowser.open_new(url)

def finish():
    frame1.pack_forget()
    frame2.pack_forget()

    thank_msg.pack(pady=30)
    bye_button.pack()
    label_web.pack(pady=20)
    canvas.pack(pady=10)
    # canvas.place(x=180, y=220)

window = Tk()
window.geometry('600x400')
window.title('ToLA_GUI2')
window.config(bg='#edbc40')

window.bind("<Return>",enter)   # keyboard event "enter"

#part1
frame = Frame(window,bg='#edbc40')
frame.pack(pady=30)

greeting_label = Label(frame,text='ToLA welcome',font = ("Arail",20),padx=100,pady=10,bd=1, relief=RAISED,bg='#f54242',fg='white')
warning_label = Label(frame, bg='#edbc40',fg='red', font = ("Arail",12), text='Wrong password,\nPlease log in again!')
login_button: Button = Button(frame,text='Log in',bg='light yellow',font = ('Arial', 15,'bold'),command=login)
create_acc_button = Button(frame,text='Create account',bg='light yellow',font = ('Arial', 15,'bold'),command=create_acc)

greeting_label.grid(row=0,column=0,columnspan=2)
login_button.grid(row=1,column=0,pady=20)
create_acc_button.grid(row=1,column=1, pady=20)

# clock
canvas = Canvas(window,bg='white',bd=3)
canvas.pack(pady=0)
# canvas.place(x=180,y=210)
time_label = Label(canvas, font=("Arail",30),bg='black',fg='orange')
time_label.pack(pady=5)

day_label = Label(canvas, font=("Ink free",20),bg='#f54242',fg='white')
day_label.pack()

date_label = Label(canvas, font=("Arail",20),bg='white')
date_label.pack()
update()    # clock function

user_email_label = Label(frame, text='User Email', bg='#edbc40', font = ('Arial', 15, 'bold'))
user_email_entry = Entry(frame, width=20, font = ('Arial', 15, 'bold'))
password = Label(frame,text='Password',bg='#edbc40',font = ('Arial', 15,'bold'))
password_entry = Entry(frame,width=20,font = ('Arial', 15,'bold'))

show_button = Button(frame,text='Show',font = ('Arial', 6,'bold'), pady=5, bg='#63dff2',command=lambda: show_hide(hide))
back_button = Button(frame,text='Back',font = ('Arial', 10,'bold'),bg='#63dff2',command=back)
start_button = Button(frame,text='Start',font = ('Arial', 15,'bold'),bg='#63dff2',command=start)
create_button = Button(frame,text='Create',font = ('Arial', 15,'bold'),bg='#63dff2',command=create)

#part2
frame1 = Frame(window,bg='#edbc40')

label = Label(frame1,text='ToLA MeNU',font = ("Arail",12),padx=220,pady=10,bd=1, relief=RAISED,bg='#f54242',fg='white')
label.pack(pady=10)
notebooks = ttk.Notebook(frame1)

milk_tea = Frame(notebooks,padx=20,pady=10,bg='#c3fa84')
fresh_milk = Frame(notebooks,padx=20,pady=10,bg='#82acf5')
soda = Frame(notebooks,padx=20,pady=10,bg='#f279fc')
order_earlier = Frame(notebooks,padx=20,pady=10,bg='#f26378')
order_history = Frame(notebooks,padx=20,pady=10,bg='#f26378')

notebooks.add(milk_tea,text='          Milk Tea          ')     #add frame(tab1) to notebook
notebooks.add(fresh_milk,text='           Fresh Milk        ')     #add frame(tab2) to notebook
notebooks.add(soda,text='            Soda            ')
notebooks.add(order_earlier,text='            Your Order          ')
notebooks.add(order_history,text='             Your History          ')
notebooks.pack(expand=True, fill='both')    #expand = expand to fill any space not otherwide use
#                                                     #fill = fill on space x and y axis

keys_menu = list(menu.keys())
milk_tea_category = Listbox(milk_tea,width=50, height=12,font = ("Arail",12), bg='light yellow',selectmode=MULTIPLE)
for i in range(0,12):
    milk_tea_category.insert(i,keys_menu[i])

fresh_milk_category = Listbox(fresh_milk,width=50, height=12,font = ("Arail",12), bg='light yellow',selectmode=MULTIPLE)
for i in range(12,18):
    fresh_milk_category.insert(i,keys_menu[i])

soda_category = Listbox(soda,width=50, height=12,font = ("Arail",12), bg='light yellow', selectmode=MULTIPLE)
for i in range(18,26):
    soda_category.insert(i,keys_menu[i])

history = Listbox(order_earlier,width=100, height=13,font = ("Arail",10), bg='light yellow', selectmode=MULTIPLE)
pro_history = Listbox(order_history,width=100, height=13,font = ("Arail",10), bg='light yellow', selectmode=MULTIPLE)

scrollbar = Scrollbar(order_history,command=pro_history.yview)
pro_history.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill =Y)

milk_tea_category.pack()
fresh_milk_category.pack()
soda_category.pack()
history.pack()
pro_history.pack()

# bottom part2
frame2 = Frame(window,bg='#40c2ed',padx=10,pady=5)

amount_label= Label(frame2,text='Amount',bg='#f54c5a',fg='white',font = ("Arail",12)).grid(row=0,column=0,padx=10)
amount_entry = Entry(frame2,font = ("Arail",12))
amount_entry.insert(0,'1')
amount_entry.grid(row=0,column=1,padx=0)
order_button = Button(frame2,text='Order',bg='#c3fa84',font = ("Arail",12),command=order).grid(row=0,column=3,padx=30)
finish_button = Button(frame2,text='Finish',bg='#fcf27c',font = ("Arail",12),command=finish).grid(row=0,column=4,padx=10)

thank_msg= Label(window, bg='#edbc40', font = ("Arail",20),fg='white', text='Please come back again next time\nThank for your support.')
bye_button = Button(window,text='BYE BYE',bg='#fcf27c',font = ("Arail",12),command=exit)

# open website
label_web = Label(window, text=f'Contact us: {url}', fg='blue',bg='#edbc40',font = ("Arail",12))
label_web.bind("<Button-1>",open_web)
window = mainloop()