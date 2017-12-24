from setuptools import setup

setup(name='robocall',
      version='0.1',
      description='Remotely controllable video call capable server',
      url='https://github.com/c4obi/robodock.git',
      author='Flying Circus',
      author_email='anthony.chinwo@gmail.com',
      license='MIT',
      packages=['robocall'],
      install_requires=[
          'tornado',
          'unittest2',
      ],
      zip_safe=False)