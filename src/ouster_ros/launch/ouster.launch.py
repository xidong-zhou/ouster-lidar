
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    rviz_config_dir = os.path.join(
        get_package_share_directory('ouster_ros'),
        'rviz',
        'ouster.rviz')
    sensor_hostname = LaunchConfiguration('sensor_hostname', default="10.5.5.86")
    lidar_mode = LaunchConfiguration('sensor_hostname', default="512x10")
    udp_dest = LaunchConfiguration('udp_dest', default="10.5.5.2")
    return LaunchDescription([

        Node(
            package='ouster_ros',
            executable='os_node',
            name='os_node',
            parameters=[{'sensor_hostname': sensor_hostname,
            		  'lidar_mode': lidar_mode,
            		  'udp_dest':udp_dest	
            		  }],
            output='screen'
			),

        Node(
            package='ouster_ros',
            executable='os_cloud_node',
            name='os_cloud_node',
			),

	#Node(
         #   package='rviz2',
          #  executable='rviz2',
           # arguments=['-d', rviz_config_dir],
		#	),
    ])

