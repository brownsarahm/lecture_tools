from lecture_tools import Presentation
import sys

def main():
    '''
    '''
    in_md = sys.argv[1]
    out_dir = sys.argv[2]
    lecture = Presentation(in_md)
    lecture.generate_lecture_repo(out_dir)
