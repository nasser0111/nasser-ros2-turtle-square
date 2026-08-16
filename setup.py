"""ROS 2 package configuration."""

from glob import glob
from setuptools import find_packages, setup


PACKAGE_NAME = "nasser_ros2_tasks"


setup(
    name=PACKAGE_NAME,
    version="1.0.0",
    packages=find_packages(exclude=("tests",)),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{PACKAGE_NAME}"]),
        (f"share/{PACKAGE_NAME}", ["package.xml"]),
        (f"share/{PACKAGE_NAME}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Nasser Mamdouh Alshareef",
    maintainer_email="nasser@example.com",
    description=(
        "ROS 2 publisher/subscriber example and a turtlesim square-motion "
        "controller."
    ),
    license="MIT",
    entry_points={
        "console_scripts": [
            "phrase_publisher = nasser_ros2_tasks.phrase_publisher:main",
            "phrase_subscriber = nasser_ros2_tasks.phrase_subscriber:main",
            "square_turtle = nasser_ros2_tasks.square_turtle:main",
        ],
    },
)
