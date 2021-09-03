# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 12:53
# @Author  : HUII
# @FileName: client.py
# @Software: PyCharm
import configparser
import json
import time
import socket
import tkinter as tk
from tkinter import messagebox
from rc4 import rc4

config = configparser.ConfigParser()
config.read('config.ini')
KEY = config.get('key', 'key')
# 设置连接超时
socket.setdefaulttimeout(2)

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.key = ''
        self.label_style1 = {
            'width': 15,
            'font': ('微软雅黑', 15)
        }
        self.label_style2 = {
            'width': 12,
            'font': ('微软雅黑', 15)
        }
        self.label_style3 = {
            'width': 8,
            'font': ('微软雅黑', 15)
        }
        self.button_small_style = {
            'width': 8,
            'height': 1,
            'font': ('微软雅黑', 10)
        }
        self.entry_style = {
            'font': ('微软雅黑', 15)
        }
        self.text_style = {
            'height': 1,
            'font': ('微软雅黑', 13)
        }
        self.init_gui()

    def connect(self):
        """
        连接服务器
        :return:
        """
        host = self.ip_val.get()
        port = self.port_val.get()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise OverflowError
        except:
            self.show_info((False, '端口号格式错误'))
            return False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((host, port))
            return True
        except:
            self.show_info((False, '连接失败,请检查服务器状态'))
            return False

    def test_connect(self):
        """
        测试连接服务器
        :return:
        """
        if self.connect():
            self.identity = str(int(time.time()))
            try:
                self.client.send(f'getkey:identity={self.identity}'.encode("utf-8"))
                time_key = self.client.recv(1024).decode("utf-8")
            except:
                self.show_info((False, '连接失败,请检查服务器状态'))
                return False
            if time_key == 'close':
                self.key = ''
                self.show_info((False, '连接失败,请检查服务器状态'))
            else:
                print(str(time_key)[:10])
                self.key = rc4(str(time_key)[:10], KEY)
                self.show_info((True, '成功连接上服务器'))
                self.transform()
        else:
            self.key = ''


    def send(self):
        """
        发送消息
        :return:
        """
        s_msg = self.raw_input.get(1.0, tk.END)

        if len(s_msg) <= 1:
            self.show_info((False, '内容不得为空'))
            return False

        if not self.connect():
            return False

        if not self.key:
            self.show_info((False, '请先点击“连接服务器”'))
            return False

        rc4_msg = rc4(s_msg, self.key)
        send_content = json.dumps({
            'content': rc4_msg,
            'identity': self.identity
        })
        print(send_content)
        self.client.send(send_content.encode("utf-8"))
        msg = self.client.recv(1024)
        smsg = msg.decode("utf-8")
        if smsg == 'success':
            self.show_info((True, '发送成功'))
            self.clean()
        elif smsg == 'close':
            self.show_info((False, '连接失败,请检查服务器状态'))
        elif smsg == 'error':
            self.show_info((False, '出现异常，请检查服务器状态或重新连接服务器！'))
        elif smsg == 'long':
            self.show_info((False, '发送内容过长！'))

    def clean(self):
        """
        清空输入内容
        :return:
        """
        self.raw_input.delete(1.0, tk.END)
        self.encode_input.delete(1.0, tk.END)

    def transform(self, event=None):
        """
        输入时实时加密
        :param event:
        :return:
        """
        if not self.key:
            self.show_info((False, '请先连接服务器或检查服务器状态！'))
            return False
        try:
            self.encode_input.delete(1.0, tk.END)
            encode_text = rc4(self.raw_input.get(1.0, tk.END), self.key)
            self.encode_input.insert(tk.INSERT, encode_text if len(encode_text) > 1 else '')
        except:
            pass

    def quit(self):
        """
        退出系统
        :return:
        """
        ask = messagebox.askyesno('确认退出', '您是否真的要退出本系统？socket连接将中断！')
        if ask:
            self.root.destroy()

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

    def init_gui(self):
        # 显示ip部分开始
        head_frame = tk.Frame(self.frame)
        head_frame.pack(side=tk.TOP)
        ip_label = tk.Label(head_frame)
        ip_label.grid(row=0, column=0)
        ip_label.config(text='设置服务端ip地址：', **self.label_style1)
        self.ip_val = tk.StringVar()
        self.ip_val.set('127.0.0.1')
        ip_input = tk.Entry(head_frame)
        ip_input.config(**self.label_style1)
        ip_input.config(textvariable=self.ip_val)
        ip_input.grid(row=0, column=1)

        port_label = tk.Label(head_frame)
        port_label.grid(row=0, column=2)
        port_label.config(text='服务器端口：', **self.label_style2)
        self.port_val = tk.StringVar()
        self.port_val.set(8001)
        port_input = tk.Entry(head_frame)
        port_input.config(**self.label_style2)
        port_input.config(textvariable=self.port_val)
        port_input.grid(row=0, column=3)
        test_connect_btn = tk.Button(head_frame, text='连接服务器', command=self.test_connect, **self.button_small_style)
        test_connect_btn.grid(row=0, column=4)

        # 显示ip部分结束
        # 明文开始
        raw_frame = tk.Frame(self.frame)
        raw_frame.pack(fill=tk.BOTH, expand=True)
        raw_label = tk.Label(raw_frame, text='发送消息明文', **self.label_style2)
        raw_label.pack(side=tk.LEFT)
        self.raw_input = tk.Text(raw_frame, **self.text_style)

        # self.raw_val = tk.StringVar()
        # raw_input = tk.Entry(raw_frame, textvariable=self.raw_val, **self.entry_style)
        self.raw_input.pack(fill=tk.BOTH, expand=True)
        self.raw_input.bind('<KeyRelease>', self.transform)

        # 明文结束
        # 加密开始
        encode_frame = tk.Frame(self.frame)
        encode_frame.pack(fill=tk.BOTH, expand=True)
        encode_label = tk.Label(encode_frame, text='加密后的消息', **self.label_style2)
        encode_label.pack(side=tk.LEFT)
        # self.encode_val = tk.StringVar()
        # encode_input = tk.Entry(encode_frame, textvariable=self.encode_val, state='readonly', **self.entry_style)
        self.encode_input = tk.Text(encode_frame, **self.text_style)
        self.encode_input.pack(fill=tk.BOTH, expand=True)

        # 加密结束
        # 底部开始
        buttom_frame = tk.Frame(self.frame)
        buttom_frame.pack(side=tk.BOTTOM)
        send_botton = tk.Button(buttom_frame, command=self.send, text='发送', **self.button_small_style)
        send_botton.grid(row=0, column=0)
        clean_botton = tk.Button(buttom_frame, command=self.clean, text='清空内容', **self.button_small_style)
        clean_botton.grid(row=0, column=2)
        close_botton = tk.Button(buttom_frame, command=self.quit, text='关闭', **self.button_small_style)
        close_botton.grid(row=0, column=4)
        # 底部结束


def main():
    root = tk.Tk()
    client = ClientGUI(root)
    root.title('客户端 2019217872 郑辉 电信科19-3班 信息系统软件设计 作业题3')
    root.iconbitmap('logo.ico')
    root.geometry('800x450+220+60')
    root.protocol("WM_DELETE_WINDOW", client.quit)
    root.mainloop()


if __name__ == '__main__':
    main()
