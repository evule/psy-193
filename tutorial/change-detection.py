from __future__ import division
import os
import sys
import random
import glob
import string
import pygame
from pygame.locals import *

# Various setup stuff
bgcol = (196, 196, 196)
textPos = (1,1)
imgPos = (0,20)
timeImage = 300
timeBlank = 200
subject = raw_input('Enter subject ID here: ')
FILE = open(os.path.join('data', subject + '.txt'), 'w')
FILE.write('Subject: %s\n' % subject)

pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,420), 16)
FONT = pygame.font.Font(None, 28)
textSpace = FONT.render('Press SPACE when you see the change.', 1, (0,0,190))
textClick = FONT.render('Click on the location of the change.', 1, (0,0,190))
textFBbad = FONT.render('Wrong location!', 1, (160,0,0))
textFBgood = FONT.render('Right!', 1, (0,160,0))

images = glob.glob(os.path.join('imgA', '*.jpg'))
imageNames = map(lambda fn: string.split(string.split(fn, os.sep)[1], '.')[0], images)

def quit():
	FILE.close()
	sys.exit(0)

def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
def readBox(imfile):
	boxfile = open(os.path.join('boxes', imfile+'.txt'), 'r')
	box = [[],[]]
	box[0] = map(int, string.split(boxfile.readline().strip(), ','))
	box[1] = map(int, string.split(boxfile.readline().strip(), ','))
	boxfile.close()
	return(box)
				
def waitForClick():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = event.pos
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	clickPos = [clickPos[0]-imgPos[0], clickPos[1]-imgPos[1]]
	return(clickPos)
	
def showText(SCREEN, text, pos=textPos):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

def runTrial(SCREEN, imfile):
	image1 = pygame.image.load(os.path.join('imgA', imfile+'.jpg'))
	image2 = pygame.image.load(os.path.join('imgB', imfile+'.jpg'))
	clickFrame = readBox(imfile)
	iterations = 0
	attempts = 0
	detected = False
	phase = 0
	totalLoopTime = 0
	timeTrialStart = pygame.time.get_ticks()
	while(not detected):
		keypressed = False
		timeLoopStart = pygame.time.get_ticks()
		while(not keypressed):
			runtime = pygame.time.get_ticks() - timeLoopStart
			modtime = runtime % (timeImage*2 + timeBlank*2)
			if(phase == 0 and modtime>0 and modtime<timeImage):
				SCREEN.fill(bgcol)
				SCREEN.blit(image1, imgPos)
				SCREEN.blit(textSpace, textPos)
				pygame.display.flip()
				phase = 1
			elif(phase == 1 and modtime>timeImage and modtime<(timeImage+timeBlank)):
				SCREEN.fill(bgcol)
				SCREEN.blit(textSpace, textPos)
				pygame.display.flip()
				phase = 2
			elif(phase == 2 and modtime>(timeImage+timeBlank) and modtime<(timeImage*2+timeBlank)):
				SCREEN.fill(bgcol)
				SCREEN.blit(image2, imgPos)
				SCREEN.blit(textSpace, textPos)
				pygame.display.flip()
				phase = 3
			elif(phase == 3 and modtime>(timeImage*2+timeBlank)):
				SCREEN.fill(bgcol)
				SCREEN.blit(textSpace, textPos)
				pygame.display.flip()
				phase = 0
				iterations += 1
				attempts += 1
			for event in pygame.event.get():
				if (event.type == KEYDOWN and event.key == K_SPACE):
					keypressed = True
				if (event.type == KEYDOWN and event.key == K_ESCAPE):
					quit()
		totalLoopTime += runtime
		SCREEN.fill(bgcol)
		SCREEN.blit(image1, imgPos)
		SCREEN.blit(textClick, textPos)
		pygame.display.flip()
		clickPos = waitForClick()
		SCREEN.fill(bgcol)
		SCREEN.blit(image1, imgPos)
		if(clickPos[0] > clickFrame[0][0] and clickPos[0] < clickFrame[1][0] and clickPos[1] > clickFrame[0][1] and clickPos[1] < clickFrame[1][1]):
			detected = True
			SCREEN.blit(textFBgood, textPos)
		else:
			SCREEN.blit(textFBbad, textPos)
		pygame.display.flip()
		pygame.time.wait(250)
	totalTrialTime = pygame.time.get_ticks() - timeTrialStart
	return({'image': imfile, 'trialTime': totalTrialTime, 'loopTime': totalLoopTime, 'iterations': iterations, 'attempts':attempts})

showText(SCREEN, 'Welcome to our experiment!', textPos)
waitForKey()
showText(SCREEN, 'Press the space bar when you see the change', textPos)
waitForKey()

random.shuffle(images)

first = True
for imfile in imageNames:
	showText(SCREEN, 'Press space for the next trial!', textPos)
	waitForKey()
	trialOutput = runTrial(SCREEN, imfile)
	header = ''
	line = ''
	for k,v in trialOutput.iteritems():
		header += k + '\t'
		line += v + '\t'
	if first:
		first = False
		FILE.write(header+'\n')
	FILE.write(line+'\n')

showText(SCREEN, 'Thank you for your participation!', textPos)
waitForKey()

quit()
