import time
import ctypes
import unittest
from public.config import Config,SDK_PATH,MKDIR_WIREFILE_PATH
from public.public import ls_cb,list_result,mk_cb
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

    def test_SetParams_1(self):
        '''测试设置客户端运行参数'''

        self.lib.Raysync_SetParams(self.instance, 10, 10, 1200, 0, 0)


    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例
