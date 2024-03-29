#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""The Lensfun Python package.  It provides common functionality for Python
scripts that want to find or read the Lensfun database.
"""

import os


def get_database_version():
    """Returns the database version of the installed Lensfun.  Note that if
    multiple versions of Lensfun are installed, the returned version number
    refers to the one that was installed together with the Python scripts.

    :return:
      the version number of Lensfun's database

    :rtype: int
    """
    return 1


def get_core_database():
    """Finds the upstream (core) database.  The core database is the database
    installed with Lensfun, or downloaded by “lensfun-update-data”.

    :return:
      the timestamp of the local core database and its path; if no core
      database is found, it returns ``(0, None)``

    :rtype: int, str
    """

    def get_timestamp(path):
        try:
            return int(open(os.path.join(path, "timestamp.txt")).read())
        except (FileNotFoundError, PermissionError, ValueError):
            return 0

    versioned_subdir = "version_{}".format(get_database_version())
    db_path_candidates = {"/var/lib/lensfun-updates",
                          os.path.expanduser("~/.local/share/lensfun/updates"),
                          ""}
    newest_path = None
    newest_timestamp = 0
    for path in db_path_candidates:
        path = os.path.join(path, versioned_subdir)
        timestamp = get_timestamp(path)
        if timestamp > newest_timestamp:
            newest_timestamp = timestamp
            newest_path = path
    return newest_timestamp, newest_path


def get_database_directories():
    """Returns the directories containing Lensfun databases.  The list returned
    should be iterated over to realise proper overriding of database entries.
    Thus, later entries take higher precedence over earlier entries.  Note that
    if multiple versions of Lensfun are installed, the returned list refers to
    the one that was installed together with the Python scripts.  Also note
    that Lensfun databases consist only of the files in a particular directory,
    and do not include automatically all files in sub-directories as well.

    All returned paths are guaranteed to exist, however, they may contain no
    database files or at least no ones readable to the current user.

    :return:
      list with paths to Lensfun databases

    :rtype: list of str
    """
    versioned_subdir = "version_{}".format(get_database_version())
    core_database_path = get_core_database()[1]
    paths = [core_database_path] if core_database_path else []
    for path in (os.path.expanduser("~/.local/share/lensfun"),
                 os.path.expanduser("~/.local/share/lensfun/" + versioned_subdir)):
        if os.path.isdir(path):
            paths.append(path)
    return paths
