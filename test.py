numbers = [x for x in range(1000000+1)]

lucky = []



for i in numbers:
    i_str = str(i)
    
    if len(i_str) < 4:
        nuls = 6-len(i_str)
        i_str = ("0" * nuls) + i_str
        
    sum1 = int(i_str[0]) + int(i_str[1]) + int(i_str[2])
    sum2 = int(i_str[-1]) + int(i_str[-2]) + int(i_str[-3])
    if int(sum1) == int(sum2):
        lucky.append(i)
        
print(lucky)