import pygame
import numpy as np
import random
import time
import os


class DenisBox:
    boxes = []
    shrink = False
    screen = None
    denisImage = pygame.image.load("denis.png")
    denisImage = pygame.transform.scale(denisImage, (300, 300))

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        DenisBox.boxes.append(self)

    def draw(self):

        if DenisBox.shrink:
            self.size = (self.size[0] - 12, self.size[1] - 12)
            if self.size[0] < 0:
                self.size = (0, 0)
                DenisBox.shrink = False
                return "Done"

        else:
            self.size = (self.size[0] + 9, self.size[1] + 9)
            if self.size[0] > 300:
                self.size = (300, 300)
                DenisBox.shrink = True

        DenisBox.screen.blit(pygame.transform.scale(DenisBox.denisImage, self.size), (self.pos[0] - self.size[0]//2, self.pos[1] - self.size[1]//2))


class main:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((600, 900))
        DenisBox.screen = self.screen
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.denis = pygame.image.load("denis.png")
        self.denis = pygame.transform.scale(self.denis,(600,900))

        self.denisLeftValue = 0
        self.denisRightValue = 300

        self.denisLeft = self.denis.subsurface((0, 0, 300, 900)) # change the FIRST one
        self.denisRight = self.denis.subsurface((300, 0, 300, 900))

        self.drawHalfDenis = False

        self.denisCover = self.denis.copy()
        self.denisCoverSize = (0, 0)
        self.denisCoverLoop = False

        self.denisSlide = self.denis.copy()
        self.denisSlidePos = (-600, 0)
        self.denisSlideLoop = False

        self.denisBoxLoop = False
        size = (0, 0)
        DenisBox((150, 150), size)
        DenisBox((450, 150), size)
        DenisBox((150, 450), size)
        DenisBox((450, 450), size)
        DenisBox((150, 750), size)
        DenisBox((450, 750), size)




        # mixer

        self.mixer = pygame.mixer
        self.mixer.set_num_channels(4)

        self.sound = self.mixer.Sound("Metamorphosis.mp3")

        self.sound.play(fade_ms=20000, loops=-1)

        self.running = True
        self.fading = False

        self.filterStartFrame = 0
        self.filterColour = (0, 0, 0)
        self.filtering = False
        self.filterChangeFast = False
        self.fitlerFlicker = False

    def run(self):

        frame = 0

        while self.running:

            frame += 1

            self.screen.blit(self.denis, (0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.sound.set_volume(1)

                    self.fading = True

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:

                        self.denisCoverLoop = True

                    if event.key == pygame.K_2:

                        self.denisSlideLoop = True

                    if event.key == pygame.K_3:
                        self.denisBoxLoop = True

                    if event.key == pygame.K_4:
                        self.drawHalfDenis = True

                    if event.key == pygame.K_8:
                        self.filtering = not self.filtering
                        self.filterStartFrame = frame

                    if event.key == pygame.K_9:
                        self.filterChangeFast = not self.filterChangeFast

                    if event.key == pygame.K_0:
                        self.fitlerFlicker = not self.fitlerFlicker

            if self.denisCoverLoop:
                self.denisCoverr()

            if self.denisSlideLoop:
                self.denisSlider()

            if self.denisBoxLoop:
                self.denisBoxes()

            if self.fading and frame % 3 == 0:
                self.fadeSound()

            if self.drawHalfDenis:
                self.drawBothHalvesOfDenis()

            if self.filtering:
                self.filter(frame)

            #print(self.mixer.Sound("Metamorphosis.mp3").get_volume())

            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()
        quit()

    def drawBothHalvesOfDenis(self):

        self.screen.blit(self.denisLeft, (self.denisLeftValue, 0))
        self.screen.blit(self.denisRight, (self.denisRightValue, 0))

        self.denisLeftValue -= 2
        self.denisRightValue += 2

        if self.denisLeftValue <= -350:
            self.denisLeftValue = 0
            self.denisRightValue = 300

            self.drawHalfDenis = False

    def filter(self, frame):

        colours = [(0, 0, 0),
                   (42,14,74),
                   (5,8,66),
                   (120,16,92),
                   (8,79,7),
                   (8,78,79)]

        frameChange = 30 if not self.filterChangeFast else random.randint(20, 21)
        if frame - self.filterStartFrame > frameChange:
            selCol = random.choice(colours)
            colours.remove(selCol)
            colours.append(self.filterColour)
            self.filterColour = selCol
            self.filterStartFrame = frame

        real = pygame.Surface((600, 900))
        real.fill(self.filterColour)
        real.set_alpha(random.randint(0, 255) if self.fitlerFlicker else 150)
        self.screen.blit(real, (0, 0))

    def changeSize(self):
        height, width = pygame.display.get_window_size()
        height += random.randint(-50, 50)
        width += random.randint(-50, 50)
        height = max(10, height)
        width = max(10, width)
        self.screen = pygame.display.set_mode((height, width))
        self.denis = pygame.transform.scale(self.denis, (height, width))

    def denisBoxes(self):
        for box in DenisBox.boxes:
            if box.draw() == "Done":
                self.denisBoxLoop = False

    def fadeSound(self):
        vol = self.sound.get_volume() - 0.01
        self.sound.set_volume(vol)
        if vol <= 0:
            self.sound.stop()
            self.running = False

    def denisSlider(self):
        self.denisSlidePos = (self.denisSlidePos[0] + 12, self.denisSlidePos[1])
        self.screen.blit(self.denisSlide, self.denisSlidePos)
        if self.denisSlidePos[0] >= 0:
            self.denisSlidePos = (-600, 0)
            self.denisSlideLoop = False

    def denisCoverr(self):
        self.denisCoverSize = (self.denisCoverSize[0] + 6, self.denisCoverSize[1] + 9)
        self.screen.blit(pygame.transform.scale(self.denisCover, self.denisCoverSize), (0 , 0))
        if self.denisCoverSize[0] >= 600:
            self.denisCoverSize = (0, 0)
            self.denisCoverLoop = False


if __name__ == "__main__":
    game = main()
    game.run()
