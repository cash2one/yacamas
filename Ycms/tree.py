# /usr/bin/env py
# -- encoding = utf-8 --

class CategoryTree(object):
    """
    功能：无限分类
    注意： 严格按照 get_children_by_id doc中规定的数据结构
    TODO：分类算法优化。 错误处理完善。现在是着急完成项目暂时凑合着用
    FIXIT: 程序不够健壮，错误处理必须完善
    """
    def __init__(self,cate_list):
        self.cate_list = cate_list
        self.cate_struct = []
        self.str_tree = []

    def tree(self, cid=0, seprator=' ', wrapper='{0}', wrapper_all=False):
        """
        参数要求/格式 见get_tree_by_struct
        seprator: 前导字符（如空格）
        warpper： 将类别名称用其包裹 
                  {0}  : name
                  {1}  : depth
                  {2}  : id
                    如 <li class="level-{1}" id="id-{2}">
                           <a href = "cate/{2}"> {0} </a>
                       </li>
        warpper_all: 将seprator也wrap起来  默认只wrap name
        """
        # 获取结构化数据
        self.get_struct_of_cate(cid)
        # 获取树
        # 初始化变量
        self.str_tree = []
        return self.get_tree_by_struct(self.cate_struct, seprator, wrapper,
                                       wrapper_all)

    def get_children_by_id(self, cid, list_dic, parent_dic={}):
        """
            功能：根据某个id获取其子元素的树形结构（只是数据结构）
            参数：
                cid: 某个id
                list_dic: 以dict为元素的list  ==> [{...},{...},....,{...}]
                          dict的数据结构:  
                                {'id':15, 'pid':0, 'parents':'0,1,2,4,5,3', 'has_child':0, 'depth':0, 'name':'14'},
                                #1 id: [必须]当前cate的id
                                #2 pid：[必须] 父id（唯一）
                                #3 path:[必须]所有长辈（逗号隔开的数字字符串，顶级cate的该项为0）
                                #4 has_child:[必须] 是否有子代
                                #5 depth:[目前必须] 目录层级（深度）可以考虑修改程序用path（取其字符数/层级数） 
                                #6 name 及 其他 ： 可选
            返回值： dict。
                注意：是dict和list的混合体（chilren是list包裹的dict）
                {'id':1, ....'children':[
                                            {'id':*,......}, 
                                            {'id':*,......}, 
                                            {'id':*,......}, 
                                            {'id':*,......'children':[
                                                                {'id':*,......}, 
                                                                {'id':*,......}, 
                                                                {'id':*,......}, 
                                                                {'id':*,......}, 
                                                            ]}, 
                                        ]}
        """

        try:# 若给的cid 不存在会出现异常
            for i in list_dic:
                if i['id'] == cid:
                    if not parent_dic :
                        parent_dic = i
                        parent_dic['children'] = []
                        #get_children_by_id(cid, list_dic, rsList, rsList) # 为啥这里不需要？？
                if i['pid'] == cid:
                    # 将当前项插入其父cat 的children列表
                    if  not 'children' in parent_dic:
                        parent_dic['children'] = []
                    parent_dic['children'].append(i)

                    if i['has_child']:
                        # 上级cat 插入 （如何确定上级cat）？
                        p_index = parent_dic['children'].index(i)
                        p_dic = parent_dic['children'][p_index]
                        self.get_children_by_id(i['id'],list_dic, p_dic)
        except:
            parent_dic = {}
                
        return parent_dic

    def get_struct_of_cate(self, cid=0):
        """
        功能： 获取整个类别表的树状结构数据（非绘制树状图）
        参数： 参考glist_dicet_children_by_id
        返回值：list。  []包裹的 get_children_by_id 的返回值列表
        """
        if not self.cate_list:
            return False
        self.cate_struct = []
        #print(self.cate_list)
        if not cid:
            for cate in self.cate_list:
                if not cate['pid']:
                    self.cate_struct.append(self.get_children_by_id(cate['id'], self.cate_list))
        else:
            self.cate_struct.append( self.get_children_by_id(cid,
                                                             self.cate_list) or
                                    False)
        return self.cate_struct
    
    def get_parents_by_id(self, cid):
        """
        功能： 根据cateid 获取所有长辈列表
        """
        cate = self.get_cate_by_id(cid)
        if cate and 'parents' in cate:
            return cate['parents']
        else:
            return false
            
    def get_cate_by_id(self, cid):
        """
        功能：根据id获取某个cate的详细内容
        """
        for cate in self.cate_list:
            if cate['id'] == cid:
                return cate
        else:
            return False

    def get_tree_by_struct(self, cate_struct, seprator='>', wrapper = '{0}',
                           wrapper_all=False, str_tree = []):
        """
            功能： 根据给出的 cate_struct (get_struct_of_cate 返回的数据类型）绘制目录树
            ###???: 为什么？？
            若self.str_tree为字符串时只能返回顶级菜单？？难道递归过程中非“原处修改”类型的变量无法传递到内层？？
            注意： 这里self.str_tree 因为是“原处修改” 因此已经是global性质，
            若两次调用本函数，则self.str_tree内是 两倍（两次结果叠加）
        """

        for i in cate_struct:
            if isinstance(i, dict):
                if wrapper_all:
                    cate_str = wrapper.format(seprator*i['depth'] + str(i['name']),
                                              i['depth'], i['id'])
                else:
                    cate_str = seprator*i['depth'] + wrapper.format(str(i['name']),
                                                                    i['depth'],
                                                                    i['id'])
                self.str_tree.append(cate_str)
                if 'children' in i and  i['children']:
                   self.get_tree_by_struct(i['children'], seprator, wrapper, wrapper_all, self.str_tree)

        return self.str_tree

# -------------- main test ---------------------

if __name__ == '__main__':

    dic = [
            {'id':1, 'pid':0, 'parents':'0', 'has_child':1, 'depth':0, 'name':'1'},
            {'id':2, 'pid':1, 'parents':'0,1', 'has_child':1, 'depth':1, 'name':'2'},
            {'id':3, 'pid':5, 'parents':'0,1,2,4,5', 'has_child':1, 'depth':4, 'name':'3'},
            {'id':4, 'pid':2, 'parents':'0,1,2', 'has_child':1, 'depth':2, 'name':'4'},
            {'id':5, 'pid':4, 'parents':'0,1,2,4', 'has_child':1, 'depth':3, 'name':'5'},
            {'id':6, 'pid':5, 'parents':'0,1,2,4,5', 'has_child':0, 'depth':4, 'name':'6'},
            {'id':7, 'pid':1, 'parents':'0,1', 'has_child':0, 'depth':1, 'name':'7'},
            {'id':8, 'pid':1, 'parents':'0,1', 'has_child':0, 'depth':1, 'name':'8'},
            {'id':9, 'pid':0, 'parents':'0', 'has_child':1, 'depth':0, 'name':'9'},
            {'id':10, 'pid':9,  'parents':'0,9', 'has_child':1, 'depth':1, 'name':'10'},
            {'id':11, 'pid':10, 'parents':'0,9,10',  'has_child':0, 'depth':2, 'name':'11'},
            {'id':12, 'pid':0, 'parents':'0',  'has_child':0, 'depth':0, 'name':'12'},
            {'id':13, 'pid':2, 'parents':'0,1,2',  'has_child':0, 'depth':2, 'name':'13'},
            {'id':15, 'pid':3, 'parents':'0,1,2,4,5,3', 'has_child':0, 'depth':5, 'name':'15'},
            {'id':16, 'pid':0, 'parents':'0', 'has_child':0, 'depth':0, 'name':'16'},
            {'id':14, 'pid':0, 'parents':'0', 'has_child':0, 'depth':0, 'name':'14'},
        ]

    
    otree = CategoryTree(dic)
    cate_tree = otree.tree(1)
    for cate in cate_tree:
         print(cate)

