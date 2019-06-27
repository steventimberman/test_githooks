import sys

from src.update_version import update_version


def main(commit_message):
	update_version(commit_message)

# if __name__ == '__main__':
# 	try:
# 		commit_message = sys.argv[1]
# 		commit_type = sys.argv[2]
# 	except IndexError:
# 		print ("""WARNING: No commit messagen or commit type found!\n
# 				Not enough system arguments were passed.\n
# 				Make sure you're prepare-commit-message git hook\n
# 				is configured correctly.""")
# 		sys.exit(1)
# 	except Exception:
# 		raise Exception("""Auto Versioning Error:\n
# 				There is a problem accessing your system arguements""")
# 	else:
# 		if commit_type == 'merge' or commit_type == 'squash':
# 			main(commit_message)