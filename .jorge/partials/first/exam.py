"""
# **Primer Parcial - Sistemas Inteligentes II**

## **Jorge Alberto Jaramillo Garzón**
### **Universidad de Caldas**

---

## **ENUNCIADO DEL PARCIAL:**

1. **(1.5) Ejercicio 1**: Implemente el procedimiento de validación cruzada de 10 particiones y úselo para determinar el desempeño de un clasificador bayesiano con distribución gaussiana sobre la base de datos Iris (considere solamente las clases setosa y versicolor pero use todas las características). Repita el procedimiento para un clasificador geométrico por mínimos cuadrados. ¿Qué diferencias encuentra? Documente los pasos, pruebas, errores y ajustes que realizó hasta obtener los resultados finales.

2. **(1.0) Ejercicio 2**: Implemente el clasificador K-NN sobre la base de datos Iris (usando las cuatro características y las tres clases) e investigue su desempeño mediante el método de bootstrapping a medida que se aumenta el número de vecinos empleado. Proponga una estrategia práctica de selección de k si este algoritmo se usara en un caso real con datos de otra naturaleza.

3. **(1.0) Ejercicio 3**: Compare y contraste los tres clasificadores vistos en clase (geométrico, bayesiano y K-NN) según los siguientes criterios: ¿Qué suposiciones hace cada uno de los modelos? ¿Cuáles son sus requerimientos de entrenamiento en términos de tiempo de cómputo y memoria? ¿Cómo cambiará el desempeño de cada uno cuando se aumenta el número de dimensiones del espacio de características? Relacione cada clasificador con un ejemplo realista de aplicación (puede ser del contexto colombiano o de su experiencia personal).

4. **(1.5) Ejercicio 4**: Sustentación oral en horario de clase.

**Entregable:** Un notebook de Jupyter con código, salidas y comentarios personales. Puede emplear las librerías que considere pertinentes para la implementación de los modelos de aprendizaje de máquina, excepto para las estrategias de validación.

---

El código está diseñado para ser **modular y verificable**, siguiendo las mejores prácticas de documentación y análisis estadístico.
"""

"""
## **1. Configuración del Experimento**

Esta sección centraliza todos los parámetros configurables para facilitar modificaciones durante la sustentación. El diseño modular permite cambiar rápidamente el dataset, características, clases objetivo, y parámetros de evaluación.
"""


class IrisNames:
    SETOSA = "Iris-setosa"
    VERSICOLOR = "Iris-versicolor"
    VIRGINICA = "Iris-virginica"


class IrisFeatures:
    SEPAL_LENGTH = "SepalLengthCm"
    SEPAL_WIDTH = "SepalWidthCm"
    PETAL_LENGTH = "PetalLengthCm"
    PETAL_WIDTH = "PetalWidthCm"


class IrisTarget:
    SPECIES = "Species"


class Keys:
    DATASET_PATH = "dataset_path"
    FEATURE_COLUMNS = "feature_columns"
    TARGET_COLUMN = "target_column"
    EXERCISE1_CLASSES = "exercise1_classes"
    EXERCISE2_CLASSES = "exercise2_classes"
    CV_FOLDS = "cv_folds"
    BOOTSTRAP_ITERATIONS = "bootstrap_iterations"
    KNN_K_RANGE = "knn_k_range"
    RANDOM_STATE = "random_state"
    TEST_SIZE = "test_size"
    CONFIDENCE_LEVEL = "confidence_level"
    HISTOGRAM_BINS = "histogram_bins"
    FIGURE_SIZE_LARGE = "figure_size_large"
    FIGURE_SIZE_MEDIUM = "figure_size_medium"
    ALPHA_TRANSPARENCY = "alpha_transparency"
    GRID_ALPHA = "grid_alpha"
    CLASS_COLORS = "class_colors"
    COMPARISON_COLORS = "comparison_colors"
    VARIABILITY_THRESHOLD = "variability_threshold"
    PROGRESS_MILESTONES = "progress_milestones"
    SIGNIFICANCE_ALPHA = "significance_alpha"
    PCA_COMPONENTS = "pca_components"
    DATASET_ENCODING = "dataset_encoding"
    DECIMAL_PRECISION = "decimal_precision"


# Configuración centralizada
CONFIG = {
    # Dataset y características
    Keys.DATASET_PATH: "dataset-iris.csv",
    Keys.FEATURE_COLUMNS: [
        IrisFeatures.SEPAL_LENGTH,
        IrisFeatures.SEPAL_WIDTH,
        IrisFeatures.PETAL_LENGTH,
        IrisFeatures.PETAL_WIDTH,
    ],
    Keys.TARGET_COLUMN: IrisTarget.SPECIES,
    # Configuración específica por ejercicio
    Keys.EXERCISE1_CLASSES: [
        IrisNames.SETOSA,
        IrisNames.VERSICOLOR,
    ],
    Keys.EXERCISE2_CLASSES: [
        IrisNames.SETOSA,
        IrisNames.VERSICOLOR,
        IrisNames.VIRGINICA,
    ],
    # Parámetros de evaluación
    Keys.CV_FOLDS: 20,  # Número de folds para validación cruzada
    Keys.BOOTSTRAP_ITERATIONS: 1000,  # Iteraciones para bootstrapping (robusto para análisis)
    Keys.KNN_K_RANGE: list(range(1, 31)),  # Rango de análisis
    #
    # Configuración general
    #
    Keys.RANDOM_STATE: 42,  # Para reproducibilidad
    Keys.TEST_SIZE: 0.3,  # Proporción para conjunto de prueba
    Keys.CONFIDENCE_LEVEL: 0.95,  # Nivel de confianza para intervalos
    # Umbrales y parámetros adicionales
    Keys.VARIABILITY_THRESHOLD: 0.001,  # Umbral para detectar variabilidad
    Keys.PROGRESS_MILESTONES: 10,  # Cada cuánto mostrar progreso (%)
    Keys.SIGNIFICANCE_ALPHA: 0.05,  # Nivel de significancia estadística
    Keys.PCA_COMPONENTS: 2,  # Componentes PCA para visualización
    # Parámetros de visualización
    Keys.HISTOGRAM_BINS: 15,  # Número de bins para histogramas
    Keys.FIGURE_SIZE_LARGE: (15, 10),  # Tamaño de figuras grandes
    Keys.FIGURE_SIZE_MEDIUM: (12, 8),  # Tamaño de figuras medianas
    Keys.ALPHA_TRANSPARENCY: 0.7,  # Transparencia para gráficos
    Keys.GRID_ALPHA: 0.3,  # Transparencia para grillas
    # Colores para clases
    Keys.CLASS_COLORS: ["skyblue", "lightcoral", "lightgreen"],
    Keys.COMPARISON_COLORS: ["lightblue", "lightgreen", "lightcoral"],
    # Textos configurables
    Keys.DATASET_ENCODING: "utf-8",  # Codificación del dataset
    Keys.DECIMAL_PRECISION: 4,  # Precisión decimal para reportes
}

print("✓ Configuración cargada exitosamente")
print(f"Dataset: {CONFIG[Keys.DATASET_PATH]}")
print(f"Características: {CONFIG[Keys.FEATURE_COLUMNS]}")
print(f"Clases Ejercicio 1: {CONFIG[Keys.EXERCISE1_CLASSES]}")
print(f"Clases Ejercicio 2: {CONFIG[Keys.EXERCISE2_CLASSES]}")
print(f"CV Folds: {CONFIG[Keys.CV_FOLDS]}")
print(f"Bootstrap Iteraciones: {CONFIG[Keys.BOOTSTRAP_ITERATIONS]}")
print(
    f"Rango K para K-NN: {min(CONFIG[Keys.KNN_K_RANGE])}-{max(CONFIG[Keys.KNN_K_RANGE])}"
)

"""
## **2. Imports y Librerías**

Importamos las librerías necesarias. Los clasificadores usarán sklearn según lo permitido, pero los evaluadores (k-fold CV y bootstrapping) serán implementados manualmente con numpy.
"""

# Librerías fundamentales
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")

# Clasificadores de sklearn
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Métricas y utilidades de sklearn (solo para métricas, no para evaluación)
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Configuración de visualización
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 10

print("✓ Todas las librerías importadas exitosamente")
print("📊 Configuración de visualización establecida")
print(
    "🔧 Clasificadores disponibles: GaussianNB, LinearDiscriminantAnalysis, KNeighborsClassifier"
)

"""
## **3. Funciones Utilitarias**

Implementamos funciones modulares y agnósticas al dataset para facilitar la experimentación y modificaciones durante la sustentación.
"""


def load_and_prepare_data(
    config: dict[str, str | int | float | list[str] | list[int]], classes=None
):
    """
    Carga y prepara los datos de forma agnóstica al dataset.

    Parámetros:
    - config: diccionario de configuración
    - classes: lista de clases a incluir (None para todas)

    Retorna:
    - X: características normalizadas
    - y: etiquetas codificadas
    - feature_names: nombres de las características
    - class_names: nombres de las clases
    - scaler: objeto scaler usado para normalización
    - label_encoder: codificador de etiquetas
    """
    # Cargar datos
    data = pd.read_csv(config["dataset_path"])

    # Filtrar clases si se especifica
    if classes is not None:
        data = data[data[config["target_column"]].isin(classes)]

    # Extraer características y etiquetas
    X = data[config["feature_columns"]].values
    y = data[config["target_column"]].values

    # Normalizar características (importante para algunos clasificadores)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Codificar etiquetas
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return (
        X_scaled,
        y_encoded,
        config["feature_columns"],
        label_encoder.classes_,
        scaler,
        label_encoder,
    )


def calculate_comprehensive_metrics(y_true, y_pred, class_names):
    """
    Calcula métricas comprehensivas para evaluación de clasificadores.

    Parámetros:
    - y_true: etiquetas verdaderas
    - y_pred: predicciones
    - class_names: nombres de las clases

    Retorna:
    - dict con todas las métricas calculadas
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro"),
        "recall_macro": recall_score(y_true, y_pred, average="macro"),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "precision_micro": precision_score(y_true, y_pred, average="micro"),
        "recall_micro": recall_score(y_true, y_pred, average="micro"),
        "f1_micro": f1_score(y_true, y_pred, average="micro"),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
        "classification_report": classification_report(
            y_true, y_pred, target_names=class_names
        ),
    }
    return metrics


def print_metrics_summary(metrics, classifier_name):
    """Imprime un resumen bonito de las métricas."""
    print(f"\n📊 **Métricas para {classifier_name}**")
    print(f"{'─' * 50}")
    print(f"Accuracy:        {metrics['accuracy']:.4f}")
    print(f"Precision (Macro): {metrics['precision_macro']:.4f}")
    print(f"Recall (Macro):    {metrics['recall_macro']:.4f}")
    print(f"F1-Score (Macro):  {metrics['f1_macro']:.4f}")
    print(f"{'─' * 50}")


print("✓ Funciones utilitarias definidas:")
print("  - load_and_prepare_data(): Carga agnóstica de datos")
print("  - calculate_comprehensive_metrics(): Métricas comprehensivas")
print("  - print_metrics_summary(): Resumen de métricas")


"""
## **4. Evaluadores Manuales**

Implementamos los evaluadores (k-fold CV y bootstrapping) manualmente usando numpy, según los requerimientos. Estos son fundamentales para los ejercicios 1 y 2.
"""


def manual_kfold_cv(
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
    print(f"📊 Total de muestras: {n_samples}")
    print(f"📋 Tamaño promedio por fold: {n_samples // k_folds}")

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
            f"  Fold {fold + 1:2d}: Acc={fold_accuracy:.4f}, Prec={fold_precision:.4f}, Rec={fold_recall:.4f}, F1={fold_f1:.4f}"
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

    print(f"\n📈 **Resultados Agregados de {k_folds}-fold CV:**")
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


print("✓ Función manual_kfold_cv implementada")


def manual_bootstrap(
    X, y, classifier_class, n_iterations=1000, random_state=42, **classifier_kwargs
):
    """
    Implementación de bootstrapping usando numpy.

    TECNICISMOS:
    - Bootstrapping genera múltiples muestras con reemplazo del dataset original
    - Cada muestra bootstrap tiene el mismo tamaño que el dataset original
    - Evaluamos en muestras out-of-bag (datos no seleccionados en el bootstrap)
    - Proporciona estimación robusta de la distribución del rendimiento
    - Útil para construir intervalos de confianza y analizar estabilidad

    Parámetros:
    - X: características
    - y: etiquetas
    - classifier_class: clase del clasificador
    - n_iterations: número de iteraciones bootstrap
    - random_state: semilla para reproducibilidad
    - **classifier_kwargs: argumentos adicionales para el clasificador

    Retorna:
    - dict con resultados de cada iteración y estadísticas agregadas
    """
    np.random.seed(random_state)
    n_samples = X.shape[0]

    bootstrap_results = []

    print(f"🔄 Ejecutando Bootstrapping con {n_iterations} iteraciones...")
    print(f"📊 Total de muestras: {n_samples}")

    # Progreso cada 10% de las iteraciones
    progress_milestones = [int(n_iterations * p / 10) for p in range(1, 11)]

    for iteration in range(n_iterations):
        # Crear muestra bootstrap (con reemplazo)
        bootstrap_indices = np.random.choice(n_samples, size=n_samples, replace=True)

        # Identificar muestras out-of-bag (no seleccionadas)
        oob_indices = np.setdiff1d(np.arange(n_samples), bootstrap_indices)

        # Si no hay muestras out-of-bag, skip esta iteración (muy raro)
        if len(oob_indices) == 0:
            continue

        # Dividir datos
        X_bootstrap, y_bootstrap = X[bootstrap_indices], y[bootstrap_indices]
        X_oob, y_oob = X[oob_indices], y[oob_indices]

        # Entrenar clasificador en muestra bootstrap
        classifier = classifier_class(**classifier_kwargs)
        classifier.fit(X_bootstrap, y_bootstrap)

        # Evaluar en datos out-of-bag
        y_pred = classifier.predict(X_oob)

        # Calcular métricas
        try:
            iteration_accuracy = accuracy_score(y_oob, y_pred)
            iteration_precision = precision_score(y_oob, y_pred, average="macro")
            iteration_recall = recall_score(y_oob, y_pred, average="macro")
            iteration_f1 = f1_score(y_oob, y_pred, average="macro")

            bootstrap_results.append(
                {
                    "iteration": iteration + 1,
                    "accuracy": iteration_accuracy,
                    "precision": iteration_precision,
                    "recall": iteration_recall,
                    "f1_score": iteration_f1,
                    "bootstrap_size": len(X_bootstrap),
                    "oob_size": len(X_oob),
                }
            )
        except:
            # Skip iteraciones con problemas (ej: solo una clase en OOB)
            continue

        # Mostrar progreso
        if (iteration + 1) in progress_milestones:
            progress = int(((iteration + 1) / n_iterations) * 100)
            print(
                f"  Progreso: {progress}% ({iteration + 1}/{n_iterations} iteraciones)"
            )

    # Calcular estadísticas agregadas
    if not bootstrap_results:
        raise ValueError("No se pudieron completar iteraciones bootstrap válidas")

    accuracies = [r["accuracy"] for r in bootstrap_results]
    precisions = [r["precision"] for r in bootstrap_results]
    recalls = [r["recall"] for r in bootstrap_results]
    f1_scores = [r["f1_score"] for r in bootstrap_results]

    # Intervalos de confianza usando percentiles
    confidence_level = 0.95
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100

    results = {
        "bootstrap_results": bootstrap_results,
        "n_valid_iterations": len(bootstrap_results),
        "mean_accuracy": np.mean(accuracies),
        "std_accuracy": np.std(accuracies),
        "median_accuracy": np.median(accuracies),
        "mean_precision": np.mean(precisions),
        "std_precision": np.std(precisions),
        "mean_recall": np.mean(recalls),
        "std_recall": np.std(recalls),
        "mean_f1": np.mean(f1_scores),
        "std_f1": np.std(f1_scores),
        "confidence_interval_accuracy": np.percentile(
            accuracies, [lower_percentile, upper_percentile]
        ),
        "confidence_interval_f1": np.percentile(
            f1_scores, [lower_percentile, upper_percentile]
        ),
    }

    print(f"\n📈 **Resultados Agregados del Bootstrapping:**")
    print(f"  Iteraciones válidas: {results['n_valid_iterations']}/{n_iterations}")
    print(
        f"  Accuracy:  {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f} (mediana: {results['median_accuracy']:.4f})"
    )
    print(
        f"  Precision: {results['mean_precision']:.4f} ± {results['std_precision']:.4f}"
    )
    print(f"  Recall:    {results['mean_recall']:.4f} ± {results['std_recall']:.4f}")
    print(f"  F1-Score:  {results['mean_f1']:.4f} ± {results['std_f1']:.4f}")
    print(
        f"  IC 95% Accuracy: [{results['confidence_interval_accuracy'][0]:.4f}, {results['confidence_interval_accuracy'][1]:.4f}]"
    )
    print(
        f"  IC 95% F1-Score: [{results['confidence_interval_f1'][0]:.4f}, {results['confidence_interval_f1'][1]:.4f}]"
    )

    return results


print("✓ Función manual_bootstrap implementada")

"""
## **5. Funciones de Visualización Mejoradas**

Funciones especializadas para crear visualizaciones informativas, incluyendo casos donde hay poca variabilidad en los resultados.
"""


def plot_normalized_distributions(X, y, feature_names, class_names, config):
    """
    Crear histogramas de distribuciones normalizadas con explicación clara.

    NOTA IMPORTANTE sobre normalización:
    - StandardScaler centra los datos en media=0 y escala por desviación estándar
    - Valores negativos = por debajo de la media general
    - Valores positivos = por encima de la media general
    - Esto NO significa valores "negativos" literales, solo posición relativa
    """
    fig, axes = plt.subplots(2, 2, figsize=config[Keys.FIGURE_SIZE_LARGE])
    fig.suptitle("Distribución de Características Normalizadas por Clase", fontsize=16)

    colors = config[Keys.CLASS_COLORS][: len(class_names)]

    for i, feature in enumerate(feature_names):
        ax = axes[i // 2, i % 2]

        for j, class_name in enumerate(class_names):
            class_data = X[y == j, i]
            label = class_name.split("-")[1] if "Iris-" in class_name else class_name
            ax.hist(
                class_data,
                alpha=config[Keys.ALPHA_TRANSPARENCY],
                bins=config[Keys.HISTOGRAM_BINS],
                color=colors[j],
                label=label,
            )

        ax.set_title(f"{feature}")
        ax.set_xlabel("Valor Normalizado (μ=0, σ=1)")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        ax.grid(True, alpha=config[Keys.GRID_ALPHA])
        ax.axvline(x=0, color="black", linestyle="--", alpha=0.5, label="Media=0")

    plt.tight_layout()

    # Agregar nota explicativa
    fig.text(
        0.5,
        0.02,
        "💡 Normalización: (-) = debajo de la media general | (+) = por encima",
        ha="center",
        fontsize=10,
        style="italic",
    )

    plt.show()


def create_comparison_visualization(results1, results2, name1, name2, config):
    """
    Crear visualización de comparación que maneja el caso de poca variabilidad.

    Si ambos clasificadores tienen varianza 0 (accuracy perfecta),
    usa visualizaciones alternativas más informativas.
    """
    # Extraer datos
    metrics = ["accuracy", "precision", "recall", "f1_score"]
    metric_names = ["Accuracy", "Precision", "Recall", "F1-Score"]

    values1 = [[r[metric] for r in results1["fold_results"]] for metric in metrics]
    values2 = [[r[metric] for r in results2["fold_results"]] for metric in metrics]

    # Verificar si hay variabilidad (usando umbral configurable)
    has_variability = any(
        np.std(vals) > config["variability_threshold"] for vals in values1 + values2
    )

    if has_variability:
        # Crear boxplots normales
        fig, axes = plt.subplots(2, 2, figsize=config["figure_size_large"])
        fig.suptitle(f"Comparación: {name1} vs {name2}", fontsize=16)

        for i, (vals1, vals2, name) in enumerate(zip(values1, values2, metric_names)):
            ax = axes[i // 2, i % 2]

            data_to_plot = [vals1, vals2]
            box = ax.boxplot(
                data_to_plot, labels=[name1, name2], patch_artist=True, notch=True
            )

            colors = config["comparison_colors"][:2]
            for patch, color in zip(box["boxes"], colors):
                patch.set_facecolor(color)

            ax.set_title(f"{name}")
            ax.set_ylabel(name)
            ax.grid(True, alpha=config["grid_alpha"])

            # Agregar valores medios
            ax.text(
                1,
                np.mean(vals1),
                f"{np.mean(vals1):.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )
            ax.text(
                2,
                np.mean(vals2),
                f"{np.mean(vals2):.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )
    else:
        # Crear visualización alternativa para accuracy perfecta
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=config["figure_size_medium"])
        fig.suptitle(
            f"Comparación: {name1} vs {name2} - Rendimiento Perfecto", fontsize=16
        )

        # Gráfico de barras de medias
        means1 = [np.mean(vals) for vals in values1]
        means2 = [np.mean(vals) for vals in values2]

        x = np.arange(len(metric_names))
        width = 0.35

        bars1 = ax1.bar(
            x - width / 2,
            means1,
            width,
            label=name1,
            color=config["comparison_colors"][0],
            alpha=0.8,
        )
        bars2 = ax1.bar(
            x + width / 2,
            means2,
            width,
            label=name2,
            color=config["comparison_colors"][1],
            alpha=0.8,
        )

        ax1.set_xlabel("Métricas")
        ax1.set_ylabel("Valor")
        ax1.set_title("Rendimiento por Métrica")
        ax1.set_xticks(x)
        ax1.set_xticklabels(metric_names)
        ax1.legend()
        ax1.grid(True, alpha=config["grid_alpha"])
        ax1.set_ylim(0.98, 1.005)  # Zoom para ver mejor

        # Agregar valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(
                    f"{height:.3f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

        # Tabla de comparación en el segundo subplot
        ax2.axis("tight")
        ax2.axis("off")

        comparison_data = []
        for i, name in enumerate(metric_names):
            comparison_data.append([name, f"{means1[i]:.4f}", f"{means2[i]:.4f}"])

        table = ax2.table(
            cellText=comparison_data,
            colLabels=["Métrica", name1, name2],
            cellLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        ax2.set_title("Tabla Comparativa", fontweight="bold")

    plt.tight_layout()
    plt.show()

    return has_variability


print("✓ Funciones de visualización mejoradas implementadas")
