# TextView.py
"""
BatteryIcon 组件 - 电池状态图标
"""
import M5  # type: ignore
from Color import Colors
from UIElement import UIElement

class TextView(UIElement):


    def __init__(self, x: int, y: int, text: str = "Default Text"):
        self.text = text
        w,h = self.measure_char_size(text)

        super().__init__(x, y,w,h) # 简单估算宽度

        self.text_color = Colors.BLACK  # 黑色文字
        self.bg_color = Colors.WHITE   # 对于文字来说，可以透出背景的颜色。
        self.text_bg_color = -1   # 对于文字来说，可以透出背景的颜色。

        self.is_pressed = False
        self._click_callback = None

        self._long_press_triggered = False
        self._long_press_callback = None

    def on_create(self):
      super().on_create()
      M5.Display.setTextSize(1)

      M5.Display.setTextColor(self.text_color, self.text_bg_color)

    def set_text(self, new_text: str):
        if self.text != new_text:
            self.text = new_text
            self.mark_dirty()

    def measure_char_size(self,char:str=""):
        try:
            char_width:int = M5.Display.textWidth(char)

            char_height:int = M5.Display.fontHeight()

            return char_width,char_height
        except Exception as e:
            print(f"measure_char_size erro ：{e}")
            return 0,0


    def draw(self):

        print(f"[TextView] 绘制文本: '{self.text}' at ({self.x}, {self.y})")

        M5.Display.fillRect(self.x,self.y,self.w,self.h,self.bg_color)#背景

        self.measure_char_size(self.text)

        M5.Display.drawString(self.text, self.x,self.y)


    def set_text_color(self,color:int=0):
      if self.text_color != color:  # 黑色文字
        self.text_color = color
        self.mark_dirty()



    def on_delete(self):
        super().on_delete()
        print(f"[TextView] Canvas 资源待系统回收")

    def set_click_callback(self, callback_func):

        self._click_callback = callback_func
        return self

    def set_long_press_callback(self, callback_func):

        self._long_press_callback = callback_func

        return self

    def handle_touch(self,tx,ty,detail):
            # 解包触摸详情
        (dx, dy, dist_x, dist_y,
         is_pressed, was_pressed, was_clicked,
         is_released, was_released, is_holding, was_hold) = detail

        # print(detail)
        if was_pressed:
            print(f"[TextView] {self.text}: 按下")
            self.is_pressed = True
            # self.mark_dirty()

        elif was_released:
            if self.is_pressed and was_clicked:
                if self._click_callback:
                    print(f"[TextView] {self.text}: 点击回调")
                    self._click_callback(self)

            print(f"[TextView] {self.text}: 释放")
            self.is_pressed = False
            # self.mark_dirty()

        elif is_holding and not self._long_press_triggered:
            print(f"[TextView] {self.text}: 长按触发")
            self._long_press_triggered = True
            if self._long_press_callback:
                self._long_press_callback(True)
