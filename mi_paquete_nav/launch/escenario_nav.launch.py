import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg = get_package_share_directory('mi_paquete_nav')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    world = os.path.join(pkg, 'worlds', 'escenario.sdf')
    params = os.path.join(pkg, 'params', 'nav2_params.yaml')

    # Para que Gazebo resuelva model://escenario (tus meshes STL)
    set_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(pkg, 'models')
    )

    # Reutiliza el sim de TB3 + Nav2, pero con TU mundo y TUS parámetros
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'tb3_simulation_launch.py')
        ),
        launch_arguments={
            'world': world,
            'params_file': params,
            'slam': 'True',
            'use_sim_time': 'True',
            'headless': 'False',
        }.items()
    )

    return LaunchDescription([
        set_resource_path,
        sim,
    ])