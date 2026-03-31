"""图标管理器 - 仅扫描和管理图标信息"""

import os


class IconManager:
    """图标管理器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self._icons = {}
        self._scan_path = None
    
    def scan(self, path="/flash/res/img"):
        """
        扫描图标目录
        
        Returns:
            list: 图标名称列表
        """
        print(f"[IconManager] 扫描目录: {path}")
        self._icons.clear()
        self._scan_path = path
        
        try:
            files = os.listdir(path)
            for f in files:
                # 使用字符串操作替代 os.path
                if "." in f:
                    parts = f.rsplit(".", 1)
                    name = parts[0]
                    ext = parts[1].lower()
                else:
                    name = f
                    ext = ""
                
                full_path = f"{path}/{f}"
                
                self._icons[name] = {
                    "path": full_path,
                    "type": ext,
                    "file": f
                }
            
            print(f"[IconManager] 扫描完成: {len(self._icons)} 个图标")
            return list(self._icons.keys())
        except Exception as e:
            print(f"[IconManager] 扫描失败: {e}")
            return []
    
    def list(self):
        """列出所有图标名称"""
        return list(self._icons.keys())
    
    def exists(self, name):
        """检查图标是否存在"""
        return name in self._icons
    
    def get_path(self, name):
        """获取图标完整路径"""
        if name in self._icons:
            return self._icons[name]["path"]
        return None
    
    def get_type(self, name):
        """获取图标文件类型（png, jpg, bmp）"""
        if name in self._icons:
            return self._icons[name]["type"]
        return None
    
    def get_info(self, name):
        """获取图标完整信息"""
        return self._icons.get(name)
    
    def get_all(self):
        """获取所有图标信息"""
        return self._icons


# 全局单例
icon_manager = IconManager()


# 便捷函数
def icons():
    return icon_manager


def scan_icons(path="/flash/res/img"):
    return icon_manager.scan(path)


def get_icon_path(name):
    return icon_manager.get_path(name)


def get_icon_type(name):
    return icon_manager.get_type(name)


def get_icon_info(name):
    return icon_manager.get_info(name)