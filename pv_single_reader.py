#!/usr/bin/python

import os
import sys
from paraview.simple import *

datadir = str(os.environ.get('MOVIEDIR'))
numframes = int(os.environ.get('NUMFRAMES'))

intfcbase = datadir + '/' + '2d-intfc'

intfcfiles = []
for r in range (1,numframes+1):
    intfcfiles.append(intfcbase + "-" + str(r) + ".vtk")

iNTFC = LegacyVTKReader(FileNames=intfcfiles)


datatype = str(os.environ.get('DATATYPE'))
base = datadir + '/' + datatype

datatypefiles = []
for r in range (1,numframes+1):
    datatypefiles.append(base + "-" + str(r) + ".vtk")

dATATYPE = LegacyVTKReader(FileNames=datatypefiles)


# get animation scene
animationScene = GetAnimationScene()

# update animation scene based on data timesteps
animationScene.UpdateAnimationUsingDataTimeSteps()

#view = CreateRenderView()
view = GetActiveViewOrCreate('RenderView')

intfcDisplay = Show(iNTFC, view)

#Reset camera so that axes line up through center of animation figure
view.ResetCamera()

dataDisplay = Show(dATATYPE, view)
dataLUT = GetColorTransferFunction(datatype)

# update the view to ensure updated data information
view.Update()

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
dataLUT.ApplyPreset('Jet', True)

animationScene.GoToLast()
dataDisplay.RescaleTransferFunctionToDataRange(False, True)

#RenderAllViews()

jpgdir = str(os.environ.get('JPGDIR'))

#SaveAnimation(jpgdir + '/' + datatype + '.jpg', view, ImageResolution=[843, 570],FrameWindow=[0, numframes-1], SuffixFormat="%04d")
SaveAnimation(jpgdir + '/' + datatype + '.jpg', view, FrameWindow=[0, numframes-1], SuffixFormat='%04d')





