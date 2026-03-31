import M5  # type: ignore


from Color import Colors # 导入颜色常量
from UIElement import UIElement

class Button(UIElement):
    def __init__(self, x: int=100, y: int=100,w:int=160,h:int=60, text: str = "Default Text"):
        super().__init__(x, y, w,h) # 简单估算宽度
        self.text = text
        self.padding = 5

        self.bg_color = Colors.WHITE   # （边框、轨道）
        self.text_color = Colors.BLACK  # 黑色文字

        self.text_bg_color = -1   # 对于文字来说，可以透出背景的颜色。

        self.char_width = M5.Display.textWidth(text)
        
        self.char_height = M5.Display.fontHeight()

        self.is_pressed = False
        self._click_callback = None
        self._long_press_callback = None
        self._long_press_triggered = False
        
        self.is_first = True
        # M5.Display.fillCircle(100,500,100,0xFFFFFF)x,y,r,color xy坐标是圆心,r是半径,color是颜色
    def set_text(self, new_text: str):
        if self.text != new_text:
            self.text = new_text
            self.mark_dirty()


    def on_show(self):
        self.is_first = True
        super().on_show()
      

    # def resume(self):
    #     self.if_first = True
    #     super().resume()
    #     """恢复元素（恢复自动刷新）"""
    #     # if self._state == UIElement.STATE_PAUSED:
    #     #     print(f"[UIElement] {self._name}: resume")
    #     #     self._state = UIElement.STATE_ACTIVE
    #     #     self._dirty = True # 恢复时可能需要重绘


    def draw(self):

      print(f"[TextView] 更新: '{self.text}' at ({self.x}, {self.y})")
      M5.Display.setEpdMode(4)

      if self.is_pressed:
          color = Colors.WHITE
      else:
          color = Colors.BLACK
      M5.Display.drawRoundRect(self.x,self.y,self.w,self.h,self.h//2,color)
      M5.Display.setEpdMode(2)
      
      if not self.is_first:
        
        return
      M5.Display.fillRoundRect(self.x+self.padding,self.y+self.padding,self.w-self.padding*2,self.h-self.padding*2,(self.h-self.padding*2)//2,self.bg_color)
      M5.Display.setTextColor(self.text_color, self.text_bg_color)
      M5.Display.drawCenterString(self.text, self.x + (self.w // 2), self.y + (self.h-self.char_height )// 2)

      self.is_first = False

        


    def handle_touch(self,tx,ty,detail):
        # 解包触摸详情
        (dx, dy, dist_x, dist_y,
         is_pressed, was_pressed, was_clicked,
         is_released, was_released, is_holding, was_hold) = detail

        # print(detail)
        if was_pressed:
            print(f"[Button] {self.text}: 按下")
            self.is_pressed = True
            self._long_press_triggered = False
            self.mark_dirty()

        elif was_released:
            if self.is_pressed and was_clicked:
                if self._click_callback:
                    print(f"[Button] {self.text}: 点击回调")
                    self._click_callback(self)
            print(f"[Button] {self.text}: 释放")

            self.is_pressed = False
            self._long_press_triggered = False
            self.mark_dirty()

        elif is_holding and not self._long_press_triggered:
            print(f"[Button] {self.text}: 长按触发")
            self._long_press_triggered = True
            if self._long_press_callback:
                self._long_press_callback(True)
            

        elif was_hold and self._long_press_triggered:
            print(f"[Button] {self.text}: 长按结束")
            self._long_press_triggered = False

            if self._long_press_callback:
                self._long_press_callback(False)   
            self.mark_dirty()

    def on_hide(self):
        super().on_hide()
        self.is_first = True