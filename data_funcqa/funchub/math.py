import math

# this function is used to round the result to 2 decimal places
# e.g. 52.3523 -> 52.35, 52.0011 -> 52, 0.00000233 -> 0.0000023
def custom_round(x, decimal_places=2):
    """
    自定义四舍五入函数，智能处理小数位数
    
    该函数用于将数字四舍五入到指定的小数位数。对于非常小的数字（如0.00000233），
    会自动调整小数位数以保留有效数字。
    
    参数:
        x (float): 需要四舍五入的数字
        decimal_places (int, 可选): 默认保留的小数位数，默认为2
    
    返回值:
        float: 四舍五入后的数字
    
    使用示例:
        >>> custom_round(52.3523)
        52.35
        >>> custom_round(52.0011)
        52.0
        >>> custom_round(0.00000233)
        0.0000023
    """
    str_x = f"{x:.10f}"
    before_decimal = str_x.split('.')[0]
    after_decimal = str_x.split('.')[1]
    leading_zeros = len(after_decimal) - len(after_decimal.lstrip('0'))
    
    if leading_zeros >= 1 and before_decimal == "0":
        return round(x, leading_zeros + 2)
    else:
        return round(x, decimal_places)

# this function converts a number in scientific notation to decimal notation
def scito_decimal(sci_str):
    """
    将科学计数法表示的数字转换为十进制表示
    
    该函数接收一个科学计数法格式的字符串（如"1.23e-4"），
    并将其转换为标准的十进制字符串表示（如"0.000123"）。
    
    参数:
        sci_str (str): 科学计数法格式的字符串，如"1.23e-4"或"5.67e+2"
    
    返回值:
        str: 十进制表示的字符串，去除了尾随的零
    
    使用示例:
        >>> scito_decimal("1.23e-4")
        "0.000123"
        >>> scito_decimal("5.67e+2")
        "567"
    """
    def split_exponent(number_str):
        parts = number_str.split("e")
        coefficient = parts[0]
        exponent = int(parts[1]) if len(parts) == 2 else 0
        return coefficient, exponent

    def multiplyby_10(number_str, exponent):
        if exponent == 0:
            return number_str

        if exponent > 0:
            index = number_str.index(".") if "." in number_str else len(number_str)
            number_str = number_str.replace(".", "")
            new_index = index + exponent
            number_str += "0" * (new_index - len(number_str))
            if new_index < len(number_str):
                number_str = number_str[:new_index] + "." + number_str[new_index:]
            return number_str

        if exponent < 0:
            index = number_str.index(".") if "." in number_str else len(number_str)
            number_str = number_str.replace(".", "")
            new_index = index + exponent
            number_str = "0" * (-new_index) + number_str
            number_str = "0." + number_str
            return number_str

    coefficient, exponent = split_exponent(sci_str)
    decimal_str = multiplyby_10(coefficient, exponent)

    # remove trailing zeros
    if "." in decimal_str:
        decimal_str = decimal_str.rstrip("0")

    return decimal_str

# normalize the result to 2 decimal places and remove trailing zeros
def normalize(res, round_to=2):
        """
        标准化数字结果，四舍五入并移除尾随零
        
        该函数将数字结果标准化为指定的小数位数，移除尾随的零，
        并处理科学计数法表示的数字。
        
        参数:
            res (float): 需要标准化的数字结果
            round_to (int, 可选): 四舍五入的小数位数，默认为2
        
        返回值:
            str: 标准化后的字符串表示
        
        使用示例:
            >>> normalize(3.14159)
            "3.14"
            >>> normalize(5.00)
            "5"
            >>> normalize(1.23e-4)
            "0.000123"
        """
        # we round the result to 2 decimal places
        res = custom_round(res, round_to)
        res = str(res)
        if "." in res:
            while res[-1] == "0":
                res = res[:-1]
            res = res.strip(".")
        
        # scientific notation
        if "e" in res:
            res = scito_decimal(res)

        return res

# 1. add
def add_(args):
    """
    加法运算函数
    
    计算参数列表中所有数字的和。支持多个数字的连续加法运算。
    
    参数:
        args (list): 包含数字的列表，如[1, 2, 3, 4]
    
    返回值:
        str: 标准化后的加法结果字符串
    
    使用示例:
        >>> add_([1, 2, 3])
        "6"
        >>> add_([1.5, 2.3, 0.2])
        "4"
    """

    return normalize(sum(args))

# 2. subtract
def subtract_(args):
    """
    减法运算函数
    
    从第一个数字开始，依次减去后续的所有数字。
    计算方式：args[0] - args[1] - args[2] - ...
    
    参数:
        args (list): 包含数字的列表，第一个数字为被减数，后续为减数
    
    返回值:
        str: 标准化后的减法结果字符串
    
    使用示例:
        >>> subtract_([10, 3, 2])
        "5"
        >>> subtract_([5.5, 1.5])
        "4"
    """

    res = args[0]
    for arg in args[1:]:
        res -= arg
    return normalize(res)

# 3. multiply
def multiply_(args):
    """
    乘法运算函数
    
    计算参数列表中所有数字的乘积。支持多个数字的连续乘法运算。
    
    参数:
        args (list): 包含数字的列表，如[2, 3, 4]
    
    返回值:
        str: 标准化后的乘法结果字符串
    
    使用示例:
        >>> multiply_([2, 3, 4])
        "24"
        >>> multiply_([1.5, 2])
        "3"
    """

    res = args[0]
    for arg in args[1:]:
        res *= arg
    return normalize(res)

# 4. divide
def divide_(args):
    """
    除法运算函数
    
    从第一个数字开始，依次除以后续的所有数字。
    计算方式：args[0] / args[1] / args[2] / ...
    
    参数:
        args (list): 包含数字的列表，第一个数字为被除数，后续为除数
    
    返回值:
        str: 标准化后的除法结果字符串
    
    使用示例:
        >>> divide_([12, 3, 2])
        "2"
        >>> divide_([7, 2])
        "3.5"
    
    注意:
        除数不能为0，否则会引发除零错误
    """

    res = args[0]
    for arg in args[1:]:
        res /= arg
    return normalize(res)

# 5. power
def power_(args):
    """
    幂运算函数
    
    从第一个数字开始，依次进行幂运算。
    计算方式：args[0] ** args[1] ** args[2] ** ...
    
    参数:
        args (list): 包含数字的列表，第一个数字为底数，后续为指数
    
    返回值:
        str: 标准化后的幂运算结果字符串
    
    使用示例:
        >>> power_([2, 3])
        "8"
        >>> power_([5, 2])
        "25"
        >>> power_([2, 3, 2])  # 2^(3^2) = 2^9 = 512
        "512"
    """
        
    res = args[0]
    for arg in args[1:]:
        res **= arg
    return normalize(res)

# 6. square root
def sqrt_(args):
    """
    平方根运算函数
    
    计算给定数字的平方根。
    
    参数:
        args (list): 包含一个数字的列表，该数字为需要开平方根的数
    
    返回值:
        str: 标准化后的平方根结果字符串
    
    使用示例:
        >>> sqrt_([9])
        "3"
        >>> sqrt_([2])
        "1.41"
        >>> sqrt_([16])
        "4"
    
    注意:
        输入的数字必须为非负数，否则会引发数学错误
    """
    res = args[0]
    return normalize(math.sqrt(res))

# 7. 10th log
def log_(args):
    """
    对数运算函数
    
    计算给定数字的对数。支持以10为底的常用对数和任意底数的对数。
    - 如果只传入一个参数，计算以10为底的对数
    - 如果传入两个参数，第二个参数作为底数
    
    参数:
        args (list): 包含1-2个数字的列表
                    - 一个参数：[真数] -> log10(真数)
                    - 两个参数：[真数, 底数] -> log_底数(真数)
    
    返回值:
        str: 标准化后的对数结果字符串
    
    使用示例:
        >>> log_([100])  # log10(100)
        "2"
        >>> log_([8, 2])  # log2(8)
        "3"
        >>> log_([1000])  # log10(1000)
        "3"
    
    异常:
        Exception: 当参数个数不是1或2时抛出异常
    
    注意:
        真数必须大于0，底数必须大于0且不等于1
    """
    # if only one argument is passed, it is 10th log
    if len(args) == 1:
        res = args[0]
        return normalize(math.log10(res))
    # if two arguments are passed, it is log with base as the second argument   
    elif len(args) == 2:
        res = args[0]
        base = args[1]
        return normalize(math.log(res, base))
    else:
        raise Exception("Invalid number of arguments passed to log function")

# 8. natural log
def ln_(args):
    """
    自然对数运算函数
    
    计算给定数字的自然对数（以e为底的对数）。
    
    参数:
        args (list): 包含一个数字的列表，该数字为真数
    
    返回值:
        str: 标准化后的自然对数结果字符串
    
    使用示例:
        >>> ln_([math.e])  # ln(e)
        "1"
        >>> ln_([1])  # ln(1)
        "0"
        >>> ln_([math.e**2])  # ln(e^2)
        "2"
    
    注意:
        输入的数字必须大于0，否则会引发数学错误
    """
    res = args[0]
    return normalize(math.log(res))


# 9. choose
def choose_(args):
    """
    组合数运算函数（C(n,r)）
    
    计算从n个不同元素中选择r个元素的组合数，也称为二项式系数。
    公式：C(n,r) = n! / (r! * (n-r)!)
    
    参数:
        args (list): 包含两个整数的列表 [n, r]
                    - n: 总元素个数
                    - r: 选择的元素个数
    
    返回值:
        str: 标准化后的组合数结果字符串
    
    使用示例:
        >>> choose_([5, 2])  # C(5,2)
        "10"
        >>> choose_([4, 1])  # C(4,1)
        "4"
        >>> choose_([6, 3])  # C(6,3)
        "20"
    
    注意:
        n >= r >= 0，且n和r都必须是非负整数
    """
    n = args[0]
    r = args[1]
    return normalize(math.comb(n, r))

# 10. permutation
def permutate_(args):
    """
    排列数运算函数（P(n,r)）
    
    计算从n个不同元素中选择r个元素进行排列的排列数。
    公式：P(n,r) = n! / (n-r)!
    
    参数:
        args (list): 包含两个整数的列表 [n, r]
                    - n: 总元素个数
                    - r: 选择并排列的元素个数
    
    返回值:
        str: 标准化后的排列数结果字符串
    
    使用示例:
        >>> permutate_([5, 2])  # P(5,2)
        "20"
        >>> permutate_([4, 1])  # P(4,1)
        "4"
        >>> permutate_([3, 3])  # P(3,3)
        "6"
    
    注意:
        n >= r >= 0，且n和r都必须是非负整数
    """
    n = args[0]
    r = args[1]
    return normalize(math.perm(n, r))

# 11. greatest common divisor
def gcd_(args):
    """
    最大公约数运算函数
    
    计算多个整数的最大公约数（Greatest Common Divisor）。
    支持计算两个或多个数字的最大公约数。
    
    参数:
        args (list): 包含整数的列表，如[12, 18, 24]
    
    返回值:
        str: 标准化后的最大公约数结果字符串
    
    使用示例:
        >>> gcd_([12, 18])  # gcd(12, 18)
        "6"
        >>> gcd_([24, 36, 48])  # gcd(24, 36, 48)
        "12"
        >>> gcd_([15, 25, 35])  # gcd(15, 25, 35)
        "5"
    
    注意:
        所有输入的数字都应该是正整数
    """
    res = args[0]
    for arg in args[1:]:
        res = math.gcd(res, arg)
    return normalize(res)

# 12. least common multiple
def lcm_(args):
    """
    最小公倍数运算函数
    
    计算多个整数的最小公倍数（Least Common Multiple）。
    支持计算两个或多个数字的最小公倍数。
    
    参数:
        args (list): 包含整数的列表，如[4, 6, 8]
    
    返回值:
        str: 标准化后的最小公倍数结果字符串
    
    使用示例:
        >>> lcm_([4, 6])  # lcm(4, 6)
        "12"
        >>> lcm_([3, 4, 5])  # lcm(3, 4, 5)
        "60"
        >>> lcm_([6, 8, 12])  # lcm(6, 8, 12)
        "24"
    
    注意:
        所有输入的数字都应该是正整数
    """
    res = args[0]
    for arg in args[1:]:
        res = res * arg // math.gcd(res, arg)
    return normalize(res)

# 13. remainder
def remainder_(args):
    """
    求余运算函数（取模运算）
    
    计算第一个数字除以第二个数字的余数。
    计算方式：args[0] % args[1]
    
    参数:
        args (list): 包含两个数字的列表 [被除数, 除数]
                    - 被除数: 要被除的数字
                    - 除数: 用来除的数字
    
    返回值:
        str: 标准化后的余数结果字符串
    
    使用示例:
        >>> remainder_([10, 3])  # 10 % 3
        "1"
        >>> remainder_([17, 5])  # 17 % 5
        "2"
        >>> remainder_([8, 4])   # 8 % 4
        "0"
    
    注意:
        除数不能为0，否则会引发除零错误
    """
    dividend = args[0]
    divisor = args[1]
    return normalize(dividend % divisor)