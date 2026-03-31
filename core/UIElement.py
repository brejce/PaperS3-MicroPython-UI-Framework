"""
UIElement 基类 - 所有UI元素的父类
提供：
- 位置和尺寸管理
- 触摸事件处理
- 生命周期管理（显示/暂停/恢复/删除）
- 脏标记优化
"""
import M5  # type: ignore

class UIElement:
    """
    UI元素基类
    生命周期状态:
    - CREATED: 刚创建，尚未显示
    - ACTIVE: 活跃状态，正常工作和刷新
    - PAUSED: 暂停状态，不刷新
    - DELETED: 已删除，资源已释放
    """

    # 状态常量
    STATE_CREATED = "created"
    STATE_ACTIVE = "active"
    STATE_PAUSED = "paused"
    STATE_DELETED = "deleted"

    def __init__(self, x: int, y: int, w: int, h: int):
        """
        初始化UI元素
        Args:
            x: 左上角X坐标
            y: 左上角Y坐标
            w: 宽度
            h: 高度
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._dirty = True  # 脏标记，需要重绘
        # 生命周期状态
        self._state = UIElement.STATE_CREATED
        self._framework = None  # Framework引用
        # 调试名称
        self._name = self.__class__.__name__
        print(f"[UIElement] 创建: {self._name} at ({x}, {y}, {w}, {h})")

    # ==================== 状态管理 ====================
    @property
    def state(self) -> str:
        """获取当前状态"""
        return self._state

    @property
    def is_active(self) -> bool:
        """是否处于活跃状态"""
        return self._state == UIElement.STATE_ACTIVE

    @property
    def is_paused(self) -> bool:
        """是否处于暂停状态"""
        return self._state == UIElement.STATE_PAUSED

    @property
    def is_deleted(self) -> bool:
        """是否已删除"""
        return self._state == UIElement.STATE_DELETED

    @property
    def is_visible(self) -> bool:
        """
        是否可见（活跃或暂停状态都可见）
        用于决定是否在 App.update 中调用其 update 方法。
        """
        return self._state in (UIElement.STATE_ACTIVE, UIElement.STATE_PAUSED)

    # ==================== 生命周期方法 ====================
    def on_create(self):
        """
        UI元素创建时调用（构造函数之后）
        子类可重写此方法进行初始化。
        """
        print(f"[UIElement] {self._name}: on_create")
        # 可在此处进行非绘制相关的初始化

    def on_show(self):
        """
        当元素被显示时调用（进入活跃状态）
        子类可重写此方法，例如进行首次绘制。
        """
        print(f"[UIElement] {self._name}: on_show")
        self._state = UIElement.STATE_ACTIVE
        self._dirty = True # 显示时通常需要重绘

    def on_hide(self):
        """
        当元素被隐藏时调用（进入暂停状态）
        子类可重写此方法，例如暂停动画。
        """
        print(f"[UIElement] {self._name}: on_hide")
        self._state = UIElement.STATE_PAUSED
        # 注意：不在此处清除 dirty 标记，保留状态以便恢复时重绘

    def on_delete(self):
        """
        当元素被销毁时调用（释放资源）
        子类必须重写此方法清理资源（如 canvas, Label 等）。
        """
        print(f"[UIElement] {self._name}: on_delete")
        self._state = UIElement.STATE_DELETED
        # 子类应在此处释放持有的资源
        # e.g., if hasattr(self, 'canvas'): del self.canvas

    def pause(self):
        """暂停元素（暂停自动刷新）"""
        if self._state == UIElement.STATE_ACTIVE:
            print(f"[UIElement] {self._name}: pause")
            self._state = UIElement.STATE_PAUSED
            # 暂停相关操作可在此添加

    def resume(self):
        """恢复元素（恢复自动刷新）"""
        if self._state == UIElement.STATE_PAUSED:
            print(f"[UIElement] {self._name}: resume")
            self._state = UIElement.STATE_ACTIVE
            self._dirty = True # 恢复时可能需要重绘

    # ==================== 触摸事件处理 ====================
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

    def handle_touch(self, tx: int, ty: int, detail):
        """
        处理触摸事件（由Framework或父元素调用）
        Args:
            tx: 触摸点X坐标
            ty: 触摸点Y坐标
            detail: 触摸详情元组
        子类可重写此方法
        """
        pass

    # ==================== 更新与绘制 ====================
    def update(self):
        """
        由父App或Framework主循环调用：检查是否需要重绘或执行周期性任务
        子类可重写此方法实现周期性任务。
        """
        # 只有在活跃状态才检查脏标记并绘制
        if self._state == UIElement.STATE_ACTIVE and self._dirty:
            self.draw()
            self._dirty = False # 绘制完成后清除脏标记

    def _check_dirty(self) -> bool:
        """
        检查并处理脏标记
        由App或Framework调用，用于判断是否需要刷新整个UI层。
        Returns:
            bool: 如果元素脏了则返回True
        """
        # 只有在活跃状态下才认为脏标记有效
        # 如果是暂停状态，即使脏了，也不代表需要立即刷新
        # 但为了状态一致性，这里仍返回当前脏值，但不清除
        # 让 update 方法在 ACTIVE 时处理并清除
        # return self._dirty if self.is_active else False # 方案1
        # 方案2：在 update 中处理，这里只返回
        return self._dirty

    def mark_dirty(self):
        """标记元素需要重绘"""
        self._dirty = True

    def draw(self):
        """
        绘制元素
        子类必须实现此方法。
        """
        raise NotImplementedError(f"{self.__class__.__name__}.draw() method must be implemented")

    # ==================== Framework关联 ====================
    def set_framework(self, framework):
        """
        设置Framework引用
        Args:
            framework: Framework实例
        """
        self._framework = framework

    def get_framework(self):
        """
        获取Framework引用
        Returns:
            Framework实例或None
        """
        return self._framework

    # ==================== 调试 ====================
    def __str__(self) -> str:
        """返回UIElement的字符串表示，用于调试和日志"""
        return (f"{self._name}(x={self.x}, y={self.y}, "
                f"w={self.w}, h={self.h}, state={self._state})")

    def __repr__(self) -> str:
        return self.__str__()
