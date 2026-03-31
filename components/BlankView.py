import M5  # type: ignore


from Color import Colors # 导入颜色常量
from UIElement import UIElement

class BlankView(UIElement):
    def __init__(self, x: int=0, y: int=0,w:int=540,h:int=960,radius = 0,border = False):
        super().__init__(x, y, w,h) # 简单估算宽度

        self.bg_color = Colors.WHITE
        self._click_callback = None
        self.radius = radius
        self.border = border


    def on_show(self):
      super().on_show()
      



    # def _draw_border(self):
        # M5.Display.draw
    def draw(self):
      
        print(f"[BlankView] 更新: at ({self.x}, {self.y})")
        if self.radius:
            M5.Display.fillRoundRect(self.x,self.y,self.w,self.h,self.radius,self.bg_color)
            if self.border:
                M5.Display.drawRoundRect(self.x,self.y,self.w,self.h,self.radius,0)
        else:
            M5.Display.fillRect(self.x,self.y,self.w,self.h, self.bg_color)#仅仅是在画面覆盖白色
            if self.border:
                M5.Display.drawRect(self.x,self.y,self.w,self.h,0)
        # if self.border:
            # M5.

        


    def handle_touch(self,tx,ty,detail):
        # 解包触摸详情
        (dx, dy, dist_x, dist_y,
         is_pressed, was_pressed, was_clicked,
         is_released, was_released, is_holding, was_hold) = detail

        # print(detail)
        if was_pressed:
            print(f"[BlankView]: 按下")
            self.is_pressed = True
            self._long_press_triggered = False
            self.mark_dirty()

        elif was_released:
            if self.is_pressed and was_clicked:
                if self._click_callback:
                    print(f"[BlankView]: 点击回调")
                    self._click_callback(self)
            print(f"[BlankView]: 释放")

            self.is_pressed = False
            self._long_press_triggered = False
            self.mark_dirty()

    def on_hide(self):
        super().on_hide()