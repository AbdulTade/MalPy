import ctypes
import os
from Crypto.Random import get_random_bytes

class Utils:
    def __init__(self) -> None:
        pass

    def stringZeros(num=0):
        string = b''
        for i in range(num):
            string += bytes('{}'.format(num), encoding='utf-8')
        return string

    def HideFile(self,filenames):
        for filename in filenames:
            # filename = os.path.join(os.getcwd(),filename)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            if(os.name == 'nt'):
                kernel32 = ctypes.WinDLL('kernel32',use_last_error=True)
                attrs = kernel32.GetFileAttributesW(filename)
                if(attrs == -1):
                    raise ctypes.WinError(ctypes.get_last_error())
                attrs |= FILE_ATTRIBUTE_HIDDEN
                if(not kernel32.SetFileAttributesW(filename,attrs)):
                    raise ctypes.WinError(ctypes.get_last_error)
                return filename
            elif(os.name == 'posix'):
                return "." + filename


    def shred(FileObject,numbytes=0,num_writes=0, overwrite_random=False):
        """
        Before you call this function make sure FileObject is
        opened in binary write mode
        """
        if(FileObject.writable()):
            for num in range(num_writes):
                if(overwrite_random):
                    randBytes = get_random_bytes(numbytes)
                    FileObject.write(randBytes)
                    print(randBytes)
                else:
                    FileObject.write(Utils.stringZeros(numbytes))
            FileObject.close()
        return None