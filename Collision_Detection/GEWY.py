from VOBJ import createVector
from ObjectDef import Object
from GuiHitboxOBJ import GUI_REGION
import colorsys
import pygame

GUI_OBJECTS = []  # this Holds all the main wrapper objects created
pygame.font.init()  # used for font... duh
GLOBAL_FONT = "Century Gothic"


# Colour Conversion functions mainly used in colour slider
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))


def rgb2hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s * 100, v / 255 * 100


class Wrapper(GUI_REGION):
    """Wrapper objects are the tabs or windows that hold gui elements"""

    def __init__(self, x, y, w, h, elem: list, nametag=""):
        super().__init__(x, y, w, h)
        self.wrapperPos = createVector(x, y)
        self.dimensions = createVector(w, h)

        self.GUI_ELEMENTS = elem  # each wrapper can only contain 1 element
        self.NameTag = nametag

        # position of object in reference to window
        self.__OBJPosInWindow = [createVector(elem[i].pos.x + self.wrapperPos.x, elem[i].pos.y + self.wrapperPos.y) for
                                 i in range(len(self.GUI_ELEMENTS))]

        self.isOpen = False  # boolean for if the wrapper is "open"/visible

    def show(self, screen):
        pygame.draw.rect(screen, (12, 12, 12),
                         pygame.Rect(self.wrapperPos.x - 2, self.wrapperPos.y - 10, self.dimensions.x + 4,
                                     self.dimensions.y + 12))
        pygame.draw.rect(screen, (28, 28, 28),
                         pygame.Rect(self.wrapperPos.x, self.wrapperPos.y, self.dimensions.x, self.dimensions.y))

        for idx, element in enumerate(self.GUI_ELEMENTS):
            element.pos = self.__OBJPosInWindow[idx]
            element.show(screen)


class Slider:
    def __init__(self, x, y, w, h, idx, range: tuple):
        self.pos = createVector(x, y)
        self.dimensions = createVector(w, h)
        self.sliderW = 4
        self.selected = False
        self.r = range

        self.sliderIDX = idx
        self.SliderPos = createVector(
            self.pos.x + (self.sliderIDX % self.r[1] / self.r[1]) * self.dimensions.x + self.r[0], self.pos.y)

    def calculateSliderPos(self):
        if self.sliderIDX >= self.r[1]:
            self.sliderIDX = self.r[1] - 0.01  # 0.01 so value doesn't wrap back around to 0
        elif self.sliderIDX <= self.r[0]:
            self.sliderIDX = self.r[0]

        amount = ((self.sliderIDX % self.r[1]) - self.r[0]) / (self.r[1] - self.r[0])
        xpos = self.pos.x + amount * self.dimensions.x
        # return createVector(xpos if amount <= 1 else self.pos.x + self.dimensions.x + self.r[0], self.pos.y)
        return createVector(xpos, self.pos.y)

    def returnValue(self):
        return self.sliderIDX % self.r[1]

    def show(self, screen):
        self.SliderPos = self.calculateSliderPos()
        pygame.draw.rect(screen, (200, 200, 200),
                         pygame.Rect(self.SliderPos.x - self.sliderW / 2, self.SliderPos.y, self.sliderW,
                                     self.dimensions.y))


class ColourSlider(Object):
    def __init__(self, x, y, width, height, slideSpacing, startingColour=(52, 1, 254)):  # old:(253, 20, 220)
        super().__init__(x, y, width, height)  # instantiating the Object
        self.slideSpacing = slideSpacing  # spacing in pixels between hue, saturation and brightness bars

        self.SC = rgb2hsv(startingColour[0], startingColour[1], startingColour[2])  # starting set colour
        self.hueSlider = Slider(x, y, width, height, self.SC[0], (0, 360))
        self.saturationSlider = Slider(x, y + (height + self.slideSpacing), width, height, self.SC[1] - 1, (0, 100))
        self.brightnessSlider = Slider(x, y + 2 * (height + self.slideSpacing), width, height, self.SC[2] - 1, (0, 100))

        self.resolution = 20
        self.hueIncr = 360 / self.resolution
        self.satIncr = 100 / self.resolution
        self.briIncr = 100 / self.resolution
        self.PTWidth = self.dimensions.x / self.resolution

    def returnColour(self) -> tuple:
        hue = self.hueSlider.returnValue()
        saturation = self.saturationSlider.returnValue()
        brightness = self.brightnessSlider.returnValue()
        return hsv2rgb(hue, saturation, brightness)

    def LeftButtonDown(self):
        # if it is between the left and right of slide bars
        mVec = createVector(self.mouseReference[0], self.mouseReference[1])
        if self.pos.x < mVec.x < self.pos.x + self.dimensions.x:

            # if Hue bar
            if self.hueSlider.pos.y < mVec.y < self.hueSlider.pos.y + self.dimensions.y:
                self.hueSlider.selected = True
                self.hueSlider.sliderIDX = ((mVec.x - self.hueSlider.pos.x) / self.dimensions.x) * 360

            # elif saturation bar
            elif self.saturationSlider.pos.y < mVec.y < self.saturationSlider.pos.y + self.dimensions.y:
                self.saturationSlider.selected = True
                self.saturationSlider.sliderIDX = ((mVec.x - self.saturationSlider.pos.x) / self.dimensions.x) * 100

            # elif brightness bar
            elif self.brightnessSlider.pos.y < mVec.y < self.brightnessSlider.pos.y + self.dimensions.y:
                self.brightnessSlider.selected = True
                self.brightnessSlider.sliderIDX = ((mVec.x - self.brightnessSlider.pos.x) / self.dimensions.x) * 100

        self.hueSlider.SliderPos = self.hueSlider.calculateSliderPos()
        self.saturationSlider.SliderPos = self.saturationSlider.calculateSliderPos()
        self.brightnessSlider.SliderPos = self.brightnessSlider.calculateSliderPos()

    def LeftButtonUp(self):
        self.hueSlider.selected = False
        self.saturationSlider.selected = False
        self.brightnessSlider.selected = False

    def MouseMotion(self):
        # if it is between the left and right of slide bars
        mVec = createVector(self.mouseReference[0], self.mouseReference[1])
        if self.pos.x < mVec.x < self.pos.x + self.dimensions.x:

            # if Hue bar
            if self.hueSlider.pos.y < mVec.y < self.hueSlider.pos.y + self.dimensions.y and self.hueSlider.selected:
                self.hueSlider.sliderIDX = ((mVec.x - self.hueSlider.pos.x) / self.dimensions.x) * 360

            # elif saturation bar
            elif self.saturationSlider.pos.y < mVec.y < self.saturationSlider.pos.y + self.dimensions.y and self.saturationSlider.selected:
                self.saturationSlider.sliderIDX = ((mVec.x - self.saturationSlider.pos.x) / self.dimensions.x) * 100

            # elif brightness bar
            elif self.brightnessSlider.pos.y < mVec.y < self.brightnessSlider.pos.y + self.dimensions.y and self.brightnessSlider.selected:
                self.brightnessSlider.sliderIDX = ((mVec.x - self.brightnessSlider.pos.x) / self.dimensions.x) * 100

        self.hueSlider.SliderPos = self.hueSlider.calculateSliderPos()
        self.saturationSlider.SliderPos = self.saturationSlider.calculateSliderPos()
        self.brightnessSlider.SliderPos = self.brightnessSlider.calculateSliderPos()

    def show(self, screen) -> None:
        for i in range(self.resolution):
            r, g, b = hsv2rgb((i * self.hueIncr), self.saturationSlider.returnValue(),
                              self.brightnessSlider.returnValue())
            pygame.draw.rect(screen, (r, g, b),
                             pygame.Rect(self.pos.x + (i * self.PTWidth), self.pos.y, self.PTWidth + 1,
                                         self.dimensions.y))

            r, g, b = hsv2rgb(self.hueSlider.returnValue(), (i * self.satIncr), self.brightnessSlider.returnValue())
            pygame.draw.rect(screen, (r, g, b), pygame.Rect(self.pos.x + (i * self.PTWidth),
                                                            self.pos.y + (self.dimensions.y + self.slideSpacing),
                                                            self.PTWidth + 1, self.dimensions.y))

            r, g, b = hsv2rgb(self.hueSlider.returnValue(), self.saturationSlider.returnValue(), (i * self.briIncr))
            pygame.draw.rect(screen, (r, g, b), pygame.Rect(self.pos.x + (i * self.PTWidth),
                                                            self.pos.y + 2 * (self.dimensions.y + self.slideSpacing),
                                                            self.PTWidth + 1, self.dimensions.y))

        self.hueSlider.pos = createVector(self.pos.x, self.pos.y)
        self.saturationSlider.pos = createVector(self.pos.x, self.pos.y + (self.dimensions.y + self.slideSpacing))
        self.brightnessSlider.pos = createVector(self.pos.x, self.pos.y + 2 * (self.dimensions.y + self.slideSpacing))
        self.hueSlider.show(screen)
        self.saturationSlider.show(screen)
        self.brightnessSlider.show(screen)


class TabSystem(GUI_REGION):
    def __init__(self, x=10, y=0, w=0, h=20):
        super().__init__(x, y, w, h)
        self.tPos = createVector(x, y)
        self.tDim = createVector(w, h)
        self.isOpen = False  # starts of false when no tabs are made
        self.mouseReference = (0, 0)
        self.hovering = False
        self.selectedTab = ""
        self.r = 5

        self.__systemTabs = []  # a list of wrappers in the system

    def addTab(self, wrapperOBJ):
        self.isOpen = True
        self.__systemTabs.append(wrapperOBJ)
        self.HB_dim.x = (20 * len(self.__systemTabs))
        self.tDim.x = self.HB_dim.x

    def __calcTabIndex(self):

        for i in range(len(self.__systemTabs)):
            # If x collision
            if self.tPos.x + (20 * i) < self.mouseReference[0] < self.tPos.x + (20 * (i + 1)):
                # If y collision
                if self.tPos.y < self.mouseReference[1] < self.tPos.y + self.tDim.y:
                    return i  # return index of selected tab
        return -1

    def MouseHover(self, screen):
        self.hovering = True
        TabSelected = self.__calcTabIndex()
        if TabSelected >= 0:
            self.selectedTab = self.__systemTabs[TabSelected].NameTag

    def LeftButtonDown(self):
        TabSelected = self.__calcTabIndex()
        if TabSelected >= 0:
            currentState = self.__systemTabs[TabSelected].isOpen
            self.__systemTabs[TabSelected].isOpen = True if not currentState else False

    def LeftButtonUp(self):  # interaction functions need to made but no functionality needs to be added.
        pass

    def MouseMotion(self):
        pass

    def show(self, screen):
        if self.__systemTabs:  # if it has any wrappers
            # Construct Box
            pygame.draw.rect(screen, (12, 12, 12),
                             pygame.Rect(self.tPos.x - 2, self.tPos.y, self.tDim.x + 4, self.tDim.y + 2))
            pygame.draw.rect(screen, (28, 28, 28), pygame.Rect(self.tPos.x, self.tPos.y, self.tDim.x, self.tDim.y))

            # draw circle tabs
            for i, wr in enumerate(self.__systemTabs):
                pygame.draw.circle(screen, (70, 70, 70), (self.tPos.x + (20 * i + 10), (self.tDim.y - self.tPos.y) / 2),
                                   self.r, 0 if wr.isOpen else 1)  # 0 = filled, 1 = border


class VariableSlider(Object):
    def __init__(self, x, y, w, min, max, nt="", displayValue=False, sVal=-1):
        super().__init__(x, y, w, 5)
        self.displayValue = displayValue
        self.sVal = (max - min) * 0.5 + min if sVal == -1 else sVal  # starting value
        self.vslider = Slider(self.pos.x, self.pos.y, w, 15, self.sVal, (min, max))

        self.min = min
        self.max = max
        self.nameTag = nt

    def returnValue(self):
        return self.vslider.returnValue()

    def LeftButtonDown(self):
        mVec = createVector(self.mouseReference[0], self.mouseReference[1])

        if self.vslider.SliderPos.x - self.vslider.sliderW / 2 - 2 <= mVec.x <= (
                self.vslider.SliderPos.x - self.vslider.sliderW / 2) + self.vslider.sliderW + 2:
            if self.vslider.SliderPos.y <= mVec.y <= self.vslider.SliderPos.y + self.vslider.dimensions.y:
                self.vslider.selected = True
                self.vslider.sliderIDX = ((mVec.x - self.vslider.pos.x) / self.dimensions.x) * (
                            self.max - self.min) + self.min

        self.vslider.SliderPos = self.vslider.calculateSliderPos()

    def LeftButtonUp(self):
        self.vslider.selected = False

    def MouseMotion(self):
        mVec = createVector(self.mouseReference[0], self.mouseReference[1])

        if self.vslider.selected:
            self.vslider.sliderIDX = ((mVec.x - self.vslider.pos.x) / self.dimensions.x) * (
                        self.max - self.min) + self.min

        self.vslider.SliderPos = self.vslider.calculateSliderPos()

    def show(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos.x, self.pos.y, self.dimensions.x, self.dimensions.y))
        self.vslider.pos = createVector(self.pos.x, self.pos.y - (self.vslider.dimensions.y - 5) / 2)

        ntag = pygame.font.SysFont(GLOBAL_FONT, 17)
        textsurface1 = ntag.render(self.nameTag, True, (255, 255, 255))

        if self.displayValue:
            textsurface2 = ntag.render(f'{round(self.returnValue(), 1)}', True, (255, 255, 255))
            screen.blit(textsurface2, (self.pos.x + self.dimensions.x + 5, self.pos.y - 10))

        screen.blit(textsurface1,
                    (self.pos.x + 5, self.pos.y - 26))  # 5, -26 are random constants that I think look good.
        self.vslider.show(screen)


class Button(Object):
    def __init__(self, x, y, w, h, nt="", state=False, textOffset=(5, -2)):
        super().__init__(x, y, w, h)
        self.state = state
        self.nameTag = nt
        self.textOffset = textOffset

    def returnState(self) -> bool:
        return self.state

    def LeftButtonDown(self):
        pass

    def LeftButtonUp(self):
        mVec = createVector(self.mouseReference[0], self.mouseReference[1])

        if self.pos.x <= mVec.x <= self.pos.x + self.dimensions.x:
            if self.pos.y <= mVec.y <= self.pos.y + self.dimensions.y:
                self.state = True if self.state == False else False

    def MouseMotion(self):
        pass

    def show(self, screen):
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(self.pos.x - 1, self.pos.y - 1, self.dimensions.x + 2, self.dimensions.y + 2))
        if self.state:
            pygame.draw.rect(screen, (195, 195, 195),
                             pygame.Rect(self.pos.x, self.pos.y, self.dimensions.x, self.dimensions.y))
        elif not self.state:
            pygame.draw.rect(screen, (70, 70, 70),
                             pygame.Rect(self.pos.x, self.pos.y, self.dimensions.x, self.dimensions.y))

        ntag = pygame.font.SysFont(GLOBAL_FONT, 17)
        textsurface = ntag.render(self.nameTag, True, (255, 255, 255))

        screen.blit(textsurface,
                    (self.pos.x + self.dimensions.x + self.textOffset[0],
                     self.pos.y - self.textOffset[1]))  # 5, -2 are random constants that I think look good.


def handleEvents(event, mVec, screen):
    """Handles all Gui interactions"""
    global GUI_OBJECTS

    for idx, wrapper in enumerate(GUI_OBJECTS):  # loop over all wrappers
        if wrapper.isOpen:
            collision = wrapper.IN_COLLISION_CHECK(mVec)  # check for collisions using mouse position
            if type(wrapper) == TabSystem:
                wrapper.hovering = False

            if collision:
                if type(wrapper) == TabSystem:
                    wrapper.mouseReference = mVec
                    wrapper.MouseHover(screen)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            wrapper.LeftButtonDown()

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            wrapper.LeftButtonUp()

                    elif event.type == pygame.MOUSEMOTION:
                        wrapper.MouseMotion()


                else:
                    for idx, element in enumerate(wrapper.GUI_ELEMENTS):
                        element.mouseReference = mVec

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                element.LeftButtonDown()

                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                element.LeftButtonUp()

                        elif event.type == pygame.MOUSEMOTION:
                            element.MouseMotion()


def display(screen):
    for idx, wrapper in enumerate(GUI_OBJECTS):
        if wrapper.isOpen:
            if type(wrapper) != TabSystem:
                wrapper.show(screen)
            else:
                wrapper.show(screen)
                if wrapper.hovering:
                    ntag = pygame.font.SysFont(GLOBAL_FONT, 15)
                    textsurface = ntag.render(wrapper.selectedTab, True, (255, 255, 255))
                    screen.blit(textsurface, (wrapper.mouseReference[0], wrapper.mouseReference[1] + 20))
