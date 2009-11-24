#!/usr/bin/python2.5

import logging
import uuid

from waveapi import events
from waveapi import model
from waveapi import robot

from brainfuck import brainfuck

# Globals
ROBOT_NAME = 'brainy'
NUM_CELLS = 30000
CELL_SIZE = 1

def OnBlipSubmitted(properties, context):
  logging.debug('Blip submitted')

  blip_id = properties['blipId']
  blip = context.GetBlipById(blip_id)
  HandleRootBlip(blip, context)

def OnDocumentChanged(properties, context):
  logging.debug('Document changed')
  blip_id = properties['blipId']
  blip = context.GetBlipById(blip_id)
  if blip.document.HasAnnotation('brainy-robot.brainfuck'):
    UpdateProgram(blip, context) 
  else:
    HandleNewProgram(blip, context)

def HandleNewProgram(root_blip, context):
  logging.debug('handle new program')
  result = brainfuck(root_blip.GetDocument().GetText())
  logging.debug('brainfuck result: %s ' % result)
  if result:
    id = uuid.uuid4().urn
    root_blip.GetDocument().AnnotateDocument('brainy-robot.brainfuck',id);
    inline_blip = root_blip.GetDocument().AppendInlineBlip()
    inline_blip.document.SetText(result)
    for bid in root_blip.GetChildBlipIds():
      context.GetBlipById(bid).document.AnnotateDocument('brainy-robot.result',id);

def UpdateProgram(blip, context):
  logging.debug('update program')
  #id = blip.GetDocument().GetAnnotation('brainy-robot.brainfuck')
  for child_id in blip.childBlipIds:
    logging.debug('child %s' % child_id)
    child_blip = context.GetBlipById(child_id)
    #if child_blip.document.HasAnnotation('brainy-robot.result'):
    if child_blip.creator == 'brainy-robot@appspot.com':
      logging.debug('annotation found')
      result = brainfuck(blip.document.GetText())
      logging.debug('updated brainfuck result: %s ' % result)
      child_blip.document.SetText(result)

def OnRobotAdded(properties, context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().document.SetText("Hello, I\'m Brainy. Every brainfuck program that you write in a blip will be translated by me. See http://de.wikipedia.org/wiki/Brainfuck")

if __name__ == '__main__':
  brainy = robot.Robot(ROBOT_NAME.capitalize(),
    version='1',
    image_url='http://brainy-robot.appspot.com/assets/%s.jpg' % ROBOT_NAME,
    profile_url='http://brainy-robot.appspot.com')
  brainy.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  brainy.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
  #brainy.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  brainy.Run(debug=True)
