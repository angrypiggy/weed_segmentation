import numpy as np
import yaml
# ret = np.empty((10, 10))
# for i in range(10):
#   ret[i] = np.arange(10)

# np.savetxt("list.txt", ret, newline="\n", fmt="%3d")
# ret = [[1],
#        [2, 3],
#        [4, 5, 6]]
# with open('list.txt', 'w') as f:
#   for item in ret:
#     f.write("\n" % item)

# data = np.loadtxt("list.txt")
# print(data)

# print(np.array(ret, dtype=object))

# ret = {'a':1, 'b':2}
# with open("yaml_test.txt", 'w') as f:
#   yaml.dump(ret, f)

data = np.loadtxt("boxes.txt")
print(data.shape)