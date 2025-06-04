# 🐉 Cursed Dungeon

*Versión actual: v0.2*

---

## 📌 Descripción general

*Cursed Dungeon* es un juego de rol por turnos ambientado en un universo oscuro y maldito. El jugador explora mazmorras, se enfrenta a enemigos cada vez más peligrosos y desarrolla sus habilidades a través de un sistema de progresión por niveles. El objetivo final es derrotar a *Ella, Diosa de la Perdición*, en el nivel 70.
El juego combina mecánicas clásicas de combate RPG con elementos estratégicos como estados alterados, gestión de recursos y enemigos con dificultad creciente. Está diseñado para ejecutarse inicialmente en terminal, con planes de expansión a una versión gráfica usando Pygame.

---

## 🧪 Versión actual

- *v0.2*  
  Incluye: sistema de combate funcional, enemigos con estados alterados, animaciones básicas en terminal, y primeras pruebas con estructura modular.

---

## 🖥️ Lenguajes utilizados

- 🐍 *Python* 3.9+

---

## 🧰 Librerías y frameworks

- asciimatics – Animaciones por terminal
- pygame – Para desarrollo futuro de la versión gráfica (en desarrollo)
- random, time, math – Librerías estándar de Python usadas para lógica y tiempos

---

## ✨ Características del proyecto

- ⚔️ Combate por turnos con animaciones de ataque y efectos
- 📈 Sistema de progresión hasta nivel 70
- 👿 Jefes únicos con habilidades especiales
- 🧪 Estados alterados con probabilidades dinámicas según tipo de enemigo
- 🧱 Estructura modular del código: separación de lógica, animación y datos
- 📁 Preparado para escalabilidad (versión gráfica futura, sistema de guardado, etc.)

---

Cursed-Dungeon/
├── data/                 # Configuración de enemigos, niveles, etc.
├── engine/               # Lógica de combate y control del juego
├── animations/           # Animaciones y efectos visuales
├── assets/               # Archivos visuales o de sonido (futuros)
├── main.py               # Punto de entrada del juego
└── README.md             # Este archivo
