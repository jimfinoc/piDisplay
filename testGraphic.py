import pygame
  
# Window size
WINDOW_WIDTH    = 400
WINDOW_HEIGHT   = 400

### initialisation
pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.set_caption("Gradient Rect")

def gradientRectHor( window, left_color, right_color, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    color_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( color_rect, left_color,  ( 0,0 ), ( 0,1 ) )            # left color line
    pygame.draw.line( color_rect, right_color, ( 1,0 ), ( 1,1 ) )            # right color line
    color_rect = pygame.transform.smoothscale( color_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( color_rect, target_rect )                                    # paint it

def gradientRectVer( window, top_color, bottom_color, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    color_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( color_rect, top_color,  ( 0,0 ), ( 1,0 ) )            # left color line
    pygame.draw.line( color_rect, bottom_color, ( 0,1 ), ( 1,1 ) )            # right color line
    color_rect = pygame.transform.smoothscale( color_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( color_rect, target_rect )                                    # paint it


### Main Loop
clock = pygame.time.Clock()
finished = False
while not finished:

    # Handle user-input
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            finished = True

    # Update the window
    window.fill( ( 0,0,0 ) )
    # gradientRectVer( window, (0, 96, 0), (0, 16, 0), pygame.Rect( 100,100, 100, 50 ) )
    # gradientRectHor( window, (0, 96, 0), (0, 16, 0), pygame.Rect( 100,100, 100, 50 ) )
    # gradientRectHor( window, (0, 96, 0), (0, 16, 0), pygame.Rect( 100,100, 100, 50 ) )
    # gradientRectVer( window, (255, 255, 0), (0, 0, 255), pygame.Rect( 100,200, 128, 64 ) )
    gradientRectVer( window, (0, 0, 0), (0, 64, 0), pygame.Rect( 100,200, 100, 64 ) )
    gradientRectVer( window, (0, 32, 0), (0, 128, 0), pygame.Rect( 200,200, 100, 64 ) )
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)

pygame.quit()
