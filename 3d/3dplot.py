from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

f = open("./Pvap_with_Clen.csv", "r").readlines()
c = []
x = []
y = []
z = []
for l in f:
  compound, dev, aad, c_len = l.rstrip().split(',')
  c.append(compound)
  x.append(float(dev))
  y.append(float(aad))
  z.append(float(c_len))

ax.scatter(x, y, z, c='r', marker='o')

ax.set_xlabel("Relative Deviation")
ax.set_ylabel("AAD")
ax.set_zlabel("Chain Length")

plt.show()