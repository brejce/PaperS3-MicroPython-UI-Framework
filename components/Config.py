#Config.py
import os
import M5  # type: ignore
# import re
from SDCardManager import sd


class Config:
    """
    需要 re os M5 
    需要挂载 sd 到/sd
    """
    TEXT_SIZE = 1.0
    FONT_COLOR = 0x000000
    FONT_BG_COLOR = -1
    BG_COLOR = 0xFFFFFF
    
    FONT_PATH = "/sd/fonts"
    FONTS = {}
    DEFAULT_FONT_INDEX = 3
    _num_pattern = None

    DEFAULT_FONT_SIZE = 32
    
    DEFAULT_FONT_LINE_SPACE = 13
    DEFAULT_FONT_LETTER_SPACE = 13

    @classmethod
    def init_fonts(cls):
        import re
        cls._num_pattern = re.compile(r'(\d+)\.vlw$')
        cls.FONTS = {}
        try:
            if sd.is_ready():
                fonts = os.listdir(cls.FONT_PATH)
                for ft in fonts:
                    match = cls._num_pattern.search(ft)
                    if match:
                        size = int(match.group(1))
                        cls.FONTS[size] = ft
        except Exception as e:
            print(f"Config Fonts get error: {e}")
            cls.FONTS = {}
    @classmethod
    def get_font_file(cls, size):
        """查找指定字号的字体文件"""
        return cls.FONTS.get(size)

    @classmethod
    def get_font_path(cls, size):
        """获取完整字体路径"""
        font_file = cls.FONTS.get(size)
        if font_file:
            return f"{cls.FONT_PATH}/{font_file}"
        return None  
     
    @classmethod
    def get_font_path_by_index(cls, index):
        font_keys = sorted(cls.FONTS.keys())
        if index < len(font_keys):
            font_file = cls.FONTS.get(font_keys[index])
            if font_file:
                return f"{cls.FONT_PATH}/{font_file}"
        return None

    @classmethod
    def update_font(cls,size=None,color=None,bg_color=None,font_size=None):

        M5.Display.setTextSize(size or Config.TEXT_SIZE)

        M5.Display.setTextColor(color or Config.FONT_COLOR, bg_color or Config.FONT_BG_COLOR)
        try:
            path = Config.get_font_path(font_size or Config.DEFAULT_FONT_SIZE)

            M5.Display.setFont(path)

        except Exception as e:
            print(f"update_font {e}")