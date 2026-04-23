
# Exercice 2. Les 3 bacs

## 1) Équations d'état du système

Les équations d'état du système sont les suivantes :

$$
\left\{
\begin{array}{l}
\dot{h}_1 = -x(h_1) - x(h_1 - h_2) + u_1 \\
\dot{h}_2 = x(h_1 - h_2) - x(h_2 - h_3) \\
\dot{h}_3 = -x(h_3) + x(h_2 - h_3) + u_2 \\
y = \begin{pmatrix} y_1 \\ y_2 \end{pmatrix} = \begin{pmatrix} h_1 \\ h_2 \end{pmatrix}
\end{array}
\right.
$$

avec \( x = \begin{pmatrix} h_1 \\ h_2 \\ h_3 \end{pmatrix} \).

On dérive la sortie \( y = \begin{pmatrix} y_1 \\ y_2 \end{pmatrix} \) jusqu'à obtenir la commande \( u = \begin{pmatrix} u_1 \\ u_2 \end{pmatrix} \).

$$
y = \begin{pmatrix} y_1 \\ y_2 \end{pmatrix} = \begin{pmatrix} h_1 \\ h_2 \end{pmatrix} = \begin{pmatrix} -x(h_1) - x(h_1 - h_2) + u_1 \\ -x(h_2) + x(h_2 - h_3) + u_2 \end{pmatrix}
$$

On pose \( b(x) = \begin{pmatrix} -x(h_1) - x(h_1 - h_2) \\ -x(h_2) + x(h_2 - h_3) \end{pmatrix} \), d'où \( y = b(x) + u \).

On choisit \( \boxed{u = v - b(x)} \), ce qui donne \( y = v \), où \( v \) peut être choisi librement.

---

## 2) Contrôle proportionnel intégral (PI)

Un contrôle proportionnel intégral permet d'écrire la commande sous la forme :

$$
v = x_0(w - y) + x_1 \int_0^t (w(z) - y(z)) \, dz + \dot{w}
$$

où :
- \( w \) est la consigne,
- \( x_0 \) et \( x_1 \) sont des coefficients déterminés par placement de pôles.

En appliquant cette commande, on obtient :

$$
y = b(x) + u \Leftrightarrow y = v \Leftrightarrow \ddot{e} + x_0 \dot{e} + x_1 e = 0
$$

avec \( e = w - y \) l'erreur du système.

Le polynôme caractéristique est :

$$
\Delta^2 + x_0 \Delta + x_1 = 0
$$

Un placement de pôles en -1 donne :

$$
\Delta^2 + x_0 \Delta + x_1 = (\Delta + 1)^2 = \Delta^2 + 2\Delta + 1
$$

On en déduit :

$$
x_0 = 2 \quad \text{et} \quad x_1 = 1
$$

---

## 3) Réécriture de la commande

On pose \( \tilde{y} = \int_0^t (w(z) - y(z)) \, dz \). On peut alors écrire la commande sous la forme :

$$
\left\{
\begin{array}{l}
\tilde{y} = w - y \\
v = \tilde{y} + 2(w - y) + \dot{w}
\end{array}
\right.
$$
