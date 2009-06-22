#!/usr/bin/python2.5

import logging

from waveapi import events
from waveapi import model
from waveapi import robot

from brainfuck import brainfuck

# Globals
ROBOT_NAME = 'brainy'
NUM_CELLS = 30000
CELL_SIZE = 1

def OnBlipSubmitted(properties, context):
  """Invoked when any blip we are interested in is submitted."""
  blip_id = properties['blipId']
  blip = context.GetBlipById(blip_id)
  if blip.IsRoot():
    HandleRootBlip(blip, context)
  #else:
  #  HandleChildBlip(blip)

def HandleRootBlip(root_blip, context):
  """Runs the contents of the root blip as a Brainfuck program."""
  result = brainfuck(root_blip.GetDocument().GetText())
  comm_blip = None
  for blip_id in root_blip.GetChildBlipIds():
    blip = context.GetBlipById(blip_id)
    if blip.GetDocument().HasAnnotation('blip-comm'):
      comm_blip = blip
      break
  if comm_blip:
    comm_blip.GetDocument().SetText(result)

def OnSelfAdded(properties, context):
    """Invoked when Brainy is first added to the wave."""
    wavelet = context.GetRootWavelet()
    blip = context.GetBlipById(wavelet.GetRootBlipId())
    if blip:
        inline_blip = blip.GetDocument().AppendInlineBlip()
        doc = inline_blip.GetDocument()
        doc.SetText('Hello! I\'m Brainy. Please input your program below '
                'and I will take care of the rest.')
        doc.AnnotateDocument('blip-comm', '1')

if __name__ == '__main__':
    brainy = robot.Robot(ROBOT_NAME.capitalize(),
            version='1',
            image_url='http://manu.appspot.com/assets/%s.jpg' % ROBOT_NAME,
            profile_url='http://manu.appspot.com')
    brainy.RegisterHandler(events.WAVELET_SELF_ADDED, OnSelfAdded)
    brainy.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    brainy.Run(debug=True)
