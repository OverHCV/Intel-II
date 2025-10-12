# Clasificadores de sklearn


from settings.config import Keys
from settings.imports import (
    accuracy_score,
    f1_score,
    np,
    precision_score,
    recall_score,
)


def kfold_cross_validation(
    X,
    y,
    classifier_class,
    k_folds=Keys.CV_FOLDS,
    random_state=Keys.RANDOM_STATE,
    **classifier_kwargs,
):
    """
    Implementación de k-fold cross-validation usando numpy.

    JUSTIFICACIÓN:
    - Dividimos los datos en k particiones aproximadamente iguales
    - Para cada fold: entrenamos en (k-1) particiones y evaluamos en 1
    - Esto proporciona una estimación robusta del rendimiento con menor varianza que hold-out
    - k=10 es un estándar que balancea sesgo vs varianza en la estimación

    Parámetros:
    - X: características
    - y: etiquetas
    - classifier_class: clase del clasificador (ej: GaussianNB)
    - k_folds: número de folds
    - random_state: semilla para reproducibilidad
    - **classifier_kwargs: argumentos adicionales para el clasificador

    Retorna:
    - dict con métricas de cada fold y estadísticas agregadas
    """
    np.random.seed(random_state)

    # Crear índices aleatorios para las particiones
    n_samples = X.shape[0]
    indices = np.random.permutation(n_samples)

    # Calcular tamaños de los folds
    fold_sizes = np.full(k_folds, n_samples // k_folds, dtype=int)
    fold_sizes[: n_samples % k_folds] += 1

    # Crear los índices de cada fold
    fold_indices = []
    current = 0
    for size in fold_sizes:
        fold_indices.append(indices[current : current + size])
        current += size

    # Almacenar resultados de cada fold
    fold_results = []

    print(f"🔄 Ejecutando {k_folds}-fold Cross Validation...")
    print(f"📊 Muestras totales: {n_samples}")
    print(f"📋 Promedio por fold: {n_samples // k_folds}")

    for fold in range(k_folds):
        # Índices para entrenamiento (todos menos el fold actual)
        train_indices = np.concatenate(
            [fold_indices[i] for i in range(k_folds) if i != fold]
        )
        test_indices = fold_indices[fold]

        # Dividir datos
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        # Entrenar clasificador
        classifier = classifier_class(**classifier_kwargs)
        classifier.fit(X_train, y_train)

        # Hacer predicciones
        y_pred = classifier.predict(X_test)

        # Métricas para este fold
        fold_accuracy = accuracy_score(y_test, y_pred)
        fold_precision = precision_score(y_test, y_pred, average="macro")
        fold_recall = recall_score(y_test, y_pred, average="macro")
        fold_f1 = f1_score(y_test, y_pred, average="macro")

        fold_results.append(
            {
                "fold": fold + 1,
                "accuracy": fold_accuracy,
                "precision": fold_precision,
                "recall": fold_recall,
                "f1_score": fold_f1,
                "train_size": len(X_train),
                "test_size": len(X_test),
            }
        )

        print(
            f"  FOLD {fold + 1:2d}: ACC={fold_accuracy:.4f}, PREC={fold_precision:.4f}, REC={fold_recall:.4f}, F1={fold_f1:.4f}"
        )

    # Calcular estadísticas agregadas
    accuracies = [r["accuracy"] for r in fold_results]
    precisions = [r["precision"] for r in fold_results]
    recalls = [r["recall"] for r in fold_results]
    f1_scores = [r["f1_score"] for r in fold_results]

    results = {
        "fold_results": fold_results,
        "mean_accuracy": np.mean(accuracies),
        "std_accuracy": np.std(accuracies),
        "mean_precision": np.mean(precisions),
        "std_precision": np.std(precisions),
        "mean_recall": np.mean(recalls),
        "std_recall": np.std(recalls),
        "mean_f1": np.mean(f1_scores),
        "std_f1": np.std(f1_scores),
        "confidence_interval_accuracy": np.percentile(accuracies, [2.5, 97.5]),
    }

    print(f"\n📈 Resultados Agregados de {k_folds}-Fold CV:")
    print(
        f"  Accuracy:  {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}"
    )
    print(
        f"  Precision: {results['mean_precision']:.4f} ± {results['std_precision']:.4f}"
    )
    print(f"  Recall:    {results['mean_recall']:.4f} ± {results['std_recall']:.4f}")
    print(f"  F1-Score:  {results['mean_f1']:.4f} ± {results['std_f1']:.4f}")
    print(
        f"  IC 95% Accuracy: [{results['confidence_interval_accuracy'][0]:.4f}, {results['confidence_interval_accuracy'][1]:.4f}]"
    )

    return results
