# ListView.py
"""
ListView 组件 - ListView
"""
import time
import M5  # type: ignore
from Color import Colors
from UIElement import UIElement
from FontSetter import FontSetter
from ListSystem import ListSystem


class ListView(UIElement):

  def __init__(self, x=20, y=50, w=500, h=800):
    super().__init__(x, y, w, h)
    self.padding = 10
    self.line_spacing = 13
    self._content_height = self.h - 2 * self.padding
    self._items = []
    self._start_item_index = 0
    # --- 新增：预计算的绘制范围 ---
    self.max_items = 0
    self._viewport_start_item_idx = 0
    self._viewport_end_item_idx = 0
    self._viewport_y_coords = [] # 对应的 Y 坐标列表
    self.percent = 0
    # ---------------------------------
    self.canvas = None
    self.color_depth = 4
    self.use_psram = True
    self.font_size = 1.0
    self.bg_color = Colors.WHITE
    self.text_color = Colors.BLACK
    self.text_bg_color = -1
    self.fontsetter = None
    self.listsystem = None
    self._item_click_callback = None

    self.is_pressed = False


    
    self.cell_x_start,self.cell_y_start,self.cell_w = self.w+8,self.y+1+self.padding,10

    self.cell_y_end = self.h-(1+self.padding)*2
    
  def set_item_click_callback(self, callback_func):
        """
        设置项目点击回调函数。
        回调函数将接收此 ListView 实例和被点击的项目文本作为参数。
        func(listview_instance: ListView, clicked_item_text: str)
        """
        self._item_click_callback = callback_func

        return self # 支持链式调用
  def _get_item_index_at(self, ty: int):
        """
        根据触摸的 Y 坐标，计算出被点击的项目在 self._items 中的索引。

        Args:
            ty (int): 触摸点的 Y 坐标。

        Returns:
            int or None: 如果触摸点在有效项目区域内，返回项目索引；否则返回 None。
        """
        if not self._items or not self.listsystem:
            return None

        # 1. 将屏幕 Y 坐标转换为相对于 ListView canvas 的 Y 坐标
        relative_ty = ty - self.y

        # 2. 检查 Y 坐标是否在 ListView 的内容区域内 (考虑 padding)
        content_top = self.padding
        content_bottom = self.h - self.padding

        if not (content_top <= relative_ty <= content_bottom):
            return None # 触摸点在 padding 或 ListView 之外

        # 3. 计算点击的是哪一行 (相对于 _start_item_index 的偏移)
        # Y 坐标减去起始偏移 (padding)，然后除以单行高度
        row_offset_from_start = int((relative_ty - content_top) // self._one_line_height)

        # 4. 计算被点击的项目的全局索引
        clicked_item_global_index = self._start_item_index + row_offset_from_start

        # 5. 检查计算出的索引是否在 _items 的有效范围内
        if 0 <= clicked_item_global_index < len(self._items):
            return clicked_item_global_index

        # 如果计算出的索引超出了 _items 的范围，说明点击了空区域
        return None
  def on_create(self):
    super().on_create()
    self.fontsetter = FontSetter()
    self.update_fontsetter()
    self._recalculate_viewport()

  def update_fontsetter(self):
    self.fontsetter.set_font_size(self.font_size) # type: ignore
    self.fontsetter.set_font_color(self.text_color, self.text_bg_color) # type: ignore
    self.char_width, self.char_height = self.fontsetter.measure_char_size("测") # type: ignore
    self._one_line_height = self.char_height + self.line_spacing
    self.set_list_system()


  def set_list_system(self):
    if self._content_height == 0 or self.char_height == 0 or self.line_spacing == 0:
      # print(f"[ListView] _content_height, char_height, line_spacing 为0")
      return
    self.listsystem = ListSystem(height=self._content_height, char_height=self.char_height, line_spacing=self.line_spacing)

  def set_font_size(self, font_size=1):
    if font_size == 0 or font_size == self.font_size:
      print(f"[ListView] font_size 为0 或者不变")
      return
    self.font_size = font_size
    self.update_fontsetter()
    # 当字体大小改变时，ListSystem 和 Viewport 都需要重新计算
    self.set_list_system()
    self._recalculate_viewport() # 重新计算 viewport
    self.mark_dirty()
  def draw_pop(self,text = "哈哈",delay_ms = 500):
      x,y = 270,10




      M5.Display.drawCenterString(text, x,y)

      M5.Display.setTextColor(Colors.WHITE, -1)

      time.sleep_ms(delay_ms) # type: ignore

      # M5.Display.drawCenterString(text, x,y)
      M5.Display.fillRect(x-80,y-2,160,40,self.bg_color)

      
      M5.Display.setTextColor(0, -1)

      pass
  def set_start_item_index(self, index=0):
    if not self.listsystem:
        print("[ListView] ListSystem 未初始化，无法设置索引")
        return
    # 限制 index 的范围
    max_start_index = max(0, len(self._items) - self.listsystem.get_max_rows())

    new_index = max(0, min(index, max_start_index))

    if new_index == self._start_item_index:
      # t = f"{new_index}--{self._start_item_index}"
      # print(t)
      self.draw_pop(text="到顶/底了")
      return # 没有变化

    self._start_item_index = new_index
    # --- 关键：在这里预计算 Viewport ---
    self._recalculate_viewport()
    # -----------------------------------
    self.mark_dirty()

  def _recalculate_viewport(self):
    """
    根据当前的 _start_item_index 和 ListSystem 信息，
    预计算出本次绘制需要的项目索引范围和对应的 Y 坐标。
    """
    if not self.listsystem:
        # 如果 ListSystem 还没准备好，清空 viewport 信息
        self._viewport_start_item_idx = 0
        self._viewport_end_item_idx = 0
        self._viewport_y_coords = []
        return

    max_items = self.listsystem.get_max_rows()
    items_y = self.listsystem.get_y_coordinates()

    # 计算绘制范围
    start_idx_to_draw = self._start_item_index
    potential_end_idx = start_idx_to_draw + max_items
    actual_end_idx = min(potential_end_idx, len(self._items))
    actual_start_idx = min(start_idx_to_draw, actual_end_idx)

    # 计算要绘制的项目数量
    items_to_draw_count = actual_end_idx - actual_start_idx

    # 存储计算结果
    self._viewport_start_item_idx = actual_start_idx
    self._viewport_end_item_idx = actual_end_idx

    # 生成对应的 Y 坐标列表 (只取需要的部分)
    # Y 坐标列表的长度应等于要绘制的项目数量
    # self._viewport_y_coords = items_y[:items_to_draw_count] # 切片获取前 N 个 Y 坐标
    self._viewport_y_coords = [rel_y + self.y for rel_y in items_y[:items_to_draw_count]]
    # print(f"[ListView._recalculate_viewport] 计算完成: 绘制范围 [{actual_start_idx}, {actual_end_idx}), Y 坐标数量: {len(self._viewport_y_coords)}")

  def set_items(self, items=None):

    if items is None:
      items = []
    if not items:
      self._items = []
      self._start_item_index = 0
      self._recalculate_viewport()
      self.mark_dirty()
      return
    self._items = items.copy()
    # 项目列表变了，需要重新计算 viewport (因为 max_start_index 会变)
    self._start_item_index = 0 # 重置滚动位置
    self._recalculate_viewport()
    self.mark_dirty()

  def draw_percen(self):


    items_len = len(self._items)
    
    percent = self._viewport_end_item_idx/items_len
    cell_y = percent*self.cell_y_end
    if cell_y >= self.cell_y_end:
      cell_y = self.cell_y_end
    if percent<self.percent:
      M5.Display.fillRect(self.cell_x_start,self.cell_y_start,self.x,self.y+self.h,self.bg_color)
    self.percent = percent
    # print(f"百分比{self.percent}----高度{cell_y}-----最后一个{self._viewport_end_item_idx}")

    M5.Display.fillRect(self.cell_x_start,self.cell_y_start,self.cell_w,int(cell_y),self.text_color)
    # M5.Display.fillRect(x,min_y,w,int(cell_y),Colors.MEDIUM_LIGHT)



    pass

  def draw(self):

    if not self._items or not self.listsystem or not self._viewport_y_coords:
      # print(f"items:{len(self._items)}, listsystem:{self.listsystem}, 或 viewport_y_coords:{len(self._viewport_y_coords)} 未初始化或为空")
      return
    self.draw_percen()
    items_len = len(self._items)
    # print(f"[ListView] 开始绘制，项目总数: {items_len}, 绘制范围: [{self._viewport_start_item_idx}, {self._viewport_end_item_idx}]")
    # self.percent = self._viewport_end_item_idx/items_len
    # print(f"开始{self.percent} ")
    M5.Display.startWrite()
    M5.Display.fillRect(self.x,self.y,self.w,self.h,self.bg_color) # 边框可选 # type: ignore

    M5.Display.drawRect(self.x,self.y,self.w,self.h,self.text_color) # 边框可选 # type: ignore
    x = self.padding+self.x

    # --- 优化后的绘制循环 ---
    # 直接遍历预计算好的 Y 坐标列表
    for i, y_coord in enumerate(self._viewport_y_coords):
        # 通过 i (在 viewport 内的相对索引) 计算出全局 item 索引
        item_global_index = self._viewport_start_item_idx + i
        # 获取项目文本
        item_text = self._items[item_global_index]
        # 设置 X 坐标
        # 使用预计算的 Y 坐标
        y = y_coord

        # print(f"  绘制项目 '{item_text}' 在 canvas 相对坐标 ({x}, {y})")
        M5.Display.drawString(item_text, x, y) # type: ignore

    # self.canvas.push(self.x, self.y) # type: ignore
    self.draw_percen()
    M5.Display.endWrite()
  def handle_touch(self, tx: int, ty: int, detail):
        """
        处理触摸事件。
        如果触摸发生在列表项目上并释放，则触发项目点击回调。
        """
        if not self.is_active:
           return
        # text = ""
        # print(f"触摸的数据时：{text}")

        # 解包触摸详情
        (dx, dy, dist_x, dist_y,
         is_pressed, was_pressed, was_clicked,
         is_released, was_released, is_holding, was_hold) = detail


        # print(detail) # 可选：打印触摸详情用于调试

        if was_pressed:
            # 可以在这里添加按下时的视觉反馈，比如高亮
            # print(f"[ListView] 按下 at ({tx}, {ty})")
            # self.mark_dirty() # 如果需要按下时刷新视觉反馈
            self.is_pressed = True
        elif was_released:
            # print(f"[ListView] 释放 at ({tx}, {ty})")
            if self.is_pressed  and was_clicked: # 确认是点击事件（而非滑动后释放）
                clicked_index = self._get_item_index_at(ty)
                if clicked_index is not None:
                    clicked_item_text = self._items[clicked_index]
                    # print(f"[ListView] 点击了项目: '{clicked_item_text}' (索引: {clicked_index})")
                    if self._item_click_callback:
                        print(f"[ListView] 触发项目点击回调 :{clicked_item_text}")
                        self._item_click_callback(clicked_item_text)
                else:
                    print(f"[ListView] 点击了无效区域 (Y: {ty})")
                self.is_pressed = False
























