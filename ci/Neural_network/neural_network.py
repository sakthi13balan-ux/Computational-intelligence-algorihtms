import numpy as np

# ---------- Activation Functions ----------
def step_binary(x, threshold):
    return np.where(x >= threshold, 1, 0)

def step_bipolar(x, threshold):
    return np.where(x >= threshold, 1, -1)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

# ---------- Input Mode ----------
print("Select Input Mode:")
print("1. CSV Dataset")
print("2. Manual Input")

mode = int(input("Enter choice: "))

# ---------- CSV INPUT ----------
if mode == 1:
    file_path = input("Enter CSV file path: ")
    data = np.loadtxt(file_path, delimiter=',')

    X = data[:, :-1]
    t = data[:, -1]

    n, m = X.shape

# ---------- MANUAL INPUT ----------
else:
    m = int(input("Enter number of features: "))

    # Auto records = 2^features
    n = 2 ** m

    print(f"\nEnter {n} records")

    X = []
    t = []

    for i in range(n):
        values = list(map(float, input().split()))

        X.append(values[:-1])
        t.append(values[-1])

    X = np.array(X)
    t = np.array(t)

# ---------- Detect Data Type ----------
if set(np.unique(X)) <= {0, 1} and set(np.unique(t)) <= {0, 1}:
    data_type = "binary"
else:
    data_type = "bipolar"

# ---------- Activation ----------
print("\nChoose Activation Function:")
print("1. Step")
print("2. Sigmoid")
print("3. Tanh")

choice = int(input("Enter choice: "))

# ---------- Threshold ----------
threshold = float(input("Enter Threshold Value: "))

# ---------- Select Activation ----------
if choice == 1:
    activation = step_binary if data_type == "binary" else step_bipolar
elif choice == 2:
    activation = sigmoid
else:
    activation = tanh

# ---------- Initialize ----------
w = np.array(list(map(float, input(f"Enter {m} initial weights: ").split())))
b = float(input("Enter bias: "))
lr = float(input("Enter learning rate: "))
epochs = int(input("Enter number of epochs: "))

# ---------- Training ----------
print("\n" + "-"*120)
print("Inputs\tTarget\tOutput\tYin\tΔW\tΔb\tWeights\tBias")
print("-"*120)

for epoch in range(epochs):

    print(f"\nEpoch {epoch+1}")

    total_weight_change = 0

    for i in range(n):

        # ---------- Yin ----------
        yin_i = np.dot(X[i], w) + b

        # ---------- Output ----------
        if choice == 1:
            y_i = activation(yin_i, threshold)

        elif choice == 2:
            y_raw = sigmoid(yin_i)
            y_i = 1 if y_raw >= threshold else 0

        else:
            y_raw = tanh(yin_i)
            y_i = 1 if y_raw >= threshold else -1

        # ---------- YOUR TARGET-ONLY UPDATE ----------
        if t[i] != y_i:
            dw_i = lr * t[i] * X[i]
            db_i = lr * t[i]
        else:
            dw_i = np.zeros_like(X[i])
            db_i = 0


        # ---------- Update ----------
        w += dw_i
        b += db_i

        # ---------- Convergence ----------
        total_weight_change += np.sum(np.abs(dw_i)) + abs(db_i)

        # ---------- Print ----------
        w_str = "[" + " ".join(f"{val:.2f}" for val in w) + "]"

        print(f"{X[i]}\t{t[i]:.2f}\t{y_i:.2f}\t{yin_i:.2f}\t"
              f"{dw_i}\t{db_i:.2f}\t{w_str}\t{b:.2f}")

    # ---------- Stop if No Change ----------
    if total_weight_change == 0:
        print("\nConverged Since no update in change in weight!")
        break

else:
    print("\nDid not converge within given epochs.")

# ---------- Final Output ----------
print("\nFinal Weights:", w)
print("Final Bias:", b)