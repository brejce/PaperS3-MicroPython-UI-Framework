# SDCardManager.py
import machine # type: ignore
import os

class SD:
    _instance = None
    _mounted = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self._sd = None
    
    def mount(self):
        if self._mounted:
            return True
        
        try:
            # 先尝试卸载（如果已挂载）
            try:
                os.umount("/sd") # type: ignore
            except:
                pass
            
            # 使用 machine.SDCard
            self._sd = machine.SDCard(
                slot=3,
                sck=39,
                miso=40,
                mosi=38,
                cs=47,
                freq=20000000
            )
            
            # 检查是否成功
            if self._sd is None:
                print("SD 卡对象创建失败")
                return False
            
            # 挂载到文件系统
            os.mount(self._sd, "/sd") # type: ignore
            self._mounted = True
            print("✓ SD 卡已挂载到 /sd")
            return True
            
        except OSError as e:
            print(f"✗ 挂载失败 (OSError): {e}")
            self._mounted = False
            return False
        except Exception as e:
            print(f"✗ 挂载失败 (Exception): {e}")
            self._mounted = False
            return False
    
    def umount(self):
        if self._mounted:
            try:
                os.umount("/sd") # type: ignore
                self._mounted = False
                self._sd = None
                print("✓ SD 卡已卸载")
                return True
            except Exception as e:
                print(f"✗ 卸载失败：{e}")
                return False
        return True
    
    def is_ready(self):
        return self._mounted

# 全局单例
sd = SD()
# sd.mount()