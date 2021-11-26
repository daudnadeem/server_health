from setuptools import setup, find_packages

REQUIRED_PACKAGES = ["requests", "pyyaml"]

setup(
    name='server_health',
    version='1',
    description='Service to monitor server health for: Magnificent',
    author='Me',
    author_email='Me',
    license='',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>3.7',
    install_requires=REQUIRED_PACKAGES,
    # Create alias 'mag_hlth' to call health_monitor.py
    entry_points={
        "console_scripts": [
            "mag_hlth = server_health.health_monitor:main",
        ],
    },
    # Include logging.yaml when installed as package
    package_data={
        "": ["*.yaml"],
    },
)
