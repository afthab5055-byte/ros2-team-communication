from setuptools import find_packages, setup

package_name = 'roshub'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/roshub/launch', ['launch/team_system.launch.py']),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='afthab',
    maintainer_email='afthab@todo.todo',
    description='ROS 2 based multi-user communication and team collaboration tool.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'chat_node = roshub.chat_node:main',
            'chat_subscriber = roshub.chat_subscriber:main',
            'presence_node = roshub.presence_node:main',
            'presence_monitor = roshub.presence_monitor:main',
            'ros_monitor = roshub.ros_monitor:main',
            'team_monitor = roshub.team_monitor:main',
            'team_gui = roshub.team_gui:main',
        ],
    },
)
