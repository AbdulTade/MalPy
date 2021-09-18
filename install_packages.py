'''
    Script file obtained from url https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    Courtesy of Glenn Thompson
'''

import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


class Install_Requirements:

    def __init__(self,requirement_list) -> None:
        self.requirement_list = requirement_list

    def __should_install_requirement(self,requirement):
        should_install = False
        try:
            pkg_resources.require(requirement)
        except (DistributionNotFound, VersionConflict):
            should_install = True
        return should_install


    def install_packages(self):
        try:
            requirements = [
                requirement
                for requirement in self.requirement_list
                if self.__should_install_requirement(requirement)
            ]
            if len(requirements) > 0:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
            else:
                print("Requirements already satisfied.")

        except Exception as e:
            print(e)

if __name__ == '__main__':
    REQUIRED = [ 
        'keyboard',
        'requests',
        'pyaescrypt',
        'Crypto'
    ]
    Install_Requirements(REQUIRED).install_packages()

