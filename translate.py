from .settings import *
import requests
import argparse


def main():
    pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_words', help="target translate words", type=str)
    parser.add_argument('lang'，help="language you use", default="en", type=str)


if __name__ == "__main__":
    pass
