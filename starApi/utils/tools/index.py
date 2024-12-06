def to_yi(n):
    try:
        n = int(n)
    except:
        return n
    s = round(n / 100000000, 2)
    if s < 1:
        s = round(n / 10000, 2)
        s = str(s) + '万'
    else:
        s = str(s) + '亿'
    return s


def to_float_list(current_value, zt_value):
    # 定义步长
    step = 0.01
    # 生成列表并四舍五入到小数点后两位
    float_list = [round(current_value + step * i, 2) for i in range(1, 6)][::-1] + [round(current_value - step * i, 2)
                                                                                    for i in range(4, -1, -1)][::-1]
    result = any(x > zt_value for x in float_list)
    if result:
        float_list = [x - step for x in float_list]
    return float_list


md_zh = ['卖5', '卖4', '卖3', '卖2', '卖1', '买1', '买2', '买3', '买4', '买5']


def merge_md(item, value):
    query = []
    for index, i in enumerate(value):
        if i == '-':
            query.append([md_zh[index], '-', i])
        else:
            query.append([md_zh[index], f"{item[index]:.2f}", round(i, 2)])
    return query
