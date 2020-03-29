import os, shutil
from IPython.display import display, Markdown, Latex
from numpy import inf
from .slides import (MarkdownSlide, ImageSlide, ImageAnimateSlide,
                    BulletAnimateSlide, HackmdExercise)
from .segments import PreModule, PostModule
import pkg_resources as pkgrs


segment_shortnames = {'md':MarkdownSlide,
                    'img':ImageSlide,
                    'img-animate': ImageAnimateSlide,
                    'animate':BulletAnimateSlide,
                    'hackmd':HackmdExercise,
                    'canvas':PreModule,
                    'prereq':PreModule,
                    'postnotes':PostModule}

copy_path = os.path.join('resources','copy')
copy_files = pkgrs.resource_listdir(__name__,copy_path)

pystring_path = os.path.join('./resources','pystrings')




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

# slide_types

handout_header = "---\nlayout: handouts\nslideset :{}\npermalink:handout/---"
slides_header = "---\nlayout:slides\nslideset :{}\npermalink:slides/---"

class Presentation():

    def __init__(self,content_file):
        '''
        load a file and create the object
        '''

        self.title, _ = content_file.split('.')
        self.sourcefile = os.path.abspath(content_file)
        self.slides = {}
        self.slide_order_list = []
        self.slide_order_dict = {}
        self.supplementary = {}
        self.curslide = 0
        self.input_md(content_file)

    def input_md(self,file):
        '''
        '''

        with open(file) as mdf:
            lect_raw = mdf.read()


        # split slides
        segments_raw = lect_raw.split('----')
        meta = segments_raw[0]
        # split header from body
        segments_header_body = [s.split('---') for s in segments_raw[1:]]
        # make one dict per slide and strucutre info into subdict
        segment_list = [{'info':{p[0].strip():p[1].strip()
                for p in [(kv.split(':')) for kv in s[0].strip().split('\n')]},
                        'body':s[1]}
                             for s in segments_header_body]

        # create a dictionary with name:SlideObject
        segments = {s['info']['name']:self.generate_object(s) for s in segment_list}
        slides = {s.name:s for s in segments.values() if s.is_slide()}
        supplementary = {s.name: s for s in segments.values() if not(s.is_slide())}

        # dictionaries do not preserve order
        title_list = [s['info']['name'] for s in segment_list]
        slide_order_list = [title for title in title_list
                                        if segments[title].is_slide() ]
        slide_order_dict = {title:i + len(self.slides)
                                for i,title in enumerate(slide_order_list)}

        if len(set(slide_order_list)) < len(slide_order_list):
            raise NameError('Reused Slide Name')
        # append all (update is dictionary apped)
        self.slides.update(slides)
        self.supplementary.update(supplementary)
        self.slide_order_list.extend(slide_order_list)
        self.slide_order_dict.update(slide_order_dict)

        # meta data parsing
        meta = meta.split('\n')
        #split all non empty ones at :
        meta = [m.split(':') for m in meta if len(m)>0]
        meta = {m[0].strip():m[1].strip() for m in meta}
        self.meta = meta

    def generate_object(self,slide_dict):
        '''
        parse the dict to create the right type of object
        '''
        # complete the info fields
        if not('type' in slide_dict['info'].keys()):
            slide_dict['info']['type'] = 'md'
        # return the slide after parsing
        return segment_shortnames[slide_dict['info']['type']](slide_dict)

    def show(self,title):
        '''
        '''
        self.curslide = self.slide_order_dict[title]
        self.slides[title].show()

    def next(self):
        '''
        '''
        self.curslide += 1
        title = self.slide_order_list[self.curslide]
        self.slides[title].show()

    def __get_item__(self,key):
        '''
        '''
        self.slides[key].show()

    def generate_lecture_repo(self,repo_dir, slide_dir = '_slides'):
        '''
        generate repository that will work with reveal.js via the
        jekyll-reveal-deck-pack theme

        '''
        # copy files
        for file in copy_files:
            source_path = os.path.join(copy_path,file)
            source = pkgrs.resource_filename(__name__,source_path)
            # with open(source,'r') as f:
            #     source_str = f.read()

            destination = os.path.join(repo_dir,file)
            shutil.copy(source,destination)
            # with open(destination,'r') as f:
            #     f.write(source_str)



        # ---------------------------------------------------------------------
        #                        process readme
        # ---------------------------------------------------------------------
        readme_path = os.path.join(pystring_path,'README.md')
        # read in readme template
        readme_file =  pkgrs.resource_filename(__name__,readme_path)
        with open (readme_file,'r') as f:
            readme_template = f.read()

        # format readme
        readme = readme_template.format(title = self.meta['title'],
                                description = self.meta['description'])

        # write readme
        with open(os.path.join(repo_dir,'README.md'),'w') as f:
            f.write(readme)

        # ---------------------------------------------------------------------
        #                        process index
        # ---------------------------------------------------------------------
        index_path = os.path.join(pystring_path,'index.md')
        # read in readme template
        index_file =  pkgrs.resource_filename(__name__,index_path)
        with open (index_file,'r') as f:
            index_template = f.read()

        # format readme
        index = index_template.format(title = self.meta['title'],
                                description = self.meta['description'])

        index += '\n## [Slides]({{ site.baseurl }}{% link slides.md %})'
        index += '\n## [Handout]({{ site.baseurl }}{% link handout.md %})'


        # write readme
        with open(os.path.join(repo_dir,'index.md'),'w') as f:
            f.write(index)


        # ---------------------------------------------------------------------
        #                        process hanouts
        # ---------------------------------------------------------------------
        handout_template_path = os.path.join(pystring_path,'handout_header.md')
        # read in readme template
        handout_file =  pkgrs.resource_filename(__name__,handout_template_path)
        with open (handout_file,'r') as f:
            handout_template = f.read()

        prereq_list = [s.content for s in self.supplementary.values() if s.is_prereq]
        prereqs = '\n<hr>\n'.join(prereq_list)
        # format readme
        handout = handout_template.format(slide_dir = slide_dir.strip('_'),
                                prereqs = prereqs)

        # write readme
        with open(os.path.join(repo_dir,'handout.md'),'w') as f:
            f.write(handout)

        # ---------------------------------------------------------------------
        #                        process slides
        # ---------------------------------------------------------------------
        slide_template_path = os.path.join(pystring_path,'slides.md')
        # read in readme template
        slides_file =  pkgrs.resource_filename(__name__,slide_template_path)
        with open (slides_file,'r') as f:
            slides_template = f.read()

        # format readme
        slides = slides_template.format(slide_dir = slide_dir.strip('_'))

        # write readme
        with open(os.path.join(repo_dir,'slides.md'),'w') as f:
            f.write(slides)

        # ---------------------------------------------------------------------
        #                        process config
        # ---------------------------------------------------------------------
        config_template_path = os.path.join(pystring_path,'config_template.yml')
        # format config file
        config_template_file =  pkgrs.resource_filename(__name__,config_template_path)
        with open (config_template_file,'r') as f:
            config_template = f.read()

        config = config_template.format(title = self.meta['title'],
                                description = self.meta['description'],
                                author = self.meta['author'],
                                authorurl = self.meta['authorurl'])

        # write config
        with open(os.path.join(repo_dir,'_config.yml'),'w') as f:
            f.write(config)

        # format strings

        # write files
        slide_dir = os.path.join(repo_dir,slide_dir)
        self.generate_md_slides(slide_dir)

    def generate_md_slides(self,write_dir):
        '''
        write slides one per md file
        '''

        # iterate over slide titles in order
        for title in self.slide_order_list:
            # extract the current slide object
            cur_slide = self.slides[title]

            # convert the whole thing to a dictionary
            slide_dict = cur_slide.__dict__
            slide_dict.pop('content')

            # merge lists with newlines and -

            for k,v in slide_dict.items():
                if type(v) == list:
                    slide_dict[k] = '\n'.join(slide_dict[k])

                    # if k == 'notes':
                    #     slide_dict[k] = '\n-'.join(slide_dict[k])
                    # else:


            # add order number
            slidenum = self.slide_order_dict[title] + 1
            slide_dict['slidenum'] = slidenum

            # remove presentation status feild
            if 'shown_points' in slide_dict.keys():
                slide_dict.pop('shown_points')

            # "" around notes
            slide_dict['notes'] = '"' + slide_dict['notes'] + '"'

            # make all strings
            for k,v in slide_dict.items():
                slide_dict[k] = str(v)

            # build the actual slide fiel content
            slide_parts = ['---']
            # merge the header info together to generate yaml
            slide_yaml = '\n'.join([': '.join([k,v]) for k,v in slide_dict.items() if not(k=='body')])
            slide_parts.append(slide_yaml)
            slide_parts.append('---')
            # append the body after the ---
            slide_parts.append(slide_dict['body'])
            # merge with newlines to build string to write to file
            slide_file_str = '\n'.join(slide_parts)

            #name the file
            slide_file_name = str(slidenum).zfill(3) + '-' + title + '.md'
            #make the directory if needed
            if not(os.path.isdir(write_dir)):
                os.makedirs(write_dir)

            # write the file
            with open(os.path.join(write_dir,slide_file_name)  ,'w') as f:
                f.write(slide_file_str)


        def generate_md_worksheet(self,file):
            '''
            '''
            with open(file) as f:
                for title in self.slide_order_list:
                    for line in self.slides[title].body:
                        f.write()


        #     def next_slide(self,title):
