import time
import ctypes
import unittest
from public.config import Config,SDK_PATH,RENAME_WIREFILE_PATH,UPLOAD_PATH
from public.public import ls_cb,list_result,re_cb,mk_cb
from public.log import logger


class TestRaysyncRename(unittest.TestCase):
    '''测试重命名基本功能'''
    URL = Config().get('URL')
    port = Config().get('PORT')
    username = Config().get('USERNAME')
    password = Config().get('PASSWORD')
    lib = ctypes.CDLL(SDK_PATH)


    def setUp(self):
        self.instance = self.lib.Raysync_CreateRaysyncInterface()
        #创建实例
        try:
            self.lib
        except:
            logger.info("dll文件不存在")
        #确认是否存在dll文件
        try:
            self.lib.Raysync_Connect(self.instance, 500)
        except:
            logger.info("Raysync_Connect 失败")
        #与dll文件建连
        try:
            self.lib.Raysync_Login(self.instance, bytes(self.URL, encoding='gbk'), self.port, bytes(self.username, encoding='gbk'),
                                 bytes(self.password, encoding='gbk'))
        except:
            logger.info('登录失败，请检查服务器地址/端口/用户名/密码是否正确')
            #登录客户端，地址，端口号，用户名，密码可在config.yml中修改
            #登录server
        self.lib.Raysync_List(self.instance, "/")
        #list操作
        time.sleep(2)

    def test_rename_1(self):
        '''测试正常重命名文件夹'''
        self.lib.Raysync_SetRenameCallback(self.instance, re_cb)
        #设置创建文件夹回调，在public中设置回调时的格式，re_cb为重命名的回调
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_Rename(self.instance, bytes("/", encoding='utf8'), bytes("AutoTestMkdir", encoding='utf8'),bytes("AutoTestMkdir_New", encoding='utf8') )
        #重命名AutoTestMkdir文件夹为AutoTestMkdir_New
        time.sleep(3)
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(2)
        rename_result = (bytes('AutoTestMkdir_New', encoding='gbk') in list_result)
        # 获取重命名后的结果
        rename_last_result = (bytes('AutoTestMkdir', encoding='gbk') in list_result)
        # 获取重命名前的结果
        self.assertTrue(rename_result)
        #判断重命名后的文件是否存在，存在为通过
        self.assertFalse(rename_last_result)
        #判断重命名前的文件是否不存在，不存在为通过

    def test_rename_2(self):
        '''测试正常重命名文件'''
        self.lib.Raysync_SetRenameCallback(self.instance, re_cb)
        #设置创建文件夹回调，在public中设置回调时的格式，re_cb为重命名的回调
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'Raysync.exe')
        # 格式化Raysync.exe 文件
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, None, 'upload_task_0')
        # 上传单个Raysync.exe 文件
        time.sleep(10)
        self.lib.Raysync_List(self.instance, "/")
        time.sleep(5)
        self.lib.Raysync_Rename(self.instance, "/", bytes("Raysync.exe", encoding='utf8'),bytes("Raysync_New.exe", encoding='utf8') )
        #重命名Raysync.exe文件为Raysync_New.exe
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(2)
        rename_result = (bytes('Raysync_New.exe', encoding='gbk') in list_result)
        #获取重命名后的结果
        rename_last_result = (bytes('Raysync.exe', encoding='gbk') in list_result)
        #获取重命名前的结果
        self.assertTrue(rename_result)
        #判断重命名后的文件是否存在，存在为通过
        self.assertFalse(rename_last_result)
        #判断重命名前的文件是否不存在，不存在为通过

    def test_rename_3(self):
        '''测试重命名文件夹失败：重命名名字已存在'''
        self.lib.Raysync_SetCreateFolderCallback(self.instance, mk_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        self.lib.Raysync_CreateFolder(self.instance, "/", bytes("AutoTestMkdir", encoding='utf8'))
        #创建AutoTestMkdir文件夹
        self.lib.Raysync_SetRenameCallback(self.instance, re_cb)
        #设置重命名文件夹回调，在public中设置回调时的格式
        self.lib.Raysync_Rename(self.instance, "/", bytes("AutoTestMkdir_New", encoding='utf8'),bytes("AutoTestMkdir", encoding='utf8') )
        #重命名AutoTestMkdir_New为刚刚创建的AutoTestMkdir文件夹
        time.sleep(3)
        with open(RENAME_WIREFILE_PATH, 'r') as x:
            error_code_now = x.read()
            #读取文件，
            x.close()
        print(error_code_now)
        self.assertFalse(error_code_now == 0)
        #判读错误码是否不为0，为0则重命名成功，非0重命名失败，不为0为真，则重命名失败。


    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例