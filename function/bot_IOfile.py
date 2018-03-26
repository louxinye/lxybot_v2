# 本地文件IO
import pickle
import threading

file_lock = threading.Lock()

# 函数功能:输入数据、文件名,执行写入文件操作
def write_pkl_data(pkl_data, pkl_name):
    file_lock.acquire()
    try:
        output = open(pkl_name, 'wb')
        pickle.dump(pkl_data, output)
    except IOError:
        file_lock.release()
        return 0
    else:
        output.close()
        file_lock.release()
        return 1


# 函数功能:输入文件名,执行读出文件操作
def read_pkl_data(pkl_name):
    file_lock.acquire()
    try:
        pkl_file = open(pkl_name, 'rb')
        pkl_data = pickle.load(pkl_file)
    except IOError:
        file_lock.release()
        return []
    else:
        pkl_file.close()
        file_lock.release()
        return pkl_data
