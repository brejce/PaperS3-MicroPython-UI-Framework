"""
AppBase - 应用程序基类
提供：
- 应用程序生命周期管理
- UI元素集合管理
- 触摸事件分发
- 与Framework的关联
>>> M5.Display.EPDMode.EPD_FAST
3
>>> M5.Display.EPDMode.EPD_FASTEST
4
>>> M5.Display.EPDMode.EPD_QUALITY
1
>>> M5.Display.EPDMode.EPD_TEXT
2
"""
# from Framework import Framework
import M5 # type: ignore
class AppBase:
    """
    应用程序基类
    生命周期状态:
    - CREATED: 刚创建，尚未显示
    - ACTIVE: 活跃状态，UI可见且可交互
    - PAUSED: 暂停状态，UI可见但暂停刷新
    - DELETED: 已销毁，资源已释放
    """

    # 状态常量
    STATE_CREATED = "created"
    STATE_ACTIVE = "active"
    STATE_PAUSED = "paused"
    STATE_DELETED = "deleted"

    def __init__(self, name: str = "UnnamedApp"):
        """
        初始化App
        Args:
            name: App名称标识
        """
        self.name = name
        self.ui_elements = []  # 子UI元素列表

        self._dirty = False  # 脏标记
        # 生命周期状态
        self._state = AppBase.STATE_CREATED
        self._framework = None  # type: ignore # Framework引用
        # 调试
        print(f"[AppBase] 创建App: {name}")
        # self.on_create()
        # print(f"[AppBase] 自动实例化所有的组件: {name}")

    # ==================== 状态管理 ====================
    @property
    def state(self) -> str:
        """获取当前状态"""
        return self._state

    @property
    def is_active(self) -> bool:
        """是否处于活跃状态"""
        return self._state == AppBase.STATE_ACTIVE

    @property
    def is_paused(self) -> bool:
        """是否处于暂停状态"""
        return self._state == AppBase.STATE_PAUSED

    @property
    def is_deleted(self) -> bool:
        """是否已删除"""
        return self._state == AppBase.STATE_DELETED

    @property
    def is_visible(self) -> bool:
        """
        是否可见（活跃或暂停状态都可见）
        用于 Framework 判断是否调用 App.update。
        """
        return self._state in (AppBase.STATE_ACTIVE, AppBase.STATE_PAUSED)

    # ==================== 生命周期方法 ====================
    def on_create(self):
        """
        App创建时调用（构造函数之后）
        子类可重写此方法进行初始化。
        """
        print(f"[AppBase] {self.name}: on_create")
        # 可在此处进行非UI相关的初始化
        # 注意：此时 App 还未被 Framework 管理，也没有Framework引用

    def on_show(self):
        """
        当App被激活显示时调用
        子类必须重写此方法创建UI元素。
        """
        # M5.Display.fillRect(0, 0, 540, 960, Colors.WHITE)#仅仅是在画面覆盖白色

        # M5.Display.clear(self.bg_color)#带有全屏刷新的情况，所以如果需要全屏刷新可以先clear
        print(f"[AppBase] {self.name}: on_show")
        was_active = self._state == AppBase.STATE_ACTIVE
        self._state = AppBase.STATE_ACTIVE
        # 如果之前不是活跃的，标记为脏
        if not was_active:
            self._dirty = True
        # 调用所有子元素的 on_show
        for elem in self.ui_elements:
            if hasattr(elem, 'on_show'):
                elem.on_show()

    def on_hide(self):
        """
        当App被切出时调用（进入暂停状态）
        子类可重写此方法暂停UI元素。
        """
        print(f"[AppBase] {self.name}: on_hide")
        was_active = self._state == AppBase.STATE_ACTIVE
        self._state = AppBase.STATE_PAUSED
        # 如果之前是活跃的，标记为脏
        if was_active:
            self._dirty = True
        # 调用所有子元素的 on_hide
        for elem in self.ui_elements:
            if hasattr(elem, 'on_hide'):
                elem.on_hide()

    def on_delete(self):
        """
        当App被销毁时调用（释放资源）
        子类必须重写此方法清理资源。
        """
        print(f"[AppBase] {self.name}: on_delete")
        self._state = AppBase.STATE_DELETED
        # 删除所有子元素
        self._cleanup_elements()

    def pause(self):
        """暂停App（暂停所有子元素的自动刷新）"""
        if self._state == AppBase.STATE_ACTIVE:
            print(f"[AppBase] {self.name}: pause")
            self._state = AppBase.STATE_PAUSED
            # 暂停所有子元素
            for elem in self.ui_elements:
                if hasattr(elem, 'pause'):
                    elem.pause()

    def resume(self):
        """恢复App（恢复所有子元素的自动刷新）"""
        if self._state == AppBase.STATE_PAUSED:
            print(f"[AppBase] {self.name}: resume")
            self._state = AppBase.STATE_ACTIVE
            self._dirty = True # 恢复时可能需要重绘
            # 恢复所有子元素
            for elem in self.ui_elements:
                if hasattr(elem, 'resume'):
                    elem.resume()

    def delete(self):
        """删除App（销毁所有资源）"""
        if self._state != AppBase.STATE_DELETED:
            print(f"[AppBase] {self.name}: delete")
            self.on_delete()
            self._state = AppBase.STATE_DELETED

    # ==================== UI元素管理 ====================
    def add_element(self, element):
        """
        添加UI元素
        Args:
            element: UIElement实例
        Returns:
            element: 返回元素以便链式调用
        """
        if element not in self.ui_elements:
            # 设置Framework引用
            if self._framework:
                element.set_framework(self._framework)
            self.ui_elements.append(element)
            print(f"[AppBase] {self.name}: 添加元素 {element}")
        return element

    def remove_element(self, element):
        """
        移除UI元素
        Args:
            element: UIElement实例
        """
        if element in self.ui_elements:
            element.delete()  # 先删除元素
            self.ui_elements.remove(element)
            print(f"[AppBase] {self.name}: 移除元素 {element}")

    def clear_elements(self):
        """清除所有UI元素"""
        self._cleanup_elements()

    def _cleanup_elements(self):
        """清理所有子元素（内部方法）"""
        # 倒序删除，避免列表修改问题
        for elem in list(self.ui_elements):
            try:
                if hasattr(elem, 'delete'):
                    elem.delete()
            except Exception as e:
                print(f"[AppBase] 清理元素失败: {e}")
        self.ui_elements.clear()

    def get_element_by_type(self, element_type):
        """
        根据类型查找元素
        Args:
            element_type: 元素类型
        Returns:
            第一个匹配的元素，或None
        """
        for elem in self.ui_elements:
            if isinstance(elem, element_type):
                return elem
        return None

    def get_elements_by_type(self, element_type):
        """
        根据类型查找所有元素
        Args:
            element_type: 元素类型
        Returns:
            匹配的元素列表
        """
        return [elem for elem in self.ui_elements if isinstance(elem, element_type)]

    def dump_elements(self):
        """打印所有元素信息（调试用）"""
        print(f"[AppBase] {self.name} 元素列表:")
        for i, elem in enumerate(self.ui_elements):
            print(f"  [{i}] {elem}")

    # ==================== 更新与绘制 ====================
    def _check_dirty(self) -> bool:
        """
        检查所有UI元素的状态，更新App自身的脏标记
        由Framework调用，用于判断是否需要刷新整个App。
        Returns:
            bool: 如果App或其任何可见子元素脏了则返回True
        """
        self._dirty = False
        for elem in self.ui_elements:
            # 只检查可见元素的脏状态
            if elem.is_visible and elem._check_dirty():
                self._dirty = True
                break # 任一元素脏，App就脏了
        return self._dirty

    def update(self):
        """
        由主循环调用：更新所有子元素
        策略：
        1. 只更新可见状态的元素 (is_visible)
        2. 元素自己负责检查脏标记并在 update 中调用 draw
        """
        # 只有 App 本身处于活跃状态才更新其子元素
        if self.is_active:
            #在此使用startWrite包裹可以让元素可以一起更新到屏幕上。
            M5.Display.startWrite()

            for elem in self.ui_elements:
                # 只更新可见状态的元素
                if elem.is_visible:
                    try:
                        elem.update()

                    except Exception as e:
                        print(f"[AppBase] 更新元素失败: {e}")
            M5.Display.endWrite()

    def mark_dirty(self):
        """标记整个App需要刷新"""
        self._dirty = True
        # 同时标记所有子元素为脏
        for elem in self.ui_elements:
            
            elem.mark_dirty()

    # ==================== Framework关联 ====================
    def set_framework(self, framework):
        """
        设置Framework引用
        Args:
            framework: Framework实例
        """
        self._framework = framework
        # 同时设置所有子元素的Framework引用
        for elem in self.ui_elements:
            elem.set_framework(framework)

    def get_framework(self):
        """
        获取Framework引用
        Returns:
            Framework实例或None
        """
        return self._framework

    # ==================== 调试 ====================
    def __str__(self) -> str:
        return (f"App({self.name}, state={self._state}, "
                f"elements={len(self.ui_elements)})")

    def __repr__(self) -> str:
        return self.__str__()
    
    def _handle_touch_recursive(self, tx: int, ty: int, detail):
        """
        递归处理触摸事件，分发给子UI元素
        """
        # 逆序遍历，优先处理后添加的元素（通常层级更高）
        for elem in reversed(self.ui_elements):
            if elem.is_visible and elem.is_touched(tx, ty):
                elem.handle_touch(tx, ty, detail)
                # 如果元素处理了触摸（例如按钮按下），可能需要阻止事件向下传递
                # 这里假设一个元素处理后就不再传递，可根据需要调整
                break
            # 如果元素本身不处理，但有子元素，可以继续递归
            # 但标准 UIElement 没有子元素概念，所以这里只处理一层
        # 如果没有UI元素处理，则App可以处理通用触摸逻辑（如果需要）