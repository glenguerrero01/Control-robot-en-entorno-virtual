# Control-robot-en-entorno-virtual
Repositorio del experimento de navegación autónoma SLAM con Turtle Bot


Navegación autónoma de un **TurtleBot3 con LiDAR** en simulación, usando **ROS 2 Jazzy** y **Gazebo** (moderno). El robot se desplaza de forma autónoma desde una pose inicial hasta un punto objetivo dentro de un escenario personalizado, construyendo el mapa en tiempo real mediante **SLAM**.

<img width="400" src="https://github.com/user-attachments/assets/5b5ad8e7-6178-4b67-8ebe-1dbbdca94490" />

## Video funcionamiento
https://youtu.be/GMJ8F4e_gUA

## Descripción

El proyecto integra el simulador Gazebo con ROS 2 a través de un paquete propio (`mi_paquete_nav`) que actúa como **punto único de entrada**: un solo archivo de lanzamiento coordina el arranque del mundo, la inserción del robot, la activación del tiempo simulado y el arranque de la pila de navegación **Nav2**.

El escenario se construyó a partir de un modelo **STL** encapsulado en un modelo SDF con geometría de visualización y de colisión, e incluido de forma modular en el mundo. La geometría de colisión es la que permite que el LiDAR detecte las paredes y obstáculos del entorno.

## Requisitos

- Ubuntu 24.04 LTS
- ROS 2 Jazzy Jalisco
- Gazebo (moderno) + Nav2
- Paquetes de simulación del TurtleBot3 (`nav2_minimal_tb3_*`)

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-nav2-minimal-tb3*
```

## Estructura del paquete

```
mi_paquete_nav/
├── CMakeLists.txt
├── package.xml
├── worlds/
│   └── escenario.sdf          # Mundo: iluminación + inclusión del escenario
├── models/
│   └── escenario/
│       ├── model.config
│       ├── model.sdf          # Encapsula el STL (visual + colisión)
│       └── meshes/
│           └── escenario.stl  # Modelo 3D del escenario
├── launch/
│   └── escenario_nav.launch.py  # Punto único de entrada
├── params/
│   └── nav2_params.yaml       # Parámetros de navegación
└── maps/
    └── mi_mapa.pgm / .yaml    # Mapa resultante del SLAM
```

## Ejecución

Clonar/copiar el paquete dentro del `src` del workspace y construir:

```bash
cd ~/ros2_ws
colcon build --packages-select mi_paquete_nav --symlink-install
source install/setup.bash
```

Lanzar el sistema completo (Gazebo + TurtleBot3 + Nav2 en modo SLAM):

```bash
ros2 launch mi_paquete_nav escenario_nav.launch.py
```

Una vez cargados Gazebo y RViz, pulsar **`Nav2 Goal`** en RViz y seleccionar un punto objetivo dentro del escenario. El robot planificará la trayectoria y se desplazará evitando los obstáculos.

> La primera carga de Gazebo puede tardar varios minutos mientras se cachean los modelos.

## Verificación

Comprobaciones técnicas con la simulación en ejecución (terminal aparte):

```bash
ros2 topic hz /scan                              # Frecuencia del LiDAR
ros2 topic echo /scan --once                     # Marco (frame_id) del LiDAR
ros2 run tf2_tools view_frames                   # Diagrama del árbol TF
ros2 param get /controller_server use_sim_time   # Tiempo simulado (True)
ros2 topic echo /clock --once                    # Reloj de simulación activo
```
<img width="400" src="https://github.com/user-attachments/assets/e6c3feec-9d02-4146-b021-d9cab473e9d2" />

## Guardar el mapa

```bash
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/mi_paquete_nav/maps/mi_mapa
```
<img width="101" src="https://github.com/user-attachments/assets/b72fd94b-a7a4-44cc-8f8f-047609707c0d" />


## Notas

- El escenario se declara como `static` y su superficie se alinea al plano `z = 0` para insertar el robot sin interpenetración con el suelo.
- La navegación se ejecuta en modo **SLAM** porque el escenario no dispone de mapa previo; el mapa se construye en tiempo real.
