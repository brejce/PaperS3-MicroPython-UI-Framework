
from IconButton import IconButton
from TextView import TextView
import M5 # type: ignore
from UIElement import UIElement
from Color import Colors

from Button import Button
from Framework import Framework
from ListView import ListView
import esp32 # type: ignore
import time
import binascii
import time
from AppBase import AppBase
from TouchZone import TouchZone
from SDCardManager import sd
import os

class BlankView1(UIElement):
    def __init__(self, x: int=0, y: int=0,w:int=540,h:int=960):
        super().__init__(x, y, w,h) 

        self.bg_color = Colors.WHITE
        self._click_callback = None
        self.radius = 20
        self.is_first = True
    def on_show(self):
        self.is_first = True
        super().on_show()

    def draw(self):
        print(f"[BlankView] 更新: at ({self.x}, {self.y})")
        if not self.is_first:
        
          return
        M5.Display.fillRoundRect(self.x,self.y,self.w,self.h,self.radius,self.bg_color)
        M5.Display.drawRoundRect(self.x,self.y,self.w,self.h,self.radius,0)
        M5.Display.drawLine(self.x+20,self.y+80,self.w,self.y+80,0) 

        self.is_first = False

class CenterTextView(TextView):
  def __init__(self, x: int, y: int, text: str = "Default Text"):

    super().__init__(x, y, text)

  def draw(self):

    print(f"[TextView] 绘制文本: '{self.text}' at ({self.x}, {self.y})")

    M5.Display.drawCenterString(self.text,self.x,self.y-self.h//2)
  def is_touched(self, tx: int, ty: int) -> bool:
        """
        检查触摸点是否在元素范围内
        Args:
            tx: 触摸点X坐标
            ty: 触摸点Y坐标
        Returns:
            bool: 如果触摸在范围内则返回True
        """
        if self.is_paused:
          return False

        return (
            self.x-self.w//2 <= tx <= self.x + self.w//2 and
            self.y-self.h//2 <= ty <= self.y + self.h//2
        )


class PopMenu(AppBase):

  def __init__(self,x=0,y=0,w=540,h=960):
    appname = self.__class__.__name__
    super().__init__(name=appname)
    self.x, self.y, self.w, self.h = x, y, w, h
    self.padding = 50

    self.char_color = Colors.BLACK
    self.bg_color = Colors.WHITE
    self.char_bg_color = -1

    self.current_menu = None


  def font_menu_instance(self):
    # 字体设置菜单
    self.font_menus = []#建立菜单view租
    font_menu_view = TextView(60,110,"字体菜单")#设置标题文字

    self.font_menus.append(font_menu_view)



    self.in_btn = Button(x=50+30,y=240,w=60,h=60,text="+")#设置++增大++字号按钮
    self.in_btn._click_callback = self.on_change_font_key_click # type: ignore
    self.font_menus.append(self.in_btn)

    ttt = CenterTextView(270,210,"选择字号")#设置菜单项目名称

    self.font_menus.append(ttt)

    #设置字号显示
    self.show_font_size = CenterTextView(270,270,f"{Config.DEFAULT_FONT_SIZE}")

    self.font_menus.append(self.show_font_size)

    self.de_btn = Button(x=430-30,y=240,w=60,h=60,text="-")#设置--减小--字号按钮
    self.de_btn._click_callback = self.on_change_font_key_click # type: ignore

    self.font_menus.append(self.de_btn)


  def read_menu_instance(self):

    self.read_menus = []
    read_menu_view = TextView(60,110,"阅读菜单")
    read_menu_view._click_callback = self.on_read_btn_click

    self.read_menus.append(read_menu_view)

    self.control_views = []

    self.font_menu_btn = Button(x=80, y=800, text="字体设置")
    self.font_menu_btn._click_callback = self.on_font_btn_click # type: ignore
    self.read_menu_btn = Button(x=300, y=800, text="阅读设置")
    self.read_menu_btn._click_callback = self.on_read_btn_click # type: ignore

    self.control_views.append(self.font_menu_btn)
    
    self.control_views.append(self.read_menu_btn)

  def on_create(self):
    super().on_create()

    # self.update_font() # 更新字体文字设置为默认设置



    # self.fontsetter.set_font_color(Colors.BLACK,-1)
    # 背景配置
    self.bg_views = [] #建立背景元素绘制

    self.blankview = BlankView1(x=20,y=80,w=500,h=800)#特别背景

    self.bg_views.append(self.blankview)

    #设置退出按钮
    self.cancel_icon = IconButton(x=500-64,y=90,path="/sd/res/icons/cancel.png")

    self.cancel_icon._click_callback = self.on_cancel_btn_click # type: ignore

    self.bg_views.append(self.cancel_icon)

    # 字体设置菜单
    self.font_menu_instance()

    # 阅读设置菜单
    self.read_menu_instance()

    self._switch_menu("font",self.font_menus)#默认进入字体设置




  def on_change_font_key_click(self,btn):
    print(f"{btn.text}")

    index = Config.DEFAULT_FONT_INDEX
    font_keys = sorted(Config.FONTS.keys())
    font_count = len(font_keys)

    if font_count == 0:
        print("No fonts available")
        return

    # ✅ 直接根据符号计算
    if "+" in btn.text:
        index +=1
    elif "-" in btn.text:
        index -=1
    
    

    # 限制范围
    # index = max(0, min(len(font_keys), index))

    # ✅ 循环索引：使用取模运算
    # 当 index 超出范围时自动循环
    index = index % font_count
    
    Config.DEFAULT_FONT_INDEX = index # type: ignore

    Config.DEFAULT_FONT_SIZE = font_keys[index]


    self.show_font_size.set_text(str(Config.DEFAULT_FONT_SIZE))


  def on_show(self):
    # M5.Display.fillRect(0, 0, 540, 960, Colors.WHITE)#仅仅是在画面覆盖白色

    Config.update_font(1,Colors.BLACK,-1,32) # 每次显示都设置为默认设置


    super().on_show()



  def _switch_menu(self,menu_name,menu_items):

    if self.current_menu == menu_name:
      print("不动")
      return

    self.ui_elements.clear()
    self.ui_elements.extend(self.bg_views)
    self.ui_elements.extend(menu_items)
    self.ui_elements.extend(self.control_views)

    for elem in self.ui_elements:#独立控制菜单页的显示
      if hasattr(elem, 'on_show'):
        elem.on_show()

    # print(self.ui_elements)
    
    self.current_menu = menu_name

    print(f"[PopMenu] ✓ 切换到 {menu_name} 菜单")

  def on_font_btn_click(self,btn):
    self._switch_menu("font", self.font_menus)

  def on_read_btn_click(self,btn):
    self._switch_menu("read", self.read_menus)

  def on_cancel_btn_click(self,btn):

    # M5.Display.clear()#如果回到上一个app，需要完全清理本app的残影，就需要调用。
    Config.update_font()

    mainapp = self._framework.get_app_by_name("ReadBookApp") # type: ignore
    # print(mainapp)
    mainapp.mark_dirty()
        # if popmenu and read_app.set_book_name(item_name):
    self._framework.switch_to(mainapp) # type: ignore
    # self._framework.switch_to(mainapp,True) # type: ignore  切换app，需要完全清理本app的残影，就需要设置True。





class BookManager():

  def __init__(self,path:str="/sd/books"):
    self.path = ""
    if os.listdir(path):
      self.path = path
    pass

  def list_books(self):

    try:
      files = os.listdir(self.path)
      files = [f for f in files if f.lower().endswith('.txt')]
      print(files)
      return files
    except Exception as e:
      print(f"[Book] 读取文件夹失败: {e}")
      return []
  def books_path(self,name:str=""):
    """获取书籍文件路径"""
    # return f"{self.path}/{book_name}.{txt}"
    return f"{self.path}/{name}"

# GridSystem.py
"""
网格坐标系统，根据画布尺寸和字符尺寸计算每个单元格的相对坐标（以内容区域左上角为原点）。
"""
class GridSystem:
    def __init__(self, width, height, char_width, char_height,
                 line_spacing=13, letter_spacing=6):
        self.width = width
        self.height = height
        self.char_width = char_width
        self.char_height = char_height
        self.line_spacing = line_spacing
        self.letter_spacing = letter_spacing

        # 计算网格行列
        self.cols = max(1, width // (char_width + letter_spacing))
        self.rows = max(1, height // (char_height + line_spacing))
        self.capacity = self.cols * self.rows

        # 计算居中偏移（使内容在区域内居中）
        used_width = self.cols * (char_width + letter_spacing) - letter_spacing
        self.offset_x = (width - used_width) // 2

        used_height = self.rows * (char_height + line_spacing) - line_spacing
        self.offset_y = (height - used_height) // 2

        # 预计算所有坐标（相对内容区域原点）
        self.coordinates = []
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.offset_x + col * (char_width + letter_spacing)
                y = self.offset_y + row * (char_height + line_spacing)
                self.coordinates.append((x, y))

    def get_coordinate(self, index):
        """返回第 index 个单元格的坐标 (x, y)"""
        if 0 <= index < len(self.coordinates):
            return self.coordinates[index]
        return None

    def get_all_coordinates(self):
        """返回所有坐标的元组列表"""
        return tuple(self.coordinates)

    def get_grid_size(self):
        """返回 (列数, 行数)"""
        return self.cols, self.rows

    def get_capacity(self):
        return self.capacity

    def get_char_size(self):
        return self.char_width, self.char_height

    def get_spacing(self):
        return self.line_spacing, self.letter_spacing
    


# LayoutInfo.py
"""
用于 BookReader 的纯布局信息，不包含坐标计算。
"""
class LayoutInfo:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.capacity = cols * rows



# ReadProgressManager.py

class ReadProgressManager:
    """使用 NVS 存储的进度管理器，支持累计阅读时长"""
    def __init__(self):
        self.nvs = esp32.NVS("readprogress")

    
    def _key(self, book_name):
        # 计算书名的 CRC32 哈希值，转为 8 位十六进制字符串
        crc = binascii.crc32(book_name.encode('utf-8')) & 0xFFFFFFFF
        return f"{crc:08x}"   # 返回类似 "a1b2c3d4" 的 8 字符键名

    def get_progress(self, book_name):
        """
        返回 (页码, 字节偏移, 累计阅读秒数)
        """
        key = self._key(book_name)
        try:
            data = self.nvs.get_str(key)
            if data:
                parts = data.split(',')
                if len(parts) == 3:
                    page, offset, total_sec = parts
                    return int(page), int(offset), int(total_sec)
        except Exception:
            pass
        return 0, 0, 0

    def update_progress(self, book_name, page, byte_offset, add_seconds=0):
        """
        更新进度：页码、偏移，并可增加累计秒数
        """
        key = self._key(book_name)
        total_sec = 0
        try:
            data = self.nvs.get_str(key)
            if data:
                parts = data.split(',')
                if len(parts) == 3:
                    _, _, total_sec = parts
                    total_sec = int(total_sec)
        except Exception:
            pass
        total_sec += add_seconds
        self.nvs.set_str(key, f"{page},{byte_offset},{total_sec}")

    def save_now(self):
        """NVS 无需显式保存，留作兼容"""
        pass


# BookReader.py
# from LayoutInfo import LayoutInfo
# from ReadProgressManager import ReadProgressManager

class BookReader:
    def __init__(self, layout_info: LayoutInfo):
        self.layout = layout_info          # 包含 cols, rows, capacity
        self.book = None
        self.book_name = ""
        self.current_page = 0
        self._current_start_offset = 0     # 当前页起始偏移
        self.page_offsets = []              # 记录每页起始偏移
        self.progress_manager = ReadProgressManager()

    def open(self, path, book_name=None):
        self.close()
        try:
            self.book = open(path, "r", encoding="utf-8")
            self.book_name = book_name
            self.page_offsets.clear()
            self.current_page = 0
            self._current_start_offset = 0

            # 恢复进度
            page, offset, _ = self.progress_manager.get_progress(self.book_name)
            if offset > 0:
                self.book.seek(offset)
                self.current_page = page
                # 预读当前页以建立偏移记录
                self._get_page_chars(self.current_page)
            return True
        except Exception as e:
            print(f"[BookReader] open failed: {e}")
            return False

    def close(self):
        if self.book:
            self.book.close()
            self.book = None

    def _read_one_page_chars(self):
        """从当前位置读取一页字符，返回 (字符列表, 起始偏移, 结束偏移)"""
        start_pos = self.book.tell()
        chars = []
        row, col = 0, 0
        while row < self.layout.rows:
            ch = self.book.read(1)
            if not ch:
                break
            if ch in ('\n', '\r'):
                row += 1
                col = 0
                continue
            chars.append(ch)
            col += 1
            if col >= self.layout.cols:
                row += 1
                col = 0
        end_pos = self.book.tell()
        if not chars:
            return None, start_pos, end_pos
        return chars, start_pos, end_pos

    def _skip_one_page(self):
        """跳过一页，仅移动文件指针"""
        _, _, success = self._read_one_page_chars()
        return success

    def _get_page_chars(self, page_index):
        """获取指定页码的字符列表（不包含坐标）"""
        if not self.book or page_index < 0:
            return None

        # 定位到该页起始
        if page_index < len(self.page_offsets):
            self.book.seek(self.page_offsets[page_index])
        else:
            # 从未访问过，需要扫描到目标页
            if self.page_offsets:
                self.book.seek(self.page_offsets[-1])
            else:
                self.book.seek(0)
            # 跳过中间页
            for _ in range(len(self.page_offsets), page_index):
                if not self._skip_one_page():
                    return None
            # 记录新页起始偏移
            start = self.book.tell()
            self.page_offsets.append(start)

        # 读取当前页
        chars, start_off, _ = self._read_one_page_chars()
        if chars is None:
            return None
        self._current_start_offset = start_off
        return chars

    def get_current_page_chars(self):
        """返回当前页的字符列表"""
        return self._get_page_chars(self.current_page)

    def next_page(self):
        chars = self._get_page_chars(self.current_page + 1)
        if chars is not None:
            self.current_page += 1
            self._save_progress()
            return chars
        return None

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            chars = self._get_page_chars(self.current_page)
            if chars is not None:
                self._save_progress()
                return chars
        return None

    def _save_progress(self):
        if not self.book or not self.book_name:
            return
        self.progress_manager.update_progress(
            self.book_name,
            self.current_page,
            self._current_start_offset,
            add_seconds=0
        )



class BookContent(UIElement):
    """书籍内容显示区域，负责将字符列表绘制到屏幕上"""
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.grid = None               # GridSystem 实例
        self.current_chars_abs = []     # 存储绝对坐标的字符列表 [(char, abs_x, abs_y), ...]

    def set_grid(self, grid):
        self.grid = grid

    def set_page_chars(self, chars):
        """
        接收字符列表（无坐标），通过 grid 转换为绝对坐标并存储
        """
        if not self.grid:
            return
        coords = self.grid.get_all_coordinates()   # 相对内容区域 (0,0) 的坐标
        self.current_chars_abs = []
        for i, ch in enumerate(chars):
            if i >= len(coords):
                break
            rel_x, rel_y = coords[i]
            self.current_chars_abs.append((ch, self.x + rel_x, self.y + rel_y))
        self.mark_dirty()

    def draw(self):
        if not self.current_chars_abs:
            # 调试框：无内容时绘制边框
            M5.Display.drawRect(self.x, self.y, self.w, self.h, Colors.BLACK)
            return
        M5.Display.startWrite()
        # 清空内容区域
        M5.Display.fillRect(self.x, self.y, self.w, self.h, Colors.WHITE)
        for ch, x, y in self.current_chars_abs:
            M5.Display.drawString(ch, x, y)
        M5.Display.endWrite()




# ReadBookApp.py

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

class BlankView(UIElement):
    def __init__(self, x: int=0, y: int=0,w:int=540,h:int=960,bg_color = Config.BG_COLOR):
        super().__init__(x, y, w,h) 

        self.bg_color = bg_color
        self._click_callback = None
        self.is_first = True
    def on_show(self):
        self.is_first = True
        super().on_show()

    def draw(self):
        print(f"[BlankView] 更新: at ({self.x}, {self.y})")
        if not self.is_first:
        
          return
        M5.Display.fillRect(self.x,self.y,self.w,self.h,self.bg_color)

        self.is_first = False

class ReadBookApp(AppBase):
    def __init__(self, x=0, y=0, w=540, h=960):
        super().__init__(name=self.__class__.__name__)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.padding = 20
        self.grid = None
        self.reader = None
        self.book_content = None
        self._reading_start = 0

    def on_create(self):
        super().on_create()

        self.back_ground = BlankView()

        self.ui_elements.append(self.back_ground)
        # 内容区域
        content_x = self.x + self.padding
        content_y = self.y + self.padding*2
        content_w = self.w - self.padding * 2
        content_h = self.h - self.padding * 4

        # 创建 GridSystem（基于当前字体）
        self._create_grid()

        # 创建 LayoutInfo 供 BookReader 使用
        cols, rows = self.grid.get_grid_size()
        layout_info = LayoutInfo(cols, rows)

        # 创建 BookReader
        self.reader = BookReader(layout_info)

        # 创建 BookContent
        self.book_content = BookContent(content_x, content_y, content_w, content_h)
        self.book_content.set_grid(self.grid)
        self.ui_elements.append(self.book_content)

        # 触摸区域
        self._create_touch_zones()

    def _create_grid(self):
        """根据当前字体创建 GridSystem"""
        Config.update_font()   # 确保应用当前字体设置
        char_w = M5.Display.textWidth("测")
        char_h = M5.Display.fontHeight()
        content_w = self.w - self.padding * 2
        content_h = self.h - self.padding * 2
        self.grid = GridSystem(
            content_w, content_h,
            char_w, char_h,
            Config.DEFAULT_FONT_LINE_SPACE,
            Config.DEFAULT_FONT_LETTER_SPACE
        )

    def _create_touch_zones(self):
        self.prev_zone = TouchZone(0, 0, 180, 960, "prev")
        self.menu_zone = TouchZone(180, 0, 180, 960, "menu")
        self.next_zone = TouchZone(360, 0, 180, 960, "next")

        self.prev_zone._click_callback = self._on_prev_page
        self.menu_zone._click_callback = self._on_menu
        self.next_zone._click_callback = self._on_next_page

        self.ui_elements.extend([self.prev_zone, self.menu_zone, self.next_zone])

    def set_book_name(self, name):
        """外部调用，打开书籍"""
        if not self.reader:
            print("[ReadBookApp] reader not initialized")
            return False
        # from BookManager import BookManager   # 假设您有 BookManager
        manager = BookManager()
        path = manager.books_path(f"{name}.txt")
        success = self.reader.open(path, book_name=name)
        if success:
            chars = self.reader.get_current_page_chars()
            self.book_content.set_page_chars(chars)
            self._dirty = True
        return success

    def _on_prev_page(self, btn):
        if self.reader:
            chars = self.reader.prev_page()
            if chars:
                self.book_content.set_page_chars(chars)
                self._dirty = True

    def _on_next_page(self, btn):
        if self.reader:
            chars = self.reader.next_page()
            if chars:
                self.book_content.set_page_chars(chars)
                self._dirty = True

    def _on_menu(self, btn):
        popmenu = self._framework.get_app_by_name("PopMenu")   # 假设 PopMenu 已注册
        if popmenu:
            self._framework.switch_to(popmenu)

    def on_show(self):
        super().on_show()
        self._reading_start = time.time()
        # 检查字体是否改变（例如从菜单返回时），重新创建 grid 并更新 reader 的布局信息
        old_grid = self.grid
        self._create_grid()
        if old_grid != self.grid:   # 简单比较，实际可比较行列数
            # 更新 BookContent 的 grid
            self.book_content.set_grid(self.grid)
            # 更新 BookReader 的布局信息
            cols, rows = self.grid.get_grid_size()
            self.reader.layout = LayoutInfo(cols, rows)
            # 重新加载当前页（字体变化可能影响分页）
            if self.reader.book:
                chars = self.reader.get_current_page_chars()
                self.book_content.set_page_chars(chars)
                self._dirty = True

    def on_hide(self):
        if self.reader and self.reader.book_name and self._reading_start > 0:
            elapsed = int(time.time() - self._reading_start)
            if elapsed > 0:
                self.reader.progress_manager.update_progress(
                    self.reader.book_name,
                    self.reader.current_page,
                    self.reader._current_start_offset,
                    add_seconds=elapsed
                )
        super().on_hide()






class BooksShelf(AppBase):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.w = M5.Display.width()
        self.h = M5.Display.height()
        self.boomanager = None
        self.listview = None
        self.list_start_x,self.list_start_y = 20,50
        self.list_w,self.list_h = 500,800

    def on_create(self):
        super().on_create()
        self.boomanager = BookManager()

        books = [b.rsplit(".", 1)[0] for b in self.boomanager.list_books()]*5

        self.listview = ListView(self.list_start_x, self.list_start_y, self.list_w, self.list_h)
        self.listview.font_size = 1.0
        self.listview.set_items(books)
        self.listview.set_item_click_callback(self.on_list_item_clicked)
        self.ui_elements.append(self.listview)

        start_x = 15
        self.btn = Button(x=start_x, y=860, text="+")
        self.btn._click_callback = self.increcen # type: ignore
        self.ui_elements.append(self.btn)

        start_x +=160+15
        self.btn_ex = Button(x=start_x, y=860, text="exit")
        self.btn_ex._click_callback = self.on_exit # type: ignore
        self.ui_elements.append(self.btn_ex)

        start_x +=160+15
        self.btn1 = Button(x=start_x, y=860, text="-")
        self.btn1._click_callback = self.deincrecen # type: ignore

        self.ui_elements.append(self.btn1)

        half = self.list_h//2

        self.tz_deincrecen = TouchZone(x=self.list_w-self.list_start_x,y=self.list_start_y,w=50,h=half,text="deincrecen")
        self.tz_increcen  = TouchZone(x=self.list_w-self.list_start_x,y=self.list_start_y+half,w=50,h=half,text="increcen")

        self.tz_increcen._click_callback = self.increcen # type: ignore
        self.tz_deincrecen._click_callback = self.deincrecen # type: ignore
        self.ui_elements.append(self.tz_increcen)
        self.ui_elements.append(self.tz_deincrecen)



        for elem in self.ui_elements:
            if hasattr(elem, 'on_create'):
                elem.on_create()
    def on_list_item_clicked(self, item_name):
        read_app = self._framework.get_app_by_name("ReadBookApp") # type: ignore
        if read_app and read_app.set_book_name(item_name):
            self._framework.switch_to(read_app) # type: ignore

    def on_exit(self,btn):
        self._framework.exit() # type: ignore

    def increcen(self, btn):
        self.listview.set_start_item_index(self.listview._start_item_index + 1) # type: ignore

    def deincrecen(self, btn):
        self.listview.set_start_item_index(self.listview._start_item_index - 1) # type: ignore

    def on_show(self):
        Config.update_font()

        super().on_show()


    def update(self):
        super().update()








# --- 主程序 ---
def setup():
    global fw
    M5.begin()
    print("--- Setup Phase (Using Imported Core) ---")
    sd.mount()
    Config.init_fonts()
    Config.update_font()


    
    fw = Framework()
    fw.add_app(ReadBookApp())
    fw.add_app(BooksShelf())
    fw.add_app(PopMenu())
    fw.start()
    fw.switch_to(fw.get_app_by_name("BooksShelf"))

    print("--- Setup Complete ---")


def loop():
    global fw
    M5.update()
    fw.handle_touch() # 如果需要触摸功能，取消注释
    fw.update()


if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        M5.Display.endWrite()
        # sd.umount()#真的有用
        M5.Display.unloadFont()
        try:
            from utility import print_error_msg # type: ignore
            print_error_msg(e)
        except ImportError:
            print("Error:", e)
