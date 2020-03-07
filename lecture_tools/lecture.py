import os
from IPython.display import display, Markdown, Latex
from numpy import inf


def md_file(name,ext='.md'):
    '''
    add md extention if not present
    '''
    
    if name[-2:] == ext:
        return name
    else:
        return name + ext
    
def ismd(name):
    return name[-2:] == '.md'
    

def show_frame(title):
    '''
    show a markdown slide saved in the slides folder with filename `title.md`
    
    Parameters
    ----------
    title : string
        file name with or without extension
    '''
    
    
    slide_file = os.path.join('slides',md_file(title))
    
    
    with open(slide_file) as f:
        slide = f.read()
        
    display(Markdown(slide))
    
def show_slide(title,line):
    '''
    show a markdown slide saved in the slides folder with filename `title.md`
    
    Parameters
    ----------
    title : string
        file name with or without extension
    '''
    
    
    slide_file = os.path.join('slides',md_file(title))
    
    
    with open(slide_file) as f:
        slide = f.read_line()
        
    display(Markdown(slide))
    
def show_image(title):
    '''
    '''
    
    display(Markdown('<img src="./slides/' + title +'.png" />'))
    
    
    
    
class Presentation():
    
    def __init__(self):
        
        self.frame_files = [f for f in os.listdir('slides') if ismd(f)]
        self.frame_status = {filename[:-3]:0 for filename in self.slide_files}
        
    def show(self,title):
        show_frame(title)
        self.frame_status[title] = inf
        
#     def next_slide(self,title):