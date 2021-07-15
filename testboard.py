a = [(1, 8, 14.0), [37, 42.2373, 'N'], [127, 7.7687, 'E'], [74, 85], 7, 7, 3, 1.25, 0.95, 1.57]
new = []
print(a[0][1])
print(a[0][2])


# new.extend(a[0])
# new.extend(a[1])
# new.extend(a[2])
# new.extend(a[3])
#
# for i in range(0, 4):
#     new.extend(a[i])
# for buf in a:
#     if len(new) < 11:
#         new.extend(buf)

new = [buf for buf in a if len(new) < 11]



# new.append(a[4])
# new.append(a[5])
# new.append(a[6])
# new.append(a[7])
# new.append(a[8])
# new.append(a[9])

print(new)