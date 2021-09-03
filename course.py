# -*- coding: utf-8 -*-
# @Time    : 2021/6/16 23:33
# @Author  : HUII
# @FileName: course.py
# @Software: PyCharm
from sql import SqlManage


class Course:
    """
    课程管理
    """
    def __init__(self):
        self.course = SqlManage('course')
        self.sc = SqlManage('sc')

    def add_course(self, cname, ccredit, cpno=None):
        if not cname:
            return False, '请输入课程名称'
        if len(cname) > 60:
            return False, '课程名称不得大于60个字符'
        if not ccredit:
            return False, '请输入课程学分'
        if cpno:
            if not self.select_course({
                'Cno': cpno
            }):
                return False, '先修课程不存在'
        self.course.cursor.execute('select cno from course')
        res = self.course.cursor.fetchall()
        maxn = 0 if len(res) == 0 else max([int(i[0]) for i in res])
        print(maxn)
        if self.course.insert({
            'Cno': maxn + 1,
            'Cname': cname,
            'Ccredit': ccredit,
            'Cpno': cpno
        }):
            return True, '新增课程成功'
        else:
            return False, '新增课程失败'

    def select_course(self, params=None, selects=None):
        """
        搜索课程
        :param params:
        :return:
        """
        return self.course.select(params, selects)

    def edit_course(self, cno, params):
        """
        修改课程信息
        :param cno: 课程编号
        :param params: 参数
        :return:
        """
        if not self.select_course({
            'Cno': cno
        }):
            return False, '课程不存在'

        if params.get('Cpno'):
            if not self.select_course({
                'Cno': params.get('Cpno')
            }):
                return False, '先修课程不存在'
            if cno == params.get('Cpno'):
                return False, '不能把自己作为先修课程'

        if self.course.update({
            'Cno': cno
        }, params):
            return True, '修改课程信息成功'
        else:
            return False, '修改课程信息失败'

    def delete_course(self, cno):
        """
        删除课程
        :param cno: 课程代码
        :return:
        """
        if not self.select_course({
            'Cno': cno
        }):
            return False, '课程不存在'
        if self.sc.select({
            'Cno': cno
        }):
            return False, '删除课程失败！选课系统中存在该课程信息'
        if self.course.select({
            'Cpno': cno
        }):
            return False, '删除课程失败！有课程以本课为先修课'
        if self.course.delete({
            'Cno': cno
        }):
            return True, '删除课程成功'
        else:
            return False, '删除课程失败'

    def delete_course_sc(self, cno):
        """
        删除课程对应所有选课
        :param cno: 课程代码
        :return:
        """
        if not self.select_course({
            'Cno': cno
        }):
            return False, '课程不存在'
        if not self.sc.select({
            'Cno': cno
        }):
            return False, '选课系统中不存在该课程信息'

        n = self.sc.delete({
            'Cno': cno
        })
        if n:
            return True, f'成功删除该课程{n}门选课信息'
        else:
            return False, '删除选课信息失败'



if __name__ == '__main__':
    course = Course()
    # course.add_course('信息系统软件设计', 1)
    # course.add_course('Python语言与系统设计', 2)
    # print(course.select_course())
    print(course.delete_course(2))
    print(course.select_course())