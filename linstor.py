import gevent
import re

import ssh
from lvm import VolumeGroup
import time


from gevent import monkey

monkey.patch_all()


class LinstorError(Exception):
    """
    Linstor basic error class with a message
    """
    def __init__(self, msg, more_errors=None):
        self._msg = msg
        if more_errors is None:
            more_errors = []
        self._errors = more_errors

    def all_errors(self):
        return self._errors

    @property
    def message(self):
        return self._msg

    def __str__(self):
        return "Error: {msg}".format(msg=self._msg)

    def __repr__(self):
        return "LinstorError('{msg}')".format(msg=self._msg)


def judge_result(result):
    # 对命令进行结果根据正则匹配进行分类
    re_suc = re.compile('SUCCESS')
    re_war = re.compile('WARNING')
    re_err = re.compile('ERROR')
    """
    suc : 0
    suc with war : 1
    war : 2
    err : 3
    """
    if re_err.search(result):
        result = {'sts':3,'rst':result}
    elif re_suc.search(result) and re_war.search(result):
        messege_war = get_war_mes(result)
        result = {'sts':1,'rst':messege_war}
    elif re_suc.search(result):
        result = {'sts':0,'rst':result}
    elif re_war.search(result):
        messege_war = get_war_mes(result)
        result = {'sts':2,'rst':messege_war}


    return result

def get_err_detailes(result):
    re_ = re.compile(r'Description:\n[\t\s]*(.*)\n')
    if re_.search(result):
        return (re_.search(result).group(1))

def get_war_mes(result):
    re_ = re.compile(r'\x1b\[1;33mWARNING:\n\x1b\[0m(.*)',re.DOTALL)
    if re_.search(result):
        return (re_.search(result).group(1))



class ResourceDenifition():
    def __init__(self,conn):
        self.conn = conn


    def create(self,name):
        cmd = f'linstor rd c {name}'
        cmd_output = self.conn.execute(cmd)
        time.sleep(1)
        result = judge_result(cmd_output)
        if result['sts'] != 0:
            raise LinstorError


    def delete(self,name):
        cmd = f'linstor rd d {name}'
        result = self.conn.execute(cmd)
        time.sleep(1)





class VolumeDenifition():
    def __init__(self,conn):
        self.conn = conn

    def create(self,rd_name,size):
        # 通过ssh对象来进行执行
        cmd = f'linstor vd c {rd_name} {size}'
        result = self.conn.execute(cmd)
        time.sleep(1)




class StoragePool():
    def __init__(self,conn):
        self.conn = conn


    def create(self,name,type,node,volume):
        cmd = f'linstor storage-pool create {type} {node} {name} {volume}'
        result = self.conn.execute(cmd)
        time.sleep(1)


    def delete(self,name,node):
        cmd = f'linstor storage-pool delete {node} {name}'
        result = self.conn.execute(cmd)
        time.sleep(1)


    def expand(self,storagepool,pvs):
        #yaml 根据storagepool获取他的驱动池（vg）
        vg = 'vg1'
        VolumeGroup(self.conn).extend(vg,pvs)
        time.sleep(1)


class Resource():
    def __init__(self,conn):
        self.conn = conn


    def create(self,vd,node,storagepool):
        cmd = f'linstor resource create {node} {vd} --storage-pool {storagepool}'
        self.conn.exctCMD(cmd)
        time.sleep(1)





class DisklessResource():
    def __init__(self,conn):
        self.conn = conn


    def create(self,name,node):
        cmd = f'linstor r c {node} {name} --diskless'
        self.conn.exctCMD(cmd)
        time.sleep(1)








# 仅用于测试
class Scheduler():
    def __init__(self):
        # self.scheme_sp = scheme_sp
        # nodes = ['ubuntu','vince2']
        # self.conn = next(self.connect_node(nodes))
        pass


    def connect_node(self,ips):
        for ip in ips:
            try:
                ssh_obj = ssh.SSHConn('host', 'port', 'username', 'password', 'timeout')
                yield ssh_obj
            except Exception as ex:
                continue


    # 扩容
    # def expand_storagepool(self):
    #     gevent_list = []
    #     # scheme_sp = {'node1':{'sp':'sp1',pv:['pv1','pv2']}}
    #     for node,sp in self.scheme_sp.items():
    #         if sp['pv']:
    #             conn = ssh.SSHConn(node)  # 根据ip就能进行ssh的连接
    #             obj_lvm = VolumeGroup(conn.SSHConnection)
    #             obj_sp = StoragePool(conn.SSHConnection)
    #             gevent_list.append(gevent.spawn(obj_sp.expand,sp['sp'],sp['pv']))
    #
    #     gevent.joinall(gevent_list)



    def create_resource_definition(self):
        # 一个ssh对象进行resource的创建
        # ips = ['111']
        # ssh_obj = next(self.connect_node(ips))
        #
        # gevent_list_rd = []
        # gevent_list_vd = []
        # gevent_list_res = []
        #
        #
        #
        # for node,sp in self.scheme_sp.items():
        #     gevent_list_rd.append(gevent.spawn(ResourceDenifition(self.conn).create,name))
        #
        #
        # for ndoe,sp in self.scheme_sp.items():
        pass


    def create_volume_definition(self):
        pass


    def create_resource_singlessh(self):
        ssh_conn = ssh.SSHConn('ubuntu')
        gevent_list = []

        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_1','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_1','vince2','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_2','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_2','vince2','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_3','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn).create,'res_singlessh_3','vince2','pool_a'))
        gevent.joinall(gevent_list)


    def create_resource_mulssh(self):
        ssh_conn1 = ssh.SSHConn('ubuntu')
        ssh_conn2 = ssh.SSHConn('vince2')
        gevent_list = []

        gevent_list.append(gevent.spawn(Resource(ssh_conn1).create,'res_mulssh_1','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn2).create,'res_mulssh_1','vince2','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn1).create,'res_mulssh_2','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn2).create,'res_mulssh_2','vince2','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn1).create,'res_mulssh_3','ubuntu','pool_a'))
        gevent_list.append(gevent.spawn(Resource(ssh_conn2).create,'res_mulssh_3','vince2','pool_a'))
        gevent.joinall(gevent_list)



    def create_resource_normal(self):
        ssh_conn = ssh.SSHConn('ubuntu')
        Resource(ssh_conn).create('res_normal_1','ubuntu','pool_a')
        Resource(ssh_conn).create('res_normal_1','vince2','pool_a')
        Resource(ssh_conn).create('res_normal_2','ubuntu','pool_a')
        Resource(ssh_conn).create('res_normal_2','vince2','pool_a')
        Resource(ssh_conn).create('res_normal_3','ubuntu','pool_a')
        Resource(ssh_conn).create('res_normal_3','vince2','pool_a')




if __name__ == '__main__':
    # 测试，结论：多协程需要使用，多ssh连接一般不需要，必要时才使用
    # import datetime
    #
    # scheduler = Scheduler()
    # start3 = datetime.datetime.now()
    # scheduler.create_resource_normal()
    # end3 = datetime.datetime.now()
    #
    #
    # start1 = datetime.datetime.now()
    # scheduler.create_resource_singlessh()
    # end1 = datetime.datetime.now()
    #
    #
    # start2 = datetime.datetime.now()
    # scheduler.create_resource_mulssh()
    # end2 = datetime.datetime.now()
    #
    #
    # print(f'不使用协程单ssh连接: {end3 - start3}')
    # print(f'单ssh连接：{end1 - start1}')
    # print(f'多ssh连接：{end2 - start2}')


    pass


