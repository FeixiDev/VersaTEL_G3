import gevent
import ssh
from gevent import monkey



# 协程相关的补丁
monkey.patch_all()




class Scheduler():
    """
    调度linstor、crm、lvm模块及ssh模块进行连接和命令的执行，多协程执行
    linstor和crm应该采用单ssh连接，多协程执行
    lvm模块的操作应该采用多ssh连接，多协程执行
    """

    def __init__(self):
        pass



    def create_mul_conn(self):
        pass



    def create_rd(self):
        pass




