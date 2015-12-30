from django import template 
from django.template.defaultfilters import stringfilter
from Ycms.cbw.language import E
register = template.Library()

@register.filter
def get_cate_name_by_id(cid, cate_list):
    """
    cate_list: 多条cate的所有字段及值的字典,组成的list
    """
    if cid and cate_list and isinstance(cate_list, list):
        for cate in cate_list:
            if cate['id'] == cid:
                return cate['name']

@register.filter
def item_in_list(item, lists=[]):
    if not item or not isinstance(lists, list):
        return False
    if item in list:
        return True
    else:
        return False

@register.filter
def _e(key, default):
    return E(key).get_lang() or default

@register.filter
def _e_space(key, default):
    return E(key,seprator=' ').get_lang() or default

@register.filter
def _e_space_no_en(key, default):
    return E(key,seprator=' ').get_lang_no_en() or default
