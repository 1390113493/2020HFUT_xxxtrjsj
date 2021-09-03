# -*- coding: utf-8 -*-
# @Time    : 2021/6/16 23:33
# @Author  : HUII
# @FileName: student.py
# @Software: PyCharm
from sql import SqlManage


class Student:
    """
    学生管理
    """
    def __init__(self):
        self.student = SqlManage('student')
        self.sc = SqlManage('sc')

    def add_student(self, sno, sname, ssex, sage, sdept):
        """
        添加学生
        :param sno: 学号
        :param sname: 姓名
        :param ssex: 性别
        :param sage: 年龄
        :param sdept: 所在系
        :return:
        """
        if len(sno) != 5:
            return False, '学号长度必须为5位'
        if not sname:
            return False, '姓名不得为空'
        if len(sname) > 20:
            return False, '姓名长度不得大于20个字符'
        if ssex not in ['男', '女']:
            return False, '性别错误'
        try:
            if int(sage) < 0:
                raise ValueError
        except:
            return False, '请输入正确年龄格式'
        if not sdept:
            return False, '请输入所在系名称'
        if len(sdept) > 15:
            return False, '所在系名称长度不得大于15个字符'

        if self.student.select({
            'Sno': sno
        }):
            return False, '该学号已存在'
        if self.student.insert({
            'Sno': sno,
            'Sname': sname,
            'Ssex': ssex,
            'Sage': sage,
            'Sdept': sdept
        }):
            return True, '成功添加学生信息'
        else:
            return False, '添加学生失败'

    def select_student(self, params=None, selects=None):
        """
        按条件搜索学生
        :param params:
        :return:
        """
        return self.student.select(params, selects)

    def edit_student(self, sno, params):
        """
        修改学生信息
        :param sno: 学号
        :param params: 参数
        :return:
        """
        if not self.select_student({
            'Sno': sno
        }):
            return False, '该学生不存在'
        if params.get('Sname') and len(params.get('Sname')) > 20:
            return False, '姓名长度不得大于20个字符'
        if params.get('Ssex') and params.get('Ssex') not in ['男', '女']:
            return False, '性别错误'
        if params.get('Sage'):
            try:
                if int(params.get('Sage')) < 0:
                    raise ValueError
            except:
                return False, '请输入正确年龄格式'
        if params.get('Sdept') and len(params.get('Sdept')) > 15:
            return False, '所在系名称长度不得大于15个字符'
        if self.student.update({
            'Sno': sno
        }, params):
            return True, '成功修改学生信息'
        else:
            return False, '修改信息失败'

    def delete_student(self, sno):
        """
        删除学生
        :param sno: 学生编号
        :return:
        """
        if not self.select_student({
            'Sno': sno
        }):
            return False, '该学生不存在'
        if self.sc.select({
            'Sno': sno
        }):
            return False, '删除学生失败！选课系统中存在该学生选课信息'
        if self.student.delete({
            'Sno': sno
        }):
            return True, '成功删除该学生'
        else:
            return False, '删除学生失败'

    def delete_student_sc(self, sno):
        """
        删除学生选课
        :param sno: 学生编号
        :return:
        """
        if not self.select_student({
            'Sno': sno
        }):
            return False, '该学生不存在'
        if not self.sc.select({
            'Sno': sno
        }):
            return False, '选课系统中不存在该学生选课信息'
        n = self.sc.delete({
            'Sno': sno
        })
        if n:
            return True, f'成功删除该学生{n}门选课信息'
        else:
            return False, '删除学生选课信息失败'


if __name__ == '__main__':
    for i in range(20):
        print(Student().add_student(f'{90003+i}', f'张三{i}', '男', 20, 'CI'))
    # print(Student().select_student({
    #     'Sname': '张三'
    # }))
    # print(Student().delete_student('90003'))