
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,f1_score, classification_report, confusion_matrix)

file_path = input("Enter CSV file path: ")
df = pd.read_csv(file_path)
print("\nColumns:", list(df.columns))

target = input("\nEnter the target column (output variable): ")

id_cols = [col for col in df.columns if col.lower() in ['id', 'index', 'row', 'rowid', 'row_id']]
if id_cols:
    print(f"\n  WARNING: Auto-dropping ID column(s): {id_cols}")
    print("     Reason: ID columns are just row numbers and cause fake 100% accuracy.")
    df = df.drop(columns=id_cols)

choice = input("\nUse all columns as features? (yes/no): ").lower()
if choice == "yes":
    X = df.drop(columns=[target])
else:
    print("\nAvailable columns:", list(df.columns))
    cols = input("Enter feature columns separated by commas: ")
    selected_cols = [col.strip() for col in cols.split(",")]
    X = df[selected_cols]

y = df[target]


X = pd.get_dummies(X)


train_percent = float(input("\nEnter training percentage (e.g., 80 for 80%): "))
test_size = 1 - (train_percent / 100)


while True:
    try:
        n_estimators = int(input("\nEnter number of estimators / trees (e.g., 100): "))
        if n_estimators > 0:
            break
        print("  Please enter a positive integer.")
    except ValueError:
        print("  Invalid input. Please enter a whole number.")

print("\nSelect criterion (splitting metric):")
print("  1 -> Gini Impurity")
print("  2 -> Entropy (Information Gain)")
while True:
    criterion_choice = input("Enter choice (1/2): ").strip()
    if criterion_choice == "1":
        criterion = "gini"
        break
    elif criterion_choice == "2":
        criterion = "entropy"
        break
    else:
        print("  Invalid choice. Enter 1, or 2.")

print(f"\n  Estimators : {n_estimators}")
print(f"  Criterion  : {criterion}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42, stratify=y
)

print(f"  Training samples : {len(X_train)}")
print(f"  Testing samples  : {len(X_test)}")

print("\n  Training Random Forest... please wait.")
model = RandomForestClassifier(
    n_estimators=n_estimators,
    criterion=criterion,
    random_state=42
)
model.fit(X_train, y_train)
print("  Training complete!")

y_pred = model.predict(X_test)

accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall    = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1        = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print("\n" + "="*50)
print("  Model Performance")
print("="*50)
print(f"  Estimators : {n_estimators}")
print(f"  Criterion  : {criterion}")
print(f"  Training % : {train_percent:.0f}%")
print(f"  Testing %  : {100 - train_percent:.0f}%")
print(f"  Accuracy   : {round(accuracy, 4)}")
print(f"  Precision  : {round(precision, 4)}")
print(f"  Recall     : {round(recall, 4)}")
print(f"  F1 Score   : {round(f1, 4)}")
print("="*50)

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print("Confusion Matrix:")
print(f"\n  TN (True Negative)  : {tn}")
print(f"  FP (False Positive) : {fp}")
print(f"  FN (False Negative) : {fn}")
print(f"  TP (True Positive)  : {tp}")