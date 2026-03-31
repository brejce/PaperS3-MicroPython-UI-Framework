# ============================================
# 第一部分：16级灰度颜色定义（24位格式）
# ============================================

# 16级灰度调色板（4bpp ePaper，但颜色值仍为24位 RGB）
# 格式：0xRRGGBB，每个分量8位
# 显示器会自动将24位颜色转换为16级灰度显示
GRAY_0 = 0x000000      # 纯黑（RGB 0,0,0）
GRAY_1 = 0x111111      # 灰度1
GRAY_2 = 0x222222      # 灰度2
GRAY_3 = 0x333333      # 灰度3
GRAY_4 = 0x444444      # 灰度4
GRAY_5 = 0x555555      # 灰度5
GRAY_6 = 0x666666      # 灰度6
GRAY_7 = 0x777777      # 灰度7
GRAY_8 = 0x888888      # 灰度8（中间值，RGB 136,136,136）
GRAY_9 = 0x999999      # 灰度9
GRAY_10 = 0xAAAAAA     # 灰度10
GRAY_11 = 0xBBBBBB     # 灰度11
GRAY_12 = 0xCCCCCC     # 灰度12
GRAY_13 = 0xDDDDDD     # 灰度13
GRAY_14 = 0xEEEEEE     # 灰度14
GRAY_15 = 0xFFFFFF     # 纯白（RGB 255,255,255）

COLORS = [
GRAY_0,
GRAY_1,
GRAY_2,
GRAY_3,
GRAY_4,
GRAY_5,
GRAY_6,
GRAY_7,
GRAY_8,
GRAY_9,
GRAY_10,
GRAY_11,
GRAY_12,
GRAY_13,
GRAY_14,
GRAY_15
]

class Colors:
    """UI 组件的标准颜色主题（16级灰度，24位格式）"""

    # 基础颜色
    BLACK = GRAY_0           # 纯黑
    DARK = GRAY_3            # 深灰
    MEDIUM_DARK = GRAY_6     # 中深灰
    MEDIUM = GRAY_8          # 中灰（边框、轨道）
    MEDIUM_LIGHT = GRAY_10   # 中浅灰
    LIGHT = GRAY_13          # 浅灰（禁用状态）
    LIGHT_WHITE = GRAY_14

    WHITE = GRAY_15          # 纯白（背景）