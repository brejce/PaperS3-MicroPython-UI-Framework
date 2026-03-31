# M5Stack PaperS3 MicroPython UI Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: M5Stack PaperS3](https://img.shields.io/badge/Platform-M5Stack%20PaperS3-blue)](https://docs.m5stack.com/en/core/papers3)
[![Language: MicroPython](https://img.shields.io/badge/Language-MicroPython-green)](https://micropython.org/)

为 M5Stack PaperS3 (4.7 英寸电子墨水屏) 设计的 MicroPython UI 框架，提供完整的应用生命周期管理、UI 组件库和墨水屏刷新优化。

## 特性

- 应用生命周期管理 - 完整的 App 创建、显示、隐藏、删除状态管理
- 组件化架构 - 基于 UIElement 基类的可扩展组件系统
- 墨水屏优化 - 脏标记 (Dirty Marking) 机制减少不必要的刷新
- 触摸事件处理 - 支持点击、长按
- 常用组件库 - Button, TextView, ListView, BatteryIcon 等
- 网格坐标系统 - 精确的字符布局计算

## 项目结构

    M5PaperS3App/
    ├── core/ # 核心框架
    │ ├── AppBase.py # 应用程序基类
    │ ├── Framework.py # 框架主控制器
    │ ├── UIElement.py # UI 元素基类
    │ └── Color.py # 颜色定义
    ├── components/ # 组件库
    │ ├── Button.py # 按钮组件
    │ ├── TextView.py # 文本显示组件
    │ ├── ListView.py # 列表视图组件
    │ ├── BatteryIcon.py # 电池图标组件
    │ ├── GridSystem.py # 网格坐标系统
    │ ├── IconManager.py # 图标资源管理
    │ ├── TouchZone.py # 触摸区域检测
    │ └── ...
    ├── simaple.py # 功能测试入口，也是整个框架的入口
    ├── README.md # 项目说明
    ├── LICENSE # 开源许可证
    └── .gitignore # Git 忽略文件

## 环境要求

- 设备：M5Stack PaperS3
- 固件：M5Stack 官方固件
- 屏幕：4.7 英寸 E-Ink (540 x 960)

## 快速开始

### 1. 烧录固件

使用 M5Burner 或 esptool 烧录 官方固件。

### 2. 上传文件
    将core和components里面的内容放到flash/libs里面即可，至此框架搭建好了。
    然后将apps/simaple.py放到flash/apps里面，重启，在applist里面点击该程序即可。
    或者将apps/simaple.py的文件内容粘贴到，UiFlow2里面。点击运行即可。

    未来可能会发布调试好的固件。


## 核心架构


### Framework (core/Framework.py)
| **方法**          | **说明**           |
| ----------------- | ------------------ |
| register_app(app) | 注册应用           |
| switch_to(app)    | 切换到指定应用     |
| back_to(app_name) | 返回指定名称的应用 |
| run()             | 运行主循环         |
| start()           | 启动框架           |
| stop(exit_code)   | 停止框架           |

### AppBase (core/AppBase.py)
| **方法**    | **说明**        |
| ----------- | --------------- |
| on_create() | 创建时调用      |
| on_show()   | 显示/激活时调用 |
| on_hide()   | 隐藏/切出时调用 |
| on_delete() | 删除时调用      |
| update()    | 主循环中调用    |

### UIElement (core/UIElement.py)

| **属性/方法**                | **说明**                                                                    |
| ---------------------------- | --------------------------------------------------------------------------- |
| x, y, w, h                   | 位置与尺寸                                                                  |
| draw                         | 绘制元素，子类必须实现此方法。，不然是不会有显示内容的，参考button/TextView |
| is_touched(tx, ty)           | 触摸检测                                                                    |
| handle_touch(tx, ty, detail) | 触摸处理                                                                    |
| mark_dirty()                 | 标记需要重绘                                                                |
| on_show/on_hide/on_delete    | 生命周期钩子                                                                |
## 组件库
| 组件          | 说明                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------- |
| Button        | 支持点击、长按回调的按钮                                                                          |
| TextView      | 文本显示，支持颜色、背景                                                                          |
| ListView      | 列表视图，支持滚动和视口                                                                          |
| BatteryIcon   | 电池状态图标，自动获取电量                                                                        |
| GridSystem    | 网格坐标计算，用于布局                                                                            |
| TouchZone     | 触摸区域检测工具                                                                                  |
| SDCardManager | SD 卡文件管理辅助，参考simple，是使用sd卡的重要库，调用sd.mount()后，即可将sd卡挂载到"/sd/"目录下 |


## 墨水屏刷新优化
    针对 E-Ink 屏幕的脏标记机制：
    显示接口：使用 M5.Display 接口进行绘图
    资源清理：在 on_delete 中及时清理资源
    刷新频率：避免高频强制全屏刷新，利用脏标记机制
    内存管理：墨水屏设备内存有限，注意 gc.collect()
    固件依赖：官方固件

## 许可证
本项目遵循 MIT 许可证 - 查看 LICENSE 文件了解详情
## 相关链接

[M5Stack PaperS3 官方文档](https://[PaperS3](https://docs.m5stack.com/zh_CN/core/PaperS3))

[M5Burner](https://docs.m5stack.com/zh_CN/uiflow/m5burner/intro)

[UiFlow2](https://docs.m5stack.com/zh_CN/uiflow2/uiflow_web)

## 最后

    本项目只是来自于微不足道的新人之手，作为一个学习的项目，
    有问题的地方请包含，大家可以互相交流呢学习。

Made with ❤️ for M5Stack PaperS3
