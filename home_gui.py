# -*- coding: utf-8 -*-
# @Time    : 2021/6/21 23:29
# @Author  : HUII
# @FileName: home_gui.py
# @Software: PyCharm
import tkinter as tk
from tkinter import messagebox, ttk

from course import Course
from sql import test_connect
from student import Student
from student_select_course import StudentSelectCourse


class HomeGUI:
    """
    首页页面
    """

    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root, bg='#91beff')
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.check_db_con()
        self.now_checked = 0
        self.choose_window_on = False
        self.checked_color = {
            'bg': '#22c9c9',
            'fg': 'white'
        }
        self.not_checked_color = {
            'bg': 'white',
            'fg': 'black'
        }
        self.button_big_style = {
            'width': 12,
            'height': 2,
            'font': ('微软雅黑', 15)
        }
        self.button_small_style = {
            'width': 8,
            'height': 1,
            'font': ('微软雅黑', 10)
        }
        self.label_btn_style = {
            'width': 12,
            'font': ('微软雅黑', 12)
        }
        self.label_style = {
            'font': ('微软雅黑', 15)
        }
        self.bg = {
            'bg': 'white'
        }
        self.tree_data_item = ()
        self.basic_title = '选课系统管理平台-'
        self.init_gui()

    def init_gui(self):
        """
        初始化界面
        :return:
        """
        # 左侧导航栏设置
        self.sidebar = tk.Frame(self.frame, bg='gray', height=100, width=13)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        # 顶部标题栏设置
        self.title = tk.Label(self.frame, font=('微软雅黑', 28), text=f'{self.basic_title}欢迎页', bg='#91beff', fg='white')
        self.title.pack(side=tk.TOP)
        # 底部版权设置
        copyright = tk.Label(self.frame, font=('楷体', 10), text='作者：郑辉 学号：2019217872 班级：电信科19-3班')
        # copyright.config(bg='white')
        copyright.pack(side=tk.BOTTOM, fill=tk.BOTH)
        # 内容设置
        self.content = tk.Frame(self.frame)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # 欢迎页内容
        welcome = tk.Label(self.content, text='欢迎来到选课管理系统！\n作者：郑辉 电信科19-3班 \n学号：2019217872', font=('微软雅黑', 25),
                           **self.bg)
        welcome.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 导航栏按钮设置
        self.student_button = tk.Button(self.sidebar, text='学生管理', command=self.stu_frame, **self.button_big_style)
        self.student_button.grid(row=1)
        self.course_button = tk.Button(self.sidebar, text='课程管理', command=self.cou_frame, **self.button_big_style)
        self.course_button.grid(row=4)
        self.sc_button = tk.Button(self.sidebar, text='选课管理', command=self.sc_frame, **self.button_big_style)
        self.sc_button.grid(row=7)
        exit_button = tk.Button(self.sidebar, text='退出系统', command=self.quit, **self.button_small_style)
        exit_button.grid(row=10)
        col_count, row_count = self.sidebar.grid_size()
        # 设置按钮之间距离
        for row in range(row_count):
            self.sidebar.grid_rowconfigure(row, minsize=18)

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

    @staticmethod
    def del_confirm():
        return messagebox.askyesno('确认删除？', '您是否真的要删除本条数据？注意：删除操作是不可逆的！')

    @staticmethod
    def del_sc_confirm():
        return messagebox.askyesno('确认删除？', '您是否真的删除该数据相关所有选课信息？注意：删除操作是不可逆的！')

    def adjust_button_distance(now):
        """
        设置按钮之间距离
        :param now:
        :return:
        """

        def func(frame):
            def decorate(self):
                print(now, self.now_checked)
                if now == self.now_checked:
                    return False
                frame(self)
                col_count, row_count = self.op_frame.grid_size()
                for column in range(col_count):
                    self.op_frame.grid_columnconfigure(column, minsize=40)
                for row in range(row_count):
                    self.op_frame.grid_rowconfigure(row, minsize=15)

            return decorate

        return func

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
        退出系统提示
        :return:
        """
        ask = messagebox.askyesno('确认退出', '您是否真的要退出本系统？请确保数据已保存,否则数据可能丢失！')
        if ask:
            self.root.destroy()

    def clean_frame_content(self):
        """
        清空页面内原来的内容
        :return:
        """
        for widget in self.content.winfo_children():
            widget.destroy()

    def clean_entry(self):
        """
        清除所有输入框内容
        :return:
        """
        for entry in self.entries:
            entry.set('')

    def treeview_click(self, event):
        """
        单击事件获得内容
        :return:
        """
        for value in self.tree.selection():
            tree_data_item = self.tree.item(value, "values")
            for i, enter_val in enumerate(self.entries):
                enter_val.set(tree_data_item[i])

    def refresh_tree(self, data):
        for c in self.tree.get_children():
            self.tree.delete(c)
        for i, value in enumerate(data):
            self.tree.insert("", i, text=i + 1, values=[i if i != None else '' for i in value])  # 0 为列的下标，第0行
            self.tree.tag_configure('oddrow', font='Arial 20')

    def data_table(self, parent, columns, data):
        self.tree = ttk.Treeview(parent)
        columns = columns
        style_value = ttk.Style()
        style_value.configure("Treeview", rowheight=25, font=("微软雅黑", 13))
        self.tree['columns'] = columns
        for column in columns:
            self.tree.column(column, width=100, anchor="center")
            self.tree.heading(column, text=column)
        self.tree.column("#0", width=8, anchor="center")
        self.refresh_tree(data)
        # 添加滚动条
        scroll = tk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.configure(yscrollcommand=scroll.set)
        # 绑定点击事件
        self.tree.bind('<ButtonRelease-1>', self.treeview_click)

    @adjust_button_distance(1)
    def stu_frame(self):
        """
        学生管理页面
        :return:
        """

        def get_values():
            sno = no_val.get()
            sname = name_val.get()
            ssex = sex_val.get()
            sage = age_val.get()
            sdept = dept_val.get()
            dt = {}
            if sno:
                dt['Sno'] = sno
            if sname:
                dt['Sname'] = sname
            if ssex:
                dt['Ssex'] = ssex
            if sage:
                dt['Sage'] = sage
            if sdept:
                dt['Sdept'] = sdept
            return dt

        def search_stu():
            """
            搜索学生
            :return:
            """
            dt = get_values()
            res = Student().select_student(dt)
            self.refresh_tree(res)

        def add_stu():
            """
            添加学生
            :return:
            """
            dt = get_values()
            res = Student().add_student(
                sno=dt.get('Sno'),
                sname=dt.get('Sname'),
                ssex=dt.get('Ssex'),
                sage=dt.get('Sage'),
                sdept=dt.get('Sdept')
            )
            self.show_info(res)
            if res[0]:
                self.clean_entry()
                search_stu()

        def update_stu():
            """
            修改学生信息
            :return:
            """
            dt = get_values()
            res = Student().edit_student(dt['Sno'], dt)
            self.show_info(res)
            if res[0]:
                self.clean_entry()
                search_stu()

        def del_stu_sc():
            """
            删除学生选课
            :return:
            """
            if self.del_sc_confirm():
                dt = get_values()
                res = Student().delete_student_sc(dt['Sno'])
                self.show_info(res)
                if res[0]:
                    self.clean_entry()
                    search_stu()

        def del_stu():
            """
            删除学生信息
            :return:
            """
            if self.del_confirm():
                dt = get_values()
                res = Student().delete_student(dt['Sno'])
                self.show_info(res)
                if res[0]:
                    self.clean_entry()
                    search_stu()

        self.now_checked = 1
        self.clean_frame_content()
        self.student_button.config(**self.checked_color)
        self.course_button.config(**self.not_checked_color)
        self.sc_button.config(**self.not_checked_color)
        self.title.config(text=f'{self.basic_title}学生管理')
        table_frame = tk.Frame(self.content)
        table_frame.pack(side=tk.TOP, fill=tk.X)
        columns = ('学号', '姓名', '性别', '年龄', '所在系')
        students = Student().select_student()
        self.data_table(table_frame, columns, students)

        self.op_frame = tk.Frame(self.content)
        self.op_frame.pack(fill=tk.BOTH)
        no_label = tk.Label(self.op_frame, text=columns[0], **self.label_style)
        no_label.grid(row=0, column=1)
        name_label = tk.Label(self.op_frame, text=columns[1], **self.label_style)
        name_label.grid(row=2, column=1)
        sex_label = tk.Label(self.op_frame, text=columns[2], **self.label_style)
        sex_label.grid(row=4, column=1)
        age_label = tk.Label(self.op_frame, text=columns[3], **self.label_style)
        age_label.grid(row=6, column=1)
        dept_label = tk.Label(self.op_frame, text=columns[4], **self.label_style)
        dept_label.grid(row=8, column=1)
        no_val = tk.StringVar()
        name_val = tk.StringVar()
        sex_val = tk.StringVar()
        age_val = tk.StringVar()
        dept_val = tk.StringVar()
        no_entry = tk.Entry(self.op_frame, textvariable=no_val)
        no_entry.grid(row=0, column=3)
        name_entry = tk.Entry(self.op_frame, textvariable=name_val)
        name_entry.grid(row=2, column=3)
        sex_entry = tk.Entry(self.op_frame, textvariable=sex_val)
        sex_entry.grid(row=4, column=3)

        age_entry = tk.Entry(self.op_frame, textvariable=age_val)
        age_entry.grid(row=6, column=3)

        dept_entry = tk.Entry(self.op_frame, textvariable=dept_val)
        dept_entry.grid(row=8, column=3)

        self.entries = [no_val, name_val, sex_val, age_val, dept_val]
        clean_button = tk.Button(self.op_frame, command=self.clean_entry, text='清空输入框', **self.label_btn_style)
        clean_button.grid(row=0, column=7)
        search_button = tk.Button(self.op_frame, command=search_stu, text='查找', **self.label_btn_style)
        search_button.grid(row=2, column=7)
        add_button = tk.Button(self.op_frame, command=add_stu, text='添加', **self.label_btn_style)
        add_button.grid(row=4, column=7)
        update_button = tk.Button(self.op_frame, command=update_stu, text='修改(按学号)', **self.label_btn_style)
        update_button.grid(row=6, column=7)
        delete_button = tk.Button(self.op_frame, command=del_stu, text='删除(按学号)', **self.label_btn_style)
        delete_button.grid(row=8, column=7)
        delete_sc_button = tk.Button(self.op_frame, command=del_stu_sc, text='删除所有选课', **self.label_btn_style)
        delete_sc_button.grid(row=8, column=9)

    @adjust_button_distance(2)
    def cou_frame(self):
        """
        课程管理界面
        :return:
        """

        def get_values():
            no = no_val.get()
            name = name_val.get()
            pno = pno_val.get()
            credit = credit_val.get()
            dt = {}
            if no:
                dt['Cno'] = no
            if name:
                dt['Cname'] = name
            if pno:
                dt['Cpno'] = pno
            if credit:
                dt['Ccredit'] = credit
            return dt

        def search_cou():
            dt = get_values()
            print(dt)
            res = Course().select_course(dt)
            self.refresh_tree(res)

        def add_cou():
            dt = get_values()
            res = Course().add_course(
                cname=dt['Cname'],
                ccredit=dt['Ccredit'],
                cpno=dt['Cpno'] if dt.get('Cpno') else '',
            )
            self.show_info(res)
            if res[0]:
                self.clean_entry()
                search_cou()

        def update_cou():
            dt = get_values()
            res = Course().edit_course(dt['Cno'], dt)
            self.show_info(res)
            if res[0]:
                self.clean_entry()
                search_cou()

        def del_cou():
            if self.del_confirm():
                dt = get_values()
                res = Course().delete_course(dt['Cno'])
                self.show_info(res)
                if res[0]:
                    self.clean_entry()
                    search_cou()

        def del_cou_sc():
            if self.del_confirm():
                dt = get_values()
                res = Course().delete_course_sc(dt['Cno'])
                self.show_info(res)
                if res[0]:
                    self.clean_entry()
                    search_cou()

        self.now_checked = 2
        self.clean_frame_content()
        self.student_button.config(**self.not_checked_color)
        self.course_button.config(**self.checked_color)
        self.sc_button.config(**self.not_checked_color)
        self.title.config(text=f'{self.basic_title}课程管理')
        table_frame = tk.Frame(self.content)
        table_frame.pack(side=tk.TOP, fill=tk.X)
        columns = ('课程编号', '课程名称', '先修课编号', '学分')
        courses = Course().select_course()
        self.data_table(table_frame, columns, courses)

        self.op_frame = tk.Frame(self.content)
        self.op_frame.pack(fill=tk.BOTH)
        no_label = tk.Label(self.op_frame, text=columns[0], **self.label_style)
        no_label.grid(row=0, column=1)
        name_label = tk.Label(self.op_frame, text=columns[1], **self.label_style)
        name_label.grid(row=2, column=1)
        pno_label = tk.Label(self.op_frame, text=columns[2], **self.label_style)
        pno_label.grid(row=4, column=1)
        credit_label = tk.Label(self.op_frame, text=columns[3], **self.label_style)
        credit_label.grid(row=6, column=1)

        no_val = tk.StringVar()
        name_val = tk.StringVar()
        pno_val = tk.StringVar()
        credit_val = tk.StringVar()
        no_entry = tk.Entry(self.op_frame, textvariable=no_val)
        no_entry.grid(row=0, column=3)
        name_entry = tk.Entry(self.op_frame, textvariable=name_val)
        name_entry.grid(row=2, column=3)
        pno_entry = tk.Entry(self.op_frame, textvariable=pno_val)
        pno_entry.grid(row=4, column=3)

        credit_entry = tk.Entry(self.op_frame, textvariable=credit_val)
        credit_entry.grid(row=6, column=3)

        self.entries = [no_val, name_val, pno_val, credit_val]
        clean_button = tk.Button(self.op_frame, command=self.clean_entry, text='清空输入框', **self.label_btn_style)
        clean_button.grid(row=0, column=7)
        search_button = tk.Button(self.op_frame, command=search_cou, text='查找', **self.label_btn_style)
        search_button.grid(row=2, column=7)
        add_button = tk.Button(self.op_frame, command=add_cou, text='添加(自动编号)', **self.label_btn_style)
        add_button.grid(row=4, column=7)
        update_button = tk.Button(self.op_frame, command=update_cou, text='修改(按课程编号)', **self.label_btn_style)
        update_button.grid(row=6, column=7)
        delete_button = tk.Button(self.op_frame, command=del_cou, text='删除(按课程编号)', **self.label_btn_style)
        delete_button.grid(row=8, column=7)
        delete_sc_button = tk.Button(self.op_frame, command=del_cou_sc, text='删除所有选课', **self.label_btn_style)
        delete_sc_button.grid(row=8, column=9)

    @adjust_button_distance(3)
    def sc_frame(self):
        """
        选课管理界面
        :return:
        """

        def choose_more_action(stutree, coutree):
            students = []
            courses = []
            for value in stutree.selection():
                tree_data_item = stutree.item(value, "values")
                students.append(tree_data_item[0])
            for value in coutree.selection():
                tree_data_item = coutree.item(value, "values")
                courses.append(tree_data_item[0])
            if not students:
                self.show_info((False, '请选择要选课的学生'))
                return False
            if not courses:
                self.show_info((False, '请选择课程'))
                return False
            n = 0
            for s in students:
                for c in courses:
                    if StudentSelectCourse().add_sc(
                        cno=c,
                        sno=s,
                    )[0]:
                        n += 1
            search_sc()
            self.show_info((True, f'共完成{n}次选课操作'))

        def close_choose_window(newWindow):
            """
            关闭选课窗口
            :param newWindow:
            :return:
            """
            self.choose_window_on = False
            newWindow.destroy()

        def choose_more_window():
            """
            批量选课窗口
            :return:
            """
            if self.choose_window_on:
                return False
            self.choose_window_on =True
            newWindow = tk.Toplevel(self.root)
            newWindow.title('批量选课')
            newWindow.geometry('800x400+200+100')
            newWindow.iconbitmap('logo.ico')
            newWindow.protocol("WM_DELETE_WINDOW", lambda: close_choose_window(newWindow))
            # newWindow.resizable(0, 0)
            choose_frame = tk.Frame(newWindow)
            choose_frame.pack(side=tk.BOTTOM, fill=tk.X)
            student_frame = tk.Frame(newWindow)
            student_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            stu_label = tk.Label(student_frame, text='学生列表', **self.label_style)
            stu_label.pack()

            # 创建学生信息列表
            stutree = ttk.Treeview(student_frame)
            columns = ['学号', '姓名', '所在系']
            style_value = ttk.Style()
            style_value.configure("Treeview", rowheight=25, font=("微软雅黑", 13))
            stutree['columns'] = columns
            stutree['show'] = 'headings'
            for column in columns:
                stutree.column(column, width=100, anchor="center")
                stutree.heading(column, text=column)
            studata = Student().select_student(selects=['Sno', 'Sname', 'Sdept'])
            print(studata)
            for i, value in enumerate(studata):
                stutree.insert("", i, text=i + 1, values=[i if i != None else '' for i in value])  # 0 为列的下标，第0行
                stutree.tag_configure('oddrow', font='Arial 20')
            # 添加滚动条
            stuscroll = tk.Scrollbar(student_frame, orient='vertical', command=stutree.yview)
            stuscroll.pack(side=tk.RIGHT, fill=tk.Y)

            stutree.pack(fill=tk.BOTH, expand=True)
            stutree.configure(yscrollcommand=stuscroll.set)

            course_frame = tk.Frame(newWindow)
            course_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            cou_label = tk.Label(course_frame, text='课程列表', **self.label_style)
            cou_label.pack()

            # 创建课程信息列表
            coutree = ttk.Treeview(course_frame)
            columns = ['课程编号', '课程名称', '学分']
            coutree['columns'] = columns
            coutree['show'] = 'headings'
            for column in columns:
                coutree.column(column, width=100, anchor="center")
                coutree.heading(column, text=column)
            coudata = Course().select_course(selects=['Cno', 'Cname', 'Ccredit'])
            for i, value in enumerate(coudata):
                coutree.insert("", i, text=i + 1, values=[i if i != None else '' for i in value])  # 0 为列的下标，第0行
                coutree.tag_configure('oddrow', font='Arial 20')
            # 添加滚动条
            couscroll = tk.Scrollbar(course_frame, orient='vertical', command=coutree.yview)
            couscroll.pack(side=tk.RIGHT, fill=tk.Y)

            coutree.pack(fill=tk.BOTH, expand=True)
            coutree.configure(yscrollcommand=couscroll.set)

            choose_button = tk.Button(choose_frame, text='批量选课', **self.button_small_style, command=lambda:choose_more_action(stutree, coutree))
            choose_button.pack()

        def get_values():
            sno = sno_val.get()
            cno = cno_val.get()
            grade = grade_val.get()
            dt = {}
            if sno:
                dt['Sno'] = sno
            if cno:
                dt['Cno'] = cno
            if grade:
                dt['Grade'] = grade
            return dt

        def search_sc():
            dt = get_values()
            res = StudentSelectCourse().select_sc(sno=dt.get('Sno'), cno=dt.get('Cno'), grade=dt.get('Grade'))
            self.refresh_tree(res)

        def add_sc():
            """
            新增选课
            :return:
            """
            dt = get_values()
            res = StudentSelectCourse().add_sc(
                cno=dt.get('Cno'),
                sno=dt.get('Sno'),
            )
            self.show_info(res)
            if res[0]:
                self.clean_entry()
                search_sc()

        def add_score():
            """
            添加成绩
            :return:
            """
            dt = get_values()
            res = StudentSelectCourse().add_score(
                cno=dt.get('Cno'),
                sno=dt.get('Sno'),
                grade=dt.get('Grade')
            )
            self.show_info(res)
            if res[0]:
                # self.clean_entry()
                # 成绩栏清空
                self.entries[0].set('')
                self.entries[2].set('')
                search_sc()

        def del_sc():
            """
            删除选课
            :return:
            """
            if self.del_confirm():
                dt = get_values()
                res = StudentSelectCourse().delete_sc(
                    sno=dt.get('Sno'),
                    cno=dt.get('Cno')
                )
                self.show_info(res)
                if res[0]:
                    self.clean_entry()
                    search_sc()

        self.now_checked = 3
        self.clean_frame_content()
        self.student_button.config(**self.not_checked_color)
        self.course_button.config(**self.not_checked_color)
        self.sc_button.config(**self.checked_color)
        self.title.config(text=f'{self.basic_title}选课管理')
        table_frame = tk.Frame(self.content)
        table_frame.pack(side=tk.TOP, fill=tk.X)
        columns = ('学号', '课程编号', '成绩', '学生姓名', '课程名称')
        scs = StudentSelectCourse().select_sc()
        self.data_table(table_frame, columns, scs)

        self.op_frame = tk.Frame(self.content)
        self.op_frame.pack(fill=tk.BOTH)
        sno_label = tk.Label(self.op_frame, text=columns[0], **self.label_style)
        sno_label.grid(row=0, column=1)
        cno_label = tk.Label(self.op_frame, text=columns[1], **self.label_style)
        cno_label.grid(row=2, column=1)
        grade_label = tk.Label(self.op_frame, text=columns[2], **self.label_style)
        grade_label.grid(row=4, column=1)

        sno_val = tk.StringVar()
        cno_val = tk.StringVar()
        grade_val = tk.StringVar()

        sno_entry = tk.Entry(self.op_frame, textvariable=sno_val)
        sno_entry.grid(row=0, column=3)
        cno_entry = tk.Entry(self.op_frame, textvariable=cno_val)
        cno_entry.grid(row=2, column=3)
        grade_entry = tk.Entry(self.op_frame, textvariable=grade_val)
        grade_entry.grid(row=4, column=3)

        self.entries = [sno_val, cno_val, grade_val]
        clean_button = tk.Button(self.op_frame, command=self.clean_entry, text='清空输入框', **self.label_btn_style)
        clean_button.grid(row=0, column=7)
        search_button = tk.Button(self.op_frame, command=search_sc, text='查找', **self.label_btn_style)
        search_button.grid(row=2, column=7)
        add_button = tk.Button(self.op_frame, command=add_sc, text='添加选课', **self.label_btn_style)
        add_button.grid(row=4, column=7)
        choose_more_button = tk.Button(self.op_frame, command=choose_more_window, text='批量选课', **self.label_btn_style)
        choose_more_button.grid(row=4, column=9)
        update_button = tk.Button(self.op_frame, command=add_score, text='添加成绩', **self.label_btn_style)
        update_button.grid(row=6, column=7)
        delete_button = tk.Button(self.op_frame, command=del_sc, text='删除', **self.label_btn_style)
        delete_button.grid(row=8, column=7)


def main():
    root = tk.Tk()
    root.title('选课管理系统 2019217872 郑辉 电信科19-3班 信息系统软件设计 作业题1')
    root.iconbitmap('logo.ico')
    root.geometry('900x600+200+50')
    root.resizable(0, 0)
    home = HomeGUI(root)
    root.protocol("WM_DELETE_WINDOW", home.quit)
    root.mainloop()


if __name__ == '__main__':
    main()