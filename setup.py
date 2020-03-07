from setuptools import setup

setup(name='Lecture Tools',
      version='0.1',
      description='tools for lecturing with notebooks',
      url='',
      author='Sarah M Brown',
      author_email='sarah_m_brown@brown.edu',
      license='MIT',
      packages=['lecture_tools'],
      zip_safe=False,
      include_package_data = True,
      install_requires=['IPython'],
#       entry_points = {
#         'console_scripts': ['wiggum-app=wiggum_app.command_line:main'],}
     )
