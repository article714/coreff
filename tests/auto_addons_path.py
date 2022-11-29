
#!/usr/bin/env python3
"""
This script updates odoo.conf configuration file in order that addons_path
configuration variable lists all and only available paths containing
Odoo modules.

It is meant to be used inside an odoo-container based container, where
addons are stored in sub-directories of "/home/odoo/addons" (static value).
"""


from os import walk, environ
from os.path import exists
from sys import exit as sysexit
import pathlib
from configparser import ConfigParser, NoSectionError, NoOptionError
import logging


def main() -> None:
    listed_addons_paths = listing_addons_path()
    odoo_conf = read_odoo_conf()
    try:
        odoo_conf.get("options", "addons_path")
    except NoSectionError:
        logging.error("Could not parse odoo.conf")
        sysexit(1)
    except NoOptionError:
        odoo_conf["options"]["addons_path"] = ""

    add_listed_addons_paths_to_odoo_conf(listed_addons_paths, odoo_conf)
    clean_invalid_path(odoo_conf)
    write_odoo_conf(odoo_conf)


def listing_addons_path() -> set:
    path = "/home/odoo/addons"

    addons_paths = set()
    for root, directory, files in walk(path):
        if "__manifest__.py" in files:
            addon_path = str(pathlib.Path(root).parent.absolute())
            addons_paths.add(addon_path)

    return addons_paths


def read_odoo_conf() -> ConfigParser:

    odoo_conf = ConfigParser()

    file_path = environ.get("ODOO_RC", "None")
    if not file_path:
        logging.error(
            f"You need to define ODOO_RC environment var pointing to odoo.conf")
    else:
        result = odoo_conf.read(file_path)

        if not result:
            logging.error(f"Could not parse file: {file_path}")

    return odoo_conf


def write_odoo_conf(odoo_conf: ConfigParser) -> None:
    if "ODOO_RC" not in environ:
        logging.error(
            f"You need to define ODOO_RC environment var pointing to odoo.conf")

    with open(environ["ODOO_RC"], "w") as odoo_conf_file:
        odoo_conf.write(odoo_conf_file)


def add_listed_addons_paths_to_odoo_conf(
    listed_addons_paths: set, odoo_conf: ConfigParser


) -> None:
    current_addons_path = odoo_conf["options"]["addons_path"]
    listed_addons_paths.update(current_addons_path.split(","))
    odoo_conf["options"]["addons_path"] = ",".join(listed_addons_paths)


def clean_invalid_path(odoo_conf: ConfigParser) -> None:
    addons_path = odoo_conf["options"]["addons_path"].split(",")
    validated_path = []
    for path in addons_path:
        if exists(path):
            validated_path.append(path)

    odoo_conf["options"]["addons_path"] = ",".join(validated_path)


if __name__ == "__main__":
    main()
