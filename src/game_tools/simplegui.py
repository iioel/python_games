#!/usr/bin/env python
'''

Simplegui module has frame class that supports drawing and events.

Created on Jun 7, 2014

@author: Robb
'''

import pygame

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')
 
# initializations
pygame.init()

ALIGNMENTS = (('left','center','right'),('top','middle','bottom'))

FONT_FACE_DICT = {'serif':pygame.font.match_font('timesnewroman'),
                  'sans-serif':pygame.font.match_font('arial')}
FONT_DICT = {}

COLOR_PALETTE = dict([('Black','Black'),
                      ('White','Ivory'),
                      ('Gray','Gray'),
                      ('Red','FireBrick'),
                      ('Blue','SteelBlue'),
                      ('Purple','Plum'),
                      ('Green',(60,179,71)),
                      ('Yellow','Gold'),
                      ('Orange',(220,94,56)),
                      ('LightBlue','SkyBlue')])

BACKGROUND_COLORS = COLOR_PALETTE.keys()

def get_font(font_face, font_size):
    '''Gets a font object'''
    if not FONT_FACE_DICT.has_key(font_face):
        raise('Not a valid font face: '+font_face+'\nShould be in: ' + FONT_FACE_DICT.keys())
    if not FONT_DICT.has_key((font_face,font_size)):
        FONT_DICT[(font_face,font_size)] = pygame.font.Font(FONT_FACE_DICT[font_face], font_size)
    return FONT_DICT[(font_face,font_size)]
    
class Frame(object):
    '''
    Creates a window for drawing and event handling.
    '''

    def __init__(self, title, size = (640, 480), control_panel_width = 0, fps = 60, canvas_color='Black', control_panel_color='Gray'):
        '''
        Creates the frame
        '''
        self.running = False
        self.title = title
        #self.screen = pygame.display.set_mode((size[0]+control_panel_width,size[1]))
        self.canvas_size = size
        self.control_panel_size = (control_panel_width,size[1])
        self.canvas = Canvas(size,color=canvas_color)
        self.screen_shot_file = None
        self.screen_shot_ext = None
        self.screen_shot_count = 0
        
        if control_panel_width != 0:
            self.control_panel = ControlPanel(self.control_panel_size,color=control_panel_color)
        else:
            self.control_panel = None
        
        #self.controls = []
        
        #pygame.display.set_caption(title)
        self.FPS = fps
        
        self.draw_handler = None
        self.mouse_left_click_handler = None
        self.mouse_right_click_handler = None
        self.mouse_move_handler = None
        self.key_down_handler = None
        self.key_up_handler = None
        
        self.surface_count = 0
        
        self.setup_screen()
        
    def setup_screen(self):
        '''Sets up the screen'''
        self.screen = pygame.display.set_mode((self.canvas_size[0]+self.control_panel_size[0],self.canvas_size[1]))
        pygame.display.set_caption(self.title)
        
    def start(self):
        '''Starts the frame'''
        self.setup_screen()
        self.running = True
        self.run()
        
    def stop(self):
        '''Stops the frame'''
        self.running = False
        
    def quit(self):
        '''Quits pygame (quitting all windows)'''
        pygame.quit()
        
    def set_draw_handler(self, draw_handler):
        '''Sets the draw handler for the frame'''
        self.draw_handler = draw_handler
        
    def set_background_color(self, color):
        '''Sets the frames background color'''
        self.canvas.set_background_color(color)
        
    def set_mouse_left_click_handler(self, mouse_left_click_handler):
        '''Sets the left click handler for the mouse'''
        self.mouse_left_click_handler = mouse_left_click_handler
    
    def set_mouse_right_click_handler(self, mouse_right_click_handler):
        '''Sets the right click handler for the mouse'''
        self.mouse_right_click_handler = mouse_right_click_handler
    
    def set_mouse_move_handler(self, mouse_move_handler):
        '''Sets the motion handler for the mouse'''
        self.mouse_move_handler = mouse_move_handler
    
    def set_key_down_handler(self, key_down_handler):
        '''Sets the key down handler'''
        self.key_down_handler = key_down_handler
    
    def set_key_up_handler(self, key_up_handler):
        '''Sets the key up handler'''
        self.key_up_handler = key_up_handler
        
    def set_screen_shot_file(self, filename, ext='.png'):
        self.screen_shot_file = filename
        self.screen_shot_ext = ext
        self.screen_shot_count = 0
        
    def add_button(self, text, handler, width, font_height):
        '''Adds a button to the control panel'''
        return self.control_panel.add_button(text, handler, width, font_height)
    
    def add_label(self, text, width=None, font_height=None):
        '''Adds a label to the control panel'''
        return self.control_panel.add_label(text, width, font_height)
    
    def screen_shot(self):
        if self.screen_shot_file and self.screen_shot_ext:
            new_file = self.screen_shot_file + '_' + str(self.screen_shot_count) + self.screen_shot_ext
            pygame.image.save(self.screen, new_file)
            self.screen_shot_count += 1
        
    def control_click_handler(self, click_pos):
        '''Calls the control panel click handler'''
        pos = (click_pos[0] - self.canvas_size[0], click_pos[1])
        if 0 <= pos[0] <= self.control_panel_size[0] and 0 <= pos[1] <= self.control_panel_size[1]:
            self.control_panel.click_handler(pos)
        
    def call_draw_handler(self):
        '''Clears the screen and calls the draw handler'''
        if self.surface_count or not self.control_panel:
            self.canvas.draw_background()
             
            if self.draw_handler:
                self.draw_handler(self.canvas)
             
            self.screen.blit(self.canvas.Surface,(0,0))
            
            self.surface_count = 0
        else:
            self.control_panel.draw_background()
            self.control_panel.draw_controls()
            self.screen.blit(self.control_panel.Surface,(self.canvas_size[0],0))
            self.surface_count = 1
         
        
        # update the display
        pygame.display.update()
            
    def run(self):
        '''Runs the frame, event handlers, and timers'''
        clock = pygame.time.Clock() 
        
        while self.running:
            # event queue iteration
            for event in pygame.event.get():
                
                # window GUI ('x' the window)
                if event.type == pygame.QUIT:
                    self.stop()
    
                # input - key and mouse event handlers
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #left clicks
                        if self.mouse_left_click_handler:
                            self.mouse_left_click_handler(pygame.mouse.get_pos())
                        
                        self.control_click_handler(pygame.mouse.get_pos())
                    elif pygame.mouse.get_pressed()[2]:
                        #right clicks
                        if self.mouse_right_click_handler:
                            self.mouse_right_click_handler(pygame.mouse.get_pos())
                            
                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_move_handler:
                        self.mouse_move_handler(pygame.mouse.get_pos())
                        
                elif event.type == pygame.KEYDOWN:
                    if self.key_down_handler:
                        self.key_down_handler(pygame.key.name(event.key))
                        
                    if pygame.key.name(event.key) == 'print screen':
                        self.screen_shot()
                        
                elif event.type == pygame.KEYUP:
                    if self.key_up_handler:
                        self.key_up_handler(pygame.key.name(event.key))
                
                # timers
                #elif event.type == timer_example:
                    #t_example()      
                    
            # the call to the draw handler
            self.call_draw_handler()
            
            # FPS limit to 60 -- essentially, setting the draw handler timing
            # it micro pauses so while loop only runs 60 times a second max.
            clock.tick(self.FPS)
            
        #pygame.quit()
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class Canvas(object):
    '''Creates the canvas to draw on.'''
    def __init__(self,size, color='Black', default_font_h=16):
        #self.Surface = pygame.display.set_mode(size)
        self.size = size
        self.Surface = pygame.Surface(size)
        self.background_color = pygame.Color(color)
        self.default_font_h = default_font_h
                
    def set_background_color(self, color):
        color = pygame.Color(color) if type(color) == str else color
        self.background_color = color
         
    def draw_background(self):
        self.Surface.fill(self.background_color)
        
    def draw_rect(self, pos, size, line_width, line_color, fill_color = None):
        '''draw a rectangle shape'''
        pos = tuple([int(p) for p in pos])
        size = tuple([int(s) for s in size])
        Rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
        if fill_color:
            fill_color = pygame.Color(fill_color) if type(fill_color) == str else fill_color
            pygame.draw.rect(self.Surface, fill_color, Rect, 0)
                
        line_color = pygame.Color(line_color) if type(line_color) == str else line_color
        pygame.draw.rect(self.Surface, line_color, Rect, line_width)
        
    def draw_polygon(self, point_list, line_width, line_color, fill_color = None):
        '''draw a shape with any number of sides'''
        if fill_color:
            fill_color = pygame.Color(fill_color) if type(fill_color) == str else fill_color
            pygame.draw.polygon(self.Surface, fill_color, point_list, 0)
                
        line_color = pygame.Color(line_color) if type(line_color) == str else line_color
        pygame.draw.polygon(self.Surface, line_color, point_list, line_width)
        
    def draw_circle(self, pos, radius, line_width, line_color, fill_color = None):
        '''draw a circle around a point'''
        pos = tuple([int(p) for p in pos])
        radius = int(radius)
        if fill_color:
            fill_color = pygame.Color(fill_color) if type(fill_color) == str else fill_color
            pygame.draw.circle(self.Surface, fill_color, pos, radius, 0)
                
        line_color = pygame.Color(line_color) if type(line_color) == str else line_color
        pygame.draw.circle(self.Surface, line_color, pos, radius, line_width)
        
    def draw_ellipse(self, pos, size, line_width, line_color, fill_color = None):
        '''draw a round shape inside a rectangle'''
        pos = tuple([int(p) for p in pos])
        size = tuple([int(s) for s in size])
        Rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
        if fill_color:
            fill_color = pygame.Color(fill_color) if type(fill_color) == str else fill_color
            pygame.draw.ellipse(self.Surface, fill_color, Rect, 0)
                
        line_color = pygame.Color(line_color) if type(line_color) == str else line_color
        pygame.draw.ellipse(self.Surface, line_color, Rect, line_width)
        
    def draw_arc(self, pos, size, start_angle, stop_angle, width=1, color='White'):
        '''draw a partial section of an ellipse'''
        pos = tuple([int(p) for p in pos])
        size = tuple([int(s) for s in size])
        color = pygame.Color(color) if type(color) == str else color
        Rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.arc(self.Surface, color, Rect, start_angle, stop_angle, width)
        
    def draw_line(self, start_pos, end_pos, width=1, color='White'):
        '''draw a straight line segment'''
        start_pos = tuple([int(p) for p in start_pos])
        end_pos = tuple([int(p) for p in end_pos])
        color = pygame.Color(color) if type(color) == str else color
        pygame.draw.line(self.Surface, color, start_pos, end_pos, width) 
        
    def draw_lines(self, closed, pointlist, width=1, color='White'):
        '''draw multiple contiguous line segments'''
        pygame.draw.lines(self.Surface, color, closed, pointlist, width)
        
    def draw_aaline(self, start_pos, end_pos, blend=1, color='White'):
        '''draw fine antialiased lines'''
        start_pos = tuple([int(p) for p in start_pos])
        end_pos = tuple([int(p) for p in end_pos])
        color = pygame.Color(color) if type(color) == str else color
        pygame.draw.aaline(self.Surface, color, start_pos, end_pos, blend)
        
    def draw_aalines(self, closed, pointlist, blend=1, color='White'):
        '''draw a connected sequence of antialiased lines'''
        color = pygame.Color(color) if type(color) == str else color
        pygame.draw.aalines(self.Surface, color, closed, pointlist, blend)
        
    def draw_text(self, text, pos, font_size, font_color, font_face='sans-serif', align=('left','top')):
        '''draw text on the canvas'''
        pos = tuple([int(p) for p in pos])
        font_color = pygame.Color(font_color) if type(font_color) == str else font_color
        font = get_font(font_face, font_size)
        s = font.render(text, True, font_color)
        size = font.size(text)
        
        if align[0] in ALIGNMENTS[0] and align[1] in ALIGNMENTS[1]:
            pos = (pos[0] - ALIGNMENTS[0].index(align[0])*0.5*size[0],
                   pos[1] - ALIGNMENTS[1].index(align[1])*0.5*size[1])
        else:
            raise('invalid alignment in draw_text')
        
        self.Surface.blit(s, pos)
        
    def draw_image(self, image, pos, angle=0):
        '''draws an image on the canvas'''
        pos = tuple([int(p) for p in pos])
        rot_img = pygame.transform.rotate(image.img, angle)
        self.Surface.blit(rot_img, pos)
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class ControlPanel(Canvas):
    '''Creates a control panel'''
    
    def __init__(self, size, color='Black', default_font_h=16):
        '''Initializes the control panel'''
        super(ControlPanel, self).__init__(size, color, default_font_h)
        self.controls = []
        self.spacing = 5
        
    
    def get_offset(self):
        '''Offset for the next item'''
        return (self.size[0]/2, sum([self.spacing + c.size[1] for c in self.controls]))
    
    offset = property(get_offset)
    
    def add_button(self, text, handler, width, font_height):
        '''Adds a button to the control panel'''
        button = Button(text, handler, self.offset, width, font_height)
        self.controls.append(button)
        return button
        
    def add_label(self, text,  width=None, font_height=None):
        '''Adds a label to the control panel'''
        if not width:
            width = self.size[0]
        if not font_height:
            font_height = self.default_font_h
        
        label = Label(text, self.offset, width, font_height)
        self.controls.append(label)
        return label
        
    def add_sprite_container(self, sprite, size=None):
        '''Adds a sprite to the control panel'''
        sprite_container = Sprite_Container(sprite, self.offset, size=size)
        self.controls.append(sprite_container)
        return sprite_container
        
    def draw_controls(self):
        '''Draws the controls'''
        for control in self.controls:
            control.draw(self)
            
    def click_handler(self, click_pos):
        '''Calls the control that was clicked on by a position'''
        for control in self.controls:
            if type(control) == Button and control.click_check(click_pos):
                control.call_handler()
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class Button(object):
    '''Creates a button.'''
    
    def __init__(self, text, handler, pos, width, font_height, color = 'grey'):
        '''Initializes the button'''
        self.text = text
        self.handler = handler
        self.pos = pos
        self.font_h = font_height
        self.size = (width, 2*self.font_h)
        self.color = color
    
    def call_handler(self):
        '''Calls the button's event handler'''
        if self.handler:
            self.handler()
            
    def draw(self, canvas):
        '''Draws the button'''
        canvas.draw_rect((self.pos[0]-self.size[0]/2,self.pos[1]), self.size, 1, 'black', self.color)
        canvas.draw_text(self.text, (self.pos[0],self.pos[1]+self.size[1]/2), self.font_h, 'black', 'sans-serif', ('center','middle'))
    
    def click_check(self, click_pos):
        '''Checks to see if the button was clicked on by a position'''
        return -self.size[0]/2 <= click_pos[0] - self.pos[0] <= self.size[0]/2 and 0 <= click_pos[1] - self.pos[1] <= self.size[1]
       
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class Label(object):
    '''Creates a Label.'''
    
    def __init__(self, text, pos, width, font_height):
        '''Initializes the label'''
        self.text = text
        self.pos = pos
        self.font_h = font_height
        self.size = (width, 2*self.font_h)
    
    def draw(self, canvas):
        '''Draws the label'''
        canvas.draw_text(self.text, (self.pos[0],self.pos[1]+self.size[1]/2), self.font_h, 'black', 'sans-serif', ('center','middle'))
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
           
class Sprite_Container(object):
    '''Creates a container for a sprite'''
    def __init__(self, sprite, pos, size=None):
        '''Initializes the container'''
        self.pos = pos
        self.sprite = sprite
        self._size = size
        
    def set_sprite(self, sprite):
        '''Sets the sprite'''
        self._sprite = sprite
        if self._sprite:
            self._sprite.pos = self.pos
            
    def get_sprite(self):
        '''Gets the sprite'''
        return self._sprite
    
    sprite = property(get_sprite, set_sprite)
    
    def draw(self, canvas):
        '''Draws the sprite'''
        #canvas.draw_rect((self.pos[0]-self.size[0]/2,self.pos[1]), self.size, 1, 'black', 'grey')
        if self.sprite:
            self.sprite.draw(canvas)
            
    def get_size(self):
        '''Gets the size of the container'''
        if self._size is None: 
            if self.sprite:
                return self.sprite.size
            else:
                return (0,0)
        else:
            return self._size
    
    size = property(get_size)
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class Sound(object):
    '''Creates a sound file, currently placeholder'''
    
    def __init__(self,sound_file):
        '''Constructor'''
        self.sound_file = sound_file
        
    def play(self):
        '''Plays the sound'''
        pass
    
    def pause(self):
        '''Pauses the sound'''
        pass
    
    def stop(self):
        '''Stops the sound'''
        pass
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return '%s(%r)' % (self.__class__, self.__dict__)
    
class Image_Info(object):
    '''Image information for an image'''
    def __init__(self, img_file, size):
        '''Constructor'''
        self.img_file = img_file
        self.size = size
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return 'Image_Info(img_file={0!r}, size={1!r})'.format(self.img_file, self.size)
    
class Image(object):
    '''Loads an image into the game'''
    def __init__(self, img_info):
        '''Constructor'''
        self.img_info = img_info
        self.img = pygame.image.load(img_info.img_file).convert_alpha()
        
    def set_size(self, size):
        '''Set the image size'''
        self.img_info.size = size
    
    def get_size(self):
        '''Get the image size'''
        return self.img_info.size
    
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return 'Image(img_info={0!r})'.format(self.img_info)
        
        
if __name__ == '__main__':
    global image1
    
    image_info1 = Image_Info('../lib/images/medium_gear.png', (400,400)) 
    def print_event(name, event_info):
        print name, event_info
        
    def draw(canvas):
        canvas.draw_text('Hello', (200,200), 16, 'white', 'serif')
        canvas.draw_image(image1,(300,0))
        
    
    frame = Frame('test', (640, 480))
    
    frame.set_key_down_handler(lambda x: print_event('Key down:', x))
    frame.set_key_up_handler(lambda x: print_event('Key up:', x))
    frame.set_mouse_left_click_handler(lambda x: print_event('Mouse Left Click:', x))
    frame.set_mouse_right_click_handler(lambda x: print_event('Mouse Right Click:', x))
    frame.set_mouse_move_handler(lambda x: print_event('Mouse Move:', x))
    image1 = Image(image_info1)
    
    frame.set_screen_shot_file("E:/Documents/EclipseWorkspace/tmp/test_screen_shot")
    
    frame.set_draw_handler(draw)
    frame.start()#nothing can come after frame.start()
    frame.quit()
    