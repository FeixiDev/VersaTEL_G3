import yaml
import re
import copy

from console import Console,ExitCode
from abc import ABCMeta, abstractmethod

import linstor
import crm
import lvm



class VtelResource(metaclass=ABCMeta):
    @abstractmethod
    def create(self, data):
        """

        :param data:资源创建所需要的数据
        :type data:dict
        :return:
        """
        pass

    # @abstractmethod
    # def delete(self, *args):
    #     pass


class ResourceFactory(object):

    def __init__(self, kind_resource):
        self.target = dict(ServiceGroup=ServiceGroup,HostGroup=HostGroup,VIPPool=VIPPool,ResourceSet=ResourceSet)
        self.resource_factory = self.target[kind_resource]


    def create(self,args):
        self.resource_factory().create(args)


    # def delete(self,args):
    #     self.resource_factory().delete(args)



class ServiceGroup(VtelResource):
    def __init__(self):
        self.con = Console()



    def create(self,data):


        # self._check_sg_name(name)
        # yaml.
        #
        # # yaml 检查list_node是不是否在数据库
        # list_all_node = []
        # if not list_node in list_all_node:
        #     self.con.error_output('不存在',ExitCode.CONDITION_NOT_SUPPORTED)
        #
        # if
        #
        #
        # # yaml 添加进配置文件中
        #
        #
        # return ExitCode.OK
        pass




    def _check_sg_name(self,name):
        """
        check service group name
        :return: bool
        """
        result = re.search(r'^[a-zA-Z][a-zA-Z0-9_]*$', name)
        if not result:
            self.con.error_output('The name does not meet the specification', ExitCode.ARGPARSE_ERROR)


    # def _check_node(self,list_node):
    #     #yaml 检查list_node是否全部存在
    #     pass


class HostGroup(VtelResource):
    def __init__(self):
        self.con = Console()


    def create(self,data):
        name = data['group_name']
        iqns = data['host_iqn']
        # self._check_hg_name(name)
        # # yaml 检查list_host是否不是在配置文件中
        #
        # # yaml 写入数据到配置文件
        #
        # return ExitCode.OK



    def _check_hg_name(self,name):
        """
        check service group name
        :return: bool
        """
        result = re.search(r'^[a-zA-Z][a-zA-Z0-9_]*$', name)
        if not result:
            self.con.error_output('The name does not meet the specification', ExitCode.ARGPARSE_ERROR)


class VIPPool(VtelResource):
    def __init__(self):
        self.con = Console()


    def create(self,data):
        network_segment = data['network_segment']
        ips = data['ip']
        tag = data['tag']

        self._check_ns_format(network_segment)
        for ip in ips:
            self._check_ip_in_ns(network_segment, ip)
            self._check_ip_format(ip)

        # 检查ip是否符合网段，或者是符合一个节点的所有网卡的网段，待确定
        pass

        # 判断ip是不是已存在


        # yaml 写入数据到配置文件
        return ExitCode.OK



    def provide_ip(self,network_segment):
        # yaml 读取到指定network_segment，available的所有数据
        ip = [][0]
        # yaml 将这个ip从available移出，加入到used
        return ip


    def _check_ip_format(self, ip,):
        ip_format = re.search(
            r'^((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})(\.((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})){3}$', ip)
        if not ip_format:
            self.con.error_output('IP does not meet specifications',ExitCode.ARGPARSE_ERROR)


    def _check_ns_format(self,network_segment):
        # yaml 获取到VIP,

        # 这里正则需要修改为IP后两位为0.0/1.0
        network_segment_format = re.search(
            r'^((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})(\.((2([0-4]\d|5[0-5]))|[1-9]?\d|1\d{2})){3}$', network_segment)
        if not network_segment_format:
            self.con.error_output('Network segment format error', ExitCode.ARGPARSE_ERROR)

    def _check_ip_in_ns(self,network_segment, ip):
        list_ns = network_segment.split('.')
        list_ip = ip.split('.')
        if list_ns[2] == '0':
            if not list_ip[:2] == list_ns[:2]:
                self.con.error_output(f'{ip} is not in the network segment', ExitCode.ARGPARSE_ERROR)
        else:
            if not list_ip[:3] == list_ns[:3]:
                self.con.error_output(f'{ip} is not in the network segment', ExitCode.ARGPARSE_ERROR)


class ResourceSet(VtelResource):
    def __init__(self):
        self.con = Console()


    def _check_size(self,str_size):
        pass



    def _check_quantity(self, service_group):
        """
        检查服务组数量是否符合要求
        :param service_group: User-specified network segment
        :type service_group: str
        :return: None
        """

        # yaml 读取Mirror Way
        mirror_way = 'yaml读取到的数据'

        if len(service_group) < int(mirror_way):
            self.con.error_output('Insufficient number of nodes in the cluster', ExitCode.CONDITION_NOT_SUPPORTED)


    def _get_available_nodes(self,service_group,spec_type,spec_size,spec_num,spec_mirroy_way):
        """
        检查集群节点的容量是否符合创建要求，返回满足条件的节点及数据
        :return:
        """

        # yaml 获取应用配置文件中服务组的节点，在数据库中的所有数据。传入service_group，返回一个字典。
        dict_node_all = yaml.get_all_node_data()

        # yaml 这里编写一个节点获取剩余空间的方法，传入节点，返回剩余空间（可用PV容量+存储池剩余容量）

        dict_available_nodes = {}
        for node in service_group['node']:
            # 调用
            if Node.get_createable_num(node,spec_type,spec_size) > spec_num:
                dict_available_nodes.update({node:dict_node_all[node]})

        if len(dict_available_nodes) < spec_mirroy_way:
            self.con.error_output('Insufficient remaining capacity of nodes in the cluster', ExitCode.CONDITION_NOT_SUPPORTED)


        return dict_available_nodes



    def create(self,data):
        # 需要的数据直接通过配置文件读取到，或者可以考虑传入一个对象，这个对象的属性存储了创建resourceSet相关数据

        # 连接多个节点
        num = data['number']
        size = data['size']
        mirror_way = data['mirror_way']
        type = data['type']
        host_group = data['host_group']
        cluster = data['cluster']['name']
        service_group = data['cluster']['service_group']
        network = data['cluster']['network']['segment']
        dedicate = data['cluster']['network']['dedicate']


        # 1.创建resource
        # 1.1 选择节点
        self._check_size(size)
        self._check_quantity(service_group)
        dict_node = self._get_available_nodes(service_group,type,size,num,mirror_way)



        nodeselector = NodeSelector(dict_node,type,size,num,mirror_way)
        nodeselector.set_strategy(NodeCapacityPolicy)
        # 返回的最终方案需要记录了节点，存储池，以及扩容对应的pv（不需要则为空）
        scheme_sp = nodeselector.get_scheme()
        # scheme_sp = {'node1':{'sp':'sp1',pv:['pv1','pv2']}}
        # 1.2 存储池扩容（可能不需要执行）
        # 考虑scheme_sp用类对象来表示，然后linstor模块的storagepool直接应用。

        # 先选择一个节点进行ssh连接，返回ssh对象（基本要求：该节点在指定服务组内）
        # 获取执行节点，获取Combined或者Controller类型的节点，获取后进行ssh连接，成功则停止，不成功继续下一个

        def connect_node(ips):
            for ip in ips:
                import ssh
                try:
                    ssh_obj = ssh.SSHConn('host','port','username','password','timeout')
                    yield ssh_obj
                except Exception as ex:
                    continue

        # ips = ['11']
        # ssh_obj = next(connect_node(ips))
        #
        # for node,sp in scheme_sp.items():
        #     # yaml 根据node获取到ip
        #     if not sp['pv']:
        #         # 直接进行resource创建
        #         res_name = '1'
        #         try:
        #             linstor.ResourceDenifition(self.).create(res_name)
        #             linstor.VolumeDenifition(se).create(res_name,size)
        #             linstor.Resource().create(res_name,node,sp)
        #         except Exception ex:
        #             pass
        #
        #     else:
        #         pass
        #         # 扩容



        # 一个ssh对象，多协程执行创建多个resource
        # for node,sp in scheme_sp.items():
        #     if sp['pv']:
        #         pass
        #     else:
        #
        #




        # 1.3 创建resource





class Node():
    def __init__(self):
        pass


    @staticmethod
    def get_createable_num(node,type,size):

        # 需要修改。

        """

        :param node:
        :param size:
        :return: 返回node能创建指定size的resource的数量
        """
        # yaml 获取到剩余空间（根据node，type）

        node = {"PV":{"pv_hdd_1":10.22,"pv_xxx_2":10},"SP":{"sp_hdd_2":22.22,"sp_hdd_3":20}}




        # 粗略的计算方法
        pv_num = int(sum(node['PV'].values()) / size)
        sp_num = 0
        for sp,sp_free_size in node['SP'].items():
            if int(sp_free_size / size) > 0 :
                sp_num += int(sp_free_size / size)


        # 严谨的检验方式（需要考虑对哪个存储池进行扩容）：
        pv_free_cap = sum(node['PV'].values())
        for sp,sp_free_cap in node['SP'].items():
            num = int((sp_free_cap + pv_free_cap) / size)
            dict_other_sp = copy.deepcopy(node['SP'])
            dict_other_sp.pop(sp)
            other_sp_num = 0
            for other_sp, other_sp_free_cap in dict_other_sp.items():
                if int(other_sp_free_cap / size) > 0:
                    other_sp_num += int(other_sp_free_cap / size)

            # 每一种情况的数量，当有一种情况符合时，则说明满足条件，可能还需要返回要进行扩容的存储池（方案）
            num_all = num + other_sp_num


        return pv_num + sp_num




# 抽象策略
class Policy(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass





# 抽象选择器
class Selector(metaclass=ABCMeta):
    @abstractmethod
    def set_strategy(self):
        pass

    @abstractmethod
    def do_strategy(self):
        pass

    @abstractmethod
    def get_scheme(self):
        pass



# 具体选择器
class NodeSelector(Selector):
    def __init__(self, node_data, limit_type, limit_size, limit_num, limit_mirror_way):
        self.node_data = node_data
        self.type = limit_type
        self.size = limit_size
        self.num = limit_num
        self.mirror_way = limit_mirror_way


    def set_strategy(self, *args):
        self.list_strategy = args

    def do_strategy(self, *args):
        # 通过工厂创建策略对象
        self.list_scheme = []
        for strategy in self.list_strategy:
            self.list_scheme.append(strategy(self.node_data,self.type,self.size,self.num,self.mirror_way).execute())
        return self.list_scheme

    def get_scheme(self):
        # 根据权重来返回出最终方案
        list_scheme = self.do_strategy()
        return list_scheme


# 具体策略
class NodeCapacityPolicy(Policy):
    """
    根据容量选择节点的策略：
    1. 优选选择存储池剩余容量能够满足要求的节点，剩余容量越靠近要求的越优先
    2. 次选需要扩容的节点，扩容之后剩余容量越靠近要求的越优先
    """
    def __init__(self,*args):
        self.node_data, self.type,self.size, self.num,self.mirror_way = args


    def execute(self):
        self.scheme = []
        self._part_one()
        self._part_two()
        self._part_three()
        return self._give_weight(self.scheme)


    def _part_one(self):
        # 优选选择存储池剩余容量能够满足要求的节点，剩余容量越靠近要求的越优先
        for node, node_data in self.node_data.items():
            sp_all = {}
            sp_all.update(node_data['sp_normal'])
            sp_all.update(node_data['sp_limited'])
            for sp, sp_data in sorted(sp_all.items(), key=lambda x: x[1], reverse=False):
                if sp_data > self.size:
                    self.scheme.append({'node':node, 'sp': sp, 'pv': []})
                    if len(self.scheme) == self.mirror_way:
                        return

    def _part_two(self):
        if len(self.scheme) == self.mirror_way:
            return
        # 次选扩容后满足
        temp_scheme = []  # 存储所有扩容方案，之后从中挑选出最优方案
        for node, node_data in self.node_data.items():
            if not node in [x['node'] for x in self.scheme] and node_data['sp_normal']:
                # 存在可扩容的存储池
                sp, sp_size = [(sp, sp_size) for sp, sp_size in node_data['sp_limited'].items()][0]
                pv_select = []
                free_size = sp_size
                for pv, pv_size in sorted(node_data['pv'].items(), key=lambda x: x[1], reverse=False):
                    free_size += pv_size
                    if free_size > self.size:
                        pv_select.append(pv)
                        temp_scheme.append(({'node':node, 'sp': sp, 'pv': pv_select}, free_size))
                        break

        mid_num = self.mirror_way - len(self.scheme) if len(temp_scheme) > self.mirror_way - len(self.scheme) else len(
            temp_scheme)
        sorted(temp_scheme, key=lambda x: x[1], reverse=False)
        for scheme in temp_scheme[:mid_num]:
            self.scheme.append(scheme[0])


    def _part_three(self):
        if len(self.scheme) == self.mirror_way:
            return self.scheme

        temp_scheme = []
        for node, node_data in self.node_data.items():
            if not node in [x['node'] for x in self.scheme] and not node_data['sp_normal']:
                pv_select = []
                free_size = 0
                for pv, pv_size in sorted(node_data['pv'].items(), key=lambda x: x[1], reverse=False):
                    free_size += pv_size
                    if free_size > self.size:
                        pv_select.append(pv)
                        temp_scheme.append(({'node':node ,'sp': None, 'pv': pv_select}, free_size))
                        break

        last_num = self.mirror_way - len(self.scheme)
        sorted(temp_scheme, key=lambda x: x[1], reverse=False)
        for scheme in temp_scheme[:last_num]:
            self.scheme.append(scheme[0])



    def _give_weight(self,list_scheme):
        """
        赋予传入的方案权重，目前简单设定为根据mirror_way数量来赋予，比如方案中有4个节点，则按顺序权重为8 6 4 2
        :param scheme:
        :return:
        """
        print('111')
        index = len(list_scheme)
        for i in range(index):
            list_scheme[i] = (list_scheme[i],(index - i) * 2)

        print(list_scheme)
        return list_scheme






# 测试
def run():
    node_data = {
        "node1": {"pv": {"pv_hdd_1": 10, "pv_xxx_2": 11}, "sp_limited": {"sp_hdd_1": 20.22}, "sp_normal": {"sp_hdd_2": 10}},
        "node2": {"pv": {"pv_hdd_3": 22, "pv_xxx_4": 23}, "sp_limited": {"sp_hdd_3": 30.22}, "sp_normal": {"sp_hdd_4": 20}},
        "node3": {"pv": {"pv_hdd_5": 24, "pv_xxx_6": 25}, "sp_limited": {"sp_hdd_5": 40.22}, "sp_normal": {"sp_hdd_6": 30}},
        "node4": {"pv": {"pv_hdd_7": 40, "pv_xxx_8": 40}, "sp_limited": {"sp_hdd_7": 10.22}, "sp_normal": {}}
    }
    selector = NodeSelector(node_data,'hdd',35,limit_num=3,limit_mirror_way=4)
    selector.set_strategy(NodeCapacityPolicy)
    result = selector.get_scheme()
    return (result)


run()

