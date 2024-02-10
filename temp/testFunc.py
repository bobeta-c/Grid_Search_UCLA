def minPastMid(timeStamp):
    if(int(timeStamp[0]) >= 8):
        return int(timeStamp[0])*60 + int(timeStamp[2:])
    elif(len(timeStamp) == 4):
         return int(timeStamp[0])*60 + 12*60 + int(timeStamp[2:])
    else:
        return int(timeStamp[0:2])*60 + int(timeStamp[3:])
    return -1

print(minPastMid("9:30"))
print(minPastMid("3:19"))
print(minPastMid("12:57"))
print(minPastMid("1:30"))
