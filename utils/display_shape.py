import shapefile
import matplotlib.pyplot as plt
import numpy as np
# TODO Generalize

sf = shapefile.Reader("ITC_OSBS_003.dbf")
fig = plt.figure()
ax = fig.add_subplot(111)
# plt.xlim([76, 85])
# plt.ylim([12, 21])
max_norm = float('-inf')
# TODO Figure out Normalization: Not if output has to be a shape file with highlighted crowns
for shape in sf.shapes(): 
    x = np.array([i[0] for i in shape.points[:]])
    y = np.array([i[1] for i in shape.points[:]])
    max_norm = max(max_norm, x.max(), y.max())
# print (max_norm)

for shape in sf.shapes():
    x = np.array([i[0] for i in shape.points[:]])
    # x /= 3285346.226354544
    x /= max_norm
    y = np.array([i[1] for i in shape.points[:]])
    y /= max_norm
    print(x,y)
    plt.plot(x,y)

print("Displaying Polygons")
plt.show()

