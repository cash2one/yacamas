"""
语言包 by Sniper
"""

import re

class E(object):
    def __init__(self, key, seprator=None):
        self.key = key
        self.seprator = seprator 
        self.lang={
            'author':'作者',
            'session':'系统会话',
            'sessions':'系统会话',
            'auth':'权限控制',
            'user':'用户',
            'users':'用户',
            'permission':'权限',
            'permissions':'权限',
            'contenttype':'模型/内容类别',
            'contenttypes':'模型/内容类别',
            'content': '内容',
            'type': '类别',
            'appcms':'内容管理系统',
            'archive':'文章',
            'category':'分类/栏目',
            'position':'推荐位',
            'group':'权限组',
            'can': '',
            'add': '新增',
            'edit': '编辑',
            'change': '修改',
            'delete': '删除',
            'read': '读取',
            'get': '获取',
        }

    def _e(self, key, no_return_key=0):
        if not key or not isinstance(key, str):
            return None

        key = key.lower().replace(r'[\s]*', '')
        if key in self.lang and self.lang[key]:
            #print(self.lang[self.key])
            return self.lang[key]
        else:
            return key


    def get_lang(self):
        if not self.seprator:
            return self._e(self.key)
        else:
            _tmplist = []
            for code in self.key.split(self.seprator):
                _tmplist.append(self._e(code))

            return ''.join(_tmplist)

    def get_lang_no_en(self):
         if not self.seprator:
            return self._e(self.key)
         else:
            _tmplist = []
            for code in self.key.split(self.seprator):
                _tmplist.append(self._e(code).replace('can', ''))

            return ''.join(_tmplist)



