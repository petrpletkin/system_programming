def invert_and_sum():
    arr = [0, 254, 126, 126, 126, 126, 126, 126, 126, 254]
    sum_val = sum([val if not (val & (1<<7)) else (~val & 0xFF) for val in arr])
    print(sum_val)

if __name__ == '__main__':
    import dis
    print(dis.dis(invert_and_sum))