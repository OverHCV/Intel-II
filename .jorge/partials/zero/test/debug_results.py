# DEBUG: ¿Por qué todos los clasificadores dan 100%?
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Cargar datos exactamente como el notebook
print("🔍 DEBUG: Investigando los resultados perfectos...")

# Cargar dataset
data = pd.read_csv('dataset-iris.csv')
print(f"Dataset original shape: {data.shape}")

# Filtrar solo setosa y versicolor (como en el ejercicio)
classes = ['Iris-setosa', 'Iris-versicolor']
filtered_data = data[data['Species'].isin(classes)]
print(f"Datos filtrados shape: {filtered_data.shape}")

# Extraer características y etiquetas
X = filtered_data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].values
y = filtered_data['Species'].values

print(f"X shape: {X.shape}")
print(f"Y classes: {np.unique(y)}")
print(f"Y distribution: {pd.Series(y).value_counts()}")

# Normalizar (como en el notebook)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Codificar etiquetas
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"X_scaled range: [{X_scaled.min():.3f}, {X_scaled.max():.3f}]")
print(f"Y_encoded: {np.unique(y_encoded)}")

# Probar con sklearn cross_val_score para comparar
print("\n📊 COMPARACIÓN CON SKLEARN:")

# Usar StratifiedKFold para reproducibilidad
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Naive Bayes
nb_scores = cross_val_score(GaussianNB(), X_scaled, y_encoded, cv=cv)
print(f"Naive Bayes (sklearn CV): {nb_scores}")
print(f"NB Mean: {nb_scores.mean():.4f} ± {nb_scores.std():.4f}")

# LDA  
lda_scores = cross_val_score(LinearDiscriminantAnalysis(), X_scaled, y_encoded, cv=cv)
print(f"LDA (sklearn CV): {lda_scores}")
print(f"LDA Mean: {lda_scores.mean():.4f} ± {lda_scores.std():.4f}")

# Probar mi implementación manual más simple
print("\n🔧 MANUAL K-FOLD SIMPLE:")
def simple_kfold_test(X, y, classifier_class, k=10):
    kf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scores = []
    
    for fold, (train_idx, test_idx) in enumerate(kf.split(X, y)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        clf = classifier_class()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        score = accuracy_score(y_test, y_pred)
        scores.append(score)
        print(f"  Fold {fold+1}: {score:.4f} | Train: {len(y_train)}, Test: {len(y_test)}")
    
    return np.array(scores)

nb_manual = simple_kfold_test(X_scaled, y_encoded, GaussianNB)
print(f"Manual NB: {nb_manual.mean():.4f} ± {nb_manual.std():.4f}")

lda_manual = simple_kfold_test(X_scaled, y_encoded, LinearDiscriminantAnalysis)
print(f"Manual LDA: {lda_manual.mean():.4f} ± {lda_manual.std():.4f}")

# Verificar si el problema es el dataset
print("\n🔍 ANÁLISIS DEL DATASET:")
print("Estadísticas por clase (datos normalizados):")
for i, class_name in enumerate(label_encoder.classes_):
    mask = y_encoded == i
    print(f"\n{class_name}:")
    for j, feature in enumerate(['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']):
        data_class = X_scaled[mask, j]
        print(f"  {feature}: μ={data_class.mean():.3f}, σ={data_class.std():.3f}")

# Verificar separabilidad lineal simple
from sklearn.svm import SVC
svm_scores = cross_val_score(SVC(kernel='linear'), X_scaled, y_encoded, cv=cv)
print(f"\nSVM Linear: {svm_scores.mean():.4f} ± {svm_scores.std():.4f}")
print("(Si SVM también da ~100%, entonces el problema es muy fácil)")