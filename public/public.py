import ctypes
import time
from public.config import MKDIR_WIREFILE_PATH,RENAME_WIREFILE_PATH,REMOVE_WIREFILE_PATH
from public.log import logger

list_result = list() #获取list结果的list





def list_cb(instance, err_code, path, files, size, file_time, is_folder):
    # print(files)
    '''创建list回调格式函数'''
    global list_result
    list_result.clear()
    if not err_code:
        print("path: ", path)
        pos = 0
        while True:
            if not files[pos]:
                break

            list_result.append(files[pos])
            print("====================================================")
            print("file", pos + 1, ":", files[pos])
            print("size", pos + 1, ":", size[pos])
            print("time", pos + 1, ":", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time[pos])))
            print("is folder", pos + 1, ":", is_folder[pos])
            print("====================================================")
            logger.info("====================================================")
            logger.info("file " + str(pos + 1) + " : " + str(files[pos]))
            logger.info("size " + str(pos + 1) + " : " + str(size[pos]))
            logger.info("time " + str(pos + 1) + " : " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time[pos])))
            logger.info("is folder " +  str(pos + 1) + " : " + str(is_folder[pos]))
            logger.info("====================================================")
            pos += 1

CLISTFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p),
                                 ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_bool))
ls_cb = CLISTFUNC(list_cb)

##############################################################################################################

def mkdir_cb(instance, err_code):
    '''创建新建文件夹回调函数'''
    with open(MKDIR_WIREFILE_PATH,'w') as f:
        f.write(str(err_code))
        #写入错误码进文件内
        f.close()

CMKDIRFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
mk_cb = CMKDIRFUNC(mkdir_cb)

################################################################################################

def rename_cb(instance, err_code):
    '''创建重命名文件夹回调函数'''
    with open(RENAME_WIREFILE_PATH,'w') as f:
        f.write(str(err_code))
        f.close()

CRENAMEFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
re_cb = CMKDIRFUNC(rename_cb)

################################################################################################
def remove_cb(instance, err_code):
    '''创建删除文回调函数'''
    with open(REMOVE_WIREFILE_PATH,'w') as f:
        f.write(str(err_code))
        f.close()

CREMOVEFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
rem_cb = CMKDIRFUNC(remove_cb)


########################################################################################################
#upload download上传下载测试用例调用
class upload_task_object:
    task_state = 0

upload_task = upload_task_object

def statechanged_cb(instance, TaskID, State):
    '''设置传输文件状态变化函数'''
    global upload_task
    upload_task.task_state = State
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "任务ID", TaskID, "状态码", State)

TASK_STATE_CHANGED = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint)
statechanged_func = TASK_STATE_CHANGED(statechanged_cb)
#######################################################################################################
#task测试用例调用

class task_object:
    TaskID = 0
task = task_object

def GetTaskInfo_cb(instance, ID):
    '''设置文件传输状态信息函数'''
    global task
    if ID[0]:
        task.TaskID = ID[0]

CGETTASKINFOFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint))
TaskInfo_cb = CGETTASKINFOFUNC(GetTaskInfo_cb)




