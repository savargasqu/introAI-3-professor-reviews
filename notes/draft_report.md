# Predicción de puntuaciones de profesores a partir de opiniones de los estudiantes

Freddy Alejandro Cuellar facuellarg\@unal.edu.co

Sergio Alejandro Vargas savargasqu\@unal.edu.co

## Introducción

Actualmente, es común combinar texto con datos numéricos para análisis
de regresión. En el estado del arte es se usan técnicas para agrupar
palabras subjetivas en categorías definidas (bueno, malo, bonito etc.),
además de técnicas de análisis morfológico para reducir el conjunto de
palabras dentro de un texto, por ejemplo, convirtiendo adjetivos y
adverbios en sustantivos (Foster, Liberman.Stine 2013). Sin embargo,
estas técnicas de *análisis de sentimientos* requieren un conjunto de
datos (a saber, listas de palabras) ya clasificados.

Para simplificar estos modelos es posible convertir el texto en
regresores usando un modelo de *bag-of-words*, que no considera
construcciones gramáticas ni semánticas del texto, solamente la
frecuencia de apariciones de una palabra en el texto.

Así, nuestro problemas es el siguiente: dada una entrada en lenguaje
natural, que expresa la opinión de un estudiante sobre un profesor,
predecir el puntaje numérico con el que el estudiante calificaría al
profesor.

## Adquisición de datos

Para la adquisición de datos usamos una técnica de *web-scraping*,
usando las librerías de Python: *requests* y *BeautifulSoup4*. Primero
extrajimos una lista de urls, correspondientes a la pagina de cada
profesor. Luego, iteramos sobre dicha lista, haciendo un
\textsc{get request} para cada elemento. Una vez adquirido el contenido
de una pagina, podemos hacer una búsqueda de las etiquetas que
correspondan a una reseña y de ahí extraer el texto. Finalmente, como
método de persistencia, guardamos cada reseña con su puntaje
correspondiente como una entrada en un archivo \textsc{json}.

## Diseño experimental

Una vez adquiridos los datos, podemos prepararlos para el modelo.
Primero, se agregan todas las palabras/*tokens* presentes en las reseñas
en un conjunto $B$. El orden no importa, solo cuales palabras están y
cuales no (ergo *bag-of-words*). Luego, para cada reseña construimos un
vector de atributos de $|B|$ entradas, donde cada entrada corresponde al
número de instancias de una palabra dentro de la reseña. Todo este
proceso está implementado por Scikit-learn con la clase
`CountVectorizer`.

Los puntajes de los profesores los guardamos en una lista. Separamos en
dos conjuntos los vectores de atributos y los puntajes, uno para
entrenar el modelo y otro para evaluarlo. La separación de los datos
junta los vectores de atributos, en una matriz.

Con los datos preparados podemos entrenar el modelo. Teniendo en cuenta
que las entradas del vector objetivo son números en un continuo, tenemos
que hacer una regresión. Y considerando que la matriz de atributos es
una matriz dispersa, podemos hacer una regresión lineal. La librería
Scikit-learn implementa un método mínimos cuadrados ordinarios (OLS).

## Resultados

El desempeño del algoritmo de regresión fue de alrededor de $n\%$. Para
algunas pruebas era frecuente ver que el modelo sobrestimaba la nota
asignada al profesor. Esto puede ser a causa de que los puntajes más
frecuentes sean 5.0, 4.0 y 4.5, y eran muy pocos los puntajes bajos
asignados a los profesores. Esto claramente inducia un sesgo en el
modelo. Efectivamente, con tantos datos optimistas el modelo resulta
igualmente optimista. Entrenar el modelo con proporciones similares de
opiniones positivas y negativas resulta en una disminución considerable
del volumen de datos y en un modelo igualmente deficiente.

## Conclusiones

Primero, vale la pena resaltar que estos modelos, todavía simples, no
capturan las **razones** por las cuales un profesor es bueno o no. Para
esto, sería necesario un análisis del modelo más cuidadoso, que indique
a posteriori cuales palabras reflejan un mejor puntaje.

De otra parte, los sesgos presentados en el modelo podrían igualmente
darnos información valiosa respecto a la población estudiantil.
Podríamos formular una hipótesis trivial: la alta frecuencia de buenos
puntajes se da porque los profesores son muy buenos. Sin embargo, esto
no nos dice nada respecto a los estudiantes que realizan las reseñas.
Más allá de esto, podríamos decir que los estudiantes con profesores
buenos tienen una inclinación mayor a opinar en linea. O de forma
reciproca, los estudiantes que inscriben con profesores malos tienen
poco interés en evaluarlos. Para poder determinar la validez de
cualquiera de estas hipótesis se tendría que trabajar con un modelo que,
además de considerar la opinión del estudiante y el puntaje del
profesor, incluya la nota que obtuvo el estudiante (también presente
dentro de cada post/reseña).

## Referencias

-   Foster, D. P., Liberman, M., Stine, R. A. (2013). Featurizing Text:
    Converting Text into Predictors for Regression Analysis. 37.

-   Russell, S., & Norvig, P. (2009). 22 Natural language processing.
    (3rd Ed.), Artificial Intelligence: A Modern Approach (pp. 860
    -882). Upper Saddle River, New Jersey: Prentice Hall.

-   Topic-4-linear-models-part-4\_good\_bad\_logit\_movie\_reviews\_XOR.
    (n.d.). Retrieved January 29, 2020, from
    <https://mlcourse.ai/articles/topic4-part4-applications/>

-   Scikit-learn: Machine learning in Python---Scikit-learn 0.22.1
    documentation. (n.d.). Retrieved February 3, 2020, from
    https://scikit-learn.org/stable/index.html
