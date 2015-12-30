"""
项目公共函数
"""

def post(request, key):
    """
    包装request.POST
    """

    if not key:
        return ''
    
    return key in request.POST and request.POST[key]

def get(request, key):
    """
    包装request.GET
    """

    if not key:
        return ''
    
    return key in request.GET and request.GET[key]

# 获取网页模版（前台）列表  添加文章和目录时 可选模版
def get_tpl_list(app=None):
    tpl_path = get_tpl_path(app)
    if not tpl_path:
        return None
    tpl_dir = tpl_path[:-1]
    #print(tpl_dir)
    try:
        import os
        dir_list = os.listdir(tpl_dir)
    except:
        dir_list = None
    return dir_list

def get_tpl_path(app=None):
    if not app:
        return None
    #导入模板设置
    import os
    from Ycms.settings import TEMPLATES
    tpl_path = os.path.join(TEMPLATES[0]['DIRS'][0], app)+'/'
    return tpl_path

# 分页类

def page(object):
    p_size = 20
    
    def __init__():
        pass

    def __str__():
        """
        分页widget
        """
        pass

    def pn():
        """
        当前页码
        """
        return self.pn
    
    def next():
        """
        下一页
        """
        pass

    def end():
        """
        最后一页
        """
        pass

    def first():
        """
        第一页
        """
        pass

    def has_next(p_int):
        pass

