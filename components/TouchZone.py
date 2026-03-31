
from Button import Button


class TouchZone(Button):
    def __init__(self, x=180, y=320, w=180, h=320, text="TouchZone"):
        super().__init__(x=x, y=y, w=w, h=h, text=text)

    def draw(self):
        pass  # 不绘制
    
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