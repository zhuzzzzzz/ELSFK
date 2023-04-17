import random


class GameRect:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.game_rect = []
        for i in range(height):
            self.game_rect.append([0] * width)

    def __repr__(self):
        res = ""
        for item in self.game_rect:
            res = res + str(item) + '\n'
        return res

    def set_value(self, obj, value):  # 设置矩阵值，可以设置一整行、或根据返回的坐标集合，设置值
        if type(obj) == int:
            for i in range(len(self.game_rect[obj])):
                self.game_rect[obj][i] = value
        else:
            for item in obj:
                self.game_rect[item[0]][item[1]] = value

    def add_rect(self, other_rect):
        res = []
        for i in range(self.height):
            res.append([a + b for a, b in zip(self.game_rect[i], other_rect[i])])
        self.game_rect = res

    def raw_state(self, r):  # 返回当前GameRect实例的game_rect属性某一行的状态：全0返回0，全1返回1，有2则返回2，1、0交替则返回0.5
        if 2 in self.game_rect[r]:
            return 2
        elif 1 in self.game_rect[r]:
            if 0 in self.game_rect[r]:
                return 0.5
            else:
                return 1
        else:
            return 0

    def shift_raw(self, r):  # 当前GameRect实例的game_rect属性从某一行开始整体向上或下平移一行，当前行丢弃，空缺行补0
        # 当r为正数表示下移，r为非正数表示上移
        if r > 0:
            self.game_rect.pop(r)
            self.game_rect.insert(0, [0] * self.width)
        else:
            self.game_rect.pop(-r)
            self.game_rect.append([0] * self.width)


class FallingRect(GameRect):
    def __init__(self, height, width, **kwargs):
        super().__init__(height, width)
        self.part_type = None
        res = self.args_analysis(kwargs)
        self.falling_part = FallingPart(self.part_type, res[0], res[1])
        self.set_value(self.falling_part.get_coordinate(), 1)  # 显示当前falling_part

    def falling(self):  # 下落、移动和旋转后都会对game_rect赋值！
        self.falling_part.r += 1
        if not self.out_of_bounds(self.falling_part.get_coordinate()):
            self.shift_raw(self.height - 1)
        else:
            self.falling_part.r -= 1

    def moving(self, x):  # 下落、移动和旋转后都会对game_rect赋值！
        self.set_value(self.falling_part.get_coordinate(), 0)  # 平移或旋转前需要刷新FallingRect.game_rect属性！
        self.falling_part.c += x
        coordinates = self.falling_part.get_coordinate()  # 获得更新后的坐标
        if not self.out_of_bounds(coordinates):  # 判断坐标更新后falling_part是否超出边界
            self.set_value(coordinates, 1)
        else:
            self.falling_part.c -= x  # 还原坐标，注意下面不能再用coordinates变量了，因为坐标已经发生变化而其没有更新
            self.set_value(self.falling_part.get_coordinate(), 1)  # 平移或旋转失败要还原FallingRect.game_rect属性！

    def rotating(self, x):  # 下落、移动和旋转后都会对game_rect赋值！
        self.set_value(self.falling_part.get_coordinate(), 0)
        self.falling_part.rotate(x)
        coordinates = self.falling_part.get_coordinate()
        if not self.out_of_bounds(coordinates):
            self.set_value(coordinates, 1)
        else:
            self.falling_part.rotate(-x)
            self.set_value(self.falling_part.get_coordinate(), 1)

    def out_of_bounds(self, obj):
        for item in obj:
            if item[0] < 0 or item[0] >= self.height:  # 如果高度超出边界
                return True
            if item[1] < 0 or item[1] >= self.width:  # 如果宽度超出边界
                return True
        return False

    def args_analysis(self, kwargs):
        temp = ['I', 'O', 'J', 'L', 'S', 'Z', 'T']
        # random.seed(0)
        if 'part_type' in kwargs.keys():  # 如果指定了part_type则按指定的来，否则随机

            if kwargs['part_type'] in temp:
                self.part_type = kwargs['part_type']
            else:
                self.part_type = random.choice(temp)
        else:
            self.part_type = random.choice(temp)
        # random.seed(0)
        if 'init_location' in kwargs.keys():  # 如果指定了生成位置则按指定的来，否则随机，但要注意随机时不能超过矩阵边界
            if kwargs['init_location'].lower() == 'mid':
                c = int((self.width - 1) / 2)
            else:
                c = random.randint(2, self.width - 3)
        else:
            c = random.randint(2, self.width - 3)
        return 2, c


class FallingPart:
    def __init__(self, part_type, point_r, point_c):
        self.part_type = part_type
        self.r = point_r  # 当前part的旋转中心坐标值
        self.c = point_c
        # random.seed(0)
        self.state = random.randint(0, 3)  # 随机生成一个旋转状态

    def rotate(self, direction):
        if direction == 1:  # 顺时针旋转为状态值递增
            self.state = (self.state + 1) % 4
        elif direction == -1:  # 逆时针旋转为状态值递减
            self.state = (self.state - 1) % 4

    def get_coordinate(self):
        if self.part_type == 'I':
            if self.state == 0:
                return {(self.r, self.c - 1), (self.r, self.c), (self.r, self.c + 1), (self.r, self.c + 2)}
            elif self.state == 1:
                return {(self.r - 1, self.c), (self.r, self.c), (self.r + 1, self.c), (self.r + 2, self.c)}
            elif self.state == 2:
                return {(self.r, self.c - 2), (self.r, self.c - 1), (self.r, self.c), (self.r, self.c + 1)}
            elif self.state == 3:
                return {(self.r - 2, self.c), (self.r - 1, self.c), (self.r, self.c), (self.r + 1, self.c)}
        elif self.part_type == 'O':  # 方块不设旋转，即返回坐标与旋转状态无关
            return {(self.r - 1, self.c), (self.r - 1, self.c + 1), (self.r, self.c), (self.r, self.c + 1)}
        elif self.part_type == 'J':
            if self.state == 0:
                return {(self.r - 2, self.c), (self.r - 1, self.c), (self.r, self.c), (self.r, self.c - 1)}
            elif self.state == 1:
                return {(self.r - 1, self.c), (self.r, self.c), (self.r, self.c + 1), (self.r, self.c + 2)}
            elif self.state == 2:
                return {(self.r, self.c), (self.r, self.c + 1), (self.r + 1, self.c), (self.r + 2, self.c)}
            elif self.state == 3:
                return {(self.r, self.c - 2), (self.r, self.c - 1), (self.r, self.c), (self.r + 1, self.c)}
        elif self.part_type == 'L':
            if self.state == 0:
                return {(self.r - 2, self.c), (self.r - 1, self.c), (self.r, self.c), (self.r, self.c + 1)}
            elif self.state == 1:
                return {(self.r + 1, self.c), (self.r, self.c), (self.r, self.c + 1), (self.r, self.c + 2)}
            elif self.state == 2:
                return {(self.r, self.c), (self.r, self.c - 1), (self.r + 1, self.c), (self.r + 2, self.c)}
            elif self.state == 3:
                return {(self.r, self.c - 2), (self.r, self.c - 1), (self.r, self.c), (self.r - 1, self.c)}
        elif self.part_type == 'S':
            if self.state == 0:
                return {(self.r - 1, self.c), (self.r - 1, self.c + 1), (self.r, self.c - 1), (self.r, self.c)}
            elif self.state == 1:
                return {(self.r - 1, self.c), (self.r, self.c), (self.r, self.c + 1), (self.r + 1, self.c + 1)}
            elif self.state == 2:
                return {(self.r, self.c), (self.r, self.c + 1), (self.r + 1, self.c - 1), (self.r + 1, self.c)}
            elif self.state == 3:
                return {(self.r - 1, self.c - 1), (self.r, self.c - 1), (self.r, self.c), (self.r + 1, self.c)}
        elif self.part_type == 'Z':
            if self.state == 0:
                return {(self.r - 1, self.c), (self.r, self.c + 1), (self.r - 1, self.c - 1), (self.r, self.c)}
            elif self.state == 1:
                return {(self.r - 1, self.c + 1), (self.r, self.c), (self.r, self.c + 1), (self.r + 1, self.c)}
            elif self.state == 2:
                return {(self.r, self.c - 1), (self.r, self.c), (self.r + 1, self.c), (self.r + 1, self.c + 1)}
            elif self.state == 3:
                return {(self.r - 1, self.c), (self.r, self.c - 1), (self.r, self.c), (self.r + 1, self.c - 1)}
        elif self.part_type == 'T':
            if self.state == 0:
                return {(self.r - 1, self.c), (self.r, self.c - 1), (self.r, self.c), (self.r, self.c + 1)}
            elif self.state == 1:
                return {(self.r - 1, self.c), (self.r, self.c), (self.r + 1, self.c), (self.r, self.c + 1)}
            elif self.state == 2:
                return {(self.r + 1, self.c), (self.r, self.c - 1), (self.r, self.c), (self.r, self.c + 1)}
            elif self.state == 3:
                return {(self.r - 1, self.c), (self.r, self.c), (self.r + 1, self.c), (self.r, self.c - 1)}


if __name__ == '__main__':
    pass
    g = GameRect(10, 10)
    print(g)
    g.set_value(1, 1)
    g.set_value({(2, 4)}, 1)
    print(g)
    g.shift_raw(0)
    print(g)
