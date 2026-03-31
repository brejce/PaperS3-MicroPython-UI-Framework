#IconButton.py


import M5  # type: ignore

from Button import Button

class IconButton(Button):

  def __init__(self, x: int=0, y: int=0,w:int=64,h:int=64,path:str = "/flash/res/img/uiflow.jpg"):

    super().__init__(x=x, y=y,w=w,h=h) 

    self.path = path
    self.is_first = True

  def on_show(self):
        self.is_first = True
        super().on_show()
        
  def draw(self):
    if not self.is_first:
        return
    if self.path.endswith(".bmp"):
        print("bmp 图片")
        M5.Display.drawBmp(self.path,self.x,self.y)
    elif self.path.endswith(".jpg"):
        print("jpg 图片")
        M5.Display.drawJpg(self.path,self.x,self.y)
    elif self.path.endswith(".png"):
        print("PNG 图片")
        M5.Display.drawPng(self.path,self.x,self.y)
    self.is_first = False

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
            self.x <= tx <= self.x + self.w and
            self.y <= ty <= self.y + self.h
        )
        