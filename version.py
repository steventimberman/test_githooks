import re


class Version:
    """
    class: represents a version of a piece of software. Divides the version
        into a major, minor, and patch version number, along with a version type.
        Example is '1.2.3-dev', where the major version number is 1, minor is
        2, with 3 patch updates, and a version type of 'dev'.
    """

    def __init__(self, version_string="0.0.0"):
        """
        Args:
            version_string(string): a string representation of
            a version. In the form a.b.c-type, where a is the
            major update number, b is the minor, c is the patch,
            and version_type is the purpose of the version
            release (version_type is optional, without we use
            a.b.c form)
        """

        validate_version_string(version_string)

        version_number_and_type = version_string.split("-")
        version_num = version_number_and_type[0]
        has_no_version_type = len(version_number_and_type) != 2
        self._version_type = "" if (has_no_version_type) else version_number_and_type[1]

        # sets object's major, minor and patch numbers (to ints)
        self._major, self._minor, self._patch = map(
            lambda x: int(x), version_number_and_type[0].split("."))

    def get_version_string(self):
        """ Gets a string representation of the version object
            Returns:
                string of the version, in the same form as an input to initialize the object
        """
        version_string = "{major}.{minor}.{patch}".format(
                major = self.major,
                minor = self.minor,
                patch = self.patch
            )

        if self.version_type:
            version_string += "-%s" %self.version_type

        return version_string

    @property
    def major(self):
        """ Get major version number
        """
        return self._major

    @property
    def minor(self):
        """ Get minor version number
        """
        return self._minor

    @property
    def patch(self):
        """ Get patch version number
        """
        return self._patch

    @property
    def version_type(self):
        """ Get version type
        """
        return self._version_type

    def increment_patch(self):
        """ Increments the patch number by 1.
        """
        self._patch += 1

    def increment_minor(self):
        """ Increments the minor number by 1. Resets the patch number to 0.
        """
        self._minor += 1
        self._patch = 0

    def increment_major(self):
        """ Increments the major number by 1. Resets the minor and
            patch number to 0.
        """
        self._major += 1
        self._minor, self._patch = 0, 0

    def __eq__(self, other):
        return (self._major == other.get_major()
                and self._minor == other.get_minor()
                and self._patch == other.get_patch()
                and self._version_type == other.get_version_type())


INPUT_FORMAT_ERR = """ Please use the format:\n'a.b.c' or 'a.b.c-type',
                    \nwhere a,b,c are integers, and type is a alphanumeric. """

def validate_version_string(version_string):
    if (not isinstance(version_string, str)
            or (not re.fullmatch(r'\d\.\d\.\d([-]\w+)*', version_string))
            or version_string.count("-") > 1
        ):
        raise Exception("Invalid version string." + INPUT_FORMAT_ERR)
