# -*- coding: utf-8 -*-
import logging
import argparse

from .pipit import build

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.StreamHandler()])


def main(args=None):
    """Console script for pipit"""
    parser = argparse.ArgumentParser(
        description="A package manager for python")
    parser.add_argument("--index", "-i", action="store", dest="index",
                        default="https://pypi.python.org/simple",
                        help="pypi index")
    parser.add_argument("--download", "-d", action="store",
                        dest="download_dir",
                        default=None,
                        help="download directory for tarball")
    results = parser.parse_args()
    build(results.index, results.download_dir)

if __name__ == "__main__":
    main()
