import updater.update_version as update_version


# print (dir())
# print (__file__)
# print (__name__)
# print (__package__)
# from .update_version import  auto_update_version

__version__ = "1.1.1"



update_version.auto_update_version(__version__)

