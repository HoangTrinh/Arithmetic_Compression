import decimal
from decimal import Decimal


def create_dictionary():
    """

    :return: probability table
    """
    # codewords dictionary size
    dict_size = 128
    decimal.getcontext().prec = 512
    # generate codeword : probability table
    codeword_table = {chr(i): [0, 0] for i in range(dict_size)}

    # first range (%)
    low = Decimal(0)
    high = Decimal(1) / Decimal(dict_size)

    for key, value in codeword_table.items():
        codeword_table[key] = [low, high]
        low = high
        high += Decimal(1) / Decimal(dict_size)

    return codeword_table


def encode(origin, codeword_table):
    """

    :param origin: string
    :param codeword_table: probability dictionary
    :return: code in real decimal form, length of origin, code in binary form
    """

    # encoding
    lower_bound = Decimal(0)
    upper_bound = Decimal(1)
    for character in origin:
        if character in codeword_table.keys():
            curr_range = Decimal(upper_bound - lower_bound)  # current range
            upper_bound = Decimal(lower_bound) + Decimal(curr_range * codeword_table[character][1])
            lower_bound = Decimal(lower_bound) + Decimal(curr_range * codeword_table[character][0])  # lower bound

    return lower_bound, len(origin), encode_generateor(lower_bound, upper_bound)


def encode_generateor(low, hight):
    """

    :param low: real number
    :param high: real number
    :return: code in binary form ( fraction part ) of a low <= code < hight
    """
    code = ["0", "."]  # Binary fractional number
    k = 2  # kth binary fraction bit

    value = GetBinaryFractionValue("".join(code))
    while (value < low):
        # Assign 1 to the kth binary fraction bit
        code.append('1')
        value = GetBinaryFractionValue("".join(code))
        if (value > hight):
            # Replace the kth bit by 0
            code[k] = '0'
        value = GetBinaryFractionValue("".join(code))
        k += 1
    return code


def GetBinaryFractionValue(binary_string):
    """

    :param binary_string: string in binary form
    :return: decimal value
    """
    value = Decimal(0)
    power = 1

    # Git the fraction bits after "."
    fraction = binary_string.split('.')[1]

    # Compute the formula value
    for i in fraction:
        value += Decimal((2 ** (-power)) * int(i))
        power += 1

    return value


def decode(compressed_data, origin_len, codeword_table):
    """

    :param compressed_data: real decimal / binary form in real practice
    :param origin_len: int
    :param codeword_table: probability dictionary
    :return: decompressed_data - string
    """

    # For limit computational, temporally ignore this code
    # compressed_data = '0.' + str(bin(compressed_data))
    # compressed_data = GetBinaryFractionValue(compressed_data)

    decompressed_data = ''

    # decoding
    while origin_len != len(decompressed_data):
        for key, value in codeword_table.items():

            if (Decimal(value[0]) <= Decimal(compressed_data) < Decimal(value[1])):
                decompressed_data += key
                lower_pound = Decimal(value[0])
                upper_pound = Decimal(value[1])
                curr_range = Decimal(upper_pound - lower_pound)
                compressed_data = Decimal((compressed_data - lower_pound) / curr_range)

    return decompressed_data
