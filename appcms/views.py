import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from Ycms.tree import CategoryTree as menuTree
from Ycms.functions import post, get, get_tpl_list, get_tpl_path
from .models import Menu, Category, Archive
def index(request):
    """
    网站首页
    """
       #print(json.dumps(_mlist))
    menu_list = _get_menus(request, 'index')

    return render_to_response('cms/index.html',{'menuJSON':
                                                json.dumps(menu_list['dict']),
                                                'menus' : menu_list['list'],
                                                }) 

def main(req):
    """
    读取分类/文章
    cid -->category id
    aid -->archive  id
    """
    # 首页： 无cid 亦无aid
    # 分类列表： 只有cid
    # 内容页： 既有cid亦有aid
    cid = int(get(req, 'cid'))
    aid = int(get(req, 'aid'))
    oCmsPages = CmsPages(cid, aid, req)
    if aid: 
        #print(__file__)
        return oCmsPages.content_page()
    elif cid: 
        #print(__file__)
        return oCmsPages.cate_page()
    elif not cid and not aid:
        page = 'index'
    else:
        page = 'Error'

    return HttpResponse(page)

    
class CmsPages():

    def __init__(self, cid, aid, request):
        self.cid = cid
        self.aid = aid
        self.request = request

    def cate_page(self):
        """
        栏目分两种：
          # 单网页
          # 多文章
        """
        # 取 cate内容

        try:
            spc = get(self.request, 'spc')
            o_cate = Category.objects.get(id=self.cid)
            #print(o_cate.cate_type)
            if o_cate.cate_type == 'NORMAL':
                # get archive list and  the content of which on top_pos
                pn =  abs(int(post(request, 'pn'))) or 1

                #rs = Group.objects.raw('drop table cmsadmin_archive')
                #print(rs)
                ppn = 'pn' in request.POST and request.POST['pn']
                # 分页参数
                p_size = 20
                item_total = Group.objects.count()
                p_total = math.ceil(item_total/p_size) 
                pn = min(p_total, pn)
                p_next = min(p_total, pn + 1)
                p_prev = max(1, pn - 1)
                # 当页内容
                start = p_size * (pn - 1)
                end   = p_size + start
                rs = arch_list = Archive.objects.all()
                if rs :
                    rs = rs[start:end]
                p_list = [p for p in range(1, p_total + 1)]
                menu_list = _get_menus(self.request, get(self.request, 'm'))
                ctx = {'pn': pn, 'ppn':ppn, 'p_next':p_next, 'p_prev':p_prev, 'p_total':p_total,
                       'p_list':p_list,'rs': rs,'menuJSON': json.dumps(menu_list),
                                                'menus' : menu_list,}

                tpl, ctx = ('cms/cate_normal.html', ctx)


            else:
               #print('sigle')
                menu_list = _get_menus(self.request, get(self.request, 'm')) # FIXIT: Error 
                if spc: 
                    tpl = ''.join(['cms/cate_spc_',
                                   o_cate.alias,
                                   '_single.html'])
                    #print(tpl)
                else:
                    tpl = 'cms/cate_single.html'
                ctx = {'menuJSON': json.dumps(menu_list),
                                                'menus' : menu_list,}

        except:
            #print('Error')
            raise Http404
        return render_to_response(tpl, ctx)

    def index_page(self):
        pass

    def content_page(self):
        """
        取page content
        类型：
            1/ normal --> cate_type == NORMAL
            2/ single --> cate_type == SINGLE
        """
        #try:
        # 取内容
        o_arch = Archive.objects.get(id=self.aid)
        
        # get cate
        cid = o_arch.cate_id
        o_cate = Category.objects.get(id=cid)
        oPCate = _get_parent_cates(o_cate)
        arch_list_of_cate = Archive.objects.filter(cate_id=cid)
        crntMenu = get(self.request, 'm')
        #print(crntMenu)
        menu_list = _get_menus(self.request, crntMenu)
        #print(menu_list)
        ctx = {'o_arch': o_arch, 
                'arch_list':arch_list_of_cate,
                'menuJSON': json.dumps(menu_list['dict']),
                'm_lower' : crntMenu,
                'm' : crntMenu.upper(),
                'menus' : menu_list['list'],}
        if o_cate.cate_type == 'NORMAL':
            tpl = 'cms/page_normal.html'
        
        else: #o_cate.cate_type == 'SINGLE':
            if o_arch.tpl:
                tpl = get_tpl_path('cms') + o_arch.tpl
            else:
                tpl = 'cms/page_single.html'
        #except:
        #    print(__file__)
            #raise Http404

        return render_to_response(tpl, ctx)




######### 获取格式化菜单 可用于json #############
def _get_menus(request, crnt_code=None):
    # 取菜单列表
    oMenuTree = Menu.objects.filter(m_type='front').order_by('list_order').values()
    #print(oMenuTree);
    # 取首页视频
    menuTreeJs =  'siteMenu' in request.session and request.session['siteMenu']
    if not menuTreeJs:
        # 组织列表写入session
        _mlist = {}
        _mlist_id_key = {}
        _mlist_list_order = {}
        tmp_list = {'list':[], 'dict':{}}
        for menu in oMenuTree:
            if_crnt = 0
            if menu['depth'] == 0:
                #print(crnt_code, '::', menu['code'])
                # FIXIT: must trim spaces!!!!
                if crnt_code == menu['code']:
                    #print('4a is crnt ')
                    if_crnt = 1
                _mlist[menu['code']] = {'name':menu['name'],
                                                'url':menu['url'],
                                                'code':menu['code'],
                                                'list_order':menu['list_order'],
                                                'if_crnt': if_crnt,
                                                'sub':[]}
                _mlist_id_key['m'+str(menu['id'])] = {'code':menu['code']}
                _mlist_list_order['m'+str(menu['list_order'])] = {'code':menu['code']}
        for menu in oMenuTree:
            if_crnt = 0
            if menu['depth'] == 1:
                #print(crnt_code, ':-- 2 --:', menu['code'])
                # 取上级菜单的 code 根据 pid
                p_code = _mlist_id_key['m' + str(menu['pid'])]['code']
                if crnt_code == menu['code']:
                    if_crnt = 1
                    _mlist[p_code]['if_crnt'] = 1
                _mlist[p_code]['sub'].append({'name': menu['name'],
                                                              'code':menu['code'],
                                                              'list_order':menu['list_order'],
                                                              'url':menu['url'],
                                                              'if_crnt': if_crnt,
                                                              'id':menu['id']})
        tmp_list['list'] =[_mlist[_mlist_list_order[key]['code']] for key in sorted(_mlist_list_order.keys())]
        tmp_list['dict'] = _mlist
        request.session['siteMenus'] = tmp_list
    else:
        tmp_list = request.session['siteMenus']
    #print(tmp_list)
    return tmp_list 

def _get_parent_cates(o_cate):
    """
    o_cate: cate 条目所有字段及内容 
    根据其获取其parentcate
    """
    pId = o_cate.pid;
    try:
        oPCate = Category.objects.get(id=pId)
    except:
        return False
    return oPCate



 


