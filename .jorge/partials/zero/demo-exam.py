# """
# # **Demo Primer Parcial - Sistemas Inteligentes II**

# ## **Jorge Alberto Jaramillo Garzón**
# ### **Universidad de Caldas**

# ---

# 1. **Ejercicio 1**: Validación cruzada de 10 particiones para clasificadores bayesiano y geométrico
# 2. **Ejercicio 2**: Análisis de K-NN con bootstrapping variando el número de vecinos
# 3. **Ejercicio 3**: Comparación teórica de los tres tipos de clasificadores

# El código está diseñado para ser **configurable y agnóstico al dataset**, permitiendo modificaciones fáciles durante la sustentación.
# """
# """
# ## **1. Configuración del Experimento**

# Esta sección centraliza todos los parámetros configurables para facilitar modificaciones durante la sustentación. El diseño modular permite cambiar rápidamente el dataset, características, clases objetivo, y parámetros de evaluación.
# """

# # Configuración centralizada del experimento
# CONFIG = {
#     # Dataset y características
#     'dataset_path': 'dataset-iris.csv',
#     'feature_columns': ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'],
#     'target_column': 'Species',

#     # Configuración específica por ejercicio
#     'exercise1_classes': ['Iris-setosa', 'Iris-versicolor'],  # Solo setosa y versicolor
#     'exercise2_classes': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'],  # Todas las clases

#     # Parámetros de evaluación
#     'cv_folds': 10,                    # Número de folds para validación cruzada
#     'bootstrap_iterations': 100,       # Iteraciones para bootstrapping (reducido para eficiencia)
#     'knn_k_range': list(range(1, 21)), # Rango de k para K-NN (1 a 20)

#     # Configuración general
#     'random_state': 42,                # Para reproducibilidad
#     'test_size': 0.3,                  # Proporción para conjunto de prueba
#     'confidence_level': 0.95,          # Nivel de confianza para intervalos
    
#     # Parámetros de visualización
#     'histogram_bins': 15,              # Número de bins para histogramas
#     'figure_size_large': (15, 10),     # Tamaño de figuras grandes
#     'figure_size_medium': (12, 8),     # Tamaño de figuras medianas
#     'alpha_transparency': 0.7,         # Transparencia para gráficos
#     'grid_alpha': 0.3,                 # Transparencia para grillas
    
#     # Colores para clases (configurable)
#     'class_colors': ['skyblue', 'lightcoral', 'lightgreen'],
#     'comparison_colors': ['lightblue', 'lightgreen', 'lightcoral'],
    
#     # Umbrales y parámetros adicionales
#     'variability_threshold': 0.001,    # Umbral para detectar variabilidad
#     'progress_milestones': 10,         # Cada cuánto mostrar progreso (%)
#     'significance_alpha': 0.05,        # Nivel de significancia estadística
#     'pca_components': 2,               # Componentes PCA para visualización
    
#     # Textos configurables
#     'dataset_encoding': 'utf-8',       # Codificación del dataset
#     'decimal_precision': 4             # Precisión decimal para reportes
# }

# print("✓ Configuración cargada exitosamente")
# print(f"Dataset: {CONFIG['dataset_path']}")
# print(f"Características: {CONFIG['feature_columns']}")
# print(f"Clases Ejercicio 1: {CONFIG['exercise1_classes']}")
# print(f"Clases Ejercicio 2: {CONFIG['exercise2_classes']}")
# print(f"CV Folds: {CONFIG['cv_folds']}")
# print(f"Bootstrap Iteraciones: {CONFIG['bootstrap_iterations']}")
# print(f"Rango K para K-NN: {min(CONFIG['knn_k_range'])}-{max(CONFIG['knn_k_range'])}")

# """
# ## **2. Imports y Librerías**

# Importamos las librerías necesarias. Los clasificadores usarán sklearn según lo permitido, pero los evaluadores (k-fold CV y bootstrapping) serán implementados manualmente con numpy.
# """

# # Librerías fundamentales
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats
# import warnings
# warnings.filterwarnings('ignore')

# # Clasificadores de sklearn
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.preprocessing import StandardScaler, LabelEncoder

# # Métricas y utilidades de sklearn (solo para métricas, no para evaluación)
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from sklearn.metrics import confusion_matrix, classification_report

# # Configuración de visualización
# plt.style.use('seaborn-v0_8')
# sns.set_palette("husl")
# plt.rcParams['figure.figsize'] = (12, 8)
# plt.rcParams['font.size'] = 10

# print("✓ Todas las librerías importadas exitosamente")
# print("📊 Configuración de visualización establecida")
# print("🔧 Clasificadores disponibles: GaussianNB, LinearDiscriminantAnalysis, KNeighborsClassifier")

# """
# ## **3. Funciones Utilitarias**

# Implementamos funciones modulares y agnósticas al dataset para facilitar la experimentación y modificaciones durante la sustentación.
# """

# def load_and_prepare_data(config, classes=None):
#     """
#     Carga y prepara los datos de forma agnóstica al dataset.

#     Parámetros:
#     - config: diccionario de configuración
#     - classes: lista de clases a incluir (None para todas)

#     Retorna:
#     - X: características normalizadas
#     - y: etiquetas codificadas
#     - feature_names: nombres de las características
#     - class_names: nombres de las clases
#     - scaler: objeto scaler usado para normalización
#     - label_encoder: codificador de etiquetas
#     """
#     # Cargar datos
#     data = pd.read_csv(config['dataset_path'])

#     # Filtrar clases si se especifica
#     if classes is not None:
#         data = data[data[config['target_column']].isin(classes)]

#     # Extraer características y etiquetas
#     X = data[config['feature_columns']].values
#     y = data[config['target_column']].values

#     # Normalizar características (importante para algunos clasificadores)
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)

#     # Codificar etiquetas
#     label_encoder = LabelEncoder()
#     y_encoded = label_encoder.fit_transform(y)

#     return X_scaled, y_encoded, config['feature_columns'], label_encoder.classes_, scaler, label_encoder

# def calculate_comprehensive_metrics(y_true, y_pred, class_names):
#     """
#     Calcula métricas comprehensivas para evaluación de clasificadores.

#     Parámetros:
#     - y_true: etiquetas verdaderas
#     - y_pred: predicciones
#     - class_names: nombres de las clases

#     Retorna:
#     - dict con todas las métricas calculadas
#     """
#     metrics = {
#         'accuracy': accuracy_score(y_true, y_pred),
#         'precision_macro': precision_score(y_true, y_pred, average='macro'),
#         'recall_macro': recall_score(y_true, y_pred, average='macro'),
#         'f1_macro': f1_score(y_true, y_pred, average='macro'),
#         'precision_micro': precision_score(y_true, y_pred, average='micro'),
#         'recall_micro': recall_score(y_true, y_pred, average='micro'),
#         'f1_micro': f1_score(y_true, y_pred, average='micro'),
#         'confusion_matrix': confusion_matrix(y_true, y_pred),
#         'classification_report': classification_report(y_true, y_pred, target_names=class_names)
#     }
#     return metrics

# def print_metrics_summary(metrics, classifier_name):
#     """Imprime un resumen bonito de las métricas."""
#     print(f"\n📊 **Métricas para {classifier_name}**")
#     print(f"{'─' * 50}")
#     print(f"Accuracy:        {metrics['accuracy']:.4f}")
#     print(f"Precision (Macro): {metrics['precision_macro']:.4f}")
#     print(f"Recall (Macro):    {metrics['recall_macro']:.4f}")
#     print(f"F1-Score (Macro):  {metrics['f1_macro']:.4f}")
#     print(f"{'─' * 50}")

# print("✓ Funciones utilitarias definidas:")
# print("  - load_and_prepare_data(): Carga agnóstica de datos")
# print("  - calculate_comprehensive_metrics(): Métricas comprehensivas")
# print("  - print_metrics_summary(): Resumen de métricas")


# """
# ## **4. Evaluadores Manuales**

# Implementamos los evaluadores (k-fold CV y bootstrapping) manualmente usando numpy, según los requerimientos. Estos son fundamentales para los ejercicios 1 y 2.
# """

# def manual_kfold_cv(X, y, classifier_class, k_folds=10, random_state=42, **classifier_kwargs):
#     """
#     Implementación de k-fold cross-validation usando numpy.

#     JUSTIFICACIÓN:
#     - Dividimos los datos en k particiones aproximadamente iguales
#     - Para cada fold: entrenamos en (k-1) particiones y evaluamos en 1
#     - Esto proporciona una estimación robusta del rendimiento con menor varianza que hold-out
#     - k=10 es un estándar que balancea sesgo vs varianza en la estimación

#     Parámetros:
#     - X: características
#     - y: etiquetas
#     - classifier_class: clase del clasificador (ej: GaussianNB)
#     - k_folds: número de folds
#     - random_state: semilla para reproducibilidad
#     - **classifier_kwargs: argumentos adicionales para el clasificador

#     Retorna:
#     - dict con métricas de cada fold y estadísticas agregadas
#     """
#     np.random.seed(random_state)

#     # Crear índices aleatorios para las particiones
#     n_samples = X.shape[0]
#     indices = np.random.permutation(n_samples)

#     # Calcular tamaños de los folds
#     fold_sizes = np.full(k_folds, n_samples // k_folds, dtype=int)
#     fold_sizes[:n_samples % k_folds] += 1

#     # Crear los índices de cada fold
#     fold_indices = []
#     current = 0
#     for size in fold_sizes:
#         fold_indices.append(indices[current:current + size])
#         current += size

#     # Almacenar resultados de cada fold
#     fold_results = []

#     print(f"🔄 Ejecutando {k_folds}-fold Cross Validation...")
#     print(f"📊 Total de muestras: {n_samples}")
#     print(f"📋 Tamaño promedio por fold: {n_samples // k_folds}")

#     for fold in range(k_folds):
#         # Índices para entrenamiento (todos menos el fold actual)
#         train_indices = np.concatenate([fold_indices[i] for i in range(k_folds) if i != fold])
#         test_indices = fold_indices[fold]

#         # Dividir datos
#         X_train, X_test = X[train_indices], X[test_indices]
#         y_train, y_test = y[train_indices], y[test_indices]

#         # Entrenar clasificador
#         classifier = classifier_class(**classifier_kwargs)
#         classifier.fit(X_train, y_train)

#         # Hacer predicciones
#         y_pred = classifier.predict(X_test)

#         # Calcular métricas para este fold
#         fold_accuracy = accuracy_score(y_test, y_pred)
#         fold_precision = precision_score(y_test, y_pred, average='macro')
#         fold_recall = recall_score(y_test, y_pred, average='macro')
#         fold_f1 = f1_score(y_test, y_pred, average='macro')

#         fold_results.append({
#             'fold': fold + 1,
#             'accuracy': fold_accuracy,
#             'precision': fold_precision,
#             'recall': fold_recall,
#             'f1_score': fold_f1,
#             'train_size': len(X_train),
#             'test_size': len(X_test)
#         })

#         print(f"  Fold {fold + 1:2d}: Acc={fold_accuracy:.4f}, Prec={fold_precision:.4f}, Rec={fold_recall:.4f}, F1={fold_f1:.4f}")

#     # Calcular estadísticas agregadas
#     accuracies = [r['accuracy'] for r in fold_results]
#     precisions = [r['precision'] for r in fold_results]
#     recalls = [r['recall'] for r in fold_results]
#     f1_scores = [r['f1_score'] for r in fold_results]

#     results = {
#         'fold_results': fold_results,
#         'mean_accuracy': np.mean(accuracies),
#         'std_accuracy': np.std(accuracies),
#         'mean_precision': np.mean(precisions),
#         'std_precision': np.std(precisions),
#         'mean_recall': np.mean(recalls),
#         'std_recall': np.std(recalls),
#         'mean_f1': np.mean(f1_scores),
#         'std_f1': np.std(f1_scores),
#         'confidence_interval_accuracy': np.percentile(accuracies, [2.5, 97.5])
#     }

#     print(f"\n📈 **Resultados Agregados de {k_folds}-fold CV:**")
#     print(f"  Accuracy:  {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
#     print(f"  Precision: {results['mean_precision']:.4f} ± {results['std_precision']:.4f}")
#     print(f"  Recall:    {results['mean_recall']:.4f} ± {results['std_recall']:.4f}")
#     print(f"  F1-Score:  {results['mean_f1']:.4f} ± {results['std_f1']:.4f}")
#     print(f"  IC 95% Accuracy: [{results['confidence_interval_accuracy'][0]:.4f}, {results['confidence_interval_accuracy'][1]:.4f}]")

#     return results

# print("✓ Función manual_kfold_cv implementada")

# def manual_bootstrap(X, y, classifier_class, n_iterations=1000, random_state=42, **classifier_kwargs):
#     """
#     Implementación de bootstrapping usando numpy.

#     TECNICISMOS:
#     - Bootstrapping genera múltiples muestras con reemplazo del dataset original
#     - Cada muestra bootstrap tiene el mismo tamaño que el dataset original
#     - Evaluamos en muestras out-of-bag (datos no seleccionados en el bootstrap)
#     - Proporciona estimación robusta de la distribución del rendimiento
#     - Útil para construir intervalos de confianza y analizar estabilidad

#     Parámetros:
#     - X: características
#     - y: etiquetas
#     - classifier_class: clase del clasificador
#     - n_iterations: número de iteraciones bootstrap
#     - random_state: semilla para reproducibilidad
#     - **classifier_kwargs: argumentos adicionales para el clasificador

#     Retorna:
#     - dict con resultados de cada iteración y estadísticas agregadas
#     """
#     np.random.seed(random_state)
#     n_samples = X.shape[0]

#     bootstrap_results = []

#     print(f"🔄 Ejecutando Bootstrapping con {n_iterations} iteraciones...")
#     print(f"📊 Total de muestras: {n_samples}")

#     # Progreso cada 10% de las iteraciones
#     progress_milestones = [int(n_iterations * p / 10) for p in range(1, 11)]

#     for iteration in range(n_iterations):
#         # Crear muestra bootstrap (con reemplazo)
#         bootstrap_indices = np.random.choice(n_samples, size=n_samples, replace=True)

#         # Identificar muestras out-of-bag (no seleccionadas)
#         oob_indices = np.setdiff1d(np.arange(n_samples), bootstrap_indices)

#         # Si no hay muestras out-of-bag, skip esta iteración (muy raro)
#         if len(oob_indices) == 0:
#             continue

#         # Dividir datos
#         X_bootstrap, y_bootstrap = X[bootstrap_indices], y[bootstrap_indices]
#         X_oob, y_oob = X[oob_indices], y[oob_indices]

#         # Entrenar clasificador en muestra bootstrap
#         classifier = classifier_class(**classifier_kwargs)
#         classifier.fit(X_bootstrap, y_bootstrap)

#         # Evaluar en datos out-of-bag
#         y_pred = classifier.predict(X_oob)

#         # Calcular métricas
#         try:
#             iteration_accuracy = accuracy_score(y_oob, y_pred)
#             iteration_precision = precision_score(y_oob, y_pred, average='macro')
#             iteration_recall = recall_score(y_oob, y_pred, average='macro')
#             iteration_f1 = f1_score(y_oob, y_pred, average='macro')

#             bootstrap_results.append({
#                 'iteration': iteration + 1,
#                 'accuracy': iteration_accuracy,
#                 'precision': iteration_precision,
#                 'recall': iteration_recall,
#                 'f1_score': iteration_f1,
#                 'bootstrap_size': len(X_bootstrap),
#                 'oob_size': len(X_oob)
#             })
#         except:
#             # Skip iteraciones con problemas (ej: solo una clase en OOB)
#             continue

#         # Mostrar progreso
#         if (iteration + 1) in progress_milestones:
#             progress = int(((iteration + 1) / n_iterations) * 100)
#             print(f"  Progreso: {progress}% ({iteration + 1}/{n_iterations} iteraciones)")

#     # Calcular estadísticas agregadas
#     if not bootstrap_results:
#         raise ValueError("No se pudieron completar iteraciones bootstrap válidas")

#     accuracies = [r['accuracy'] for r in bootstrap_results]
#     precisions = [r['precision'] for r in bootstrap_results]
#     recalls = [r['recall'] for r in bootstrap_results]
#     f1_scores = [r['f1_score'] for r in bootstrap_results]

#     # Intervalos de confianza usando percentiles
#     confidence_level = 0.95
#     alpha = 1 - confidence_level
#     lower_percentile = (alpha / 2) * 100
#     upper_percentile = (1 - alpha / 2) * 100

#     results = {
#         'bootstrap_results': bootstrap_results,
#         'n_valid_iterations': len(bootstrap_results),
#         'mean_accuracy': np.mean(accuracies),
#         'std_accuracy': np.std(accuracies),
#         'median_accuracy': np.median(accuracies),
#         'mean_precision': np.mean(precisions),
#         'std_precision': np.std(precisions),
#         'mean_recall': np.mean(recalls),
#         'std_recall': np.std(recalls),
#         'mean_f1': np.mean(f1_scores),
#         'std_f1': np.std(f1_scores),
#         'confidence_interval_accuracy': np.percentile(accuracies, [lower_percentile, upper_percentile]),
#         'confidence_interval_f1': np.percentile(f1_scores, [lower_percentile, upper_percentile])
#     }

#     print(f"\n📈 **Resultados Agregados del Bootstrapping:**")
#     print(f"  Iteraciones válidas: {results['n_valid_iterations']}/{n_iterations}")
#     print(f"  Accuracy:  {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f} (mediana: {results['median_accuracy']:.4f})")
#     print(f"  Precision: {results['mean_precision']:.4f} ± {results['std_precision']:.4f}")
#     print(f"  Recall:    {results['mean_recall']:.4f} ± {results['std_recall']:.4f}")
#     print(f"  F1-Score:  {results['mean_f1']:.4f} ± {results['std_f1']:.4f}")
#     print(f"  IC 95% Accuracy: [{results['confidence_interval_accuracy'][0]:.4f}, {results['confidence_interval_accuracy'][1]:.4f}]")
#     print(f"  IC 95% F1-Score: [{results['confidence_interval_f1'][0]:.4f}, {results['confidence_interval_f1'][1]:.4f}]")

#     return results

# print("✓ Función manual_bootstrap implementada")

# """
# ## **5. Funciones de Visualización Mejoradas**

# Funciones especializadas para crear visualizaciones informativas, incluyendo casos donde hay poca variabilidad en los resultados.
# """

# def plot_normalized_distributions(X, y, feature_names, class_names, config):
#     """
#     Crear histogramas de distribuciones normalizadas con explicación clara.
    
#     NOTA IMPORTANTE sobre normalización:
#     - StandardScaler centra los datos en media=0 y escala por desviación estándar
#     - Valores negativos = por debajo de la media general
#     - Valores positivos = por encima de la media general
#     - Esto NO significa valores "negativos" literales, solo posición relativa
#     """
#     fig, axes = plt.subplots(2, 2, figsize=config['figure_size_large'])
#     fig.suptitle('Distribución de Características Normalizadas por Clase', fontsize=16)
    
#     colors = config['class_colors'][:len(class_names)]
    
#     for i, feature in enumerate(feature_names):
#         ax = axes[i//2, i%2]
        
#         for j, class_name in enumerate(class_names):
#             class_data = X[y == j, i]
#             label = class_name.split('-')[1] if 'Iris-' in class_name else class_name
#             ax.hist(class_data, alpha=config['alpha_transparency'], 
#                    bins=config['histogram_bins'], color=colors[j], label=label)
        
#         ax.set_title(f'{feature}')
#         ax.set_xlabel('Valor Normalizado (μ=0, σ=1)')
#         ax.set_ylabel('Frecuencia')
#         ax.legend()
#         ax.grid(True, alpha=config['grid_alpha'])
#         ax.axvline(x=0, color='black', linestyle='--', alpha=0.5, label='Media=0')
    
#     plt.tight_layout()
    
#     # Agregar nota explicativa
#     fig.text(0.5, 0.02, 
#              '💡 Normalización: Valores negativos = por debajo de la media general, positivos = por encima',
#              ha='center', fontsize=10, style='italic')
    
#     plt.show()
    
# def create_comparison_visualization(results1, results2, name1, name2, config):
#     """
#     Crear visualización de comparación que maneja el caso de poca variabilidad.
    
#     Si ambos clasificadores tienen varianza 0 (accuracy perfecta), 
#     usa visualizaciones alternativas más informativas.
#     """
#     # Extraer datos
#     metrics = ['accuracy', 'precision', 'recall', 'f1_score']
#     metric_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
#     values1 = [[r[metric] for r in results1['fold_results']] for metric in metrics]
#     values2 = [[r[metric] for r in results2['fold_results']] for metric in metrics]
    
#     # Verificar si hay variabilidad (usando umbral configurable)
#     has_variability = any(np.std(vals) > config['variability_threshold'] for vals in values1 + values2)
    
#     if has_variability:
#         # Crear boxplots normales
#         fig, axes = plt.subplots(2, 2, figsize=config['figure_size_large'])
#         fig.suptitle(f'Comparación: {name1} vs {name2}', fontsize=16)
        
#         for i, (vals1, vals2, name) in enumerate(zip(values1, values2, metric_names)):
#             ax = axes[i//2, i%2]
            
#             data_to_plot = [vals1, vals2]
#             box = ax.boxplot(data_to_plot, labels=[name1, name2], 
#                            patch_artist=True, notch=True)
            
#             colors = config['comparison_colors'][:2]
#             for patch, color in zip(box['boxes'], colors):
#                 patch.set_facecolor(color)
            
#             ax.set_title(f'{name}')
#             ax.set_ylabel(name)
#             ax.grid(True, alpha=config['grid_alpha'])
            
#             # Agregar valores medios
#             ax.text(1, np.mean(vals1), f'{np.mean(vals1):.3f}', 
#                    ha='center', va='bottom', fontweight='bold')
#             ax.text(2, np.mean(vals2), f'{np.mean(vals2):.3f}', 
#                    ha='center', va='bottom', fontweight='bold')
#     else:
#         # Crear visualización alternativa para accuracy perfecta
#         fig, (ax1, ax2) = plt.subplots(1, 2, figsize=config['figure_size_medium'])
#         fig.suptitle(f'Comparación: {name1} vs {name2} - Rendimiento Perfecto', fontsize=16)
        
#         # Gráfico de barras de medias
#         means1 = [np.mean(vals) for vals in values1]
#         means2 = [np.mean(vals) for vals in values2]
        
#         x = np.arange(len(metric_names))
#         width = 0.35
        
#         bars1 = ax1.bar(x - width/2, means1, width, label=name1, 
#                        color=config['comparison_colors'][0], alpha=0.8)
#         bars2 = ax1.bar(x + width/2, means2, width, label=name2, 
#                        color=config['comparison_colors'][1], alpha=0.8)
        
#         ax1.set_xlabel('Métricas')
#         ax1.set_ylabel('Valor')
#         ax1.set_title('Rendimiento por Métrica')
#         ax1.set_xticks(x)
#         ax1.set_xticklabels(metric_names)
#         ax1.legend()
#         ax1.grid(True, alpha=config['grid_alpha'])
#         ax1.set_ylim(0.98, 1.005)  # Zoom para ver mejor
        
#         # Agregar valores en las barras
#         for bars in [bars1, bars2]:
#             for bar in bars:
#                 height = bar.get_height()
#                 ax1.annotate(f'{height:.3f}',
#                            xy=(bar.get_x() + bar.get_width() / 2, height),
#                            xytext=(0, 3), textcoords="offset points",
#                            ha='center', va='bottom', fontweight='bold')
        
#         # Tabla de comparación en el segundo subplot
#         ax2.axis('tight')
#         ax2.axis('off')
        
#         comparison_data = []
#         for i, name in enumerate(metric_names):
#             comparison_data.append([name, f'{means1[i]:.4f}', f'{means2[i]:.4f}'])
        
#         table = ax2.table(cellText=comparison_data,
#                          colLabels=['Métrica', name1, name2],
#                          cellLoc='center',
#                          loc='center')
#         table.auto_set_font_size(False)
#         table.set_fontsize(12)
#         table.scale(1.2, 1.5)
#         ax2.set_title('Tabla Comparativa', fontweight='bold')
    
#     plt.tight_layout()
#     plt.show()
    
#     return has_variability

# def analyze_perfect_performance(results1, results2, name1, name2):
#     """
#     Análisis especializado para el caso de rendimiento perfecto.
#     """
#     print("🎯 **ANÁLISIS DE RENDIMIENTO PERFECTO**")
#     print("=" * 60)
    
#     print("📊 **Interpretación de los Resultados:**")
#     print(f"✅ Ambos clasificadores ({name1} y {name2}) obtuvieron:")
#     print("   - Accuracy = 1.0000 (100% de clasificaciones correctas)")
#     print("   - Precision = 1.0000 (sin falsos positivos)")
#     print("   - Recall = 1.0000 (sin falsos negativos)")
#     print("   - F1-Score = 1.0000 (balance perfecto)")
    
#     print(f"\n🔍 **¿Por qué ambos clasificadores son perfectos?**")
#     print("   - Las clases setosa y versicolor son linealmente separables")
#     print("   - Las características del dataset Iris discriminan muy bien estas clases")
#     print("   - Ambos algoritmos son adecuados para este problema simple")
    
#     print(f"\n📈 **Test Estadístico:**")
#     print("   - No se puede realizar test t (varianza = 0)")
#     print("   - Diferencia entre clasificadores: 0.0000")
#     print("   - Conclusión: Rendimiento idéntico y perfecto")
    
#     print(f"\n💡 **Implicaciones Prácticas:**")
#     print("   - Para este subconjunto de datos, cualquier clasificador es válido")
#     print("   - La diferencia se vería en datasets más complejos o ruidosos")
#     print("   - Ambos algoritmos demuestran robustez en problemas simples")

# print("✓ Funciones de visualización mejoradas implementadas")
