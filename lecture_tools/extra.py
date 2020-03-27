
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

def show_response(base_url):
    response_url = base_url + '/download/markdown'
    display(Markdown())

def show_prompt(base_url):
    promp_url = base_url + '?edit'
    prompt_link = '[Excercise](' + propmp_url + ')'
    display(Markdown(prompt_link))
