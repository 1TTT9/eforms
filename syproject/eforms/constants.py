#-*- coding:utf-8 -*-

"""
REQUEST_IDENTIFIER = 'Initial'

REQUEST_STATUS = (
    ('Initiated', 'Initiated'),
    ('Withdrawn', 'Withdrawn'),
    ('Completed', 'Completed')
)

TASK_STATUS = (
    ('Not Started', 'Not Started'),
    ('In Progress', 'In Progress'),
    ('Rolled Back', 'Rolled Back'),
    ('Completed', 'Completed')
)
# register workflow apps here
# enable 'tests' app only for manual testing purpose

WORKFLOW_APPS = [
    'tests'
]
"""

FORM_LIST = (
#    ('0', '派工申請單'),
#    ('1', '採購申請單'),
#    ('2', '出差申請單'),
    ('3', '請款申請單'),
#    ('4', '派車申請單'),
#    ('5', '簽呈申請單'),    
#    ('6', '費用報銷單'),
#    ('7', '加班申請單'),
#    ('8', '請假申請單'),
)

STATE_LIST = (
    ('0', '已提交'),
    ('1', '审批中'),        
    ('2', '已审批'),
    ('3', '已拒绝'),
    ('4', '已处理'),
    ('5', '已确认'),
)

ACT_LIST = (
	('0', '审批中'),
    ('1', '已审批'),
    ('2', '已拒绝'),
)

PURPOSE_LIST = (
    ('0', '貨款'),
    ('1', '定金'),    
    ('2', '其他'),
)

PAYWAY_LIST = (
    ('0', '現金'),
    ('1', '轉帳/電匯'),    
    ('2', '支票'),
)

PRIVILUSER = (
    {'pri':10, 'name':'accounting', 'name_title':u'會計', 'block_num': 0},

    {'pri':20, 'name':'supervisor', 'name_title': u'主管', 'block_num': 1}, #0
    {'pri':30, 'name':'ma', 'name_title': u'特助', 'block_num': 2},
    {'pri':40, 'name':'manager', 'name_title': u'總經理', 'block_num': 3},
    {'pri':50, 'name':'vp', 'name_title':u'董事', 'block_num': 4},
    {'pri':99, 'name':'admin', 'name_title':u'管理者', 'block_num': 0},     #5
)


class Acts:
    waiting = 0
    approved = 1
    rejected = 2

class Nemas:
    accounting = "accounting"
    supervisor = "supervisor"
    ma = "ma"
    manager = "manager"
    vp = "vp"
    admin = "admin"
