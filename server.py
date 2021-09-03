# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 12:53
# @Author  : HUII
# @FileName: server.py
# @Software: PyCharm
import configparser
import json
import threading
import time
import tkinter as tk
import socket

from tkinter import messagebox, ttk
from threading import Thread

from rc4 import rc4
from sql import test_connect, SqlManage

config = configparser.ConfigParser()
config.read('config.ini')
KEY = config.get('key', 'key')


class ChatData:
    def __init__(self):
        self.chat = SqlManage('chat')

    def get(self):
        """
        获得信息记录列表
        :return:
        """
        sql = 'select * from chat order by create_time desc;'
        res = self.chat.carry(sql)
        return res

    def save(self, ip, content, key):
        """
        保存信息
        :param key: 密钥
        :param ip:
        :param content: 消息内容
        :return:
        """
        self.chat.insert({
            'ip': ip,
            'content': content,
            '`key`': key
        })


class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.check_db_con()
        self.start_s = False
        self.chat = ChatData()
        self.keys = {}
        self.entry_style = {
            'font': ('微软雅黑', 15)
        }

        self.label_style1 = {
            'width': 13,
            'font': ('微软雅黑', 15)
        }
        self.label_style2 = {
            'width': 8,
            'font': ('微软雅黑', 15)
        }
        self.button_small_style = {
            'width': 8,
            'height': 1,
            'font': ('微软雅黑', 10)
        }

        self.text_style = {
            'width': 1,
            'font': ('微软雅黑', 13)
        }
        self.init_gui()

    def check_db_con(self):
        """
        检查数据库连接情况
        :return:
        """
        if not test_connect():
            messagebox.showerror('数据库错误', '数据库连接异常！请检查数据库连接后再打开本软件！')
            self.root.destroy()

    def quit(self):
        """
        退出提示
        :return:
        """
        ask = messagebox.askyesno('确认退出', '您是否真的要退出本系统？socket连接将中断！')
        if ask:
            self.root.destroy()

    def refresh(self):
        """
        刷新表格
        :return:
        """
        for c in self.tree.get_children():
            self.tree.delete(c)
        for i, value in enumerate(self.get_data()):
            self.tree.insert("", i, text=i + 1, values=[i if i is not None else '' for i in value])  # 0 为列的下标，第0行
            self.tree.tag_configure('oddrow', font='Arial 20')

    def clean_timeout_key(self):
        """
        清除长期不用的key
        :return:
        """
        while True:
            time.sleep(10 * 60)
            print(self.keys)
            print('清除过期密钥中。。。')
            now = int(time.time())
            for k, v in self.keys.items():
                if now - v['update_time'] > 30 * 60:
                    print(f'清除了{k}的密钥')
                    del self.keys[k]
            print(self.keys)

    def get_key(self):
        """
        获得加密密钥
        :return:
        """
        import time
        now = int(time.time())
        key = rc4(str(now)[:10], KEY)
        print(key)
        return key, now

    def get_message(self):
        """
        从客户端获得数据
        :return:
        """

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.port_val.get()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise OverflowError
        except:
            self.start_s = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.show_info((False, '端口号格式错误'))
            return False

        self.s.bind(('0.0.0.0', port))
        self.s.listen(10)
        while True:
            try:
                self.c, addr = self.s.accept()  # 建立客户端连接
            except:
                break
            ip = addr[0]
            print(f'来自{ip}的连接')

            msg = self.c.recv(10240).decode('utf-8')
            if 'getkey:identity=' in msg:
                identity = msg.split('=')[1]
                key, time_key = self.get_key()
                self.keys[identity] = {
                    'key': key,
                    'update_time': time_key
                }
                self.c.send(str(time_key).encode("utf-8"))
                self.c.close()
                print(self.keys)
            else:
                try:
                    try:
                        data = json.loads(msg)
                    except:
                        self.c.send('long'.encode("utf-8"))
                        self.c.close()
                        return False
                    key = self.keys.get(data['identity'])['key']
                    self.keys[data['identity']]['update_time'] = int(time.time())
                    content = data['content']

                    self.or_text.delete(0.0, tk.END)
                    self.par_text.delete(0.0, tk.END)
                    self.or_text.insert(tk.INSERT, content)
                    self.par_text.insert(tk.INSERT, rc4(content, key))

                    self.save_msg(ip, content, key)
                    self.c.send('success'.encode("utf-8"))
                    t2 = threading.Thread(target=self.refresh)
                    t2.start()

                except:
                    self.c.send('error'.encode("utf-8"))
                finally:
                    self.c.close()

    @staticmethod
    def get_ip_address():
        """
        获得本机ip地址
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        finally:
            s.close()
        return ip

    @staticmethod
    def show_info(info):
        """
        弹窗显示信息
        :param info:
        :return:
        """
        if info[0]:
            messagebox.showinfo('提示', info[1])
        else:
            messagebox.showerror('提示', info[1])

    def start(self):
        """
        启动服务
        :return:
        """
        # self.status = 1
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        # print(self.port_val.get())
        if not self.start_s:
            self.start_s = True
            thread = Thread(target=self.get_message)
            thread.setDaemon(True)
            thread.start()

    def stop(self):
        """
        停止服务
        :return:
        """
        try:
            self.c.close()
            print('关闭c成功')
        except:
            print('关闭c失败')
        self.s.close()
        self.start_s = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def get_data(self):
        """
        从数据库获得信息
        :return:
        """
        datas = list(self.chat.get())
        return datas

    def save_msg(self, ip, msg, key):
        """
        保存消息
        :param ip:
        :param msg:
        :return:
        """
        if msg:
            self.chat.save(ip, msg, key)

    def treeview_click(self, event):
        """
        单击事件获得内容
        :return:
        """
        for value in self.tree.selection():
            raw = self.tree.item(value, "values")[2]
            key = self.tree.item(value, "values")[4]
            parsed = rc4(raw, key)
            self.or_text.delete(0.0, tk.END)
            self.par_text.delete(0.0, tk.END)
            self.or_text.insert(tk.INSERT, raw)
            self.par_text.insert(tk.INSERT, parsed)

    def init_gui(self):
        # 显示ip部分开始
        head_frame = tk.Frame(self.frame)
        head_frame.pack(side=tk.TOP)
        ip_label = tk.Label(head_frame)
        ip_label.grid(row=0, column=0)
        ip_label.config(text='服务器ip地址：', **self.label_style1)
        ip = self.get_ip_address()
        ip_val = tk.StringVar()
        ip_val.set(ip)
        ip_input = tk.Entry(head_frame)
        ip_input.config(**self.label_style1)
        ip_input.config(textvariable=ip_val, state='readonly')
        ip_input.grid(row=0, column=1)

        port_label = tk.Label(head_frame)
        port_label.grid(row=0, column=2)
        port_label.config(text='服务器端口：', **self.label_style1)
        self.port_val = tk.StringVar()
        self.port_val.set(8001)
        port_input = tk.Entry(head_frame)
        port_input.config(**self.label_style2)
        port_input.config(textvariable=self.port_val)
        port_input.grid(row=0, column=3)
        self.start_btn = tk.Button(head_frame, text='启动', command=self.start, **self.button_small_style)
        self.start_btn.grid(row=0, column=4)
        self.stop_btn = tk.Button(head_frame, text='停止', command=self.stop, **self.button_small_style)
        self.stop_btn.grid(row=0, column=5)
        self.stop_btn.config(state=tk.DISABLED)

        # 显示ip部分结束
        # 消息记录开始
        chat_ls_frame = tk.Frame(self.frame)
        chat_ls_frame.pack(fill=tk.X)
        chat_ls_label = tk.Label(chat_ls_frame, text='服务器接收数据记录')
        chat_ls_label.pack()
        self.tree = ttk.Treeview(chat_ls_frame)
        columns = ('id', '客户端IP地址', '接收到的内容', '接收时间', '加密密钥')
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        for column in columns:
            self.tree.column(column, width=100, anchor="center")
            self.tree.heading(column, text=column)
        # 数据加载过慢
        treedata = Thread(target=self.refresh)
        treedata.start()
        # 添加滚动条
        scroll = tk.Scrollbar(chat_ls_frame, orient='vertical', command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind('<ButtonRelease-1>', self.treeview_click)
        # 消息记录结束
        # 消息内容开始

        msg_content_frame = tk.Frame(self.frame)
        msg_content_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        la_frame = tk.Frame(msg_content_frame)
        la_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        origin_label = tk.Label(la_frame, text='原始内容')
        origin_label.pack(side=tk.LEFT, expand=True)
        parsed_label = tk.Label(la_frame, text='解析后内容')
        parsed_label.pack(side=tk.RIGHT, expand=True)

        input_frame = tk.Frame(msg_content_frame)
        input_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.or_text = tk.Text(input_frame, **self.text_style)
        self.or_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.par_text = tk.Text(input_frame, **self.text_style)
        self.par_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 消息内容结束
        threading1 = Thread(target=self.clean_timeout_key)
        threading1.setDaemon(True)
        threading1.start()


def main():
    root = tk.Tk()
    server = ServerGUI(root)
    root.title('服务端 2019217872 郑辉 电信科19-3班 信息系统软件设计 作业题3')
    root.iconbitmap('logo.ico')
    root.geometry('800x450+180+40')
    root.protocol("WM_DELETE_WINDOW", server.quit)

    root.mainloop()


if __name__ == '__main__':
    main()
