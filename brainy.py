#!/usr/bin/python2.5

import logging
import uuid

from waveapi import events
from waveapi import model
from waveapi import robot

from brainfuck import brainfuck

# Globals
ROBOT_NAME = 'brainy'

def OnDocumentChanged(properties, context):
  logging.debug('Document changed')
  blip_id = properties['blipId']
  blip = context.GetBlipById(blip_id)
  if blip.document.HasAnnotation('brainy-robot.brainfuck'):
    UpdateProgram(blip, context) 
  else:
    HandleNewProgram(blip, context)

def HandleNewProgram(blip, context):
  logging.debug('handle new program')
  result = brainfuck(blip.GetDocument().GetText())
  logging.debug('brainfuck result: %s ' % result)
  if result:
    id = uuid.uuid4().urn
    blip.GetDocument().AnnotateDocument('brainy-robot.brainfuck',id);
    inline_blip = blip.GetDocument().AppendInlineBlip()
    inline_blip.document.SetText(result)
    inline_blip.document.AnnotateDocument('brainy-robot.result',id);

def UpdateProgram(blip, context):
  logging.debug('update program')
  result = brainfuck(blip.document.GetText())
  if result:
    logging.debug('updated brainfuck result: %s ' % result)
    inline_blip = blip.GetDocument().AppendInlineBlip()
    inline_blip.document.SetText(result)
    inline_blip.document.AnnotateDocument('brainy-robot.result',id);
  

def OnRobotAdded(properties, context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().document.SetText("Hello, I\'m Brainy. Every brainfuck program that you write in a blip will be translated by me. See http://de.wikipedia.org/wiki/Brainfuck")

if __name__ == '__main__':
  brainy = robot.Robot(ROBOT_NAME.capitalize(),
    version='2',
    image_url='http://brainy-robot.appspot.com/assets/%s.jpg' % ROBOT_NAME,
    profile_url='http://brainy-robot.appspot.com')
  brainy.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  #brainy.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
  brainy.RegisterHandler(events.BLIP_SUBMITTED, OnDocumentChanged)
  brainy.Run(debug=True)
