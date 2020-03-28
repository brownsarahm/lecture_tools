from lecture_tools import Presentation
import sys


def main():
    '''
    takes two parameters: a markdown file as input and a directory to write the
    presentation out to

    generates a reveal.js compatible repo
    '''
    in_md = sys.argv[1]
    out_dir = sys.argv[2]
    lecture = Presentation(in_md)
    lecture.generate_lecture_repo(out_dir)
