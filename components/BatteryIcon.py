# BatteryIcon.py
"""
BatteryIcon 组件 - 电池状态图标
"""
import time
import M5  # type: ignore
from Color import Colors
from UIElement import UIElement


class BatteryIcon(UIElement):
    """电池状态图标组件"""

    def __init__(self, x: int = 440, y: int = 0):
        """
        初始化电池图标

        Args:
            x: 左上角X坐标
            y: 左上角Y坐标
        """
        self.padding = 4
        self.x = x
        self.y = y
        self.w = 60
        self.h = 30

        super().__init__(x, y, self.w, self.h)

        # 回调
        self._click_callback = None

        # 电量状态
        self._last_battery_level = -1
        self.battery_level = 50
        self.get_battery_level_countdown = 60  # 60秒获取一次电量
        self.is_charging = False
        self.is_increased = False
        # self.is_auto_refresh = True
        self._last_update_time = time.time()
        self.draw_lighting = None

        # 获取初始电量状态
        self.get_battery_status()

        print(f"[BatteryIcon] 创建电池图标 at ({x}, {y})")

    # ==================== 生命周期 ====================

    def on_show(self):
        """显示电池图标"""
        self.full_draw()

        super().on_show()


    def on_hide(self):
        """隐藏电池图标"""
        super().on_hide()

    def on_delete(self):
        """销毁电池图标"""
        print(f"[BatteryIcon] 销毁电池图标")
        # 清理资源（如果需要）
        pass

    def _on_pause(self):
        """暂停时调用"""
        print("[BatteryIcon] 暂停自动刷新")

    def _on_resume(self):
        """恢复时调用"""
        print("[BatteryIcon] 恢复自动刷新")
        self._last_update_time = time.time()  # 重置计时器

    # ==================== 回调设置 ====================

    def set_click_callback(self, cb):
        """设置点击回调"""
        self._click_callback = cb
        return self

    # ==================== 电量相关 ====================

    def set_battery_level(self, level: int):
        """设置电量"""
        # 限制范围
        level = max(0, min(100, level))
        if level == self._last_battery_level :
            
            return
        self.is_increased = level > self._last_battery_level
        # 更新电量
        self.battery_level = level
        self._last_battery_level = level
        self._dirty = True

    def get_battery_status(self):
        """自动获取电量（从M5.Power）"""
        try:
            level = M5.Power.getBatteryLevel()
            self.set_battery_level(level)
            self.is_charging = M5.Power.isCharging()
            print(f"power level :{level},is charging :{self.is_charging}")
        except Exception as e:
            print(f"[BatteryIcon] 自动获取电量失败：{e}")

    # ==================== 绘制方法 ====================

    def _draw_value_area(self):
        """绘制电量区域"""
        M5.Display.fillRoundRect(
            self.x + 6, self.y + 6, 42, 18, 2, Colors.WHITE)  # 容量区

    def _draw_battery_level(self):
        """根据电量计算电量条宽度"""
        if not self.is_increased:
          self._draw_value_area()
        effective_width = int(40 * self.battery_level / 100)
        M5.Display.fillRoundRect(
            self.x + 7, self.y + 7, effective_width, 16, 1, Colors.BLACK)  # 电量

    def _draw(self):
        """绘制电池形状"""
        M5.Display.fillRoundRect(
            self.x + 47, self.y + 9, 9, 12, 3, Colors.BLACK)  # 电池帽子
        M5.Display.fillRoundRect(
            self.x + self.padding, self.y + self.padding, 46, 22, 3, Colors.BLACK)  # 电池体

    def _draw_charging_icon(self):
        """绘制充电闪电图标（当 is_charging=True 时显示）"""
        # 检查状态是否变化，如果没有变化则跳过绘制
        if hasattr(self, 'draw_lighting') and self.draw_lighting == self.is_charging:
            return  # 状态未变化，直接返回
        
        # 更新状态跟踪
        self.draw_lighting = self.is_charging
        lighting_color = Colors.BLACK if self.is_charging else Colors.WHITE

        icon_x = self.x + self.w + 5  # 电池右侧5像素处
        center_y = self.y + self.h // 2  # 垂直居中

        # 闪电形状由两个三角形组成
        M5.Display.fillTriangle(icon_x + 8, center_y - 10,
                                icon_x + 6, center_y,
                                icon_x, center_y,
                                lighting_color)

        M5.Display.fillTriangle(icon_x + 8, center_y,
                                icon_x, center_y + 10,
                                icon_x + 2, center_y,
                                lighting_color)

    def full_draw(self):
        """绘制电池图标"""
        M5.Display.setEpdMode(4)

        self._draw()
        self._draw_value_area()
        self._draw_battery_level()
        self._draw_charging_icon()
        M5.Display.setEpdMode(2)

    # ==================== 更新方法 ====================

    def update(self):
        """更新电池图标"""
        # 使用基类的状态检查
        if not self.is_active:

            return

        # 自动刷新
        # if self.is_auto_refresh:
        now = time.time()

        if (now - self._last_update_time) >= self.get_battery_level_countdown:
            
            self._last_update_time = time.time()
            self.get_battery_status()

        else:
            return  # 未到刷新时间

        # 绘制,局部绘制
        if self._dirty:
            if self.battery_level != self._last_battery_level :
                pass
                # return
                self._draw_battery_level()
            self._draw_charging_icon()
            self._dirty = False

    # ==================== 触摸事件 ====================

    def handle_touch(self, tx: int, ty: int, detail):
        """处理触摸事件"""
        # 使用基类的状态检查
        if not self.is_active:
            return

        (dx, dy, dist_x, dist_y,
         is_pressed, was_pressed, was_clicked,
         is_released, was_released, is_holding, was_hold) = detail

        # 按下
        if was_pressed:
            print(f"[BatteryIcon]: 按下")
            if self._click_callback:
                print(f"[BatteryIcon]: 点击回调")
                self._click_callback()
