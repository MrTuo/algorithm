# coding:utf-8
import random
import time


class Solution(object):
    # A->B
    def whichSide(self, A, B, C):
        P1 = (B[0] - A[0], B[1] - A[1])
        P2 = (A[0] - C[0], A[1] - C[1])

        result = P1[0] * P2[1] - P1[1] * P2[0]

        # 右侧
        if result > 0:
            return "r"
        else:
            if result == 0:
                return 'i'
            else:
                return "l"

    def isSide(self, A, B, C):
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        result = x2 * y3 - y2 * x3 - (x1 * y3 - y1 * x3) + (x1 * y2 - y1 * x2)

        if result == 0:
            return 'A'
        else:
            if result > 0:
                return 'B'
            else:
                return 'C'

    def calculateDis(self, A, B, C):
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        result = x2 * y3 - y2 * x3 - (x1 * y3 - y1 * x3) + (x1 * y2 - y1 * x2)

        if result >= 0:
            return result
        else:
            return -result

    def calculate(self, A, B, C):
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        result = x2 * y3 - y2 * x3 - (x1 * y3 - y1 * x3) + (x1 * y2 - y1 * x2)

        return result

    def lineIsOk(self, set, line):
        result = dict()
        for x in set:
            temp = self.isSide(line[0], line[1], x)
            if result.has_key(temp):
                result[temp] += 1
            else:
                result[temp] = 1
        if len(result) <= 2:
            return True
        else:
            return False

    def force(self, set):
        """
        :type set: List[pair]
        :rtype: List[pair]
        """
        line_set = []
        # 首先要生成n(n-1)/2条直线
        i = 0
        while i < len(set) - 1:
            j = i + 1
            while j < len(set):
                temp = []
                temp.append(set[i])
                temp.append(set[j])
                line_set.append(temp)
                j += 1
            i += 1

        result = []

        for x in line_set:
            if self.lineIsOk(set, x) == True:
                result.append(x)

        return result

    def getTop(self, result, min, max, set):

        if max[0] == min[0]:
            result.append([min, max])
            return
        if len(set) < 1:
            result.append([min, max])
            return
        left = max if max[1] >= min[1] else min
        right = max if max[1] < min[1] else min

        top = []

        for x in set:
            if (right[0] - left[0]) * self.calculate(left, right, x) > 0:
                top.append(x)
        if len(top) == 0:
            result.append([min, max])
            return
        max_dis = -1
        max_point = None
        for x in top:
            temp = self.calculateDis(left, right, x)
            if temp > max_dis:
                max_dis = temp
                max_point = x
        self.getTop(result, left, max_point, top)
        self.getTop(result, right, max_point, top)

    def getBottom(self, result, min, max, set):

        if max[0] == min[0]:
            result.append([min, max])
            return
        if len(set) < 1:
            result.append([min, max])
            return
        left = max if max[1] >= min[1] else min
        right = max if max[1] < min[1] else min

        bottom = []

        for x in set:
            if (right[0] - left[0]) * self.calculate(left, right, x) < 0:
                bottom.append(x)
        if len(bottom) == 0:
            result.append([min, max])
            return
        max_dis = -1
        max_point = None
        for x in bottom:
            temp = self.calculateDis(left, right, x)
            if temp > max_dis:
                max_dis = temp
                max_point = x
        self.getBottom(result, left, max_point, bottom)
        self.getBottom(result, right, max_point, bottom)

    def divide(self, set):

        if len(set) < 3:
            return []
        max_index = -1
        min_index = -1
        max = -1
        min = 200
        for index, x in enumerate(set):
            if x[0] > max:
                max = x
                max_index = index
            if x[0] < min:
                min = x
                min_index = index

        result = []
        self.getTop(result, min, max, set)
        self.getBottom(result, min, max, set)
        return result

    def dealPoints(self, set, target):
        result = []
        for x in set:
            temp_x = x[0] - target[0]
            temp_y = x[1] - target[1]
            result.append((temp_x, temp_y))
        return result

    def returnPoints(self, set, target):
        result = []
        for x in set:
            temp_x = x[0] + target[0]
            temp_y = x[1] + target[1]
            result.append((temp_x, temp_y))
        return result

    def calculateCos(self, P1, P2):
        result = P1[0] * P2[0] + P1[1] * P2[1]
        P1_mod = pow(P1[0] * P1[0] + P1[1] * P1[1], 0.5)
        P2_mod = pow(P2[0] * P2[0] + P2[1] * P2[1], 0.5)
        return result / P1_mod / P2_mod

    def getAbsolute(self, x):
        if x <= 0:
            return -x
        else:
            return x

    # 根据距离远近排序
    def subQuickSort(self, set, cos):
        if len(set) <= 1:
            return set, cos
        set_mid = set[len(set) / 2]
        cos_mid = cos[len(cos) / 2]

        set_left = []
        set_mid_list = []
        set_right = []

        cos_left = []
        cos_mid_list = []
        cos_right = []

        for index, x in enumerate(set):
            if self.getAbsolute(set[index][0]) < self.getAbsolute(set_mid[0]):
                set_left.append(set[index])
                cos_left.append(cos[index])

            if self.getAbsolute(set[index][0]) == self.getAbsolute(set_mid[0]):
                set_mid_list.append(set[index])
                cos_mid_list.append(cos[index])

            if self.getAbsolute(set[index][0]) > self.getAbsolute(set_mid[0]):
                set_right.append(set[index])
                cos_right.append(cos[index])

        set_left_result, cos_left_result = self.quickSort(set_left, cos_left)

        set_right_result, cos_right_result = self.quickSort(set_right, cos_right)

        return set_left_result + set_mid_list + set_right_result, cos_left_result + cos_mid_list + cos_right_result

    # 根据cos大小为点从大到小排序，角度相同的点按照距离由小到大排序,
    def quickSort(self, set, cos):
        if len(set) <= 1:
            return set, cos
        set_mid = set[len(set) / 2]
        cos_mid = cos[len(cos) / 2]

        set_left = []
        set_mid_list = []
        set_right = []

        cos_left = []
        cos_mid_list = []
        cos_right = []

        for index, x in enumerate(set):
            if cos[index] > cos_mid:
                set_left.append(set[index])
                cos_left.append(cos[index])

            if cos[index] == cos_mid:
                set_mid_list.append(set[index])
                cos_mid_list.append(cos[index])

            if cos[index] < cos_mid:
                set_right.append(set[index])
                cos_right.append(cos[index])

        set_left_result, cos_left_result = self.quickSort(set_left, cos_left)

        set_right_result, cos_right_result = self.quickSort(set_right, cos_right)

        # 如果cos角度相同，则按距离由小到大排序
        sorted_set_mid_list, sorted_cos_mid_list = self.subQuickSort(set_mid_list, cos_mid_list)

        return set_left_result + sorted_set_mid_list + set_right_result, cos_left_result + sorted_cos_mid_list + cos_right_result

    def getSide(self, l):
        result = []
        i = 0
        while i < len(l) - 1:
            result.append([l[i], l[i + 1]])
            i += 1
        result.append([l[-1], l[0]])
        return result

    def grahamScan(self, set):
        low_point_y = 200
        low_point = None
        # 找到y值最低的点
        for x in set:
            if x[1] < low_point_y:
                low_point = x
                low_point_y = x[1]

        set.remove(low_point)
        # 以该点为原点，将所有点平移到对应位置
        dealed_set = self.dealPoints(set, low_point)

        # 为每个点计算其与X轴的夹角CosΘ
        cos = []
        for x in dealed_set:
            P1 = (1, 0)
            P2 = x
            temp = self.calculateCos(P1, P2)
            cos.append(temp)

        # 将点按照CosΘ从大到小排序，如CosΘ相同，将距离小的排前面
        sorted_set, _ = self.quickSort(dealed_set, cos)

        my_stack = []
        # 按照步骤4开始将凸包上的点加入my_stack
        my_stack.append((0, 0))
        for index, x in enumerate(sorted_set):
            if index == 0:
                my_stack.append(x)
                continue
            A = my_stack[-1]
            B = my_stack[-2]

            while self.whichSide(B, A, x) == 'r':
                my_stack.pop(-1)
                A = my_stack[-1]
                B = my_stack[-2]

            my_stack.append(sorted_set[index])

        # 把所有点连成边
        result = self.returnPoints(my_stack, low_point)
        return self.getSide(result)


# 在100×100的矩阵里 生成指定数目的浮点点
def generateRandom(num):
    result = dict()
    i = 0
    while i < num:
        temp = (random.uniform(0, 200), random.uniform(0, 200))
        if result.has_key(temp):
            continue
        else:
            result[temp] = 1
        i += 1
    return result


so = Solution()

print "测试用例1"
print so.force([(2, 5), (3, 2), (4, 8), (5, 6), (6, 4), (8, 2), (8, 6), (9, 8), (10, 1), (12, 9), (13, 5)])
print so.divide([(2, 5), (3, 2), (4, 8), (5, 6), (6, 4), (8, 2), (8, 6), (9, 8), (10, 1), (12, 9), (13, 5)])
print so.grahamScan([(2, 5), (3, 2), (4, 8), (5, 6), (6, 4), (8, 2), (8, 6), (9, 8), (10, 1), (12, 9), (13, 5)])
print "测试用例2"
print so.force([(1, 1), (1, 5), (2, 4), (6, 1), (6, 5)])
print so.divide([(1, 1), (1, 5), (2, 4), (6, 1), (6, 5)])
print so.grahamScan([(1, 1), (1, 5), (2, 4), (6, 1), (6, 5)])
print "测试用例3"
print so.force([(2, 2), (2, 6), (3, 4), (5, 3), (6, 5), (7, 1), (7, 6)])
print so.divide([(2, 2), (2, 6), (3, 4), (5, 3), (6, 5), (7, 1), (7, 6)])
print so.grahamScan([(2, 2), (2, 6), (3, 4), (5, 3), (6, 5), (7, 1), (7, 6)])

# my_list = []
#
# for x in xrange(21):
#     my_list.append((x + 1) * 100)
#
# force_cost = open("./force_cost", "w")
# divide_cost = open("./divide_cost", "w")
# grahamScan_cost = open("grahamScan_cost", "w")
#
# for x in my_list:
#     test_dict = generateRandom(x)
#     test = []
#     for x in test_dict.keys():
#         test.append(x)
#
#     time_start = time.time()
#     so.force(test)
#     time_end = time.time()
#     print('force cost', time_end - time_start)
#     force_cost.write('%.6f' % (time_end - time_start))
#     force_cost.write('\n')
#     force_cost.flush()
#
#     time_start = time.time()
#     so.divide(test)
#     time_end = time.time()
#     print('divide cost', time_end - time_start)
#     divide_cost.write('%.6f' % (time_end - time_start))
#     divide_cost.write('\n')
#     divide_cost.flush()
#
#     time_start = time.time()
#     so.grahamScan(test)
#     time_end = time.time()
#     print('grahamScan cost', '%.6f' % (time_end - time_start))
#     grahamScan_cost.write('%.6f' % (time_end - time_start))
#     grahamScan_cost.write('\n')
#     grahamScan_cost.flush()
#
# force_cost.close()
# divide_cost.close()
# grahamScan_cost.close()
