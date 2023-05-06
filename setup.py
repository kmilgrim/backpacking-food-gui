from setuptools import setup, find_packages

setup(
    name='backpacking_food_gui',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Pillow==8.3.2',
        'bcrypt==3.2.0',
        'customtkinter==5.1.2'
    ],
    entry_points={
        'console_scripts': [
            'backpacking_food_gui = main_app:main'
        ]
    },
    author='Kira Milgrim',
    author_email='kmilgrim@bu.edu',
    description='A GUI application for planning your backpacking meals and ingredients',
    url='https://github.com/kmilgrim/backpacking-food-gui',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='backpacking food gui',
    project_urls={
        'Bug Reports': 'https://github.com/kmilgrim/backpacking-food-gui/issues',
        'Source': 'https://github.com/kmilgrim/backpacking-food-gui'
    },
)
