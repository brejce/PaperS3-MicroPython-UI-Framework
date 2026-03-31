
"""
CoordinateCalculator - 坐标计算器
根据给定的区域、字体、行间距等参数，预计算可用于绘制列表项的 Y 坐标。
X 坐标通常由外部（如 padding 或 GridSystem）决定。
"""






import math

class ListSystem:
    """
    坐标计算器 - 用于计算垂直列表项的绘制 Y 坐标
    """

    def __init__(self, height: int, char_height: int, line_spacing: int = 0):
        """
        初始化坐标计算器。

        Args:
            height: 计算区域的高度
            char_height: 单个字符的高度 (用于计算行高)
            line_spacing: 行间距 (字符高度之外的额外间距)
            start_y: 起始绘制的 Y 坐标偏移量 (可选，默认为 0)
        """
        self.height = height
        self.char_height = char_height
        self.line_spacing = line_spacing
        self.start_y = self.line_spacing # 新增起始 Y 偏移

        # 预计算参数
        self._one_line_height = char_height + line_spacing
        # 计算在给定高度内最多可以容纳多少行
        self.max_rows = max(1, height // self._one_line_height)
        # 计算每一行的 Y 坐标
        self._calculate_coordinates()

    def _calculate_coordinates(self):
        """预计算所有可能的 Y 坐标"""
        self.y_coordinates = []
        for row_index in range(self.max_rows):
            y = self.start_y + row_index * self._one_line_height
            self.y_coordinates.append(y)

    def get_y_coordinates(self) -> list[int]:
        """
        获取预计算的所有 Y 坐标列表。

        Returns:
            list[int]: [y1, y2, ...] Y 坐标列表
        """
        return self.y_coordinates.copy() # 返回副本，防止外部修改

    def get_coordinate_for_row(self, row_index: int, x: int) -> tuple[int, int] | None:
        """
        获取指定行号的绘制坐标 (X 需要外部提供)。

        Args:
            row_index: 行号 (从 0 开始)
            x: 指定的 X 坐标

        Returns:
            tuple[int, int] | None: (x, y) 坐标，如果行号超出范围则返回 None
        """
        if 0 <= row_index < len(self.y_coordinates):
            y = self.y_coordinates[row_index]
            return (x, y)
        return None

    def get_y_for_row(self, row_index: int) -> int | None:
        """
        获取指定行号的 Y 坐标。

        Args:
            row_index: 行号 (从 0 开始)

        Returns:
            int | None: Y 坐标，如果行号超出范围则返回 None
        """
        if 0 <= row_index < len(self.y_coordinates):
            return self.y_coordinates[row_index]
        return None

    def get_max_rows(self) -> int:
        """
        获取计算区域内最大可容纳的行数。

        Returns:
            int: 最大行数
        """
        return self.max_rows

    def get_line_height(self) -> int:
        """
        获取单行的高度 (字符高度 + 间距)。

        Returns:
            int: 单行高度
        """
        return self._one_line_height