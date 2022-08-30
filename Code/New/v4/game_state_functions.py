import pygame
import GEWY
from MapProcessing import WIDTH, HEIGHT

def Pause_Screen(screen, pScreen, Player, Tabs, pw, pb, rw, rb, ew, eb, TextSurface):
    """
    Parameters
    ----------
    screen    : main pygame window surface
    pScreen   : the pause screen gray overlay
    Player    : the player object
    Tabs      : tab system
    pw / pb   : play wrapper / play button
    rw / rb   : restart wrapper / restart button
    ew / eb   : exit wrapper / exit button
    pauseText : pygame text surface
    """
    Tabs.disableAllTabs()
    pw.isOpen, rw.isOpen, ew.isOpen = True, True, True
    rw.wrapperPos.y, ew.wrapperPos.y = 410, 520
    rw.top_bar_drag()
    ew.top_bar_drag()
    pb.nameTag = "Resume"
    pb.textOffset = (-220, -15)
    eb.textOffset = (-190, -15)

    pScreen.fill((50, 50, 50))
    textsurface = TextSurface.render(f'PAUSED', False, (255, 255, 255))  # renders onto screen
    pScreen.blit(textsurface, ((WIDTH / 2) - 140, 30))	
    screen.blit(pScreen, (0, 0))
    GEWY.display(screen)

    if pb.returnState(): 
        Player.canMove = True
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        pb.state = False
        return "play"

    if rb.returnState(): 
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        rb.state = False
        return "restart"

    if eb.returnState(): return "exit"


def Death_Screen(screen, pScreen, Player, Tabs, rw, rb, ew, eb, TextSurface):
    """
    Parameters
    ----------
    screen    : main pygame window surface
    pScreen   : the death screen red overlay
    Player    : the player object
    Tabs      : tab system
    rw / rb   : restart wrapper / restart button
    ew / eb   : exit wrapper / exit button
    pauseText : pygame text surface
    """
    Player.canMove = False

    Tabs.disableAllTabs()
    rw.isOpen, ew.isOpen = True, True
    rw.wrapperPos.y, ew.wrapperPos.y = 300, 460
    rw.top_bar_drag()
    ew.top_bar_drag()

    pScreen.fill((255, 0, 0))
    textsurface = TextSurface.render(f'DEAD', False, (255, 255, 255))  # renders onto screen
    pScreen.blit(textsurface, ((WIDTH / 2) - 100, 30))	
    screen.blit(pScreen, (0, 0))
    GEWY.display(screen)

    if rb.returnState(): 
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        rb.state = False
        return "restart"

    if eb.returnState(): return "exit"


def Start_Screen(screen, sScreen, Player, Tabs, pw, pb, sw, sb, ew, eb, TextSurface):
    """
    Parameters
    ----------
    screen    : main pygame window surface
    sScreen   : the start screen black overlay
    Player    : the player object
    Tabs      : tab system
    pw / pb   : play wrapper / play button
    sw / sb   : settings wrapper / settings button
    ew / eb   : exit wrapper / exit button
    pauseText : pygame text surface
    """
    Player.canMove = False

    Tabs.disableAllTabs()
    pw.isOpen, sw.isOpen, ew.isOpen = True, True, True
    pb.nameTag = "Play"
    pb.textOffset = (-190, -15)
    ew.wrapperPos.y = 520
    ew.top_bar_drag()

    sScreen.fill((50, 50, 50))
    textsurface = TextSurface.render(f'ZOMBOCALYPSE', False, (255, 255, 255))  # renders onto screen
    sScreen.blit(textsurface, ((WIDTH / 2) - 250, 100))	
    screen.blit(sScreen, (0, 0))
    GEWY.display(screen)

    Player.step = sb.returnValue()

    if pb.returnState(): 
        pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
        pb.state = False
        return "play"

    if eb.returnState(): return "exit"


def End_Screen(screen, sScreen, Player, Tabs, ew, eb, TextSurface, EndTsurface):
    """
    Parameters
    ----------
    screen    : main pygame window surface
    sScreen   : the start screen black overlay
    Player    : the player object
    Tabs      : tab system
    pw / pb   : play wrapper / play button
    sw / sb   : settings wrapper / settings button
    ew / eb   : exit wrapper / exit button
    pauseText : pygame text surface
    """
    Player.canMove = False

    Tabs.disableAllTabs()
    ew.isOpen = True

    sScreen.fill((0, 0, 0))
    textsurface = TextSurface.render(f'Score: {round(Player.score * 420)}', False, (255, 255, 255))  # renders onto screen
    Esurface    = EndTsurface.render(f'You Win!', False, (255,255,255))
    sScreen.blit(textsurface, ((WIDTH / 2) - 250, 325))	
    sScreen.blit(Esurface, ((WIDTH / 2) - 160, 100))
    screen.blit(sScreen, (0, 0))
    GEWY.display(screen)

    if eb.returnState(): return "exit"