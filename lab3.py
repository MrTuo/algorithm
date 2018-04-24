# coding:utf-8
import random
import pulp as tf
import time


class Solution(object):
    def generateTotalF(self, X, F, nums):
        selected_point = []
        first = []
        # 随机选20个点出来
        for x in xrange(20):
            temp = random.randrange(len(X))
            selected_point.append(X[temp])
            first.append(X[temp])
            X.pop(temp)

        F.append(first)
        self.generateF(X, F, first, selected_point)
        self.generateLast(selected_point, nums, F)

    def generateF(self, X, F, first, selected_points):

        pre = first
        while len(X) > 20:
            temp = self.getPointsFromPre(pre, selected_points, X)
            F.append(temp)
        F.append(X)
        while len(X) != 0:
            selected_points.append(X[0])
            X.pop(0)

    def generateLast(self, selected_points, nums, F):

        while len(F) < nums:
            result = []
            length = random.randrange(20)
            i = 0
            index_map = {}
            while i < length:
                index = random.randrange(len(selected_points))
                if index_map.has_key(index):
                    continue
                else:
                    index_map[index] = 1
                    result.append(selected_points[index])
                i += 1
            F.append(result)

    # 产生一个[1, 20]区间内的的随机数n代表𝑆1集合大小，再产生一个[1, n]区间内的随机数x代表需要从𝑋 ∖ 𝑆0随机选x个点放入𝑆1中，另外从𝑆0中随机选𝑛 − 𝑥个点放入𝑆1中
    def getPointsFromPre(self, pre, selected_point, X):
        result = []
        length = random.randrange(len(pre))
        length += 1
        x = random.randrange(length)
        x += 1

        for p in xrange(x):
            result.append(selected_point[random.randrange(len(selected_point))])
        for p in xrange(length - x):
            temp = X[random.randrange(len(X))]
            selected_point.append(temp)
            result.append(temp)
            X.remove(temp)
        return result

    # 贪心选择:选择能覆盖最多未被覆盖元素的子集
    def greedySetCover(self, X, F):
        result = []
        cover = []
        while len(cover) < len(X):
            pre, cover = self.selectMax(cover, F)
            result.append(pre)
        return result

    def selectMax(self, pre, F):
        now = list(pre)
        max_index = -1
        max_length = -1
        max_item = None

        for i, x in enumerate(F):
            temp = self.cover(now, x)
            if len(temp) > max_length:
                max_item = temp
                selected_item = F[i]
                max_index = i
                max_length = len(temp)
        F.pop(max_index)
        return selected_item, max_item

    def cover(self, now, new):
        result = {}
        for x in now:
            if result.has_key(x):
                continue
            else:
                result[x] = 1
        for x in new:
            if result.has_key(x):
                continue
            else:
                result[x] = 1
        new_result = []
        for x in result.keys():
            new_result.append(x)

        return new_result

        # max: 2 * x1 + 5 * x2
        #
        # 约束：
        #
        # 1.
        # 2 * x1 - x2 <= 4
        #
        # 2.
        # x1 + 2 * x2 <= 9
        #
        # 3. - x1 + x2 <= 3

    def linearProgramming(self, X, F):

        # name = ['apple', 'orange', 'pel', 'pp', 'ew']
        name = []
        # xs代表F是否在C中
        for index, x in enumerate(F):
            name.append("x%s" % str(index))
        low = {}
        for x in name:
            low[x] = 0

        up = {}
        for x in name:
            up[x] = 1
        # A dictionary of the costs of each of the Ingredients is created
        # low = {'apple': 1, 'ew': 1, 'orange': 1, 'pel': 1, 'pp': 1}

        # A dictionary of the protein percent in each of the Ingredients is created
        # up = {'apple': 10, 'ew': 10, 'orange': 10, 'pel': 10, 'pp': 10}

        prob = tf.LpProblem("The SetCover Problem", tf.LpMinimize)

        points = tf.LpVariable.dicts("Ingr", name, 0, cat='Integer')

        ok = []
        for index, x in enumerate(name):
            ok.append(points["x%s" % str(index)])
        prob += tf.lpSum(ok)

        def get(s):
            return str(s) + 'low'

        name1 = list(map(get, name))
        name1 = dict(zip(name, name1))

        def get(s):
            return str(s) + 'up'

        name2 = list(map(get, name))
        name2 = dict(zip(name, name2))

        for i in name:
            prob += points[i] - low[i] >= 0, name1[i]
            prob += points[i] - up[i] <= 0, name2[i]

        for x in X:
            temp = []
            for index2, y in enumerate(F):
                if x in y:
                    temp.append(points["x%s" % str(index2)])
                # prob += temp >= 1

            prob += tf.lpSum(temp) >= 1

        prob.solve()
        # print(prob)
        result = []
        for index, v in enumerate(prob.variables()):  ##变量输出
            # print(v.name, "=", v.varValue)
            if v.varValue == 1:
                num = int(v.name[v.name.find('x') + 1:])
                result.append(F[num])
        return result


# 产生nums个0-200的不同的值
def generateX(nums):
    result = {}
    i = 0
    while i != nums:
        temp = random.uniform(0, 200)
        if result.has_key(temp):
            continue
        result[temp] = 1
        i += 1
    new_result = []
    for x in result.keys():
        new_result.append(x)
    return new_result


so = Solution()
F = []
linearProgramming_cost = open("linearProgramming_cost", "w")
greedy_cost = open("greedy_cost", "w")
for x in xrange(30):
    N = (x + 1) * 100
    X = generateX(N)
    so.generateTotalF(generateX(N), F, N)

    time_start = time.time()
    so.greedySetCover(X, F)
    time_end = time.time()
    print('greedy cost', '%.6f' % (time_end - time_start))
    greedy_cost.write('%.6f' % (time_end - time_start))
    greedy_cost.write('\n')
    greedy_cost.flush()
    time_start = time.time()
    so.linearProgramming(X, F)
    time_end = time.time()
    print('linearProgramming cost', '%.6f' % (time_end - time_start))
    linearProgramming_cost.write('%.6f' % (time_end - time_start))
    linearProgramming_cost.write('\n')
    linearProgramming_cost.flush()
greedy_cost.close()
linearProgramming_cost.close()

# 测试正确性
# print so.greedySetCover([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#                         [[1, 4, 7], [2, 6, 9, 4, 7], [3, 5], [4, 7, 1, 3, 6, ], [1, 6, 8, 3, 9], [2, 5, 8, 0, 3, ],
#                          [5, 7, 2, 4, 6],
#                          [4, 6, 8, 3, 2], [9, 6, 3, 7, 4, ], [4, 6], [7, 9, 8], [2, 4, 6]])
#
# print so.linearProgramming(
#     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#     [[1, 4, 7], [2, 6, 9, 4, 7], [3, 5], [4, 7, 1, 3, 6, ], [1, 6, 8, 3, 9], [2, 5, 8, 0, 3, ], [5, 7, 2, 4, 6],
#      [4, 6, 8, 3, 2], [9, 6, 3, 7, 4, ], [4, 6], [7, 9, 8], [2, 4, 6]])
