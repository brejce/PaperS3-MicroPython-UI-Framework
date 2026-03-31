#GridSystem.py

class GridSystem:
    """
    网格坐标系统（纯坐标计算）
    只负责预计算坐标，绘制工作由外部完成
    """
    
    def __init__(self, width=540, height=960, char_width=29, char_height=32,
                 line_spacing=13, letter_spacing=13):
        """
        初始化网格系统
        
        Args:
            width: 画布宽度
            height: 画布高度
            char_width: 单个字符宽度
            char_height: 单个字符高度
            line_spacing: 行间距（字符高度外额外间距）
            letter_spacing: 字间距（字符宽度外额外间距）
        """
        # 保存配置
        self.width = width
        self.height = height
        self.char_width = char_width
        self.char_height = char_height
        self.line_spacing = line_spacing
        self.letter_spacing = letter_spacing
        
        # 网格信息
        self.grid_cols = 0
        self.grid_rows = 0
        self.total_cells = 0
        
        # 起始偏移
        self.offset_x = 0
        self.offset_y = 0
        
        # 坐标数组 [index] = (x, y)
        self.coordinates = []
        
        # 初始化
        self._init_grid()
    
    def _init_grid(self):
        """初始化网格"""
        # 计算网格行列数
        self.grid_cols = self.width // (self.char_width + self.letter_spacing)
        self.grid_rows = self.height // (self.char_height + self.line_spacing)
        self.total_cells = self.grid_cols * self.grid_rows
        
        # 计算空闲空间并居中
        used_width = self.grid_cols * (self.char_width + self.letter_spacing) - self.letter_spacing
        free_x = self.width - used_width
        self.offset_x = free_x // 2
        
        used_height = self.grid_rows * (self.char_height + self.line_spacing) - self.line_spacing
        free_y = self.height - used_height
        self.offset_y = free_y // 2
        
        # 预计算坐标
        self._precalculate_coordinates()
        
        # 打印信息
        
        print(f"[GridSystem] 初始化完成")
        print(f"  画布: {self.width}x{self.height}")
        print(f"  字符: {self.char_width}x{self.char_height}")
        print(f"  间距: 行={self.line_spacing}, 字={self.letter_spacing}")
        print(f"  网格: {self.grid_cols}列 x {self.grid_rows}行 = {self.total_cells}字符")
        print(f"  占用: {used_width}x{used_height}")
        print(f"  空闲: {free_x}x{free_y}")
        print(f"  偏移: ({self.offset_x}, {self.offset_y})")
        print(f"  坐标数: {len(self.coordinates)}")
    
    def _precalculate_coordinates(self):
        """预计算所有坐标"""
        self.coordinates = []
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = self.offset_x + col * (self.char_width + self.letter_spacing)
                y = self.offset_y + row * (self.char_height + self.line_spacing)
                
                index = row * self.grid_cols + col
                self.coordinates.append((x, y))
    
    # ==================== 对外接口 ====================
    
    def get_coordinate(self, index):
        """
        获取第index个位置的坐标
        
        Args:
            index: 字符索引（0-based）
            
        Returns:
            (x, y) 坐标元组，超出范围返回 None
        """
        if 0 <= index < len(self.coordinates):
            return self.coordinates[index]
        return None
    
    def get_index(self, row, col):
        """
        根据行列获取索引
        
        Args:
            row: 行号（0-based）
            col: 列号（0-based）
            
        Returns:
            索引值，无效返回 -1
        """
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            return row * self.grid_cols + col
        return -1
    
    def get_row_col(self, index):
        """
        根据索引获取行列号
        
        Args:
            index: 索引（0-based）
            
        Returns:
            (row, col) 元组，无效返回 None
        """
        if 0 <= index < self.total_cells:
            row = index // self.grid_cols
            col = index % self.grid_cols
            return (row, col)
        return None
    
    def get_capacity(self):
        """获取网格容量"""
        return self.total_cells
    
    def get_char_size(self):
        """获取字符尺寸"""
        return (self.char_width, self.char_height)
    
    def get_spacing(self):
        """获取间距"""
        return (self.line_spacing, self.letter_spacing)
    
    def get_offset(self):
        """获取起始偏移"""
        return (self.offset_x, self.offset_y)
    
    def get_grid_size(self):
        """获取网格行列数"""
        return (self.grid_cols, self.grid_rows)
    
    def get_all_coordinates(self):
        """获取所有坐标（只读）"""
        return tuple(self.coordinates)
