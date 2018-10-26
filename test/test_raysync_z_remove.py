import time
import ctypes
import unittest
from public.config import Config,SDK_PATH,REMOVE_WIREFILE_PATH
from public.public import ls_cb,list_result,rem_cb
from public.log import logger



class TestRaysyncRemove(unittest.TestCase):
    '''测试删除基本功能'''
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
        time.sleep(2)
        #list,sleep2-3s 再进行下一步的操作

    def test_remove_1(self):
        '''测试正常删除单个文件'''
        self.lib.Raysync_SetDeleteTaskCallback(self.instance, rem_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'167-mov.mov')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance, "/", files)
        except:
            logger.info("需要删除的文件不存在！")
        #创建AutoTestMkdir文件夹
        time.sleep(2)
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(3)
        ret = (bytes('167-mov.mov', encoding='gbk') in list_result)
        #判断167-mov.mov文件是否在列表中，如果不在则表示删除成功，用例pass，注意bytes格式，二进制格式
        self.assertFalse(ret)


    def test_remove_2(self):
        '''测试正常删除单个空文件夹'''
        self.lib.Raysync_SetDeleteTaskCallback(self.instance, rem_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'AutoTestMkdir')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance, "/", files)
        except:
            logger.info("需要删除的文件不存在！")
        time.sleep(2)
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(3)
        ret = (bytes('AutoTestMkdir', encoding='gbk') in list_result)
        #判断167-mov.mov文件是否在列表中，如果不在则表示删除成功，用例pass，注意bytes格式，二进制格式
        self.assertFalse(ret)

    def test_remove_3(self):
        '''测试正常删除单个文件夹'''
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_SetDeleteTaskCallback(self.instance, rem_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'upload_task')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance, "/", files)
        except:
            logger.info("需要删除的文件不存在！")
        time.sleep(10)
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(3)
        ret = (bytes('upload_task', encoding='gbk') in list_result)
        #判断167-mov.mov文件是否在列表中，如果不在则表示删除成功，用例pass，注意bytes格式，二进制格式
        self.assertFalse(ret)


    def test_remove_4(self):
        '''测试正常删除多个文件'''
        self.lib.Raysync_SetDeleteTaskCallback(self.instance, rem_cb)
        #设置创建文件夹回调，在public中设置回调时的格式

        remove_files = ['167_MPG.mpg','167-mov.mov','英文max-webm.webm','中文maya_mp4格式.mp4','中文maya—WNV.wmv']

        files = (ctypes.c_char_p * (len(remove_files) + 1))()
        a = 0
        for i in remove_files:
                b = i
                files[a] = ctypes.c_char_p(bytes(b, encoding='utf8'))
                a = a + 1
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        try:
            self.lib.Raysync_Remove(self.instance, "/", files)
        except:
            logger.info("需要删除的文件不存在！")
        time.sleep(3)
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(3)
        ret = (bytes('167_MPG.mpg', encoding='utf8') in list_result)
        #判断167-mov.mov文件是否在列表中，如果不在则表示删除成功，用例pass，注意bytes格式，二进制格式
        self.assertFalse(ret)

    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例