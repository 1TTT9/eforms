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

SYSTEM_TITLE = u'簽核系統'



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

"""
PRIVILUSER = (
    {'pri':10, 'name':'accounting', 'name_title':u'會計', 'block_num': 0},

    {'pri':20, 'name':'supervisor', 'name_title': u'主管', 'block_num': 1}, #0
    {'pri':30, 'name':'ma', 'name_title': u'特助', 'block_num': 2},
    {'pri':40, 'name':'manager', 'name_title': u'總經理', 'block_num': 3},
    {'pri':50, 'name':'vp', 'name_title':u'董事', 'block_num': 4},
    {'pri':99, 'name':'admin', 'name_title':u'管理者', 'block_num': 0},     #5
)
"""
class Man(object):
    def __init__(self, n, t, p, block_num):
        self.name = n
        self.title = t
        self.pri = p
        self.block_num = block_num

class NemasPU:
    accounting  = Man("accounting", u'會計', 10, 0)
    supervisor  = Man("supervisor", u'主管', 20, 1)
    ma          = Man("ma", u'特助', 30, 2)
    manager     = Man("manager", u'總經理', 40, 3)
    vp          = Man("vp", u'董事', 50, 4)
    admin       = Man("admin", u'管理者', 99, 0)

    
PRIVILUSER = (NemasPU.accounting, NemasPU.supervisor, NemasPU.ma, NemasPU.manager, NemasPU.vp, NemasPU.admin)


class Acts:
    waiting = 0
    approved = 1
    rejected = 2





class NemasEFMRequest06:

    EFMID = '6'
    EFMName = u'費用報銷單'

    title =  u'标题' 
    description =  u'描述'   

    project_code =  u'工代' 
    department   = u'部門'
    creator = u'创建者'
    review = u'審查'
    creation_date = u'創建日期'
    last_updated  = u'上次更新' 

    proof_description = u'摘要'
    proof_cost = u'花費'
    proof_file = u'單據'


class NemasEReview:
    title = u'标题'
    description = u'描述'

    status = u'状态'

    opinion = u'审批意见'

    act = u'状态'

    rep_time = u'回覆时间'

    create_time = u'创建时间'
    expire_time = u'期望时间'
    finish_time = u'完成时间'


class NemasEFMRequest03:

    EFMID = '3'
    EFMName = u'請款申請單'


    title =  u'标题' 
    description =  u'描述'   

    project_code =  u'工代' 
    department   = u'部門'
    creator = u'创建者'
    review = u'審查'
    creation_date = u'創建日期'
    last_updated  = u'上次更新' 

    adv_payment = u'請款金額'
    purpose = u'用途'
    method = u'付款方式'
    adv_paydate =  u'付款日期'

    receiver_name = u'姓名/公司名稱'
    receiver_account = u'帳號'
    receiver_bank = u'開戶行地址'


    unknown_01 = u'實收金額'
    unknown_02 = u'報銷日期'
    unknown_03 = u'報銷抵銷金額'
    unknown_04 = u'歸還金額'


FORM_LIST = (
#    ('0', '派工申請單'),
#    ('1', '採購申請單'),
#    ('2', '出差申請單'),
    (NemasEFMRequest03.EFMID, NemasEFMRequest03.EFMName),
#    ('4', '派車申請單'),
#    ('5', '簽呈申請單'),
    (NemasEFMRequest06.EFMID, NemasEFMRequest06.EFMName),
#    ('7', '加班申請單'),
#    ('8', '請假申請單'),
)
