import csv
import math
from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split as sk_split

def entropy(data, target_index):
    total = len(data)
    counts = Counter([row[target_index] for row in data])

    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)

    return ent


def gini(data, target_index):
    total = len(data)
    counts = Counter([row[target_index] for row in data])

    g = 1
    for count in counts.values():
        p = count / total
        g -= p ** 2

    return g

def information_gain(data, attr_index, target_index, method="entropy"):
    total = len(data)

    if method == "entropy":
        parent = entropy(data, target_index)
    else:
        parent = gini(data, target_index)

    subsets = defaultdict(list)
    for row in data:
        subsets[row[attr_index]].append(row)

    weighted_sum = 0

    for subset in subsets.values():
        weight = len(subset) / total

        if method == "entropy":
            subset_measure = entropy(subset, target_index)
        else:
            subset_measure = gini(subset, target_index)

        weighted_sum += weight * subset_measure

    gain = parent - weighted_sum
    return gain


def find_root(data, attributes, method):
    target_index = len(attributes) - 1
    gains = {}

    for i in range(target_index):
        gain = information_gain(data, i, target_index, method)
        gains[attributes[i]] = gain

    print("\nInformation Gains:")
    for k, v in gains.items():
        print(k, ":", round(v, 4))

    root = max(gains, key=gains.get)
    print("\nBest Root Node:", root)

    return root


def build_tree(data, attributes, method):
    target_index = len(attributes) - 1
    target_values = [row[target_index] for row in data]

    if len(set(target_values)) == 1:
        return target_values[0]

    if len(attributes) == 1:
        return Counter(target_values).most_common(1)[0][0]

    root = find_root(data, attributes, method)
    root_index = attributes.index(root)

    tree = {root: {}}
    values = set([row[root_index] for row in data])

    for value in values:
        subset = [row[:root_index] + row[root_index+1:]
                  for row in data if row[root_index] == value]

        new_attributes = attributes[:root_index] + attributes[root_index+1:]

        if not subset:
            tree[root][value] = Counter(target_values).most_common(1)[0][0]
        else:
            tree[root][value] = build_tree(subset, new_attributes, method)

    return tree


def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "->", tree)
        return

    for root, branches in tree.items():
        print(indent + "[" + root + "]")
        for value, subtree in branches.items():
            print(indent + "  ├─", value)
            print_tree(subtree, indent + "  │   ")

def predict_single(tree, attributes, record):
    if not isinstance(tree, dict):
        return tree

    root = list(tree.keys())[0]
    root_index = attributes.index(root)

    value = record[root_index]

    if value in tree[root]:
        subtree = tree[root][value]
        new_attributes = attributes[:root_index] + attributes[root_index+1:]
        new_record = record[:root_index] + record[root_index+1:]
        return predict_single(subtree, new_attributes, new_record)
    else:
        return None


def predict_dataset(tree, attributes, test_data):
    predictions = []
    actual = []

    target_index = len(attributes) - 1

    for row in test_data:
        actual.append(row[target_index])
        prediction = predict_single(tree, attributes, row)
        predictions.append(prediction)

    return actual, predictions

def calculate_metrics(actual, predicted):
    tp = fp = tn = fn = 0

    classes = list(set(actual))
    positive = classes[0]

    for a, p in zip(actual, predicted):
        if p is None:
            continue

        if a == positive and p == positive:
            tp += 1
        elif a != positive and p == positive:
            fp += 1
        elif a != positive and p != positive:
            tn += 1
        elif a == positive and p != positive:
            fn += 1

    total = tp + tn + fp + fn

    accuracy = (tp + tn) / total if total != 0 else 0
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    print("\n=========== MODEL PERFORMANCE ===========")
    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


def csv_mode():
    filename = input("Enter CSV filename: ")

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    attributes = data[0]
    data = data[1:]

    print("\nAvailable Columns:", attributes)
    class_field = input("Enter Class Field Name: ")

    if class_field not in attributes:
        print("Invalid class field name!")
        return
    class_index = attributes.index(class_field)
    attributes.append(attributes.pop(class_index))

    for row in data:
        row.append(row.pop(class_index))

    print("\nClass Field Selected:", class_field)

    method_choice = input("Choose method (entropy/gini): ").lower()
    method = "entropy" if method_choice == "entropy" else "gini"

    training_percent = float(input("Enter Training Percentage: "))
    test_size = 1 - (training_percent / 100)

    train_data, test_data = sk_split(data, test_size=test_size, random_state=42)

    print("\nTraining Records:", len(train_data))
    print("Testing Records :", len(test_data))

    tree = build_tree(train_data, attributes, method)

    print("\n=========== FINAL DECISION TREE ===========")
    print_tree(tree)

    actual, predicted = predict_dataset(tree, attributes, test_data)

   # print("\nActual Values   :", actual)
    #print("Predicted Values:", predicted)

    calculate_metrics(actual, predicted)


def manual_mode():
    n = int(input("Enter number of attributes (including class label): "))

    attributes = []
    for i in range(n):
        attributes.append(input(f"Enter name of attribute {i+1}: "))

    print("\nAvailable Attributes:", attributes)

    class_field = input("Enter Class Field Name: ")

    if class_field not in attributes:
        print("Invalid class field name!")
        return
    
    class_index = attributes.index(class_field)
    attributes.append(attributes.pop(class_index))

    m = int(input("\nEnter number of training records: "))

    data = []
    for i in range(m):
        print(f"\nEnter values for record {i+1}:")
        row = []
        for attr in attributes:
            row.append(input(f"{attr}: "))
        data.append(row)

    method_choice = input("\nChoose method (entropy/gini): ").lower()
    method = "entropy" if method_choice == "entropy" else "gini"

    tree = build_tree(data, attributes, method)

    print("\n=========== FINAL DECISION TREE ===========")
    print_tree(tree)


def main():
    print("1. Manual Mode")
    print("2. CSV Mode")

    choice = input("Choose option (1/2): ")

    if choice == "1":
        manual_mode()
    elif choice == "2":
        csv_mode()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()