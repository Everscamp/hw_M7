from setuptools import setup, find_packages

setup(name='clean_folder_sort_folder',
      version='0.0.1',
      entry_points={
        'console_scripts': ['clean-folder = clean_folder.clean:main']
      },
      url='https://github.com/Everscamp/hw_M7',
      description='Sort folder by file types',
      author='Everscamp',
      packages=find_packages()
)