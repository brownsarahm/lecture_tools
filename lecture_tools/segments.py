
default_parameters = {}

class Segment():
    '''
    '''
    def __init__(self,info_dict):
        self.name = info_dict['info']['name']
        self.content  = info_dict['body'].split('\n')


    def is_slide(self):
        return False

class Canvas(Segment):
    '''

    '''
    def __init__(self,info_dict):
        super().__init__(info_dict)



class Slide(Segment):
    '''
    base class for Slides
    '''


    def __init__(self,slide_dict):
        super().__init__(slide_dict)

        self.strip_notes()

        # self.type = slide_dict['info']['type']

    def is_slide(self):
        return True

    def strip_notes(self):

        body = []
        notes = []

        # iterate line by line and determine notes or text
        for item in self.content:
            if len(item)>0 and item[0] == '>':
                notes.append('- '+item[1:])
            else:
                body.append(item)

        # merge body back into one
        body = '\n'.join(body)

        # merge notes back together
        notes = '\n\n'.join(notes)

        self.body = body
        self.notes = notes
