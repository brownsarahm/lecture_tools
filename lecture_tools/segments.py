
default_parameters = {}

class Segment():
    '''
    '''
    def __init__(self,info_dict):
        '''
        set name and content
        '''
        self.name = info_dict['info']['name']
        self.content  = info_dict['body'].split('\n')


    def is_slide(self):
        return False

    def is_prereq(self):
        return True

class Module(Segment):
    '''
    Pre requisite modules

    '''
    def __init__(self,info_dict):
        super().__init__(info_dict)
        self.content = '\n'.join(self.content)


class PreModule(Module):
    '''

    '''

class PostModule(Module):
    '''

    '''

    def is_prereq(self):
        return False



class Slide(Segment):
    '''
    base class for Slides
    '''


    def __init__(self,slide_dict):
        '''
        Do segment requirements and strip notes
        '''
        super().__init__(slide_dict)
        self.strip_notes()

        # self.type = slide_dict['info']['type']

    def is_slide(self):
        '''
        Slides
        '''
        return True


    def is_prereq(self):
        '''
        Slides are not prereqs
        '''
        return True

    def strip_notes(self):
        '''
        remove lines that start with > from the body and separate into the
        notes feild
        '''

        body = []
        notes = []


        # iterate line by line and determine notes or text
        for item in self.content:
            if len(item)>0:
                if item[0] == '>':
                    notes.append('- '+item[1:])
                else:
                    body.append(item)

        # merge body back into one
        body = '\n'.join(body)

        # merge notes back together
        notes = '\n\n'.join(notes)

        self.body = body
        self.notes = notes
