"""Train the chatbot model and report accuracy.

Run:  python train.py
"""
from sklearn.model_selection import StratifiedKFold, cross_val_score

from chatbot_engine import MODEL_PATH, build_pipeline, get_training_data, load_intents, train_and_save


def main():
    data = load_intents()
    texts, labels = get_training_data(data)
    print(f"Intents: {len(data['intents'])} | Training sentences: {len(texts)}")

    # 4-fold cross validation: train on 3/4 of the sentences, test on unseen 1/4.
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    scores = cross_val_score(build_pipeline(), texts, labels, cv=cv)
    print(f"Cross-validation accuracy: {scores.mean() * 100:.1f}% (+/- {scores.std() * 100:.1f})")

    train_and_save()
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
