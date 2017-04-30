from pymysql import *
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import datetime
from tkinter import messagebox

# Initial_Confriguations
db = Connect('localhost', 'root', '1234', 'mydb', 3306)
cursor = db.cursor()

# Window_Frames
def sign_up():
    signWin = Toplevel(root)
    signWin.title('** SignUp **')
    ttk.Label(signWin,text=' First Name : ').grid(row=0, column=0)
    fn=ttk.Entry(signWin)
    fn.grid(row=0, column=1)
    ttk.Label(signWin,text=' Last Name : ').grid(row=1, column=0)
    ln = ttk.Entry(signWin)
    ln.grid(row=1, column=1)
    ttk.Label(signWin,text=' Display Name : ').grid(row=2, column=0)
    dn = ttk.Entry(signWin)
    dn.grid(row=2, column=1)
    ttk.Label(signWin,text=' Password : ').grid(row=3, column=0)
    password = ttk.Entry(signWin,show='*')
    password.grid(row=3, column=1)

    def write():
        try:
            cursor.execute('Insert into blog_author(display_name,password,first_name,last_name) Values(%s,%s,%s,%s)', (dn.get(), password.get(), fn.get(), ln.get()))
            db.commit()
            msg = 'Operation Successful'
        except:
            print('Error in Writing')
            db.rollback()
            msg = 'Operation Failed'
        ttk.Label(signWin, text=msg).grid(row=5)

    ttk.Button(signWin, text='SignUp', command=write).grid(row=4)

def author_log_in():
    logWin = Toplevel(root)
    logWin.title('Log In')
    ttk.Label(logWin,text=' Display Name : ').grid(row=0,column=0)
    dn = ttk.Entry(logWin)
    dn.grid(row=0, column=1)
    ttk.Label(logWin, text=' Password : ').grid(row=1, column=0)
    password = ttk.Entry(logWin, show='*')
    password.grid(row=1, column=1)

    def check():
        cursor.execute('Select login_id from blog_author where display_name=%s and password=%s',(dn.get(),password.get()))
        author_id = cursor.fetchone()
        print(author_id)
        if not author_id:
            msg='Wrong Credentials'
        else:
            msg='\t Logging In \t'
            post(author_id[0])
        ttk.Label(logWin,text=msg).grid(row=3)
    ttk.Button(logWin, text='Log In', command=check).grid(row=2)


def post(author_id):
    postWin = Toplevel(root)
    postWin.title('** Post **')
    postWin.geometry('800x600')
    cursor.execute('Select display_name from blog_author where login_id= %s', author_id)
    authorDisplayName = cursor.fetchone()[0]
    Label(postWin, text=authorDisplayName, font='Times 40 bold').grid(row=0, column=1)
    date = datetime.datetime.now()
    post_date = str(date.year)+'-'+str(date.month)+'-'+str(date.day)+' '+str(date.hour)+':'+str(date.minute)+':'+str(date.second)
    ttk.Label(postWin, text='Title : ', font='Times 10 bold').grid(row=1, column=0, columnspan=1)
    title = ttk.Entry(postWin, width=50)
    title.grid(row=1, column=1, columnspan=3)
    ttk.Label(postWin, text='Write your Post here :', font='Times 10 bold').grid(row=2)
    post = ScrolledText(postWin)
    post.grid(row=3, column=1)
    commentEnabled = IntVar()
    ttk.Checkbutton(postWin, text='Comment Enabled', variable=commentEnabled ).grid(row=4, column=0)
    def write():
        try:
            cursor.execute('Insert into blog_post(title,article,date_published,comment_enabled,blog_author_login_id,stars) Values(%s,%s,%s,%s,%s,%s)', (title.get(), post.get(1.0, 'end-1c'), post_date, commentEnabled.get(), author_id, '0'))
            db.commit()
            msg = 'Post Successful'
        except ValueError:
            msg = 'Attempt Failed'
        ttk.Label(postWin, text=msg).grid(row=5, column=1)

    ttk.Button(postWin, text='Post', command=write).grid(row=4, column=1)


def home():
    homeWin = Toplevel(root)
    homeWin.geometry('225x250')
    homeWin.title('Authors')
    boxFrame = Frame(homeWin)
    scrollbar = ttk.Scrollbar(boxFrame)
    scrollbar.grid(row=0, column=1, sticky=NS)
    listbox = Listbox(boxFrame, yscrollcommand=scrollbar.set, fg='#0f0faf', bg='#89DA59', font='Consalas 12 italic')
    cursor.execute('Select * from blog_author')
    for row in cursor:
        listbox.insert(END, row[1])
    listbox.grid(row=0, column=0)
    scrollbar.config(command=listbox.yview)
    boxFrame.grid(row=0, column=0)

    def author_call():
        cursor.execute('Select login_id from blog_author where display_name= %s', listbox.get(ACTIVE))
        author(int(cursor.fetchone()[0]))

    ttk.Button(homeWin, text='Enter', command=author_call).grid()


def author(author_id):
    authorWin = Toplevel(root)
    authorWin.configure(bg='#d81b60')
    authorWin.geometry('260x300')
    authorWin.title('** Blogs **')
    cursor.execute('Select display_name from blog_author where login_id= %s', author_id)
    authorDisplayName = cursor.fetchone()[0]
    Label(authorWin, text=authorDisplayName, font='Times 25 bold', bg='#9c27b0').pack(fill=X)
    boxFrame = Frame(authorWin)
    scrollbar = ttk.Scrollbar(boxFrame)
    scrollbar.grid(row=0, column=1, sticky=NS)
    listbox = Listbox(boxFrame, yscrollcommand=scrollbar.set, fg='#0f0faf', bg='#89DA59', font='Consalas 12 italic')
    cursor.execute('Select * from blog_post where blog_author_login_id=%s',(author_id))
    for row in cursor:
        listbox.insert(0, row[1])
    listbox.grid(row=0, column=0)
    scrollbar.config(command=listbox.yview)
    boxFrame.pack()

    def blog_call():
        cursor.execute('Select id from blog_post where title= %s', listbox.get(ACTIVE))
        blogs(cursor.fetchone()[0], authorDisplayName)

    ttk.Button(authorWin, text='Enter', command=blog_call).pack()


def blogs(blogId, authorDisplayName):
    blogWin = Toplevel(root)
    blogWin.configure(bg='#dc67f0')
    blogWin.geometry('500x500')
    blogWin.title(authorDisplayName)
    Label(blogWin, text=authorDisplayName, font='Times 25 bold', bg='#8c17a0').pack(fill=X)
    cursor.execute('Select title from blog_post where id=%s', (blogId))
    title=cursor.fetchone()[0]
    Label(blogWin, text=title, font='Times 15 bold', bg='#ac37c0').pack(fill=X)
    cursor.execute('Select article from blog_post where id=%s', (blogId))
    content = cursor.fetchone()[0]
    contentWin = Frame(blogWin)
    Label(contentWin, text='\n'+content).pack(fill=X, pady=10)
    contentWin.pack()
    date = datetime.datetime.now()
    comment_date = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + ' ' + str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)

    commentWin = Frame(blogWin)
    scrollbar = ttk.Scrollbar(commentWin)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(commentWin,yscrollcommand=scrollbar.set, width=200, height=10, bg='#cccccc')

    ttk.Label(blogWin, text='Comments', font='Times 10 bold').pack()
    cursor.execute('Select * from blog_comment where blog_post_id=%s', (blogId))
    for i,com in enumerate(cursor.fetchall()):
        if int(com[6]):
            userName = 'Anonymous:  '
        elif int(com[5]):
            cursor.execute('Select name from blog_user where user_id=%s', (com[5]))
            userName = cursor.fetchone()[0]+':  '
        text = userName+str(com[1])
        listbox.insert(END,text)
    listbox.pack()
    scrollbar.config(command=listbox.yview)
    commentWin.pack(padx=40, pady=20, fill=X)

    comment = ScrolledText(blogWin, width=400, height=6)
    comment.pack(padx=25, fill=X)
    anonymous = IntVar()
    anonymous.set(1)
    ttk.Checkbutton(blogWin, text='Anonymous', variable=anonymous).pack(padx=30, side=LEFT)
    msg = 'status'

    def write():
        global msg
        if anonymous.get():
            try:
                cursor.execute('insert into blog_comment(comment_text,blog_post_id,date,anonymous) Values(%s,%s,%s,%s)', (comment.get(1.0, 'end-1c'), blogId, comment_date, '1'))
                db.commit()
                msg = 'Post Successful'
            except:
                msg = 'Attemp Failed'
        else:
            msg = ''
            logWin = Toplevel(root)
            logWin.title('Log In')
            ttk.Label(logWin, text=' Name : ').grid(row=0, column=0)
            dn = ttk.Entry(logWin)
            dn.grid(row=0, column=1)
            ttk.Label(logWin, text=' Password : ').grid(row=1, column=0)
            password = ttk.Entry(logWin, show='*')
            password.grid(row=1, column=1)

            def check():
                global msg
                cursor.execute('Select user_id from blog_user where name=%s and password=%s',
                               (dn.get(), password.get()))
                userId = cursor.fetchone()
                if userId:
                    msgin= 'Posted'
                    try:
                        cursor.execute(
                            'insert into blog_comment(comment_text,blog_post_id,date,blog_user_user_id,anonymous) Values(%s,%s,%s,%s,%s)',
                            (comment.get(1.0, 'end-1c'), blogId, comment_date, userId, '0'))
                        db.commit()
                        msg = 'Post Successful'
                    except:
                        msg = 'Attempt Failed'
                else:
                    msgin = 'Wrong Credentials'

                ttk.Label(logWin, text=msgin).grid(row=3)

            ttk.Button(logWin, text='Log In', command=check).grid(row=2)

        ttk.Label(blogWin, text=msg).pack(fill=X, side=BOTTOM)
    ttk.Button(blogWin, text='Post', command=write).pack(padx=40,side=RIGHT)


# Root_Window:
root = Tk()
root.title("Blogger's Pride ")
root.geometry('228x138')
root.config(bg='#6d7d8e')
Label(text="Blogger's Pride", font='Times 25 bold', bg='#4d5d6e').pack(fill=X)
key=ttk.Entry(root, width=30)
key.pack(side=TOP)

def search():
    find=key.get()
    cursor.execute('Select * from blog_author where display_name=%s or first_name=%s or last_name=%s',(find,find,find))
    result = cursor.fetchone()
    if result:
        author(result[0])
    else:
        cursor.execute('Select * from blog_post where title=%s',(find))
        result = cursor.fetchone()
        if result:
            blogId = result[0]
            cursor.execute('Select display_name from blog_author where login_id=%s',(result[8]))
            authorDisplayName = cursor.fetchone()[0]
            blogs(blogId, authorDisplayName)

ttk.Button(text='Search', command=search).pack()
ttk.Button(text='Login', command=author_log_in).pack(side=LEFT)
ttk.Button(text='Home', command=home).pack(side=LEFT)
ttk.Button(text='SignUp', command=sign_up).pack(side=LEFT)

#Closing_Confriguations:

#cursor.close()
#db.close()
root.mainloop()