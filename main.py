import requests
import pickle
import tkinter as tk
import tkinter.messagebox
from jxgl import login, getKccj, getTjfx
import os


def login_with_enter(self):
    """
    只是用来配合enter事件监听罢了
    :return: None
    """
    user_login()


def user_login():
    """
    登录command for 登录按钮，调用login()返回状态信息并作出反应，调用getKccj(), getTjfx()使得在当前目录生成 'all-result.txt'
    :return: None
    """
    user_name = var_user_name.get()
    user_pwd = var_user_pwd.get()
    login_text.place(x=55, y=140)
    window.update_idletasks()

    # if user_name == '2018002009':
    #     tkinter.messagebox.showwarning(title='Warning', message='怎么回事？小老弟~')
    #     return

    try:
        result = login(user_name, user_pwd)
        if '登录成功。' not in result:
            tkinter.messagebox.showerror(title='Error', message=result)
        else:
            getKccj()
            getTjfx()
            login_text.place_forget()
            tkinter.messagebox.showinfo(title='Clear', message='登录成功')
            remember_me()
    except requests.Timeout:
        tkinter.messagebox.showerror(title='Error', message='登录超时！')
    except:
        tkinter.messagebox.showerror(title='Error', message='程序出错！')


def user_search():
    """
    查询command for查询按钮：在Text文本框中输出 'all_result.txt' 中的全部内容
    :return: None
    """
    try:
        with open('user/all_result.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                text_show_result.insert('end', line)
                text_show_result.insert(tk.INSERT, '\n')
    except:
        tk.messagebox.showerror(title='Error', message='程序出错！')


def remember_me():
    """
    发生在按下登录按钮以后。判断 '记住我' Checkbutton：若勾选，在登录成功后保存至 'user_info.pkl'，否则清空 'user_info.pkl'
    :return: None
    """
    if var_ck_remember.get() == 1:
        with open('user/user_info.pkl', 'wb') as f:
            user_name = var_user_name.get()
            user_pwd = var_user_pwd.get()
            user_info = (user_name, user_pwd)
            pickle.dump(user_info, f)
    else:
        f = open('user/user_info.pkl', 'wb')
        f.close()


if __name__ == '__main__':
    if not os.path.exists(r'user/'):
        os.mkdir(r'user/')

    window = tk.Tk()
    window.title('TyPT')
    window.geometry('1000x600')

    # 用户信息输入提示
    tk.Label(window, text='学号:', font=('Arial', 14)).place(x=10, y=10)
    tk.Label(window, text='密码:', font=('Arial', 14)).place(x=10, y=50)
    login_text = tk.Label(window, text='正在登录...', font=('宋体', 10))
    login_text.place_forget()

    # 用户输入框
    # 学号
    var_user_name = tk.StringVar()
    var_user_name.set('')
    entry_user_name = tk.Entry(window, textvariable=var_user_name, font=('Arial', 14))
    entry_user_name.place(x=70, y=13)
    # 密码
    var_user_pwd = tk.StringVar()
    var_user_pwd.set('')
    entry_user_pwd = tk.Entry(window, textvariable=var_user_pwd, show='*', font=('Arial', 14))
    entry_user_pwd.place(x=70, y=53)

    # 登录按钮
    btn_login = tk.Button(window, text='登录', command=user_login)
    btn_login.place(x=60, y=100)

    # 查询按钮
    btn_search = tk.Button(window, text='查询', command=user_search)
    btn_search.place(x=210, y=100)

    # Text窗口
    text_show_result = tk.Text(window, width=700, height=44)
    text_show_result.place(x=300, y=10)

    # 图片Canvas
    canvas = tk.Canvas(window, height=360, width=270)
    image_file = tk.PhotoImage(file='image.png')
    image = canvas.create_image(135, 180, image=image_file)
    canvas.place(x=15, y=200)

    # check_botton -记住我
    var_ck_remember = tk.IntVar()
    var_ck_remember.set(1)
    ck_remember = tk.Checkbutton(window, text='记住我', variable=var_ck_remember, onvalue=1, offvalue=0)
    ck_remember.place(x=100, y=110)

    # 事件监听，用enter键登录
    window.bind("<Return>", login_with_enter)

    # 读取记忆中的user_info
    try:
        with open('user/user_info.pkl', 'rb') as f:
            user_info = pickle.load(f)
            (user_name, user_passpwd) = user_info
            var_user_name.set(str(user_name))
            var_user_pwd.set(str(user_passpwd))
    except:
        var_user_name.set('')
        var_user_pwd.set('')

    window.mainloop()
