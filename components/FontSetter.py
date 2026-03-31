import M5  # type: ignore

DEFAULT_FONT_PATH = "/flash/res/font/HarmonyOS_Sans_SC_Regular_28.vlw"

class FontSetter:
    """字体设置工具"""

    def __init__(self, path=None, display:M5.Display=None, size=1, measure_text="测"):
        """
        初始化字体设置

        Args:
            path: 字体文件路径
            display: 显示对象（默认M5.Display）
            size: 字体大小
            measure_text: 用于测量字符的文本
        """
        self.font_path = path if path else DEFAULT_FONT_PATH
        self.font_size = size
        self.display = display if display else M5.Display
        self.measure_text = measure_text
        self.char_width:int = 0

        self.char_height:int = 0
        # 尝试设置字体，如果失败则忽略
        try:
            self.display.setFont(self.font_path)
            self.set_font_size(size)
        except OSError:
            print(
                f"Warning: Could not load font {self.font_path}. Using default font.")

        # self.set_font_size()
        # self.set_font_color()
    def unloadFont(self):
        M5.Display.unloadFont()
        
    def measure_char_size(self,char:str=""):
        if char == "":
            char = self.measure_text

        try:
            self.char_width:int = self.display.textWidth(char)

            self.char_height:int = self.display.fontHeight()

            return self.char_width,self.char_height
        except Exception as e:
            print(f"measure_char_size erro ：{e}")
            return self.char_width,self.char_height
        
    def set_font_size(self, size=1):

        self.font_size = size
        self.display.setTextSize(size)

    def set_font_color(self,text_color=0,bg_color=-1):
        self.text_color = text_color
        self.bg_color = bg_color
        self.display.setTextColor(text_color, bg_color)