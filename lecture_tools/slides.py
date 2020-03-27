from IPython.display import display, Markdown, Latex
from .segments import Slide


class MarkdownSlide(Slide):
    '''
    '''

    def show(self):
        '''
        show a markdown slide saved in the slides folder with filename `title.md`

        Parameters
        ----------
        title : string
            file name with or without extension
        '''

        display(Markdown(self.body))


class ImageSlide(Slide):
    '''
    display an image that has the file name
    '''
    def __init__(self, slide_dict):
        super().__init__(slide_dict)

    def show(self):
        '''
        '''
        display(Markdown('<img src="./slides/' + self.name +'.png" />'))



class ImageAnimateSlide(Slide):
    '''
    display a sequence of images in the same location to overlap
    '''
    def __init__(self, slide_dict):
        super().__init__(slide_dict)

        self.img_list = slide_dict['info']['img_list']

    # def show():
    def show(self):
        '''
        '''
        display(Markdown('<img src="./slides/' + self.name +'.png" />'))



class BulletAnimateSlide(Slide):
    '''
    Slide where markdown points are displayed one at a time on sequential calls
    to show()

    set type to 'animate' and use `--` to separate parts of the slide that will
    be animated
    '''
    def __init__(self,slide_dict):
        super().__init__(slide_dict)
        self.shown_points = 0
        self.body = self.body.split('\n--\n')

    def show(self):
        '''
        '''
        if self.shown_points <=len(self.body):
            self.shown_points +=1

        cur_display = self.body[:self.shown_points]
        display(Markdown(''.join(cur_display)))


class HackmdExercise(Slide):
    '''
    an exercise typ that sends students to a hackmd file
    and then reads back the text from that markdown file to the notebook
    '''

    def __init__(self,slide_dict):
        super().__init__(slide_dict)
        self.url = slide_dict['info']['url']
        self.prompt_shown = False

    def show(self):
        '''
        '''
        if self.prompt_shown:
            self.show_response()
        else:
            self.prompt_shown = True
            self.show_prompt()


    def show_response(self):
        response_url = 'https://' + self.url + '/download/markdown'
        display(Markdown(response_url))

    def show_prompt(self):
        prompt_url = 'https://' +  self.url + '?edit'
        prompt_link = '[Excercise](' + prompt_url + ')'
        display(Markdown(prompt_link))


class GridAppSlide(Slide):
    '''
    '''
    def __init__(self,slide_dict):
        super().__init__(slide_dict)
        self.appgrid = GridspecLayout(len(cur_slide),15)

        self.buttons = []

        self.slide_display = Output()
        with slide_display:
            display(Markdown(self.body[0]))

        self.appgrid[:,1:] = slide_display

        for i in range(len(self.body)-1):
            self.buttons.append(create_toggle(''))
            self.appgrid[i+1,0] = self.buttons[i]
            self.buttons[i].observe(reveal,names='value',)


    def reveal(b):
        sself.lide_display.clear_output()
        cur_lines = [0]
        cur_lines.extend([i+fixed_len for i,bt in enumerate(button) if bt.value])
        with self.slide_display:
    #         display(Markdown(cur_lines))
            display(Markdown(''.join([self.body[l] for l in cur_lines])))

    def show(self):
        return self.appgrid
