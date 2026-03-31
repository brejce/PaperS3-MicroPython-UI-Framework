"""
Framework - 应用程序框架主控制器
提供：
- 应用程序注册和切换
- 触摸事件分发
- 主循环更新
- 退出管理（sys.exit()）
"""
import M5  # type: ignore
import sys
# 提前导入以使用状态常量
from AppBase import AppBase

class Framework:
    """
    应用框架主控制器
    职责：
    - 管理所有注册的App
    - 控制当前活动App
    - 分发触摸事件
    - 主循环更新
    - 程序退出管理
    生命周期：
    - Framework是最终基座，退出时调用sys.exit()
    """

    # 状态常量
    STATE_STOPPED = "stopped"
    STATE_RUNNING = "running"

    def __init__(self):
        """初始化Framework"""
        self.apps = []  # 注册的应用列表
        self.current_app = None  # 当前活动App
        self._dirty = False  # 全局脏标记
        self._state = Framework.STATE_STOPPED  # 运行状态
        # 退出相关
        self._exit_requested = False
        self._exit_code = 0
        print("[Framework] 初始化完成")

    # ==================== 状态管理 ====================
    @property
    def state(self) -> str:
        """获取当前状态"""
        return self._state

    @property
    def is_running(self) -> bool:
        """是否正在运行"""
        return self._state == Framework.STATE_RUNNING

    # ==================== App管理 ====================
    def add_app(self, app:AppBase):
        """
        注册应用程序
        Args:
            app: AppBase实例
        Returns:
            app: 返回App以便链式调用
        """
        if app not in self.apps:
            app.set_framework(self) # 设置 Framework 引用
            app.on_create()
            self.apps.append(app)
            print(f"[Framework] 注册App: {app.name}")
        return app

    def get_app_by_name(self, name: str):
        """
        根据名称查找App
        Args:
            name: App名称
        Returns:
            App实例或None
        """
        for app in self.apps:
            if app.name == name:
                return app
        return None

    def switch_to(self, app,need_clear = False):
        """
        切换到指定App
        Args:
            app: AppBase实例
            need_clear:如果需要清理屏幕
        """
        if app not in self.apps:
            print(f"[Framework] 错误: App '{app.name}' 未注册")
            return

        if self.current_app == app:
            print(f"[Framework] App '{app.name}' 已经是当前App")
            return

        print(f"[Framework] 切换App: {self.current_app.name if self.current_app else 'None'} -> {app.name}")

        # 隐藏当前App（如果存在）
        if self.current_app:
            self.current_app.on_hide() # 调用 on_hide，内部会暂停子元素
        if need_clear:
            M5.Display.clear()
        # 显示新App
        self.current_app = app
        self.current_app.on_show() # 调用 on_show，内部会显示子元素

    def back_to(self, app_name: str):
        """
        返回指定名称的App
        Args:
            app_name: App名称
        """
        app = self.get_app_by_name(app_name)
        if app:
            self.switch_to(app)
        else:
            print(f"[Framework] 错误: 未找到App '{app_name}'")

    # ==================== 生命周期方法 ====================
    def start(self):
        """启动Framework"""
        if self._state == Framework.STATE_RUNNING:
            print("[Framework] 已经在运行中")
            return
        print("[Framework] 启动")
        self._state = Framework.STATE_RUNNING
        self._exit_requested = False

    def stop(self, exit_code: int = 0):
        """
        停止Framework（会退出整个程序）
        Args:
            exit_code: 退出码
        """
        print(f"[Framework] 停止Framework (退出码: {exit_code})")
        self._exit_requested = True

    def exit(self, exit_code: int = 0):
        """
        退出程序（相当于sys.exit()）
        这是Framework的最终退出方式：
        1. 销毁当前App
        2. 销毁所有App
        3. 调用sys.exit()
        Args:
            exit_code: 退出码
        """
        print(f"[Framework] 退出程序 (退出码: {exit_code})")
        # 销毁所有App
        self._cleanup_all_apps()
        # 设置状态
        self._state = Framework.STATE_STOPPED
        self.current_app = None
        # 调用sys.exit()退出程序
        # sys.exit(exit_code)

        M5.Display.setTextSize(1)
        M5.Display.endWrite()
        M5.Display.unloadFont()
        sys.exit(exit_code)

    def _cleanup_all_apps(self):
        """清理所有App（内部方法）"""
        print("[Framework] 清理所有App")
        for app in list(self.apps): # 使用副本列表避免迭代时修改
            try:
                if app.state != AppBase.STATE_DELETED:
                    app.delete()
            except Exception as e:
                print(f"[Framework] 清理App失败: {e}")
        self.apps.clear()

    # ==================== 事件处理 ====================

    
    # def handle_touch(self):
    #     if M5.Touch.getCount() == 0:
    #         return
    #     try:
    #         x, y = M5.Touch.getX(), M5.Touch.getY()
    #         detail = M5.Touch.getDetail(0)
    #         if self.current_app:
    #             self.current_app._handle_touch_recursive(x, y, detail)
    #     except (OSError, IndexError):
    #         # 触摸设备可能未就绪
    #         pass
    #     except Exception as e:
    #         print(f"[Framework] 触摸处理错误: {e}\n可能是子元素错误")
    def handle_touch(self):
        """处理触摸事件（由主循环调用）"""
        if not self.current_app or not self.current_app.is_active:
            return # 只有当前活跃App才处理触摸

        if self._exit_requested:
            return

        try:
            # 检查触摸数量
            touch_count = M5.Touch.getCount()
            if touch_count == 0:
                return

            # 获取第一个触摸点
            x = M5.Touch.getX()
            y = M5.Touch.getY()
            detail = M5.Touch.getDetail(0)

            # 分发给当前App
            if self.current_app:
                self.current_app._handle_touch_recursive(x, y, detail)

        except (OSError, IndexError):
            # 触摸设备可能未就绪
            pass
        except Exception as e:
            print(f"[Framework] 触摸处理错误: {e}\n可能是子元素错误")

    def update(self):
        """
        主循环更新函数
        """
        # 检查退出请求
        if self._exit_requested:
            self.exit(self._exit_code)
            return # 理论上 exit 会终止程序，但这行以防万一

        # 更新当前App（如果它处于活跃状态）
        if self.current_app:
            # 检查App状态 - 只有活跃App才更新
            if self.current_app.is_active:
                try:
                    self.current_app.update()
                except Exception as e:
                    print(f"[Framework] 更新App错误: {e}")

            # 检查App的脏标记，决定是否需要刷新屏幕
            # 注意：这里的 _check_dirty 会影响 Framework 的 _dirty
            # 如果 App 或其子元素脏了，Framework 也应该认为整体脏了
            # 但 Framework 本身通常不直接绘制，而是由 App 负责
            # 因此 Framework 的 _dirty 更多可能是为了其他目的（如全局刷新判断）
            # 在墨水屏场景下，App 管理自己的 UIElement 脏标记和绘制通常已足够
            # Framework 可以简单地信任 App 的更新即可
            # self._dirty = self.current_app._check_dirty() # 如果需要全局判断，可启用

    # ==================== 调试 ====================
    def dump_apps(self):
        """打印所有App信息（调试用）"""
        print("[Framework] App列表:")
        for i, app in enumerate(self.apps):
            print(f"  [{i}] {app}")


