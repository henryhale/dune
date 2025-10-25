from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas


def display_class_distribution(df: pandas.DataFrame):
    """
    Plot the distribution os each class on a graph
    """
    plt.figure(figsize=(20, 10))
    sns.countplot(data=df, x="label")
    plt.title("Distribution of Command Classes")
    plt.xlabel("Command Class")
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def evaluate_set(y_true, y_pred, labels):
    """
    Evaluate the model on a given set of data(validation or testing)
    """
    print("classification report (validation set):")
    report = classification_report(
        y_true,
        y_pred,
        zero_division=0,
        target_names=labels,
        # output_dict=True,
    )
    print(f"{report}")

    accuracy = accuracy_score(y_true, y_pred)
    print(f"overall accuracy (validation set): {accuracy:.4f}")

    plt.figure(figsize=(20, 10))
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", xticks_rotation=90)
    plt.title(f"confusion matrix (accuracy: {accuracy:.4f})")
    plt.tight_layout()
    plt.show()
