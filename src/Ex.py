import matplotlib.pyplot as plt

# ข้อมูล PMF
x = [2, 3, 4, 5, 6, 7, 8, 9, 10]
pmf = [1/25, 2/25, 3/25, 4/25, 5/25, 4/25, 3/25, 2/25, 1/25]

# ข้อมูล CDF
cdf = [1/25, 3/25, 6/25, 10/25, 15/25, 19/25, 22/25, 24/25, 1]

# วาดกราฟ PMF
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.stem(x, pmf, use_line_collection=True)
plt.xlabel('X')
plt.ylabel('P(X = x)')
plt.title('PMF')

# วาดกราฟ CDF
plt.subplot(1, 2, 2)
plt.step(x, cdf, where='post')
plt.xlabel('X')
plt.ylabel('F_X(x)')
plt.title('CDF')

plt.tight_layout()
plt.show()