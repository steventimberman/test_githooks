import sys
import subprocess
from enum import Enum
from .version import Version, validate_version_string
from tempfile import mkstemp
from os import remove, getcwd
from shutil import move


class CommitType(Enum):
    """ Standard types of commits.

    Extends:
        Enum

    Variables:
        PATCH {str} -- A patch update (small fix)
        MINOR {str} -- A minor update (default)
        MAJOR {str} -- A major update (breaking change)
    """
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"

def get_commit_type(commit_message):
    """
    Parses a commit message string for the type (major, minor, patch)
    trailing a '#'

    Arguments:
        commit_message {string} -- The commit message to be parsed

    Returns:
        string -- The parsed commit type
    """
    split = set(commit_message.lower().split())
    if '#patch' in split:
        return CommitType.PATCH
    elif '#minor' in split:
        return CommitType.MINOR
    elif '#major' in split:
        return CommitType.MAJOR

    return CommitType.MINOR

def update_version_string(commit_type, old_version_string):
    """
    Updates a version string (ex. '1.3.4-Dev' -> '1.3.5-Dev') based on
    the commit type

    Arguments:
        commit_type {string} -- Type of commit, either patch, minor or major
        old_version_string {string} -- String representation of a version

    Returns:
        string -- String representation of the updated version
    """
    current_version = Version(old_version_string)
    if commit_type == CommitType.PATCH:
        current_version.increment_patch()
    elif commit_type == CommitType.MINOR:
        current_version.increment_minor()
    elif commit_type == CommitType.MAJOR:
        current_version.increment_major()
    new_version_string = current_version.get_version_string()
    return new_version_string


def write_new_version(old_version_string, new_version_string):
    """

    Writes the new version to a projects _version.py file's __version_
    attribute, if the version is in the same directory (or same file)

    Arguments:
        old_version_string {string} -- String representation of the version pre-update
        new_version_string {string} -- String representation of the version post-update
    """
    tmpfile, tmpdir = mkstemp()
    with open("_version.py", "r") as old_file:
        with open(tmpdir, 'w') as new_file:
            for line in old_file:
                for line in old_file:
                    new_file.write(line.replace(old_version_string, new_version_string))
    remove("_version.py")
    move(tmpdir, getcwd()+"/"+"version.py")


def update_local_version(old_version_string, commit_message):
    """ Given a commit message and version string, when in a _version.py
        file (containing a __version__ atribute), updates the __version__
        attribute

    Arguments:
        commit_message {string} -- A string commit message
        old_version_string {string} -- String representation of the version pre-update
    """
    commit_type = get_commit_type(commit_message)
    new_version_string = update_version_string(commit_type, old_version_string)
    write_new_version(old_version_string, new_version_string)
    return new_version_string

def add_git_tag_and_amend(version_string):
    validate_version_string(version_string)
    subprocess.run(["git", "commit", "--amend", "_version.py"])
    subprocess.run(["git", "tag", version_string])


def auto_update_version(old_version_string):
    """ Updates the _version.py file based on commit information.

    First, checks the system arguments for a commit message and commit type.
    Then, checks that a squash or merge is taking place, and if so, proceeds
    to update the _version.py file based on commit message.

    Arguments:
        old_version_string {string} -- String representation of the version pre-update

    argv:
        sys.argv[1]: commit message string
        sys.argv[2]: commit type string (ex. 'merge', 'squash', 'message')

    Raises:
        Exception -- [description]
    """
    try:
        commit_message = sys.argv[1]
        commit_type = sys.argv[2]
    except IndexError:
        print ("""WARNING: No commit message or commit type found!\n
                Not enough system arguments were passed.\n
                Make sure you're prepare-commit-message git hook\n
                is configured correctly.""")
        sys.exit(1)
    except Exception:
        raise Exception("""Auto Versioning Error:\n
                There is a problem accessing your system arguements""")
    else:
        if commit_type == 'merge' or commit_type == 'squash':
            new_version_string = update_local_version(old_version_string, commit_message)
            add_git_tag(new_version_string)
            print ("You're new version is " + version_string)







