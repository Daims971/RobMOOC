# Exercice 2 — Les 3 bacs

---

## 1) Équations d'état du système

Les équations d'état du système sont :

$$
\dot{h}_1 = -h_1 - (h_1 - h_2) + u_1
$$

$$
\dot{h}_2 = (h_1 - h_2) - (h_2 - h_3)
$$

$$
\dot{h}_3 = -h_3 + (h_2 - h_3) + u_2
$$

$$
y =
\begin{pmatrix}
y_1 \\
y_2
\end{pmatrix}
=
\begin{pmatrix}
h_1 \\
h_2
\end{pmatrix}
$$

avec :

$$
x =
\begin{pmatrix}
h_1 \\
h_2 \\
h_3
\end{pmatrix}
$$

---

On dérive la sortie :

$$
\dot{y} =
\begin{pmatrix}
\dot{h}_1 \\
\dot{h}_2
\end{pmatrix}
$$

$$
=
\begin{pmatrix}
- h_1 - (h_1 - h_2) + u_1 \\
- h_2 + (h_2 - h_3) + u_2
\end{pmatrix}
$$

---

On pose :

$$
b(x) =
\begin{pmatrix}
- h_1 - (h_1 - h_2) \\
- h_2 + (h_2 - h_3)
\end{pmatrix}
$$

---

D'où :

$$
\dot{y} = b(x) + u
$$

---

On choisit :

$$
u = v - b(x)
$$

ce qui donne :

$$
\dot{y} = v
$$

où \( v \) est une nouvelle entrée libre.

---

## 2) Contrôle proportionnel intégral (PI)

On choisit :

$$
v = x_0 (w - y) + x_1 \int_0^t (w(z) - y(z)) \, dz + \dot{w}
$$

avec :

- \( w \) la consigne  
- \( x_0, x_1 \) des gains  

---

On pose :

$$
e = w - y
$$

Alors :

$$
\ddot{e} + x_0 \dot{e} + x_1 e = 0
$$

---

Polynôme caractéristique :

$$
\lambda^2 + x_0 \lambda + x_1 = 0
$$

Placement de pôles en -1 :

$$
(\lambda + 1)^2 = \lambda^2 + 2\lambda + 1
$$

Donc :

$$
x_0 = 2, \quad x_1 = 1
$$

---

## 3) Réécriture de la commande

On pose :

$$
\tilde{y} = \int_0^t (w(z) - y(z)) \, dz
$$

Alors :

$$
\dot{\tilde{y}} = w - y
$$

$$
v = \tilde{y} + 2(w - y) + \dot{w}
$$
