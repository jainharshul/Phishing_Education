# phishing_model.py

import os
import numpy as np
import joblib

# These imports are needed if your keras/logreg pipeline uses them.
# The SVM pipeline does NOT need them, but having them here is harmless.
from custom_transformers import TextStats, CombinedFeatures

# ---------------------------------------------------------
# Load available models
# ---------------------------------------------------------

PIPELINES = {}


def _try_load(model_name, filename):
    """
    Load a pipeline from a .pkl file if it exists.
    """
    if not os.path.exists(filename):
        print(f"[phishing_model] File not found for '{model_name}': {filename}")
        return

    try:
        pipeline = joblib.load(filename)
        PIPELINES[model_name] = pipeline
        print(f"[phishing_model] Loaded '{model_name}' from {filename}")
    except Exception as e:
        print(f"[phishing_model] Failed to load '{model_name}' from {filename}: {e}")


# Adjust filenames if needed
_try_load("logreg", "phishing_pipeline.pkl")      # LogisticRegression pipeline
_try_load("svm", "phishing_pipeline_svm.pkl")     # Your SVM pipeline

if not PIPELINES:
    raise RuntimeError(
        "No model pipelines loaded. Make sure 'phishing_pipeline.pkl' or "
        "'phishing_pipeline_svm.pkl' are in the same directory."
    )

# Prefer SVM if available, otherwise fall back to logreg, otherwise first model
if "svm" in PIPELINES:
    DEFAULT_MODEL = "svm"
elif "logreg" in PIPELINES:
    DEFAULT_MODEL = "logreg"
else:
    DEFAULT_MODEL = next(iter(PIPELINES.keys()))

LABELS = {
    0: "Safe Email",
    1: "Phishing Email",
}


def _compute_proba(pipeline, text):
    """
    Return a probability-like vector [P(class 0), P(class 1)].

    - If the underlying classifier has predict_proba, use it.
    - Otherwise, use decision_function and convert scores to probabilities.
    """
    # Try normal predict_proba first (works for logreg pipeline)
    try:
        proba = pipeline.predict_proba([text])[0]
        return np.asarray(proba, dtype=float)
    except AttributeError:
        # Fall back to decision_function (works for SVC with probability=False)
        scores = pipeline.decision_function([text])
        scores = np.ravel(np.asarray(scores, dtype=float))

        if scores.size == 1:
            # Binary classification: single score (distance to hyperplane).
            logit = scores[0]
            p1 = 1.0 / (1.0 + np.exp(-logit))  # sigmoid
            p0 = 1.0 - p1
            return np.array([p0, p1], dtype=float)
        else:
            # Multi-class (just in case): softmax over scores
            scores = scores - np.max(scores)
            exps = np.exp(scores)
            probs = exps / np.sum(exps)
            return probs


def predict_email(text, model=None):
    """
    Use one of the trained pipelines to classify a single email.

    Parameters
    ----------
    text : str
        The email text to classify.
    model : {"svm", "logreg", None}, optional
        Which model to use. If None, uses DEFAULT_MODEL.

    Returns
    -------
    dict
        {
          "model_used": "svm" or "logreg",
          "label": "Safe Email" or "Phishing Email",
          "label_idx": 0 or 1,
          "probabilities": {
              "safe": float,
              "phishing": float,
          },
        }
    """
    # Choose which model to use
    if model is None:
        model = DEFAULT_MODEL

    if model not in PIPELINES:
        print(
            f"[phishing_model] Requested model '{model}' not loaded. "
            f"Falling back to '{DEFAULT_MODEL}'."
        )
        model = DEFAULT_MODEL

    pipeline = PIPELINES[model]

    # ✅ IMPORTANT: use helper that handles both logreg and SVM
    proba = _compute_proba(pipeline, text)

    # Expecting two classes: 0 (safe), 1 (phishing)
    if proba.shape[0] != 2:
        raise ValueError(
            f"Expected 2 classes (0,1) but got proba vector of shape {proba.shape}"
        )

    safe_prob = float(proba[0])
    phishing_prob = float(proba[1])

    label_idx = int(np.argmax(proba))  # 0 or 1
    label = LABELS.get(label_idx, f"Class {label_idx}")

    return {
        "model_used": model,
        "label": label,
        "label_idx": label_idx,
        "probabilities": {
            "safe": safe_prob,
            "phishing": phishing_prob,
        },
    }
