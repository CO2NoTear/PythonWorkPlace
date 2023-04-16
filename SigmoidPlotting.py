import matplotlib.pyplot as plt
import numpy as np
size = 1000

x = np.linspace(-3,3, num=size)
y = np.concatenate((np.full(size//2,0), np.full(size//2, 1)), axis=None)
def sigmoid(x, alpha):
    return 1/(1+np.exp(-x*alpha))

y_alpha_5 = sigmoid(x,5)
y_alpha_10 = sigmoid(x,10)
y_alpha_50 = sigmoid(x,50)

plt.figure(dpi=200)
plt.plot(x, y, label=r"$\Theta(x)$")
plt.plot(x, y_alpha_5, label=r"$\Theta(\alpha x)$, $\alpha=5$", linestyle="--")
plt.plot(x, y_alpha_10, label=r"$\Theta(\alpha x)$, $\alpha=10$", linestyle="--")
plt.plot(x, y_alpha_50, label=r"$\Theta(\alpha x)$, $\alpha=50$", linestyle="--")
plt.axhline(y=0.5, c='gray', linestyle='--')
plt.legend()
plt.show()
