from tkinter import *
from tkinter import messagebox
from datetime import date,datetime,timedelta
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="LibOm1"
)
mycursor = mydb.cursor()


root=Tk()
root.title("LibOm")
count=0


def clear_root():
    widgets = root.winfo_children()
    for widget in widgets:
        widget.destroy()
    #creating buttons
    add_button=Button(root,text="Add",command=lambda:addbook())
    delete_button=Button(root,text="Delete",command=lambda:delbook())
    issue_button=Button(root,text="Issue",command=lambda:issuebook())
    return_button=Button(root,text="Return",command=lambda:returnbook())
    pending_button=Button(root,text="Pending",command=lambda:pending())
    view_button=Button(root,text="View_Records",command=lambda:viewrecords())

    #putting buttons on screen
    add_button.grid(row=0,column=0,sticky="ew")
    delete_button.grid(row=0,column=1,sticky="ew")
    issue_button.grid(row=0,column=2,sticky="ew")
    return_button.grid(row=0,column=3,sticky="ew")
    pending_button.grid(row=0,column=4,sticky="ew")
    view_button.grid(row=0,column=5,sticky="ew")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.grid_columnconfigure(5, weight=1)

def setup(function):
    
    if function=="add":
        addbook()
    elif function=="delete":
        delbook()
    elif function=="return":
        returnbook()
    elif function=="pending":
        pending()
    elif function=="viewrecords":
        viewrecords()
    else:
        issuebook()

#MAIN_FUNTION-1 : TO ADD BOOK IN THE LIBRARY
def addbook():
    clear_root()
    #book name
    global count
    label=Label(root,text="Book's Name: ** ",height=3).grid(row=1,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=1,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #author's name
    label2=Label(root,text="Author's Name: ",height=3).grid(row=2,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #quantity
    label3=Label(root,text="Quantity: **",height=3).grid(row=3,column=0,sticky='ew')
    box3=Entry(root)
    box3.insert(0,"ONLY DIGITS")
    box3.grid(row=3,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    
    #status bar
    status=Label(root,text="Book: "+str(count+1),bd=1,relief=SUNKEN,anchor=E)
    status.grid(row=5,column=0,columnspan=4,sticky="ew",pady=30)
    #submit button
    submit_add=Button(root,text="SUBMIT",bg="red",command=lambda:submit_entry(box1,box2,box3,status))
    submit_add.grid(row=4,column=0,padx=100)
    
    return
#Subfunctions of addbook()
def submit_entry(box1,box2,box3,status):
    global count
    if box1.get() and (box3.get().isdigit()):
        if box2.get()=="":
            box2.insert(0,"unknown")
        sql = "INSERT INTO BOOKS (BookName, AuthorName,Quantity) VALUES (%s, %s, %s)"
        val = (box1.get(), box2.get(),box3.get())
        mycursor.execute(sql, val)
        mydb.commit()
        count += 1
        status=Label(root,text="Book: "+str(count+1),bd=1,relief=SUNKEN,anchor=E)
        status.grid(row=5,column=0,columnspan=4,sticky="ew",pady=30)
        setup("add")
    
    else:
         messagebox.showwarning("Error", "Please fill in all fields appropriately.")


#MAIN_FUNCTION-2: DELETE BOOKS FROM TTHE LIBRARY
def delbook():
    clear_root()
    #book name
    label=Label(root,text="Book's Name: ",height=3).grid(row=1,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=1,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #authors name
    label2=Label(root,text="Author's Name: ",height=3).grid(row=2,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)

    ques=Label(root,text="How many copies would you like to delete?",height=3).grid(row=3,column=0,columnspan=3,sticky="ew")
    opt=IntVar()
    Radiobutton(root,text="Some Copies",variable=opt,value=2).grid(row=5,column=0,sticky="e")
    Radiobutton(root,text="All Copies",variable=opt,value=1).grid(row=5,column=2,sticky="w")
    del_button=Button(root,text="DELETE",command=lambda:choice(opt.get(),box1.get(),box2.get()))
    del_button.grid(row=6,column=1,sticky="ew")
    return
#Subfunctions of deletebook()
def choice(option,book,aut):#allows user to delete all or few copies of the entered book
    if book and aut:
        sql="SELECT * FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME=%s"
        mycursor.execute(sql,(book,aut))
        rows=mycursor.fetchall()
        mydb.commit
        
        if(len(rows)==0):#book is not present in the library
            messagebox.showwarning("Error","No such book exists in the database!!")
        else:
            if option==1:#delete all copies of the book
                sql="DELETE FROM BOOKS WHERE BOOKNAME =%s AND AUTHORNAME = %s"
                mycursor.execute(sql,(book,aut))
                mydb.commit()
                messagebox.showinfo("Delete Books","All copies of "+book+" by "+aut+" are deleted")
                setup("delete")
            else:#delete few copies of the book
                num=Label(root,text="Enter no. of copies to be deleted: ",height=3).grid(row=8,column=0,sticky="ew")
                box10=Entry(root)
                box10.insert(0,"ONLY DIGITS")
                box10.grid(row=8,column=1,sticky="ew")
                sql="SELECT QUANTITY FROM BOOKS WHERE BOOKNAME =%s AND AUTHORNAME=%s"
                mycursor.execute(sql,(book,aut))
                
                quan=mycursor.fetchall()
                mydb.commit()
                
                button=Button(root,text="delete",bg="red",command=lambda:update_books(quan[0],box10.get(),book,aut))
                button.grid(row=8,column=2,sticky="ew")            
    else:#displays message if all boxes are not properly filled
        messagebox.showwarning("Error!","Please fill in all the fields appropriately!")
        
def update_books(prev,new,book,aut):#updates stock of books
    if new.isdigit():
        if int(new)>prev[0]:
            messagebox.showwarning("Error","ONLY "+str(prev)+" COPIES OF THIS BOOK ARE AVAILABLE IN STOCK")
        else:
            sql="UPDATE BOOKS SET QUANTITY=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            mycursor.execute(sql,(prev[0]-int(new),book,aut))
            mydb.commit()

            messagebox.showinfo("Delete Books",new+"copies of "+book+" by "+aut+" are deleted")
            setup("delete")
    else:
        messagebox.showwarning("Error","Please enter digits!!")
    return

#MAIN_FUNCTION-3: TO ISSUE A BOOK TO THE CUSTOMER
def issuebook():
    clear_root()
    #book name
    label=Label(root,text="Book's Name: ",height=3).grid(row=1,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=1,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #authors name
    label2=Label(root,text="Author's Name: ",height=3).grid(row=2,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #customer's name
    label3=Label(root,text="Customer's Name: ",height=3).grid(row=3,column=0,sticky='ew')
    box3=Entry(root)
    box3.grid(row=3,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #contact no
    label4=Label(root,text="Contact no: ",height=3).grid(row=4,column=0,sticky='ew')
    box4=Entry(root)
    box4.insert(0,"ONLY DIGITS")
    box4.grid(row=4,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #date of issue
    today=date.today()
    label4=Label(root,text="Date: ",height=3).grid(row=5,column=0,sticky="ew")
    box_date=Entry(root)
    box_date.insert(0,date.today().day)
    box_date.grid(row=5,column=1,sticky="ew")
    label5=Label(root,text="Month: ",height=3).grid(row=5,column=2,sticky="ew")
    box_month=Entry(root)
    box_month.insert(0,date.today().month)
    box_month.grid(row=5,column=3,sticky="ew")
    label6=Label(root,text="Year: ",height=3).grid(row=5,column=4,sticky="ew")
    box_year=Entry(root)
    box_year.insert(0,date.today().year)
    box_year.grid(row=5,column=5,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_columnconfigure(3,weight=1)
    root.grid_columnconfigure(4,weight=1)
    root.grid_columnconfigure(5,weight=1)
        #submit
    submit_issue=Button(root,text="ISSUE",bg="red",command=lambda:issue_entry(box1.get(),box2.get(),box3.get(),box4.get(),box_date.get(),box_month.get(),box_year.get()))
    submit_issue.grid(row=6,column=6,columnspan=4,sticky="ew")
    return
#Subfinctions of issuebook()
def issue_entry(book,aut,cust,cont,date,month,year):
        sql="SELECT * FROM PENDING WHERE CONTACT=%s"#view pending dues of the customer
        mycursor.execute(sql,(cont,))
        rows=mycursor.fetchall()
        mydb.commit()
        if len(rows)!=0:#display warning message if fine is pending
            sql="SELECT FINE FROM PENDING WHERE CONTACT=%s"
            mycursor.execute(sql,(cont,))
            amt=int((mycursor.fetchone())[0])
            mydb.commit()
            messagebox.showwarning("Due Fine","Your fine of amt Rs. "+amt+" is due")
        else:#issue the book and remove 1 from the stock
            if book and aut and cust and cont:
                sql="SELECT QUANTITY FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME =%s"
                mycursor.execute(sql,(book,aut))
                rows=mycursor.fetchall()
                mydb.commit()
                if len(rows)==0 or rows[0][0]==0:
                    messagebox.showwarning("Error","BOOK IS NOT IN STOCK")
                else:
                    if len(str(cont))<10:
                        messagebox.showwarning("Error","INVALID MOBILE NUMBER")
                    else:
                        sql="INSERT INTO ISSUE (BOOKNAME,AUTHORNAME,CUSTOMER,CONTACT,DATE_OF_ISSUE) VALUES (%s,%s,%s,%s,%s)"
                        mycursor.execute(sql,(book,aut,cust,int(cont),date+"-"+month+"-"+year))
                        mydb.commit()
                        #remove from books table
                        sql="SELECT QUANTITY FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME=%s"
                        mycursor.execute(sql,(book,aut))
                        rows=mycursor.fetchall()
                        quan=int(rows[0][0])
                        mydb.commit()
                        sql="UPDATE BOOKS SET QUANTITY=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
                        mycursor.execute(sql,(quan-1,book,aut))
                        mydb.commit()
        

            else:
                messagebox.showwarning("Error","Please fill in all fields appropriately!")
        setup("issue")
        return 
#MAIN_FUNCTION-4: TO KEEP TRACK OF RETURNED BOOKS AND FINE  
def returnbook():
    
    clear_root()
    label1=Label(root,text="Contact no.",height=3).grid(row=1,column=0,sticky="ew")
    box=Entry(root)
    box.grid(row=1,column=1,columnspan=3,sticky="ew")
    
    
    global submit
    submit=Button(root,text="SUBMIT",command=lambda:return_entry(box.get()))#user will feed contact no and rest will be shown
    submit.grid(row=8,column=1,sticky="ew")                                 #the system
#Subfunctions of returnbook()
def return_entry(cont):#it will give contact no. of the reader of issued book
    
    global submit
    submit.destroy()#remove the submit button from the return window
    
    sql="SELECT * FROM ISSUE WHERE CONTACT=%s"#to display ret of the information
    val=int(cont)
    mycursor.execute(sql,(val,))
    rows=mycursor.fetchall()
    mydb.commit()
    #display book_name
    
    label2=Label(root,text="Book Name:",height=3).grid(row=2,column=0,sticky="ew")
    box2=Entry(root)
    box2.insert(0,rows[0][0])
    box2.grid(row=2,column=1,columnspan=3,sticky="ew")
    #display author_name
    label3=Label(root,text="Author Name",height=3).grid(row=3,column=0,sticky="ew")
    box3=Entry(root)
    box3.insert(0,rows[0][1])
    box3.grid(row=3,column=1,columnspan=3,sticky="ew")
    #diplay customer_name
    label4=Label(root,text="Customer Name:",height=3).grid(row=4,column=0,sticky="ew")
    box4=Entry(root)
    box4.insert(0,rows[0][2])
    box4.grid(row=4,column=1,columnspan=3,sticky="ew")
    
    #display return date i.e. current date
    today=date.today()
    #date
    label_date=Label(root,text="Date: ",height=3).grid(row=5,column=0,sticky="ew")
    box_date=Entry(root)
    box_date.insert(0,date.today().day)
    box_date.grid(row=5,column=1,sticky="ew")
    #month
    label_month=Label(root,text="Month: ",height=3).grid(row=5,column=2,sticky="ew")
    box_month=Entry(root)
    box_month.insert(0,date.today().month)
    box_month.grid(row=5,column=3,sticky="ew")
    #year
    label_year=Label(root,text="Year: ",height=3).grid(row=5,column=4,sticky="ew")
    box_year=Entry(root)
    box_year.insert(0,date.today().year)
    box_year.grid(row=5,column=5,sticky="ew")
    #insert return date into the table "issue"
    sql="UPDATE ISSUE SET  DATE_OF_RETURN =%s WHERE CONTACT=%s"
    dateofreturn=str(date.today().day)+"-"+str(date.today().month)+"-"+str(date.today().year)
    mycursor.execute(sql,(dateofreturn,val))
    mydb.commit()
    #display date of issue
    date1=rows[0][4]
    date_obj=datetime.strptime(date1,"%d-%m-%Y")
    date2=date_obj.strftime("%d")
    month=date_obj.strftime("%m")
    year=date_obj.strftime("%Y")
    #date
    label_d=Label(root,text="DATE OF ISSUE: ").grid(row=6,column=0,sticky="ew")
    label_d=Label(root,text="Date: ",height=3).grid(row=7,column=0,sticky="ew")
    box_d=Entry(root)
    box_d.insert(0,date2)
    box_d.grid(row=7,column=1,sticky="ew")
    #month
    label_m=Label(root,text="Month: ",height=3).grid(row=7,column=2,sticky="ew")
    box_m=Entry(root)
    box_m.insert(0,month)
    box_m.grid(row=7,column=3,sticky="ew")
    #year
    label_y=Label(root,text="Year: ",height=3).grid(row=7,column=4,sticky="ew")
    box_y=Entry(root)
    box_y.insert(0,year)
    box_y.grid(row=7,column=5,sticky="ew")
    
    sql="SELECT * FROM ISSUE WHERE CONTACT=%s"#select return issue and return date from the table "issue"
    mycursor.execute(sql,(val,))
    rows=mycursor.fetchall()
    mydb.commit()

    #calculate difference of dates and generate fine
    datereturn=rows[0][5]
    dateissue=rows[0][4]
    date_return = datetime.strptime(datereturn,"%d-%m-%Y")
    date_issue = datetime.strptime(dateissue,"%d-%m-%Y")
    diff=int((date_return-date_issue).total_seconds())
    diff=diff/(60*60*24)

    fine_oneday=10#fine for 1 day
    total_fine=0
    #implement fine if diff >14 i.e delay in returning the book
    if diff>14:
        total_fine=(diff-14)*fine_oneday
        
    #display fine data
    label_fine=Label(root,text="FINE DATA",bd=1,relief=SUNKEN)
    label_fine.grid(row=9,column=0,sticky="ew",pady=20)
    label_amt=Label(root,text="Fine: Rs."+str(total_fine),height=3).grid(row=10,column=0,sticky="e")

    if total_fine>0:
        paid=IntVar()
        #input data of payment (if fine exists)
        option1=Radiobutton(root,text="Paid",variable=paid,value=1).grid(row=10,column=1,sticky="ew")
        option2=Radiobutton(root,text="Not Paid",variable=paid,value=0).grid(row=10,column=2,sticky="ew")
        #if fine is not paid.... insert the user info in the table "pending"
        if paid.get()==0:
            sql="INSERT INTO PENDING (CONTACT, BOOKNAME, AUTHORNAME, CUSTOMER, FINE)VALUES(%s,%s,%s,%s,%s)"
            mycursor.execute(sql,(val,book.get(),aut.get(),cust.get(),total_fine))
            mydb.commit()
        else:
            pass
    else:
        pass

    #add the returned book in the stock
    sql="SELECT QUANTITY FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME=%s"
    mycursor.execute(sql,(box2.get(),box3.get()))
    rows=mycursor.fetchall()
    quan=int(rows[0][0])
    mydb.commit()
    sql="UPDATE BOOKS SET QUANTITY=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
    mycursor.execute(sql,(quan+1,box2.get(),box3.get()))
    mydb.commit()
    button=Button(root,text="SUBMIT",bg="red",command=lambda:reset())
    button.grid(row=11,column=1,pady=10)    
    return
#calling reset()
def reset():
    setup("return")
    return


#MAIN_FINCTION-5: TO KEEP THE TRACK OF PENDING DUES
def pending():
    clear_root()
    #display all the data of "pending" table
    Label(root,text="CUSTOMER_NAME",height=3).grid(row=1,column=0,sticky="ew")
    Label(root,text="CONTACT_NO",height=3).grid(row=1,column=1,sticky="ew",padx=15)
    Label(root,text="BOOK",height=3).grid(row=1,column=2,sticky="ew",padx=15)
    Label(root,text="AUTHOR",height=3).grid(row=1,column=3,sticky="ew",padx=15)
    Label(root,text="FINE",height=3).grid(row=1,column=4,sticky="ew",padx=15)
    Label(root,text="",height=3).grid(row=1,column=5,sticky="ew",padx=15)
    
    sql="SELECT * FROM PENDING"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    print(rows)
    global i
    i=2
    for row in rows:
        
        Label(root,text="-----------------------------").grid(row=i,column=0,columnspan=5,sticky="ew")
        i+=1
        Label(root,text=row[3],height=3).grid(row=i,column=0,sticky="ew")
        Label(root,text=row[0],height=3).grid(row=i,column=1,sticky="ew",padx=15)
        Label(root,text=row[1],height=3).grid(row=i,column=2,sticky="ew",padx=15)
        Label(root,text=row[2],height=3).grid(row=i,column=3,sticky="ew",padx=15)
        Label(root,text=row[4],height=3).grid(row=i,column=4,sticky="ew",padx=15)
        status=Button(root,text="paid",bg="green",command=lambda:fine_paid(row[0]))#create button
        status.grid(row=i,column=5,sticky="ew",padx=15)
        
        i+=1
#Subfunctions of pending()
def fine_paid(contact):#delete the user from "pending" if dues are cleared
    global i
    sql="DELETE FROM PENDING WHERE CONTACT=%s"
    value=int(contact)
    mycursor.execute(sql,(value,))
    mydb.commit()
    submit_pending=Button(root,text="SUBMIT",bg="red",command=lambda:setup("pending"))
    submit_pending.grid(row=i,column=2,columnspan=2,sticky="ew",pady=10)
    return


#MAIN_FUNCTION-6 :TO VIEW CERTAIN RECORDS OF THE LIBRARY
def viewrecords():
    clear_root()
    stock=Button(root,text="View Stock",height=5,command=lambda:viewstock())
    stock.grid(row=1,column=0,sticky="ew",padx=250,pady=40)
    
    issue=Button(root,text="View Issued Books",height=5,command=lambda:viewissue())
    issue.grid(row=1,column=1,sticky="ew",padx=15,pady=40)

    max_issue=Button(root,text="Max Issues Books",height=5,command=lambda:max_issue())
    max_issue.grid(row=2,column=0,sticky="ew",padx=250,pady=20)

    min_issue=Button(root,text="MinIssued Books",height=5,command=lambda:min_issue())
    min_issue.grid(row=2,column=1,sticky="ew",padx=15,pady=20)
#Subfunctions of viewrecords()
def viewstock():#view stock of the library
    clear_root()
    sql="SELECT * FROM BOOKS"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    Label(root,text="ID",height=3).grid(row=1,column=0,sticky="ew")
    Label(root,text="BOOK_NAME",height=3).grid(row=1,column=1,sticky="ew",padx=15)
    Label(root,text="AUTHOR_NAME",height=3).grid(row=1,column=2,sticky="ew",padx=15)
    Label(root,text="QUANTITY",height=3).grid(row=1,column=3,sticky="ew",padx=15)
    global j
    j=2
    for row in rows:
        
        Label(root,text="-----------------------------").grid(row=j,column=0,columnspan=5,sticky="ew")
        j+=1
        Label(root,text=row[0],height=3).grid(row=j,column=0,sticky="ew")
        Label(root,text=row[1],height=3).grid(row=j,column=1,sticky="ew",padx=15)
        Label(root,text=row[2],height=3).grid(row=j,column=2,sticky="ew",padx=15)
        Label(root,text=row[3],height=3).grid(row=j,column=3,sticky="ew",padx=15)
        j+=1
    ok=Button(root,text="OK",bg="skyblue",command=lambda:setup("viewrecords"))
    ok.grid(row=j+1,column=0,sticky="ew",padx=5)

def viewissue():#view issued books
    clear_root()
    sql="SELECT * FROM ISSUE"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    Label(root,text="BOOK_NAME",height=3).grid(row=1,column=0,sticky="ew")
    Label(root,text="AUTHOR_NAME",height=3).grid(row=1,column=1,sticky="ew",padx=15)
    Label(root,text="CUSTOMER_NAME",height=3).grid(row=1,column=2,sticky="ew",padx=15)
    Label(root,text="DATE_OF_ISSUE",height=3).grid(row=1,column=3,sticky="ew",padx=15)
    Label(root,text="DATE_OF_RETURN",height=3).grid(row=1,column=3,sticky="ew",padx=15)
    
    
    
#creating buttons
add_button=Button(root,text="Add",command=lambda:addbook())
delete_button=Button(root,text="Delete",command=lambda:delbook())
issue_button=Button(root,text="Issue",command=lambda:issuebook())
return_button=Button(root,text="Return",command=lambda:returnbook())
pending_button=Button(root,text="Pending",command=lambda:pending())
view_button=Button(root,text="View_Records",command=lambda:viewrecords())

#putting buttons on screen
add_button.grid(row=0,column=0,sticky="ew")
delete_button.grid(row=0,column=1,sticky="ew")
issue_button.grid(row=0,column=2,sticky="ew")
return_button.grid(row=0,column=3,sticky="ew")
pending_button.grid(row=0,column=4,sticky="ew")
view_button.grid(row=0,column=5,sticky="ew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.mainloop()
