#!/usr/bin/python2.5

import logging

from waveapi import events
from waveapi import model
from waveapi import robot

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
  result = ExecBrainfuck(root_blip.GetDocument().GetText(), context)
  comm_blip = None
  for blip_id in root_blip.GetChildBlipIds():
    blip = context.GetBlipById(blip_id)
    if blip.GetDocument().HasAnnotation('blip-comm'):
      comm_blip = blip
      break
  if comm_blip:
    comm_blip.GetDocument().SetText(result)


def ExecBrainfuck(code, context):
    cells = [0] * NUM_CELLS
    maxint = (2 ** (CELL_SIZE * 8))
    cellpointer = 0
    codecursor = 0
    code = purify(code)
    result = ''
    while True:
        i = code[codecursor]
        if i == '+':
            if cells[cellpointer] < maxint:
                cells[cellpointer] += 1
            else:
                cells[cellpointer] = 0
        elif i == '-':
            if cells[cellpointer] == 0:
                cells[cellpointer] = maxint
            else:
                cells[cellpointer] -= 1
        elif i == '.':
            result += (chr(cells[cellpointer]))
        elif i == ',':
            cells[cellpointer] = ord(getchar())
        elif i == '<':
            cellpointer -= 1
        elif i == '>':
            cellpointer += 1
        elif i == '[':
            if cells[cellpointer] == 0:
                codecursor = matchingbracket(codecursor, code)
        elif i == ']':
            if cells[cellpointer] != 0:
                codecursor = matchingbracket(codecursor, code)
        if codecursor == len(code) - 1:
            break
        else:
            codecursor += 1
    return result

def purify(code):
    return filter(lambda x: x in '[],.<>-+', code)
                            
def matchingbracket(codepointer, code):
    '''Takes a position in a string and that string as input, and if the character at that position is an opening or closing bracket, finds and returns the position of the matching bracket.'''
    if code[codepointer] == '[':
        opens = 0
        for i in range(codepointer, len(code)):
            if code[i] == '[':
                opens += 1
            elif code[i] == ']':
                opens -= 1
            if opens == 0:
                match = i
                break
    elif code[codepointer] == ']':
        closeds = 0
        for i in range(codepointer, -1, -1):
            if code[i] == ']':
                closeds += 1
            elif code[i] == '[':
                closeds -= 1
            if closeds == 0:
                match = i
            break
    return match

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
