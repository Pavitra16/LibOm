from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from datetime import date,datetime,timedelta
import mysql.connector
import statistics
from statistics import mode

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="LIBMAN"
)

mycursor = mydb.cursor()
root=Tk()
root.title("LibOm")
root.iconbitmap("C:\\Users\\admin\\Downloads\\icon.ico")
count=0

heading_font = Font(family="Helvetica", size=20, weight="bold",underline=1)
heading2_font=Font(family="Helvetica", size=18, weight=NORMAL,underline=1)
label_font=Font(family="Helvetica",size=15,weight=NORMAL)
label2_font=Font(family="Helvetica",size=12,weight=NORMAL)
button_font=Font(family="Helvetica",size=12,weight="bold")
button2_font=Font(family="Helvetica",size=7,weight=NORMAL)
button3_font=Font(family="Helvetica",size=12,weight=NORMAL)
button_color="#EF5A6F"
button2_color="#399918"
button3_color="#03AED2"
button_heading="#FFB4C2"
set_color="#088395"
add_color="#96C9F4"
del_color="#C39898"
issue_color="#EAD8C0"
return_color="#E8C5E5"
view_color="#DCFFB7"
pending_color="#FEFBD8"
search_color="#DFCCFB"
color="grey"

def setup_scrollable_frame(parent):
    global color
    # Create a Canvas widget for scrolling
    canvas = Canvas(parent, width=550, height=665,bg=color)
    
    canvas.grid(row=3, column=0,columnspan=9, sticky="nsew")

    # Create a Scrollbar widget and attach it to the Canvas
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=3, column=9, sticky="ns")  # Place scrollbar next to the canvas
    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=canvas.yview)
    # Create a Frame to contain the inner content
    inner_frame = Frame(canvas,bg=color)
    #inner_frame.configure(bg="lightblue")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Function to configure scrolling
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_configure)
    parent.update_idletasks()

    return inner_frame, scrollbar

def clear_root():
    widgets = root.winfo_children()
    for widget in widgets:
        widget.destroy()
    #creating buttons
    setup_button=Button(root,text="SetUp",bg=button_heading,command=lambda:set_lib()).grid(row=0,column=0,sticky="ew")
    add_button=Button(root,text="Add",bg=button_heading,command=lambda:addbook()).grid(row=0,column=1,sticky="ew")
    delete_button=Button(root,text="Delete",bg=button_heading,command=lambda:delbook()).grid(row=0,column=2,sticky="ew")
    issue_button=Button(root,text="Issue",bg=button_heading,command=lambda:issuebook()).grid(row=0,column=3,sticky="ew")
    return_button=Button(root,text="Return",bg=button_heading,command=lambda:returnbook()).grid(row=0,column=4,sticky="ew")
    pending_button=Button(root,text="Pending",bg=button_heading,command=lambda:pending()).grid(row=0,column=5,sticky="ew")
    view_button=Button(root,text="View_Records",bg=button_heading,command=lambda:viewrecords()).grid(row=0,column=6,sticky="ew")
    search_button=Button(root,text="Search",bg=button_heading,command=lambda:search()).grid(row=0,column=7,sticky="ew")
    

    

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.grid_columnconfigure(5, weight=1)
    root.grid_columnconfigure(6, weight=1)
    root.grid_columnconfigure(7, weight=1)

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
    elif function=="search":
        search()
    else:
        issuebook()

#MAIN_FUNTION-1 : TO SET UP IN THE LIBRARY
sql="INSERT INTO SETLIB (FINE,DAY_FINE,BOOK) VALUES (%s,%s,%s)"
val=(0,0,0)
mycursor.execute(sql,val)
mydb.commit()
def set_lib():
    clear_root();
    global color
    color=set_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    color
    
    global limit,fine,day_fine

    
    Label(inner_frame,text="SET UP YOUR LIBRARY",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    
    Label(inner_frame,text="Fine Per Day: ** ",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    box_fine=Entry(inner_frame)
    box_fine.grid(row=2,column=1,columnspan=5,sticky="ew")
    

    Label(inner_frame,text="Fine Start Day: ** ",height=3,font=label_font,bg=color).grid(row=3,column=0,sticky="ew")
    box_fineday=Entry(inner_frame)
    box_fineday.grid(row=3,column=1,columnspan=5,sticky="ew")
    

    Label(inner_frame,text="Books Per Person ** ",height=3,font=label_font,bg=color).grid(row=4,column=0,sticky="ew")
    box_limit=Entry(inner_frame)
    box_limit.grid(row=4,column=1,columnspan=5,sticky="ew")
   

    
    Label(inner_frame,text="View Previous Data",height=4,font=label_font,bg=color).grid(row=5,column=0,columnspan=5,pady=10,sticky="ew")
    go_author=Button(inner_frame,text="VIEW",bg=button2_color,font=button2_font,bd=1,command=lambda:viewdata())
    go_author.grid(row=5,column=5,padx=30,sticky="ew")
    
    submit_add=Button(inner_frame,text="DONE",bg=button_color,font=button_font,command=lambda:setvalues(box_fine.get(),box_fineday.get(),box_limit.get()))
    submit_add.grid(row=14,column=0,padx=100)
    def setvalues(fine,day,limit):
        global color
        color=set_color
    
        mycursor.execute("TRUNCATE TABLE SETLIB")
        mydb.commit()
        sql="INSERT INTO SETLIB (FINE,DAY_FINE,BOOK) VALUES (%s,%s,%s)"
        val=(int(fine),int(day),int(limit))
        mycursor.execute(sql,val)
        mydb.commit()
        clear_root()
    
    
    

    def viewdata():
        global color
        color=set_color
    
        sql="SELECT * FROM SETLIB"
        mycursor.execute(sql)
        rows=mycursor.fetchall()
        mydb.commit()
        
        Label(inner_frame,text="Fine Per Day: ",height=3,font=label2_font,bg=color).grid(row=6,column=0,rowspan=2,sticky="ew")
        Label(inner_frame,text=rows[0][0],height=3,font=label2_font,bd=1,bg=color).grid(row=6,column=1,sticky="ew")
        
        Label(inner_frame,text="Fine Start Day: ",height=3,font=label2_font,bg=color).grid(row=9,column=0,rowspan=2,sticky="ew")
        Label(inner_frame,text=rows[0][1],height=3,font=label2_font,bd=1,bg=color).grid(row=9,column=1,sticky="ew")

        Label(inner_frame,text="Books Per Person: ",height=3,font=label2_font,bg=color).grid(row=12,column=0,sticky="ew")
        Label(inner_frame,text=rows[0][2],height=3,font=label2_font,bd=1,bg=color).grid(row=12,column=1,sticky="ew")

        submit_add=Button(inner_frame,text="DONE",bg=button2_color,font=button2_font,command=lambda:set_lib())
        submit_add.grid(row=13,column=0,padx=100,pady=30)


    
sql="SELECT * FROM SETLIB"
mycursor.execute(sql)
rows=mycursor.fetchall()
mydb.commit()
global fine,day_fine,limit
fine=int(rows[0][0])

day_fine=int(rows[0][1])

limit=int(rows[0][2])
    
    
#MAIN_FUNTION-2: TO ADD BOOK IN THE LIBRARY
def addbook():
    clear_root()
    global color
    color=add_color
    root.configure(bg=color)
    Label(root,text="ADD BOOK: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    #book name
    global count
    Label(root,text="Book's Name: ** ",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #author's name
    Label(root,text="Author's Name: ",height=3,font=label_font,bg=color).grid(row=3,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=3,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #quantity
    Label(root,text="Quantity: **",height=3,font=label_font,bg=color).grid(row=4,column=0,sticky='ew')
    box3=Entry(root)
    box3.insert(0,"ONLY DIGITS")
    box3.grid(row=4,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    
    #status bar
    status=Label(root,text="Book: "+str(count+1),bd=1,relief=SUNKEN,anchor=E,font=label_font,bg=color)
    status.grid(row=7,column=0,columnspan=4,sticky="ew",pady=30)
    #submit button
    submit_add=Button(root,text="SUBMIT",bg=button_color,font=button_font,command=lambda:submit_entry(box1,box2,box3,status))
    submit_add.grid(row=6,column=0,padx=100)
    
    return
#Subfunctions of addbook()
def submit_entry(box1,box2,box3,status):
    global count
    global color
    color=add_color
    
    if box1.get() and (box3.get().isdigit()):
        if box2.get()=="":
            box2.insert(0,"unknown")
        sql="SELECT * FROM BOOKS WHERE BOOKNAME =%s AND AUTHORNAME=%s"
        val=(box1.get(),box2.get())
        mycursor.execute(sql,val)
        rows=mycursor.fetchall()
        if len(rows)!=0:
            sql="UPDATE BOOKS SET QUANTITY=%s, QUANTITY_LEFT=%s WHERE ID=%s "
            val=(int(rows[0][3])+int(box3.get()),int(rows[0][4])+int(box3.get()),int(rows[0][0]))
            mycursor.execute(sql,val)
            mydb.commit()
        else:
            sql = "INSERT INTO BOOKS (BookName, AuthorName,Quantity,QUANTITY_LEFT) VALUES (%s, %s, %s,%s)"
            val = (box1.get(), box2.get(),box3.get(),box3.get())
            mycursor.execute(sql, val)
            mydb.commit()
        count += 1
        status=Label(root,text="Book: "+str(count+1),bd=1,relief=SUNKEN,anchor=E,font=label_font,bg=color)
        status.grid(row=5,column=0,columnspan=4,sticky="ew",pady=30)
        setup("add")
    
    else:
         messagebox.showwarning("Error", "Please fill in all fields appropriately.")


#MAIN_FUNCTION-3: DELETE BOOKS FROM THE LIBRARY
def delbook():
    clear_root()
    global color
    color=del_color
    root.configure(bg=color)
    Label(root,text="DELETE BOOK: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")

    #book name
    Label(root,text="Book's Name**: ",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #authors name
    Label(root,text="Author's Name: ",height=3,font=label_font,bg=color).grid(row=3,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=3,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)

    Label(root,text="How many copies would you like to delete?**",height=3,font=label_font,bg=color).grid(row=4,column=0,columnspan=3,sticky="ew")
    opt=IntVar()
    Radiobutton(root,text="Some Copies",variable=opt,value=2,bg=color).grid(row=6,column=0,sticky="e")
    Radiobutton(root,text="All Copies",variable=opt,value=1,bg=color).grid(row=6,column=2,sticky="w")
    del_button=Button(root,text="DELETE",bg=button_color,font=button2_font,command=lambda:choice(opt.get(),box1.get(),box2.get()))
    del_button.grid(row=7,column=1,sticky="ew")
    return
#Subfunctions of deletebook()
def choice(option,book,aut):#allows user to delete all or few copies of the entered book
    #global color
    #color=del_color
    
    if book:
        if aut:
            aut=aut
        else:
            aut="unknown"
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
                Label(root,text="Enter no. of copies to be deleted: ",height=3,font=label_font,bg=color).grid(row=8,column=0,sticky="ew")
                box10=Entry(root)
                box10.insert(0,"ONLY DIGITS")
                box10.grid(row=8,column=1,sticky="ew")
                sql="SELECT QUANTITY FROM BOOKS WHERE BOOKNAME =%s AND AUTHORNAME=%s"
                mycursor.execute(sql,(book,aut))
                
                quan=mycursor.fetchall()
                mydb.commit()
                
                button=Button(root,text="delete",bg=button_color,font=button_font,command=lambda:update_books(quan[0],box10.get(),book,aut))
                button.grid(row=8,column=2,sticky="ew")            
    else:#displays message if all boxes are not properly filled
        messagebox.showwarning("Error!","Please fill in all the fields appropriately!")
        
def update_books(prev,new,book,aut):#updates stock of books
    global color
    color=del_color
    
    if new.isdigit():
        if int(new)>int(prev[0]):
            messagebox.showwarning("Error","ONLY "+str(prev)+" COPIES OF THIS BOOK ARE AVAILABLE IN STOCK")
        else:
            sql="UPDATE BOOKS SET QUANTITY=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            mycursor.execute(sql,(int(prev[0])-int(new),book,aut))
            mydb.commit()

            messagebox.showinfo("Delete Books",new+"copies of "+book+" by "+aut+" are deleted")
            setup("delete")
    else:
        messagebox.showwarning("Error","Please enter digits!!")
    return

#MAIN_FUNCTION-4: TO ISSUE A BOOK TO THE CUSTOMER
def issuebook():
    clear_root()
    global color
    color=issue_color
    root.configure(bg=color)
    Label(root,text="ISSUE BOOK: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")

    #book name
    Label(root,text="Book's Name: ",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky='ew')
    box1=Entry(root)
    box1.grid(row=2,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #authors name
    Label(root,text="Author's Name: ",height=3,font=label_font,bg=color).grid(row=3,column=0,sticky='ew')
    box2=Entry(root)
    box2.grid(row=3,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #customer's name
    Label(root,text="Student's Name: ",height=3,font=label_font,bg=color).grid(row=4,column=0,sticky='ew')
    box3=Entry(root)
    box3.grid(row=4,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #contact no
    Label(root,text="Contact no: ",height=3,font=label_font,bg=color).grid(row=5,column=0,sticky='ew')
    box4=Entry(root)
    box4.insert(0,"ONLY DIGITS")
    box4.grid(row=5,column=1,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)
    #date of issue
    today=date.today()
    Label(root,text="Date: ",height=3,font=label_font,bg=color).grid(row=6,column=0,sticky="ew")
    box_date=Entry(root)
    box_date.insert(0,date.today().day)
    box_date.grid(row=6,column=1,sticky="ew")
    Label(root,text="Month: ",height=3,font=label_font,bg=color).grid(row=6,column=2,sticky="ew")
    box_month=Entry(root)
    box_month.insert(0,date.today().month)
    box_month.grid(row=6,column=3,sticky="ew")
    Label(root,text="Year: ",height=3,font=label_font,bg=color).grid(row=6,column=4,sticky="ew")
    box_year=Entry(root)
    box_year.insert(0,date.today().year)
    box_year.grid(row=6,column=5,sticky="ew")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_columnconfigure(3,weight=1)
    root.grid_columnconfigure(4,weight=1)
    root.grid_columnconfigure(5,weight=1)
        #submit
    submit_issue=Button(root,text="ISSUE",bg=button_color,font=button_font,command=lambda:issue_entry(box1.get(),box2.get(),box3.get(),box4.get(),box_date.get(),box_month.get(),box_year.get()))
    submit_issue.grid(row=6,column=6,columnspan=4,sticky="ew")
    return
#Subfinctions of issuebook()
def issue_entry(book,aut,cust,cont,date,month,year):
        global limit
        global color
        color=issue_color
        root.configure(bg=color)
    
        sql="SELECT * FROM PENDING WHERE CONTACT=%s"#view pending dues of the customer
        mycursor.execute(sql,(cont,))
        rows1=mycursor.fetchall()
        mydb.commit()
        if len(rows1)!=0:#display warning message if fine is pending
            sql="SELECT FINE FROM PENDING WHERE CONTACT=%s"
            mycursor.execute(sql,(cont,))
            amt=int((mycursor.fetchone())[0])
            mydb.commit()
            messagebox.showwarning("Due Fine","Your fine of amt Rs. "+amt+" is due")
        
            
            
            
                
        else:#issue the book and remove 1 from the stock
            sql="SELECT ISSUED,RETURNED FROM RETURNRECORD WHERE CONTACT =%s"
            mycursor.execute(sql,(cont,))
            rows2=mycursor.fetchall()
            mydb.commit()
            sql="SELECT BOOK FROM SETLIB"
            mycursor.execute(sql)
            limit=mycursor.fetchall()
            limit=int(limit[0][0])
            if len(rows2)!=0 and int(rows2[0][0])>=limit:
                messagebox.showinfo("Limit Exceed!","You have reached the limit to get the books issued!")
            else:
                
                    if book and aut and cust and cont:
                        sql="SELECT ID , QUANTITY FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME =%s"
                        mycursor.execute(sql,(book,aut))
                        rows=mycursor.fetchall()
                        mydb.commit()
                       
                        #print(id_book)
                        if len(rows)==0 or rows[0][1]==0:
                            messagebox.showwarning("Error","BOOK IS NOT IN STOCK")
                        else:
                            if len(str(cont))<10:
                                messagebox.showwarning("Error","INVALID MOBILE NUMBER")
                            else:
                                id_book=rows[0][0]
                                sql="INSERT INTO ISSUE (ID,BOOKNAME,AUTHORNAME,CUSTOMER,CONTACT,DATE_OF_ISSUE) VALUES (%s,%s,%s,%s,%s,%s)"
                                mycursor.execute(sql,(id_book,book,aut,cust,int(cont),date+"-"+month+"-"+year))
                                mydb.commit()
                                #remove from books table
                                sql="SELECT QUANTITY_LEFT FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME=%s"
                                mycursor.execute(sql,(book,aut))
                                rows=mycursor.fetchall()
                                quan=int(rows[0][0])
                                mydb.commit()
                                sql="UPDATE BOOKS SET QUANTITY_LEFT=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
                                mycursor.execute(sql,(quan-1,book,aut))
                                mydb.commit()

                        #update returnrecord table
                                sql="SELECT ISSUED FROM RETURNRECORD WHERE CONTACT=%s"
                                mycursor.execute(sql,(cont,))
                                rows2=mycursor.fetchall()
                                mydb.commit()
                                if len(rows2)!=0:
                                    count_issued=int(rows2[0][0])
                                    sql="UPDATE RETURNRECORD SET ISSUED = %s WHERE CONTACT =%s"
                                    mycursor.execute(sql,(count_issued+1,cont))
                                else:
                                    sql="INSERT INTO RETURNRECORD (CONTACT, ISSUED, RETURNED) VALUES (%s,%s,%s)"
                                    mycursor.execute(sql,(int(cont),1,0))
                                    mydb.commit()
                                #enter record in issued table
                                sql="INSERT INTO ISSUED (ID,BOOKNAME,AUTHORNAME,CUSTOMER,CONTACT) VALUES (%s,%s,%s,%s,%s)"
                                values=(id_book,book,aut,cust,int(cont))
                                mycursor.execute(sql,values)
                                mydb.commit()
                        
        

                    else:
                        messagebox.showwarning("Error","Please fill in all fields appropriately!")
        setup("issue")
        return 
#MAIN_FUNCTION-5: TO KEEP TRACK OF RETURNED BOOKS AND FINE  
def returnbook():
    
    clear_root()
    global color
    color=return_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    
    Label(inner_frame,text="RETURN THE  BOOK: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")

    label1=Label(inner_frame,text="Contact no.",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    box=Entry(inner_frame)
    box.grid(row=2,column=1,columnspan=5,sticky="ew")
    
    
    global submit
    submit=Button(root,text="SUBMIT",bg=button_color,font=button_font,command=lambda:return_entry(box.get()))#user will feed contact no and rest will be shown
    submit.grid(row=3,column=1,sticky="ew")                                 #the system
#Subfunctions of returnbook()
def return_entry(cont):#it will give contact no. of the reader of issued book
    global color
    color=return_color
    
    inner_frame, scrollbar = setup_scrollable_frame(root)
    global submit
    submit.destroy()#remove the submit button from the return window
    
    
    sql="SELECT * FROM ISSUE WHERE CONTACT=%s"#to display reSt of the information
    val=int(cont)
    mycursor.execute(sql,(val,))
    rows=mycursor.fetchall()
    mydb.commit()
    if len(rows)==0:
        messagebox.showwarning("Error!","Incorrect Contact No.")
    else:
        
        global m
        m=2
        for i ,row in enumerate(rows):
            #display book_name
            Label(inner_frame,text="Book Name:",height=3,font=label_font,bg=color).grid(row=m,column=0,sticky="ew")
            Label(inner_frame,text=row[1],height=1,font=label_font,bd=1,relief=SUNKEN,bg=color).grid(row=m,column=1,columnspan=3,sticky="ew")

            
            #display author_name
            Label(inner_frame,text="Author Name",height=3,font=label_font,bg=color).grid(row=m+1,column=0,sticky="ew")
            Label(inner_frame,text=row[2],height=1,font=label_font,bd=1,bg=return_color).grid(row=m+1,column=1,columnspan=3,sticky="ew")
            
            #diplay student_name
            Label(inner_frame,text="Student Name:",height=3,font=label_font,bg=color).grid(row=m+2,column=0,sticky="ew")
            Label(inner_frame,text=row[3],height=1,font=label_font,bd=1,bg=color).grid(row=m+2,column=1,columnspan=3,sticky="ew")

           
            #go button
            go=Button(inner_frame,text="GO",bg=button2_color,font=button2_color,command=lambda j=row:details(j[1],j[2],j[3],int(j[4])))
            go.grid(row=m+3,column=2,columnspan=4,sticky="ew")
            Label(inner_frame,text="",height=2,bg=return_color).grid(row=m+4,column=0,sticky="ew")
            m=m+5
        def details(book,author,cust,cont):
            global day_fine,fine
            clear_root()
            global color
            color=return_color
    
            inner_frame, scrollbar = setup_scrollable_frame(root)
            #display book_name
            Label(inner_frame,text="Book Name:",height=3,font=label_font,bg=color).grid(row=1,column=0,sticky="ew")
            Label(inner_frame,text=book,height=1,font=label_font,bd=1,bg=color).grid(row=1,column=1,columnspan=3,sticky="ew")

            #display author_name
            Label(inner_frame,text="Author Name",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
            Label(inner_frame,text=author,height=1,font=label_font,bd=1,bg=color).grid(row=2,column=1,columnspan=3,sticky="ew")

            
            #diplay student_name
            Label(inner_frame,text="Student Name:",height=3,font=label_font,bg=color).grid(row=3,column=0,sticky="ew")
            Label(inner_frame,text=cust,height=1,font=label_font,bd=1,relief=SUNKEN,bg=color).grid(row=3,column=1,columnspan=3,sticky="ew")

            
            
            #display return date i.e. current date
            today=date.today()
            #date
            Label(inner_frame,text="Date: ",height=3,font=label_font,bg=color).grid(row=4,column=0,sticky="ew")
            box_date=Entry(inner_frame)
            box_date.insert(0,date.today().day)
            box_date.grid(row=4,column=1,sticky="ew")
            #month
            Label(inner_frame,text="Month: ",height=3,font=label_font,bg=color).grid(row=4,column=2,sticky="ew")
            box_month=Entry(inner_frame)
            box_month.insert(0,date.today().month)
            box_month.grid(row=4,column=3,sticky="ew")
            #year
            Label(inner_frame,text="Year: ",height=3,font=label_font,bg=color).grid(row=4,column=4,sticky="ew")
            box_year=Entry(inner_frame)
            box_year.insert(0,date.today().year)
            box_year.grid(row=4,column=5,sticky="ew")
            #insert return date into the table "issue"
            sql="UPDATE ISSUE SET  DATE_OF_RETURN =%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            dateofreturn=str(date.today().day)+"-"+str(date.today().month)+"-"+str(date.today().year)
            mycursor.execute(sql,(dateofreturn,book,author))
            mydb.commit()
            #display date of issue
            sql="SELECT * FROM ISSUE WHERE BOOKNAME=%s"#select return issue and return date from the table "issue"
            mycursor.execute(sql,(book,))
            rows=mycursor.fetchall()
            mydb.commit()
            
            date1=rows[0][5]
            date_obj=datetime.strptime(date1,"%d-%m-%Y")
            date2=date_obj.strftime("%d")
            month=date_obj.strftime("%m")
            year=date_obj.strftime("%Y")
            #date
            
            Label(inner_frame,text="DATE OF ISSUE: ",font=label_font,bg=color).grid(row=5,column=0,sticky="ew")
            
            Label(inner_frame,text="Date: ",height=3,font=label_font,bg=color).grid(row=6,column=0,sticky="ew")
            box_d=Entry(inner_frame)
            box_d.insert(0,date2)
            box_d.grid(row=6,column=1,sticky="ew")
            #month
            Label(inner_frame,text="Month: ",height=3,font=label_font,bg=color).grid(row=6,column=2,sticky="ew")
            box_m=Entry(inner_frame)
            box_m.insert(0,month)
            box_m.grid(row=6,column=3,sticky="ew")
            #year
            Label(inner_frame,text="Year: ",height=3,font=label_font,bg=color).grid(row=6,column=4,sticky="ew")
            box_y=Entry(inner_frame)
            box_y.insert(0,year)
            box_y.grid(row=6,column=5,sticky="ew")

            #DATE OF RETURN
            date1=rows[0][6]
            date_obj=datetime.strptime(date1,"%d-%m-%Y")
            date2=date_obj.strftime("%d")
            month=date_obj.strftime("%m")
            year=date_obj.strftime("%Y")
            #date
            
            Label(inner_frame,text="DATE OF RETURN: ",font=label_font,bg=color).grid(row=7,column=0,sticky="ew")
            
            Label(inner_frame,text="Date: ",height=3,font=label_font,bg=color).grid(row=8,column=0,sticky="ew")
            box_d=Entry(inner_frame)
            box_d.insert(0,date2)
            box_d.grid(row=8,column=1,sticky="ew")
            #month
            Label(inner_frame,text="Month: ",height=3,font=label_font,bg=color).grid(row=8,column=2,sticky="ew")
            box_m=Entry(inner_frame)
            box_m.insert(0,month)
            box_m.grid(row=8,column=3,sticky="ew")
            #year
            Label(inner_frame,text="Year: ",height=3,font=label_font,bg=color).grid(row=8,column=4,sticky="ew")
            box_y=Entry(inner_frame)
            box_y.insert(0,year)
            box_y.grid(row=8,column=5,sticky="ew")
            
            
            #calculate difference of dates and generate fine
            datereturn=rows[0][6]
            dateissue=rows[0][5]
            date_return = datetime.strptime(datereturn,"%d-%m-%Y")
            date_issue = datetime.strptime(dateissue,"%d-%m-%Y")
            diff=int((date_return-date_issue).total_seconds())
            diff=diff/(60*60*24)
            total_fine=0
            #implement fine if diff >14 i.e delay in returning the book
            
            if diff>day_fine:
                total_fine=(diff-14)*fine
                
            #display fine data
            label_fine=Label(inner_frame,text="FINE DATA",bd=1,relief=SUNKEN,font=label_font,bg=color)
            label_fine.grid(row=9,column=0,sticky="ew",pady=20)
            Label(inner_frame,text="Fine: Rs."+str(total_fine),height=3,font=label_font,bg=color).grid(row=10,column=0,sticky="e")

            if total_fine>0:
                paid=IntVar()
                #input data of payment (if fine exists)
                option1=Radiobutton(inner_frame,text="Paid",variable=paid,value=1,bg=color).grid(row=11,column=1,sticky="ew")
                option2=Radiobutton(inner_frame,text="Not Paid",variable=paid,value=0,bg=color).grid(row=11,column=2,sticky="ew")
                #if fine is not paid.... insert the user info in the table "pending"
                if paid.get()==0:
                    sql="INSERT INTO PENDING (CONTACT, BOOKNAME, AUTHORNAME, CUSTOMER, FINE)VALUES(%s,%s,%s,%s,%s)"
                    mycursor.execute(sql,(val,book.get(),aut.get(),cust.get(),total_fine))
                    mydb.commit()
                    
                else:
                    pass
            else:
                pass
            #update returnrecord table
            sql="SELECT * FROM RETURNRECORD WHERE CONTACT=%s"
            mycursor.execute(sql,(val,))
            row=mycursor.fetchall()
            count_return=int(row[0][2])
            mydb.commit()
            sql="UPDATE RETURNRECORD SET RETURNED=%s WHERE CONTACT=%s"
            mycursor.execute(sql,(count_return+1,val))
            mydb.commit()
            if count_return+1 == int(row[0][1]):
                sql="DELETE FROM RETURNRECORD WHERE CONTACT =%s"
                mycursor.execute(sql,(val,))
                mydb.commit()

            #add the returned book in the stock and in ISSUED
            sql="SELECT ID,QUANTITY,QUANTITY_LEFT FROM BOOKS WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            mycursor.execute(sql,(book,author))
            rows=mycursor.fetchall()
            id_book=int(rows[0][0])
            quan=int(rows[0][1])
            quan_left=int(rows[0][2])
            mydb.commit()
            sql="UPDATE BOOKS SET QUANTITY_LEFT=%s WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            mycursor.execute(sql,(quan_left+1,book,author))
            mydb.commit()

            
            
            

            #delete from issue
            sql="DELETE FROM ISSUE WHERE BOOKNAME=%s AND AUTHORNAME=%s"
            mycursor.execute(sql,(book,author))
            mydb.commit()
            button=Button(inner_frame,text="SUBMIT",bg=button_color,font=button_font,command=lambda:reset())
            button.grid(row=14,column=1,pady=10)    
        return
#calling reset()
def reset():
    setup("return")
    return


#MAIN_FINCTION-6: TO KEEP THE TRACK OF PENDING DUES
def pending():
    
    clear_root()
    global color
    color=pending_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="PENDING DUES: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")

    #display all the data of "pending" table
    Label(inner_frame,text="STUDENT_NAME",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    Label(inner_frame,text="CONTACT_NO",height=3,font=label_font,bg=color).grid(row=2,column=1,sticky="ew",padx=15)
    Label(inner_frame,text="BOOK",height=3,font=label_font,bg=color).grid(row=2,column=2,sticky="ew",padx=15)
    Label(inner_frame,text="AUTHOR",height=3,font=label_font,bg=color).grid(row=2,column=3,sticky="ew",padx=15)
    Label(inner_frame,text="FINE",height=3,font=label_font,bg=color).grid(row=2,column=4,sticky="ew",padx=15)
    Label(inner_frame,text="",height=3,font=label_font,bg=color).grid(row=2,column=5,sticky="ew",padx=15)
    
    sql="SELECT * FROM PENDING"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    print(rows)
    global i
    i=3
    for row in rows:
        
        Label(inner_frame,text="-----------------------------").grid(row=i,column=0,columnspan=5,sticky="ew")
        i+=1
        Label(inner_frame,text=row[3],height=3,font=label_font,bg=color).grid(row=i,column=0,sticky="ew")
        Label(inner_frame,text=row[0],height=3,font=label_font,bg=color).grid(row=i,column=1,sticky="ew",padx=15)
        Label(inner_frame,text=row[1],height=3,font=label_font,bg=color).grid(row=i,column=2,sticky="ew",padx=15)
        Label(inner_frame,text=row[2],height=3,font=label_font,bg=color).grid(row=i,column=3,sticky="ew",padx=15)
        Label(inner_frame,text=row[4],height=3,font=label_font,bg=color).grid(row=i,column=4,sticky="ew",padx=15)
        status=Button(inner_frame,text="paid",bg="green",command=lambda:fine_paid(row[0]))#create button
        status.grid(row=i,column=5,sticky="ew",padx=15)
        
        i+=1
#Subfunctions of pending()
def fine_paid(contact):#delete the user from "pending" if dues are cleared
    global color
    color=pending_color
    
    global i
    sql="DELETE FROM PENDING WHERE CONTACT=%s"
    value=int(contact)
    mycursor.execute(sql,(value,))
    mydb.commit()
    submit_pending=Button(root,text="SUBMIT",bg="red",command=lambda:setup("pending"))
    submit_pending.grid(row=i,column=2,columnspan=2,sticky="ew",pady=10)
    return


#MAIN_FUNCTION-7 :TO VIEW CERTAIN RECORDS OF THE LIBRARY
def viewrecords():
    clear_root()
    global color
    color=view_color
    root.configure(bg=color)
    Label(root,text="VIEW RECORDS: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    
    #view stock
    Label(root,text="View Stock",font=label_font,height=4,bg=color).grid(row=2,column=0,columnspan=5,pady=10,sticky="ew")
    go_book=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:viewstock())
    go_book.grid(row=2,column=5,padx=30,sticky="ew")

    #view all issued books
    Label(root,text="All Issued Books",height=4,font=label_font,bg=color).grid(row=3,column=0,columnspan=5,pady=10,sticky="ew")
    go_author=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:allissue())
    go_author.grid(row=3,column=5,padx=30,sticky="ew")
    
    #max_issued books
    Label(root,text="Max Issued Books",height=4,font=label_font,bg=color).grid(row=4,column=0,columnspan=5,pady=10,sticky="ew")
    go_quan=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:viewmax())
    go_quan.grid(row=4,column=5,padx=30,sticky="ew")

    #min_issued books
    Label(root,text="Min Issued Books",height=4,font=label_font,bg=color).grid(row=5,column=0,columnspan=5,pady=10,sticky="ew")
    go_quan=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:viewmin())
    go_quan.grid(row=5,column=5,padx=30,sticky="ew")

    #view issued books
    Label(root,text="View Issued Books",height=4,font=label_font,bg=color).grid(row=6,column=0,columnspan=5,pady=10,sticky="ew")
    go_author=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:viewissue())
    go_author.grid(row=6,column=5,padx=30,sticky="ew")
   
#Subfunctions of viewrecords()
def viewstock():#view stock of the library
    clear_root()
    global color
    color=view_color
    
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="LIBRARY STOCK: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")

    sql="SELECT * FROM BOOKS"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    Label(inner_frame,text="ID",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    Label(inner_frame,text="BOOK_NAME",height=3,font=label_font,bg=color).grid(row=2,column=1,sticky="ew",padx=15)
    Label(inner_frame,text="AUTHOR_NAME",height=3,font=label_font,bg=color).grid(row=2,column=2,sticky="ew",padx=15)
    Label(inner_frame,text="QUANTITY",height=3,font=label_font,bg=color).grid(row=2,column=3,sticky="ew",padx=15)
    Label(inner_frame,text="QUANTITY_LEFT",height=3,font=label_font,bg=color).grid(row=2,column=4,sticky="ew",padx=15)

    global j
    j=3
    for row in rows:
        
        Label(inner_frame,text="-----------------------------").grid(row=j,column=0,columnspan=5,sticky="ew")
        j+=1
        Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=j,column=0,sticky="ew")
        Label(inner_frame,text=row[1],height=3,font=label2_font,bg=color).grid(row=j,column=1,sticky="ew",padx=15)
        Label(inner_frame,text=row[2],height=3,font=label2_font,bg=color).grid(row=j,column=2,sticky="ew",padx=15)
        Label(inner_frame,text=row[3],height=3,font=label2_font,bg=color).grid(row=j,column=3,sticky="ew",padx=15)
        Label(inner_frame,text=row[4],height=3,font=label2_font,bg=color).grid(row=j,column=4,sticky="ew",padx=15)

        j+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:setup("viewrecords"))
    ok.grid(row=j,column=2,sticky="ew",padx=5)
    
    

def allissue():#view all issued books
    clear_root()
    global color
    color=view_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="ISSUED BOOKS: ",height=4,font=heading_font,bg=view_color).grid(row=1,column=0,columnspan=5,sticky="ew")

    sql="SELECT * FROM ISSUED"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    Label(inner_frame,text="BOOK_ID",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    Label(inner_frame,text="BOOK_NAME",height=3,font=label_font,bg=color).grid(row=2,column=1,sticky="ew",padx=15)
    Label(inner_frame,text="AUTHOR_NAME",height=3,font=label_font,bg=color).grid(row=2,column=2,sticky="ew",padx=15)
    Label(inner_frame,text="STUDENT_NAME",height=3,font=label_font,bg=color).grid(row=2,column=3,sticky="ew",padx=15)
    Label(inner_frame,text="CONTACT",height=3,font=label_font,bg=color).grid(row=2,column=4,sticky="ew",padx=15)
    global k
    k=3
    for row in rows:
        
        Label(inner_frame,text="-----------------------------").grid(row=k,column=0,columnspan=5,sticky="ew")
        k+=1
        Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=k,column=0,sticky="ew")
        Label(inner_frame,text=row[1],height=3,font=label2_font,bg=color).grid(row=k,column=1,sticky="ew",padx=15)
        Label(inner_frame,text=row[2],height=3,font=label2_font,bg=color).grid(row=k,column=2,sticky="ew",padx=15)
        Label(inner_frame,text=row[3],height=3,font=label2_font,bg=color).grid(row=k,column=3,sticky="ew",padx=15)
        Label(inner_frame,text=row[4],height=3,font=label2_font,bg=color).grid(row=k,column=4,sticky="ew",padx=15)
        k+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:setup("viewrecords"))
    ok.grid(row=k,column=2,sticky="ew",padx=5)

def viewmax():#view max issued books
    clear_root()
    global color
    color=view_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    sql="SELECT ID FROM ISSUED"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    dic=dict()
    
    for i in rows:
        dic[int(i[0])]=rows.count(i)
    max_value = max(dic.values())
    lst=[]
    for i in dic:
        if dic[i]==max_value:
            lst.append(i)
    Label(inner_frame,text="MAXIMUM ISSUED BOOKS: ",font=heading2_font,bg=color).grid(row=4,column=3,sticky="ew",pady=30)
    sql="SELECT BOOKNAME, AUTHORNAME FROM BOOKS WHERE ID=%s"
    global m
    m=3
    for i in lst:
        mycursor.execute(sql,(i,))
        rows=mycursor.fetchall()
        m+=2
        Label(inner_frame,text="Book_Name: ",font=label_font,bg=color).grid(row=m,column=1,sticky="ew",pady=20)
        Label(inner_frame,text=rows[0][0],font=label2_font,bd=1,relief=SUNKEN,bg=color).grid(row=m,column=2,sticky="ew",pady=20)
        Label(inner_frame,text="Author_Name: ",font=label_font,bg=color).grid(row=m+1,column=1,sticky="ew")
        Label(inner_frame,text=rows[0][1],font=label2_font,bd=1,relief=SUNKEN,bg=color).grid(row=m+1,column=2,sticky="ew")
        Label(inner_frame,text="__________________________________________________________________",bg=view_color).grid(row=m+2,column=2,columnspan=7,sticky="ew")
        m+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:setup("viewrecords"))
    ok.grid(row=m+2,column=2,sticky="ew",padx=5)
        
    
    
    
def viewmin():#view min issued books
    clear_root()
    global color
    color=view_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    sql="SELECT ID FROM ISSUED"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    dic=dict()
    print(rows)
    for i in rows:
        dic[int(i[0])]=rows.count(i)
    min_value = min(dic.values())
    lst=[]
    print(dic)
    
    for i in dic:
        if dic[i]==min_value:
            lst.append(i)
    print(lst)
    Label(inner_frame,text="MINIMUM ISSUED BOOKS: ",font=heading2_font,bg=color).grid(row=4,column=3,sticky="ew",pady=30)
    sql="SELECT BOOKNAME, AUTHORNAME FROM BOOKS WHERE ID=%s"
    global m
    m=3
    for i in lst:
        mycursor.execute(sql,(i,))
        rows=mycursor.fetchall()
        m+=2
        Label(inner_frame,text="Book_Name: ",font=label_font,bg=color).grid(row=m,column=1,sticky="ew",pady=20)
        Label(inner_frame,text=rows[0][0],font=label2_font,bd=1,relief=SUNKEN,bg=color).grid(row=m,column=2,sticky="ew",pady=20)
        Label(inner_frame,text="Author_Name: ",font=label_font,bg=color).grid(row=m+1,column=1,sticky="ew")
        Label(inner_frame,text=rows[0][1],font=label2_font,bd=1,relief=SUNKEN,bg=color).grid(row=m+1,column=2,sticky="ew")
        Label(inner_frame,text="__________________________________________________________________").grid(row=m+2,column=2,columnspan=7,sticky="ew")
        m+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:setup("viewrecords"))
    ok.grid(row=m+2,column=2,sticky="ew",padx=5)
    
def viewissue():#view currently issued books
    clear_root()
    global color
    color=view_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="ISSUE BOOKS: ",height=4,font=heading_font,bg=color).grid(row=1,column=0,columnspan=5,sticky="ew")

    sql="SELECT * FROM ISSUE"
    mycursor.execute(sql)
    rows=mycursor.fetchall()
    mydb.commit()
    Label(inner_frame,text="BOOK_ID",height=3,font=label_font,bg=color).grid(row=2,column=0,sticky="ew")
    Label(inner_frame,text="BOOK_NAME",height=3,font=label_font,bg=color).grid(row=2,column=1,sticky="ew",padx=15)
    Label(inner_frame,text="AUTHOR_NAME",height=3,font=label_font,bg=color).grid(row=2,column=2,sticky="ew",padx=15)
    Label(inner_frame,text="STUDENT_NAME",height=3,font=label_font,bg=color).grid(row=2,column=3,sticky="ew",padx=15)
    Label(inner_frame,text="CONTACT",height=3,font=label_font,bg=color).grid(row=2,column=4,sticky="ew",padx=15)
    Label(inner_frame,text="DATE_OF_ISSUE",height=3,font=label_font,bg=color).grid(row=2,column=5,sticky="ew",padx=15)
    Label(inner_frame,text="DATE_OF_RETURN",height=3,font=label_font,bg=color).grid(row=2,column=6,sticky="ew",padx=15)
    global k
    k=3
    for row in rows:
        
        Label(inner_frame,text="-----------------------------").grid(row=k,column=0,columnspan=5,sticky="ew")
        k+=1
        Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=k,column=0,sticky="ew")
        Label(inner_frame,text=row[1],height=3,font=label2_font,bg=color).grid(row=k,column=1,sticky="ew",padx=15)
        Label(inner_frame,text=row[2],height=3,font=label2_font,bg=color).grid(row=k,column=2,sticky="ew",padx=15)
        Label(inner_frame,text=row[3],height=3,font=label2_font,bg=color).grid(row=k,column=3,sticky="ew",padx=15)
        Label(inner_frame,text=row[4],height=3,font=label2_font,bg=color).grid(row=k,column=4,sticky="ew",padx=15)
        Label(inner_frame,text=row[5],height=3,font=label2_font,bg=color).grid(row=k,column=5,sticky="ew",padx=15)
        Label(inner_frame,text=row[6],height=3,font=label2_font,bg=color).grid(row=k,column=6,sticky="ew",padx=15)
        k+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:setup("viewrecords"))
    ok.grid(row=k,column=2,sticky="ew",padx=5)        
    
             
    
#MAIN_FUNTION-8 : TO SEARCH FOR A PARTICULAR DATA IN THE LIBRARY
def search():
    clear_root()
    global color
    color=search_color
    root.configure(bg=color)
    Label(root,text="SEARCH FOR: ",height=5,font=heading_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    #bookname
    Label(root,text="Book_Name",font=label_font,height=4,bg=color).grid(row=2,column=0,pady=10,sticky="ew")
    book=Entry(root)
    book.grid(row=2,column=1,columnspan=5,sticky="ew")
    go_book=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:search_bookname(book.get()))
    go_book.grid(row=2,column=6,columnspan=2,padx=30,sticky="ew")
    #authorname
    Label(root,text="Author_Name",height=4,font=label_font,bg=color).grid(row=3,column=0,pady=10,sticky="ew")
    author=Entry(root)
    author.grid(row=3,column=1,columnspan=5,sticky="ew")
    go_author=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:search_authorname(author.get()))
    go_author.grid(row=3,column=6,columnspan=2,padx=30,sticky="ew")
    
    #quantity
    Label(root,text="Quantity",height=4,font=label_font,bg=color).grid(row=4,column=0,pady=10,sticky="ew")
    quantity=Entry(root)
    quantity.grid(row=4,column=1,columnspan=5,sticky="ew")
    go_quan=Button(root,text="GO",bg=button2_color,font=button2_font,bd=1,command=lambda:search_quantity(quantity.get()))
    go_quan.grid(row=4,column=6,columnspan=2,padx=30,sticky="ew")

    #done button
    done=Button(root,text="DONE",bg=button_color,font=button_font,command=lambda:setup("search"))
    done.grid(row=5,column=2,sticky="ew")

    
#Subfunctions of search()
def search_bookname(book):
    clear_root()
    global color
    color=search_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="DATA OF BOOK: "+book,height=5,font=heading2_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    sql="SELECT * FROM BOOKS WHERE BOOKNAME=%s"
    mycursor.execute(sql,(book,))
    rows=mycursor.fetchall()
    mydb.commit()
    #display the record
    if len(rows)==0:
        Label(inner_frame,text="\'"+book+"\'" +" IS NOT AVAILABLE IN STOCK",height=4,font=label_font,bg=color).grid(row=2,column=0,columnspan=7,sticky="ew")
        ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
        ok.grid(row=3,column=0,sticky="ew",padx=5)
    else:
        Label(inner_frame,text="ID",height=3,font=label_font,bg=color).grid(row=2,column=0,columnspan=3,sticky="ew")
        Label(inner_frame,text="AUTHORNAME",height=3,font=label_font,bg=color).grid(row=2,column=3,columnspan=3,sticky="ew")
        Label(inner_frame,text="QUANTITY",height=3,font=label_font,bg=color).grid(row=2,column=6,columnspan=3,sticky="ew")

        global l
        l=3
        for row in rows:
            
            Label(inner_frame,text="-----------------------------",bg=color).grid(row=l,column=0,columnspan=5,sticky="ew")
            l+=1
            Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=l,column=0,columnspan=3,sticky="ew")
            Label(inner_frame,text=row[2],height=3,font=label2_font,bg=color).grid(row=l,column=3,columnspan=3,sticky="ew",padx=15)
            Label(inner_frame,text=row[3],height=3,font=label2_font,bg=color).grid(row=l,column=6,columnspan=3,sticky="ew",padx=15)
            l+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
    ok.grid(row=l+1,column=0,sticky="ew",padx=5)
def search_authorname(author):
    clear_root()
    global color
    color=search_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="DATA OF AUTHOR: "+author,height=5,font=heading2_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    sql="SELECT * FROM BOOKS WHERE AUTHORNAME=%s"
    mycursor.execute(sql,(author,))
    rows=mycursor.fetchall()
    mydb.commit()
    #display the record
    if len(rows)==0:
        Label(inner_frame,text="\'"+author+"\'"+" IS NOT AVAILABLE IN STOCK",height=4,font=label_font,bg=color).grid(row=2,column=0,columnspan=7,sticky="ew")
        ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
        ok.grid(row=3,column=0,sticky="ew",padx=5)
    else:
        Label(inner_frame,text="ID",height=3,font=label_font,bg=color).grid(row=2,column=0,columnspan=3,sticky="ew")
        Label(inner_frame,text="BOOKNAME",height=3,font=label_font,bg=color).grid(row=2,column=3,columnspan=3,sticky="ew")
        Label(inner_frame,text="QUANTITY",height=3,font=label_font,bg=color).grid(row=2,column=6,columnspan=3,sticky="ew")

        global l
        l=3
        for row in rows:
            
            Label(inner_frame,text="_________________________________________________________________________________________________").grid(row=l,column=0,columnspan=5,sticky="ew")
            l+=1
            Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=l,column=0,columnspan=3,sticky="ew")
            Label(inner_frame,text=row[1],height=3,font=label2_font,bg=color).grid(row=l,column=3,columnspan=3,sticky="ew",padx=15)
            Label(inner_frame,text=row[3],height=3,font=label2_font,bg=color).grid(row=l,column=6,columnspan=3,sticky="ew",padx=15)
            l+=1
    
        ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
        ok.grid(row=l+1,column=0,sticky="ew",padx=5)
def search_quantity(quan):
    clear_root()
    global color
    color=search_color
    inner_frame, scrollbar = setup_scrollable_frame(root)
    Label(inner_frame,text="DATA OF QUANTITY: "+quan,height=5,font=heading2_font,bg=color).grid(row=1,column=0,columnspan=7,sticky="ew")
    sql="SELECT * FROM BOOKS WHERE QUANTITY=%s"
    mycursor.execute(sql,(int(quan),))
    rows=mycursor.fetchall()
    mydb.commit()
    #display the record
    if len(rows)==0:
        Label(inner_frame,text="\'"+quan+"\'"+" IS NOT AVAILABLE IN STOCK",height=4,font=label_font,bg=color).grid(row=2,column=0,columnspan=7,sticky="ew")
        ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
        ok.grid(row=3,column=0,sticky="ew",padx=5)
    else:
        Label(inner_frame,text="ID",height=3,font=label_font,bg=color).grid(row=2,column=0,columnspan=3,sticky="ew")
        Label(inner_frame,text="BOOKNAME",height=3,font=label_font,bg=color).grid(row=2,column=3,columnspan=3,sticky="ew")
        Label(inner_frame,text="AUTHORNAME",height=3,font=label_font,bg=color).grid(row=2,column=6,columnspan=3,sticky="ew")
        global l
        l=3
        for row in rows:
            
            Label(inner_frame,text="_______________________________________________________________________________________________________________________________________").grid(row=l,column=1,columnspan=6,sticky="ew")
            l+=1
            Label(inner_frame,text=row[0],height=3,font=label2_font,bg=color).grid(row=l,column=0,columnspan=3,sticky="ew")
            Label(inner_frame,text=row[1],height=3,font=label2_font,bg=color).grid(row=l,column=3,columnspan=3,sticky="ew",padx=15)
            Label(inner_frame,text=row[2],height=3,font=label2_font,bg=color).grid(row=l,column=6,columnspan=3,sticky="ew",padx=15)
            l+=1
    ok=Button(inner_frame,text="OK",font=button3_font,bg=button3_color,command=lambda:search())
    ok.grid(row=l+1,column=0,sticky="ew",padx=5)
    
#creating buttons
setup_button=Button(root,text="SetUp",bg=button_heading,command=lambda:set_lib()).grid(row=0,column=0,sticky="ew")
add_button=Button(root,text="Add",bg=button_heading,command=lambda:addbook()).grid(row=0,column=1,sticky="ew")
delete_button=Button(root,text="Delete",bg=button_heading,command=lambda:delbook()).grid(row=0,column=2,sticky="ew")
issue_button=Button(root,text="Issue",bg=button_heading,command=lambda:issuebook()).grid(row=0,column=3,sticky="ew")
return_button=Button(root,text="Return",bg=button_heading,command=lambda:returnbook()).grid(row=0,column=4,sticky="ew")
pending_button=Button(root,text="Pending",bg=button_heading,command=lambda:pending()).grid(row=0,column=5,sticky="ew")
view_button=Button(root,text="View_Records",bg=button_heading,command=lambda:viewrecords()).grid(row=0,column=6,sticky="ew")
search_button=Button(root,text="Search",bg=button_heading,command=lambda:search()).grid(row=0,column=7,sticky="ew")



root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.mainloop()
