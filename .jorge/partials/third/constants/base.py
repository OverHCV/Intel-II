"""
Constants and Feature Mappings for Student Performance Dataset.

WHY: Feature names in the dataset are cryptic (e.g., "Fedu", "schoolsup").
     This file provides human-readable descriptions for better interpretability.
"""

# Feature names and descriptions from student.txt
FEATURE_DESCRIPTIONS = {
    # Demographic features
    "school": "Escuela (GP: Gabriel Pereira, MS: Mousinho da Silveira)",
    "sex": "Género (F: Femenino, M: Masculino)",
    "age": "Edad del estudiante (15-22 años)",
    "address": "Tipo de domicilio (U: Urbano, R: Rural)",
    # Family features
    "famsize": "Tamaño familiar (LE3: ≤3 miembros, GT3: >3 miembros)",
    "Pstatus": "Estado parental (T: Juntos, A: Separados)",
    "Medu": "Educación madre (0: Ninguna, 1: Primaria, 2: 5to-9no, 3: Secundaria, 4: Superior)",
    "Fedu": "Educación padre (0: Ninguna, 1: Primaria, 2: 5to-9no, 3: Secundaria, 4: Superior)",
    "Mjob": "Trabajo madre (teacher, health, services, at_home, other)",
    "Fjob": "Trabajo padre (teacher, health, services, at_home, other)",
    "guardian": "Tutor del estudiante (madre, padre, otro)",
    # School-related features
    "reason": "Razón para elegir escuela (home, reputation, course, other)",
    "traveltime": "Tiempo viaje casa-escuela (1: <15min, 2: 15-30min, 3: 30min-1h, 4: >1h)",
    "studytime": "Tiempo semanal de estudio (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)",
    "failures": "Número de reprobaciones previas (0-4)",
    "schoolsup": "Apoyo educativo extra (sí/no)",
    "famsup": "Apoyo educativo familiar (sí/no)",
    "paid": "Clases pagas extra (sí/no)",
    "activities": "Actividades extracurriculares (sí/no)",
    "nursery": "Asistió a guardería (sí/no)",
    "higher": "Desea educación superior (sí/no)",
    # Social features
    "internet": "Acceso a internet en casa (sí/no)",
    "romantic": "En relación romántica (sí/no)",
    "famrel": "Calidad relaciones familiares (1: Muy mala - 5: Excelente)",
    "freetime": "Tiempo libre después escuela (1: Muy bajo - 5: Muy alto)",
    "goout": "Salidas con amigos (1: Muy bajo - 5: Muy alto)",
    "Dalc": "Consumo alcohol días laborales (1: Muy bajo - 5: Muy alto)",
    "Walc": "Consumo alcohol fin de semana (1: Muy bajo - 5: Muy alto)",
    "health": "Estado de salud actual (1: Muy malo - 5: Muy bueno)",
    # Academic features (removed in preprocessing)
    "absences": "Número de ausencias escolares (0-93)",
    "G1": "Nota primer periodo (0-20) [REMOVIDO: Fuga de datos]",
    "G2": "Nota segundo periodo (0-20) [REMOVIDO: Fuga de datos]",
    "G3": "Nota final (0-20) [VARIABLE OBJETIVO]",
}

# Shortened feature names for visualizations
FEATURE_SHORT_NAMES = {
    "school": "School",
    "sex": "Gender",
    "age": "Age",
    "address": "Address",
    "famsize": "Fam.Size",
    "Pstatus": "Parents",
    "Medu": "Mother Edu",
    "Fedu": "Father Edu",
    "Mjob": "Mother Job",
    "Fjob": "Father Job",
    "reason": "School Reason",
    "guardian": "Guardian",
    "traveltime": "Travel Time",
    "studytime": "Study Time",
    "failures": "Failures",
    "schoolsup": "School Support",
    "famsup": "Family Support",
    "paid": "Paid Classes",
    "activities": "Activities",
    "nursery": "Nursery",
    "higher": "Higher Ed",
    "internet": "Internet",
    "romantic": "Romantic",
    "famrel": "Fam Relations",
    "freetime": "Free Time",
    "goout": "Go Out",
    "Dalc": "Weekday Alcohol",
    "Walc": "Weekend Alcohol",
    "health": "Health",
    "absences": "Absences"
}

# Feature categories for grouping
FEATURE_CATEGORIES = {
    "Demographic": ["school", "sex", "age", "address"],
    "Family": ["famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "guardian"],
    "Academic": ["reason", "studytime", "failures", "schoolsup", "famsup", "paid", "absences"],
    "Social": ["activities", "nursery", "higher", "internet", "romantic"],
    "Behavior": ["traveltime", "freetime", "goout", "Dalc", "Walc", "health", "famrel"]
}

# Dataset information
DATASET_INFO = {
    "math": {
        "name": "Mathematics Course",
        "filename": "student-mat.csv",
        "n_students": 395,
        "usage": "Test set (cross-domain validation)",
        "why": "Smaller dataset, different subject → tests generalization"
    },
    "portuguese": {
        "name": "Portuguese Language Course",
        "filename": "student-por.csv",
        "n_students": 649,
        "usage": "Training set",
        "why": "Larger dataset → more examples for learning patterns"
    },
    "overlap": {
        "count": 382,
        "description": "Students who took both Math and Portuguese courses"
    }
}

# Target engineering strategies
TARGET_STRATEGIES = {
    "binary": {
        "name": "Binary (Pass/Fail)",
        "threshold": 10,
        "classes": ["Fail", "Pass"],
        "description": "G3 < 10 = Fail, G3 ≥ 10 = Pass",
        "why": "Simple, actionable for intervention programs"
    },
    "three_class": {
        "name": "Three-class (Low/Medium/High)",
        "thresholds": [10, 14],
        "classes": ["Low", "Medium", "High"],
        "description": "G3 < 10 = Low, 10 ≤ G3 < 14 = Medium, G3 ≥ 14 = High",
        "why": "More granular for targeted interventions"
    },
    "five_class": {
        "name": "Five-class (A/B/C/D/F)",
        "thresholds": [10, 12, 14, 16],
        "classes": ["F", "D", "C", "B", "A"],
        "description": "Standard letter grading system",
        "why": "Familiar to educators, aligns with traditional grading"
    }
}

# Balancing methods
BALANCING_METHODS = {
    "smote": {
        "name": "SMOTE (Synthetic Minority Over-sampling)",
        "description": "Creates synthetic examples by interpolating between minority class samples",
        "pros": "Adds diversity, reduces overfitting",
        "cons": "Can create unrealistic samples if minority class is very small",
        "recommended_when": "Imbalance ratio > 2.0 and sufficient minority samples (>5)"
    },
    "random_over": {
        "name": "Random Over-sampling",
        "description": "Duplicates random samples from minority class",
        "pros": "Simple, no risk of unrealistic samples",
        "cons": "Increases overfitting risk (exact duplicates)",
        "recommended_when": "Quick baseline or when SMOTE creates unrealistic samples"
    },
    "random_under": {
        "name": "Random Under-sampling",
        "description": "Removes random samples from majority class",
        "pros": "Fast, reduces dataset size",
        "cons": "Loses potentially useful information",
        "recommended_when": "Massive imbalance and computational constraints"
    },
    "none": {
        "name": "No Balancing",
        "description": "Keep original class distribution",
        "recommended_when": "Classes are already balanced (ratio < 1.5)"
    }
}

def get_feature_description(feature_name: str) -> str:
    """Get human-readable description for a feature."""
    return FEATURE_DESCRIPTIONS.get(feature_name, feature_name)

def get_feature_short_name(feature_name: str) -> str:
    """Get short name for visualizations."""
    return FEATURE_SHORT_NAMES.get(feature_name, feature_name)

def get_features_by_category(category: str) -> list:
    """Get list of features in a category."""
    return FEATURE_CATEGORIES.get(category, [])

