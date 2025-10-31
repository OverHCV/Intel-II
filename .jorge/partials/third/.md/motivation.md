# Student Performance Dataset
Este dataset representa otra opción excelente, particularmente si se valora la rapidez en la experimentación y la oportunidad de demostrar habilidades en ingeniería de características. Se enfoca en predecir el rendimiento académico de estudiantes de secundaria en Portugal, utilizando una amplia gama de atributos.   

## Contexto y Relevancia

El dataset contiene datos de 649 estudiantes y 33 atributos, cubriendo aspectos demográficos, sociales y escolares. Su tamaño más manejable permite un ciclo de experimentación y ajuste de modelos más rápido, lo cual es una ventaja significativa en un entorno de examen con tiempo limitado. El problema de predecir el éxito estudiantil es un área de investigación activa y de gran relevancia social, lo que proporciona un contexto significativo para la interpretación de los resultados.   

## Análisis de Atributos

La riqueza de los atributos es uno de los puntos fuertes de este dataset. Incluye información variada como 'school' (escuela), 'sex' (sexo), 'age' (edad), 'address' (tipo de domicilio), 'Medu' (educación de la madre), 'Fedu' (educación del padre), 'studytime' (tiempo de estudio semanal), 'failures' (fallos en clases pasadas), 'famsup' (apoyo educativo familiar), 'goout' (salidas con amigos), 'Dalc' (consumo de alcohol en días laborables), 'Walc' (consumo de alcohol en fin de semana), y las notas de los tres periodos ('G1', 'G2', 'G3'). Esta diversidad permite un análisis exploratorio profundo y la construcción de modelos potencialmente muy informativos.   

### Idoneidad para Clasificación

Este dataset presenta un desafío interesante y educativo para la tarea de clasificación. Las variables de rendimiento 'G1', 'G2' y 'G3' son numéricas, con un rango de 0 a 20. Para utilizar un clasificador de árboles de decisión, el estudiante debe primero realizar una ingeniería de la variable objetivo. Esto implica transformar la variable numérica G3 (nota final) en una variable categórica. Por ejemplo, se podría crear una variable binaria ('Aprobado'/'Reprobado') estableciendo un umbral en 10, o una variable multinivel ('Rendimiento Muy Bajo', 'Rendimiento Bajo', 'Rendimiento Medio', 'Rendimiento Alto', 'Rendimiento Muy Alto') con umbrales apropiados (umbral en 4 puntos cada nivel hasta llegar a 20). Este paso es una oportunidad para demostrar una habilidad clave en la aplicación práctica del machine learning.

Al igual que con el dataset de marketing, este conjunto de datos también presenta una advertencia sobre la fuga de datos. La nota final, G3, está fuertemente correlacionada con las notas del primer y segundo periodo, G1 y G2. Predecir G3 utilizando G1 y G2 como predictores es una tarea trivial que no ofrece valor predictivo para futuros estudiantes al inicio del curso. Un análisis riguroso implicaría excluir G1 y G2 del conjunto de características para construir un modelo que prediga el rendimiento final basándose únicamente en los atributos socio-demográficos y de comportamiento, lo cual es un problema mucho más desafiante y realista.   

### Idoneidad para Clustering

El dataset es muy apropiado para el clustering, con el objetivo de identificar perfiles o arquetipos de estudiantes. De hecho, una de las publicaciones asociadas al dataset utiliza K-means para clasificar el comportamiento de los estudiantes. Se podrían descubrir grupos como "estudiantes de alto rendimiento con fuerte apoyo familiar", "estudiantes en riesgo con alta actividad social y bajo tiempo de estudio", o "estudiantes resilientes con bajo apoyo pero alta dedicación". Al igual que con el dataset de marketing, se requerirá un preprocesamiento cuidadoso, aplicando Encodings a las numerosas variables categóricas y binarias, y estandarizando las numéricas antes de aplicar los algoritmos de clustering.

#### Attributes for both student-mat.csv (Math course) and student-por.csv (Portuguese language course) datasets:

1 school - student's school (binary: "GP" - Gabriel Pereira or "MS" - Mousinho da Silveira)
2 sex - student's sex (binary: "F" - female or "M" - male)
3 age - student's age (numeric: from 15 to 22)
4 address - student's home address type (binary: "U" - urban or "R" - rural)
5 famsize - family size (binary: "LE3" - less or equal to 3 or "GT3" - greater than 3)
6 Pstatus - parent's cohabitation status (binary: "T" - living together or "A" - apart)
7 Medu - mother's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
8 Fedu - father's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
9 Mjob - mother's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
10 Fjob - father's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
11 reason - reason to choose this school (nominal: close to "home", school "reputation", "course" preference or "other")
12 guardian - student's guardian (nominal: "mother", "father" or "other")
13 traveltime - home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour)
14 studytime - weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)
15 failures - number of past class failures (numeric: n if 1<=n<3, else 4)
16 schoolsup - extra educational support (binary: yes or no)
17 famsup - family educational support (binary: yes or no)
18 paid - extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)
19 activities - extra-curricular activities (binary: yes or no)
20 nursery - attended nursery school (binary: yes or no)
21 higher - wants to take higher education (binary: yes or no)
22 internet - Internet access at home (binary: yes or no)
23 romantic - with a romantic relationship (binary: yes or no)
24 famrel - quality of family relationships (numeric: from 1 - very bad to 5 - excellent)
25 freetime - free time after school (numeric: from 1 - very low to 5 - very high)
26 goout - going out with friends (numeric: from 1 - very low to 5 - very high)
27 Dalc - workday alcohol consumption (numeric: from 1 - very low to 5 - very high)
28 Walc - weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)
29 health - current health status (numeric: from 1 - very bad to 5 - very good)
30 absences - number of school absences (numeric: from 0 to 93)

# these grades are related with the course subject, Math or Portuguese:
31 G1 - first period grade (numeric: from 0 to 20)
31 G2 - second period grade (numeric: from 0 to 20)
32 G3 - final grade (numeric: from 0 to 20, output target)

Additional note: there are several (382) students that belong to both datasets.
These students can be identified by searching for identical attributes that characterize each student, as shown in the annexed R file.
