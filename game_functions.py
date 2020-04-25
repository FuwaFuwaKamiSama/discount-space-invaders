'''File containing functions related to updating the Space Invaders game'''
import pygame
import sys
from alien import Alien
from bullet import Bullet
from time import sleep

def check_keydown(event, settings, screen, ship, bullets):
    '''Function that determines what to do when input is given'''
    if event.key == pygame.K_RIGHT:
        ship.rightMove = True
    elif event.key == pygame.K_LEFT:
        ship.leftMove = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup(event, ship):
    '''Function that determines what to do when input is released'''
    if event.key == pygame.K_RIGHT:
        ship.rightMove = False
    elif event.key == pygame.K_LEFT:
        ship.leftMove = False

def check_events(settings, screen, ship, bullets, stats, button, aliens, sb):
    '''Function that checks for player input and quits the game when QUIT command
    is inputted'''
    for event in pygame.event.get():
        #Shut down system on quit command
        if event.type == pygame.QUIT:
            sys.exit()

        #Checking for movement key input
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, settings, screen, ship, bullets)

        #Checking if user stops giving input
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, ship, aliens, bullets, stats, button, mouse_x, mouse_y, sb)

def check_play_button(settings, screen, ship, aliens, bullets, stats, button, mouse_x, mouse_y, sb):
    '''Function that starts or restarts new game if Play is clicked on'''
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset game settings and previously stored stats
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        settings.initialize_dynamic_settings()
        stats.game_active = True

        #Reset scoreboard images and lives
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Empty alien and bullet list and create new fleet and ship
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(settings, screen, ship, bullets, aliens, stats, button, sb):
    '''Function that updates screen accordingly as gamestate changes'''
    sb.show_score()
    if not stats.game_active:
        button.draw_button()

    pygame.display.flip()
    screen.fill(settings.bgColor)
    ship.blitship()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.drawBullet()

def update_bullets(aliens, bullets, settings, screen, ship, stats, sb):
    '''Function that updates position of bullets, checks for collisions,
    with aliens, clears off screen bullet, and creates new bullets as needed'''
    bullets.update()
    check_bullet_alien_collisions(settings, screen, ship, aliens, bullets, stats, sb)
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def check_bullet_alien_collisions(settings, screen, ship, aliens, bullets, stats, sb):
    '''Respond to bullet alien collisions'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #Update score if any aliens hit
    if collisions:
        for aliens in collisions.values():
            stats.score += (settings.alien_points * len(aliens))
            sb.prep_score()
        check_high_score(stats, sb)

    #If entire fleet is destroyed, reset bullets and level up all aspects of game
    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(settings, screen, ship, aliens)

def update_aliens(settings, aliens, ship, stats, screen, bullets, sb):
    '''Update all aliens positions in fleet'''
    check_fleet_edges(settings, aliens)
    aliens.update()
    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets, sb)

def ship_hit(settings, stats, screen, ship, aliens, bullets, sb):
    '''React to ship getting hit by alien'''
    if stats.shipsLeft > 0:
        #Reduce lives by one and keep game going
        stats.shipsLeft -= 1
        sb.prep_ships()
        #Reset everything else and regenerate alien fleet
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        #Stop game when lives are depleted
        stats.game_active = False
        pygame.mouse.set_visible(True)

def fire_bullet(settings, screen, ship, bullets):
    '''Function that fires a new bullet if permitted'''
    if len(bullets) < settings.maxBullets:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def get_num_aliens(settings, width):
    '''Function that gets the number of aliens that fit in a row'''
    screenSpace_x = settings.screenWidth - (2 * width)
    numAliens_x = int(screenSpace_x / (2 * width))
    return numAliens_x

def get_num_rows(settings, shipHeight, alienHeight):
    '''Function that gets the number of rows of aliens to create for the fleet'''
    screenSpace_y = (settings.screenHeight - (3 * alienHeight) - shipHeight)
    numRows_y = int(screenSpace_y / (2 * alienHeight))
    return numRows_y

def make_alien(settings, screen, aliens, alienNumber, rowNumber):
    '''Function that creates an alien and adds it to the current list/fleet
    of aliens'''
    alien = Alien(settings, screen)
    alienWidth = alien.rect.width
    alien.x = alienWidth + (2 * alienWidth * alienNumber)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * rowNumber
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    '''Function that creates a whole army of aliens and stores them for game use'''
    #Determining number of aliens that can fit per row
    alien = Alien(settings, screen)
    alienWidth = alien.rect.width
    numAliens_x = get_num_aliens(settings, alienWidth)
    numRows_y = get_num_rows(settings, ship.rect.height, alien.rect.height)

    #Fill a row with aliens
    for currRow in range(numRows_y):
        for alienIndex in range(numAliens_x):
            make_alien(settings, screen, aliens, alienIndex, currRow)

def check_fleet_edges(settings, aliens):
    '''Decide how to respond when alien fleet collides with edge of game window'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    '''Drop fleet 1 row and reverse direction after wall collision'''
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb):
    '''Check if aliens have reached bottom of screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat alien hitting bottom of screen like a collision with ship
            ship_hit(settings, stats, screen, ship, aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    '''Function that checks for new high score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
