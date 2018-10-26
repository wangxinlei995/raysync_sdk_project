import time
import ctypes
import unittest
from public.config import Config, SDK_PATH, MKDIR_WIREFILE_PATH
from public.public import ls_cb, list_result, mk_cb
from public.log import logger



class TestRaysyncMkdir(unittest.TestCase):
    '''测试新建文件夹基本功能'''
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

    def test_mkdir_1(self):
        '''测试正常创建文件夹'''
        self.lib.Raysync_SetCreateFolderCallback(self.instance, mk_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'AutoTestMkdir')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_CreateFolder(self.instance, "/", bytes("AutoTestMkdir", encoding='utf8'))
        #创建AutoTestMkdir文件夹
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_List(self.instance, "/")
        #返回list列表
        time.sleep(3)
        ret = (bytes('AutoTestMkdir', encoding='gbk') in list_result)
        #判断raysync.exe文件是否在列表中，注意bytes格式，二进制格式
        self.assertTrue(ret)



    def test_mkdir_2(self):
        '''测试创建文件夹失败：已存在该文件夹'''
        self.lib.Raysync_SetCreateFolderCallback(self.instance, mk_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        self.lib.Raysync_CreateFolder(self.instance, "/", bytes("AutoTestMkdir", encoding='utf8'))
        # #返回list列表
        time.sleep(3)
        with open(MKDIR_WIREFILE_PATH, 'r') as x:
            error_code_now = x.read()
            #读取文件，
            x.close()
        print(error_code_now)
        self.assertFalse(error_code_now == 0)
        #判读错误码是否不为0，为0则新建成功，非0创建失败，不为0为真，则新建失败。



    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例
