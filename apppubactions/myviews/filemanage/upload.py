import os, re, json, random, time
from datetime import datetime
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from Ycms.settings import BASE_DIR, STATICFILES_DIRS
from .configJson import ueditor_conf


def Controller(req):
    act = 'action' in req.GET and req.GET['action'].replace(' ', '') or None
    upact = UpAct(req, ueditor_conf);
    if act == 'config':
        conf_file = os.path.join(os.path.dirname(__file__) , 'configJson.py')
        with open(conf_file, 'r') as fh:
            conf_json = fh.read()
            conf_json = re.subn(r'#[^\n]*#*[^\n]*#', '', conf_json)[0]
            conf_json = conf_json.replace('ueditor_conf=', 
                                          '').replace('True',
                                           'true').replace('False',
                                           'false')
            result = conf_json
            # print(ueditor_conf['scrawlPathFormat'])
    elif act == 'uploadimage':
        f = req.FILES.getlist('upfile')[0]
        # name
        # size
        # content_type
        # readline()
        # readlines()
        # encoding
        # print(f.content_type)
        # print(f.name)
        # print(f.size)
        result = upact.imageUp();
    elif act == 'uploadscrawl':
        print(act)
    elif act == 'uploadfile':
        print(act)
    elif act == 'listimage':
        print(act)
    elif act == 'listfile':
        print(act)
    elif act == 'catchimage':
        print(act)
    else:
        rs = json.dumps({'state':'error'})
    return HttpResponse(result)

class UpAct(object):
    def __init__(self, request, confDict):
        self.confDict = confDict
        self.request = request

    def imageUp(self):
        """
        upload image processer
        """
        objconf = {}
        #print(objconf['imagemaxsize'])
        objconf['imageMaxSize'] = self.confDict['imageMaxSize']
        objconf['imageAllowFiles'] = self.confDict['imageAllowFiles']
        objconf['imageCompressEnable'] = self.confDict['imageCompressEnable']
        objconf['imageCompressBorder'] = self.confDict['imageCompressBorder']
        objconf['imageInsertAlign'] = self.confDict['imageInsertAlign']
        objconf['imageUrlPrefix'] = self.confDict['imageUrlPrefix']
        objconf['imagePathFormat'] = self.confDict['imagePathFormat']
        strrs = Uploader(self.request, objconf).upload()

        return HttpResponse(strrs)


class Uploader(object):
    """
    upload main processer class
    """
    def __init__(self, request, objconf):
        self.objconf = objconf
        self.request = request
        self.mime_list ={ 'image/png':'.png',
                         'image/gif':'.gif',
                         'image/jpeg':'.jpg',
                         'image/bmp':'.bmp' }

    # 取配置参数
    # 取上传的文件
    def get_upfile_list(self):
        files = self.request.FILES
        return 'upfile' in files and files.getlist('upfile')
 
    # 存储文件
        # 生成保存路径
    def get_upload_path(self):
        #"imagepathformat": "{static_upfiles}/image/{yyyy}{mm}{dd}/{time}{rand:6}"
        path_format = '/'.join(self.objconf['imagePathFormat'].split('/')[:3])
        now = str(datetime.now())
        path = path_format.format(STATIC_UPFILES= self.get_upfile_dir(),
                           yyyy=now[:4], mm=now[5:7], dd=now[8:10])

        return path
        
    def get_upfile_dir(self):
        for d in STATICFILES_DIRS:
            if d[0] == 'upfiles':
                upfile_dir = d[1]
        return os.path.join(BASE_DIR, upfile_dir) or false

        # 格式化文件名
    def get_file_name(self, suffix):
        print(suffix)
        return ''.join([str(time.time()).replace('.', '-'), '.', suffix])
        #return 'jpg'
        # 检查文件夹/新建文件夹
    def make_dir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        return True

    def check_and_get_suffix(self, file_type):
        suffix = file_type in self.mime_list and self.mime_list[file_type]
        return  (suffix in  self.objconf['imageAllowFiles']) and suffix


    def upload(self):
        file_list = self.get_upfile_list()
        path = self.get_upload_path()
        self.make_dir(path)

        fInfo = {}
        for _file in file_list:
            suffix = self.check_and_get_suffix(_file.content_type)
            if _file.size > self.objconf['imageMaxSize']:
                return False
            des_file_path = os.path.join(path, self.get_file_name(suffix))
            # 写入文件
            with open(des_file_path, 'wb+') as fh:
                for chunk in _file.chunks():
                    fh.write(chunk)
            now = str(datetime.now())
            fInfo['state'] = 'SUCCESS' 
            fInfo['url'] = '/'.join(des_file_path.split('/')[-4:])
            fInfo['title'] = ''
            fInfo['original'] = '' 
            fInfo['type'] = 'jpg'
            fInfo['size'] = _file.size
        return json.dumps(fInfo)

       # "imagemaxsize": 2048000, # 上传大小限制，单位b #
       # "imageallowfiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], # 上传图片格式显示 #
       # "imagecompressenable": true, # 是否压缩图片,默认是true  py 是首字母大写 返回json数据给前端js时 要改成小写#
       # "imagecompressborder": 1600, # 图片压缩最长边限制 #
       # "imageinsertalign": "none", # 插入的图片浮动方式 #
       # "imageurlprefix": "upfiles", # 图片访问路径前缀 #
       # "imagePathFormat": "{STATIC_UPFILES}/image/{yyyy}{mm}{dd}/{time}{rand:6}", # 上传保存路径,可以自定义保存路径和文件名格式 #
 
        # 检查文件格式是否允许
        # 格式化返回信息
           # "state" => $this->stateInfo,
           # "url" => $this->fullName,
           # "title" => $this->fileName,
           # "original" => $this->oriName,
           # "type" => $this->fileType,
           # "size" => $this->fileSize
