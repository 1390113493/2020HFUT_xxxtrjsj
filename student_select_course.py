# -*- coding: utf-8 -*-
# @Time    : 2021/6/16 23:35
# @Author  : HUII
# @FileName: student_select_course.py
# @Software: PyCharm
from sql import SqlManage


class StudentSelectCourse:
    """
    学生选课
    """
    def __init__(self):
        self.sc = SqlManage('sc')

    def add_sc(self, sno, cno):
        """
        新增选课
        :param sno: 学号
        :param cno: 课程编号
        :return:
        """
        if not sno:
            return False, '学号不得为空'
        if not cno:
            return False, '课程代码不得为空'
        if self.select_sc(sno, cno):
            return False, '已选课'
        if not SqlManage('Student').select({
            'Sno': sno
        }):
            return False, '对应学生不存在'
        if not SqlManage('Course').select({
            'Cno': cno
        }):
            return False, '对应课程不存在'
        if self.sc.insert({
            'Sno': sno,
            'Cno': cno
        }):
            return True, '选课成功！'
        else:
            return False, '选课失败'

    def add_score(self, sno, cno, grade):
        """
        为选课增加成绩
        :param sno: 学号
        :param cno: 课程编码
        :param grade: 成绩
        :return:
        """
        if not sno:
            return False, '学号不得为空'
        if not cno:
            return False, '课程代码不得为空'
        if not grade:
            return False, '成绩不得为空'
        try:
            if not 0 <= int(grade) <= 100:
                return False, '成绩区间错误，请确保0≤成绩≤100'
        except:
            return False, '成绩为整数！'
        if self.sc.update({
            'Sno': sno,
            'Cno': cno
        }, {
            'Grade': grade
        }):
            return True, '增加成绩成功'
        else:
            return False, '增加成绩失败'

    def delete_sc(self, sno, cno):
        """
        删除选课记录
        :param sno: 学号
        :param cno: 课程编号
        :return:
        """

        if self.sc.delete({
            'Sno': sno,
            'Cno': cno
        }):
            return True, '删除选课成功'
        else:
            return False, '删除选课失败'

    def select_sc(self, sno=None, cno=None, grade=None):
        """
        搜索选课记录
        :param sno:
        :param cno:
        :param grade:
        :return:
        """
        # if not (sno and cno and grade):
        #     return self.sc.select()
        params = {}
        if sno:
            params['Sno'] = sno
        if cno:
            params['Cno'] = cno
        if grade:
            params['Grade'] = grade
        s = ';'
        if params:
            s = 'and ' + ' and '.join([f"sc.{k}='{v}'" for k, v in params.items()])+';'
        sql = 'select student.Sno, course.Cno, sc.Grade , student.Sname, course.Cname from student, course, ' \
              'sc where student.Sno = sc.Sno and course.Cno = sc.Cno '
        sql = sql + s
        # print(sql)
        return self.sc.carry(sql)

if __name__ == '__main__':
    sc = StudentSelectCourse()
    # print(sc.add_sc('95010', 3))
    # print(sc.add_sc('95011', 3))
    # print(sc.delete_sc('95010', 3))
    # print(sc.add_score('95011', 3, 95))
    print(sc.select_sc())