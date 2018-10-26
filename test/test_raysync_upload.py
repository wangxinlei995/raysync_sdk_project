import ctypes
import unittest
from public.config import Config,SDK_PATH,UPLOAD_PATH,BASE_PATH
import os
from public.log import logger
import time
from public.public import ls_cb,list_result,statechanged_func,upload_task



class TestRaysyncUpload(unittest.TestCase):
    '''测试上传基本功能'''
    URL = Config().get('URL')
    port = Config().get('PORT')
    username = Config().get('USERNAME')
    password = Config().get('PASSWORD')
    lib = ctypes.CDLL(SDK_PATH)


    def setUp(self):
        self.instance = self.lib.Raysync_CreateRaysyncInterface()
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
        upload_task.task_state = 0  # 初始化upload_task.task_state = 0
        self.lib.Raysync_List(self.instance, "/")
        #list操作
        time.sleep(2)
        self.lib.Raysync_DeleteAllTask(self.instance)   #清空传输列表
        time.sleep(1)

    def test_upload_1(self):
        '''正常上传单个文件'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'167-mov.mov')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, None, 'upload_task_1')
        # 上传单个167-mov.mov 文件
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)

    def test_upload_2(self):
        '''正常上传单个文件夹'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'upload_task')
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
        except:
            logger.info('服务器不存在该文件，无需删除')

        time.sleep(5)
        self.lib.Raysync_Upload(self.instance,bytes(BASE_PATH, encoding='utf8') ,'/',files,None,'upload_task_2')
        #上传upload_task目录
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)



    def test_upload_3(self):
        '''正常上传多个文件'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        upload_file = []
        for i in os.walk(UPLOAD_PATH):
            # 遍历文件夹
            upload_file.append(i)
            #遍历上传文件所在的文件夹，并将文件名加入upload_file数组
        files = (ctypes.c_char_p * (len(upload_file[0][2]) + 1))()
        #将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1

        a = 0
        for i in upload_file:
            for b in i[2]:
                files[a] = ctypes.c_char_p(bytes(b, encoding='utf8'))
                a = a + 1
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_Upload(self.instance,bytes(UPLOAD_PATH, encoding='utf8') , '/' , files , None , 'upload_task_3')
        #判断raysync.exe文件是否在列表中，注意bytes格式，二进制格式
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)

    def test_upload_4(self):
        '''正常上传单个文件,指定目标名称为test.mov'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调

        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'167-mov.mov')
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
        except:
            logger.info('服务器不存在该文件，无需删除')
        upload_files = (ctypes.c_char_p * 2)()
        upload_files[0] = ctypes.c_char_p(b'test.mov')
        # 格式化167-mov.mov 文件
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, upload_files, 'upload_task_4')
        # 上传单个167-mov.mov 文件
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        self.lib.Raysync_List(self.instance, "/")
        time.sleep(2)
        ret = (bytes('test.mov', encoding='gbk') in list_result)
        #判断raysync.exe文件是否在列表中，注意bytes格式，二进制格式
        self.assertTrue(ret)




    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例