import copy

from game_rects import *


class GameContainer(GameRect):
    def __init__(self, height, width):
        super().__init__(height, width)
        # 父类的game_rect属性在这里代表已经固定下来的方格

        #
        self.falling_rect = None
        self.fall_flag = False

        #
        self.score = 0
        self.run_flag = True

    def new_falling_rect(self):  # 新增一个下落元素
        self.falling_rect = FallingRect(self.height, self.width)
        self.fall_flag = True

    def ctrl_moving(self, direction):  # 控制左右平移，若平移后将发生 碰撞 则平移无效
        if self.fall_flag:  # 只有当有元素处于下落状态时才执行本函数
            if direction.lower() == 'left':
                self.falling_rect.moving(-1)
                if self.collision_detect(self.falling_rect.game_rect):
                    self.falling_rect.moving(1)  # 如果发生碰撞则还原先前状态
            elif direction.lower() == 'right':
                self.falling_rect.moving(1)
                if self.collision_detect(self.falling_rect.game_rect):
                    self.falling_rect.moving(-1)

    def ctrl_rotating(self, direction):  # 控制旋转，若旋转后将发生 碰撞 或 ？ 则旋转无效！
        # 本来是需要考虑触底的，但是在FallingRect类中已经考虑了越过边界的问题，因此不会发生越过边界的情况，触底可以在下落时考虑
        if self.fall_flag:  # 只有当有元素处于下落状态时才执行本函数
            if direction.lower() == 'clockwise':
                self.falling_rect.rotating(1)
                if self.collision_detect(self.falling_rect.game_rect):
                    self.falling_rect.rotating(-1)  # 如果发生碰撞则还原先前状态
            elif direction.lower() == 'anti-clockwise':
                self.falling_rect.rotating(-1)
                if self.collision_detect(self.falling_rect.game_rect):
                    self.falling_rect.rotating(1)

    # 平移和旋转只涉及属性falling_rect的变化，不会固定当前GameContainer类的game_rect属性，
    # 也就是说只有下落后才会触发固定当前下落方块元素的判断机制，未下落时都可以进行平移或旋转（只要不超越边界或产生碰撞）
    def ctrl_falling(self):
        if self.fall_flag:  # 只有当有元素处于下落状态时才执行本函数
            self.falling_rect.falling()
            if self.collision_detect(self.falling_rect.game_rect):
                self.falling_rect.shift_raw(0)  # 如果发生碰撞则还原状态，并将fall_flag置为False
                self.fall_flag = False
                self.add_rect(self.falling_rect.game_rect)  # 固定当前GameContainer类的game_rect属性
                self.falling_rect = None  # 清空当前falling_rect
            elif self.bottom_reached(self.falling_rect.game_rect):
                self.fall_flag = False
                self.add_rect(self.falling_rect.game_rect)
                self.falling_rect = None  #
            else:
                # 下落时既没有碰撞也没有沉底，需要继续下落，则不能有下面这行代码！这行代码是实时更新地图上已固定元素的！
                # self.add_rect(self.falling_rect.game_rect)
                pass

    def post_fall(self):  # 元素下落且固定之后需要进行的操作（计分、消除堆满的方块、判断是否越界游戏结束）
        # （返回值确定是否要延时消除方块）
        for i in range(0, 5):
            if self.raw_state(i) == 2:
                self.run_flag = False
                return False
        res = self.raw_check()
        if res:
            self.raw_clear(res)
            if len(res) == 1:
                self.score += 1
            elif len(res) == 2:
                self.score += 2
            elif len(res) == 3:
                self.score += 4
            elif len(res) == 4:
                self.score += 8
            return True
        else:
            return False



    def collision_detect(self, other_rect):  # 接收一个game_rect矩阵，判断当前game_rect与其相加时是否发生碰撞，不会改变任何属性值！
        temp = copy.deepcopy(self.game_rect)
        self.add_rect(other_rect)
        for i in range(self.height):
            if self.raw_state(i) == 2:
                self.game_rect = temp
                return True
        self.game_rect = temp
        return False

    def bottom_reached(self, other_rect):  # 接收一个game_rect矩阵，判断该game_rect是否已经沉底
        if 1 in other_rect[self.height - 1]:
            return True
        else:
            return False

    def raw_check(self):  # 返回当前全1的行
        res = []
        for i in range(self.height):
            if self.raw_state(i) == 1:
                res.append(i)
        res.reverse()
        return res

    def raw_clear(self, res):  # 消除返回的全1行，其余行正常下路至底端
        flag = 0
        for i in res:
            self.shift_raw(i + flag)  # 从底端下上消除，每消除一行，原先全0行的所在行数都会+1
            flag += 1

    def display_rect(self):  # 结合当前类的game_rect及falling_part的game_rect返回可供实时显示的画面矩阵
        if self.falling_rect is None:
            return self.game_rect, None
            # print(self)
        else:
            temp = copy.deepcopy(self)  # 深拷贝本类对象以使用类方法
            temp.add_rect(self.falling_rect.game_rect)
            return temp.game_rect, self.falling_rect.game_rect  # 返回两个game_rect方便上色
            # print(temp)  # 本来是应该返回game_rect属性的，但是多维列表不方便输出调试


if __name__ == '__main__':
    pass
    gc = GameContainer(10, 10)
    gc.display_rect()
    gc.new_falling_rect()
    gc.display_rect()
    for i in range(0, 10):
        gc.ctrl_falling()
        gc.display_rect()
