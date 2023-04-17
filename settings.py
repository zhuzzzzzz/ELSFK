class Settings:
    def __init__(self):
        self.unit_length = 40  # 单元格像素长度
        self.row_num = 20  # 行数
        self.column_num = 10  # 列数
        self.height = self.row_num * self.unit_length  # 行像素高度
        self.width = self.column_num * self.unit_length  # 列像素高度

        self.refresh_time = 20  # 程序刷新时间
        self.fall_time = 500  # 元素下落间隔时间

        self.background_color = (255, 255, 255)
        self.falling_rect_color = (0, 156, 255)
        self.rect_color = (104, 104, 104)
        self.bad_colar = (255, 0, 0)
