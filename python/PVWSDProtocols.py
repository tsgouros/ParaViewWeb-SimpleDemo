# This code is released under the Creative Commons zero license.  Go wild, but
# it would be nice to preserve the credit if you find it helpful.
#
# Tom Sgouros
# Center for Computation and Visualization
# Brown University
# March 2018.
import os, sys, logging, types, inspect, traceback, logging, re, json, base64
from time import time

# import RPC annotation
from wslink import register as exportRPC

# import paraview modules.
import paraview

from paraview import simple, servermanager
from paraview.web import protocols as pv_protocols

# This class inherits from the standard ParaViewWeb protocols, and adds a
# few new ones with the @exportRPC decorator.  These become RPC calls that
# can be invoked from the web client.
class PVWSDTest(pv_protocols.ParaViewWebProtocol):

    def __init__(self):
        super(PVWSDTest, self).__init__()

        # Set initial conditions.
        self.colorToggle = True
        self.coneShown = True

    def addListener(self, dataChangedInstance):
        self.dataListeners.append(dataChangedInstance)

    # This function is not invoked remotely, just used to set up the
    # paraview visualization and the data in it.  If you are editing this,
    # try recording a Paraview session with the trace turned on, and then
    # compare it to this code.
    def drawCone(self):

        ##################################################
        # create a new Cone object
        self.cone1 = simple.Cone()

        ## In a Paraview Trace recorded session, the 'simple.' object is
        ## not necessary.  Take your Trace output and add 'simple.' to all
        ## the capitalized functions and add 'self.' to the local
        ## variables, and try just dropping it in here.

        # set active source
        simple.SetActiveSource(self.cone1)

        # get active view
        self.renderView1 = simple.GetActiveViewOrCreate('RenderView')

        # show data in view
        self.cone1Display = simple.Show(self.cone1, self.renderView1)

        # trace defaults for the display properties.
        self.cone1Display.Representation = 'Surface'

        # reset view to fit data
        self.renderView1.ResetCamera()

        # Properties modified on cone1
        self.cone1.Resolution = 12

        # change solid color
        self.cone1Display.DiffuseColor = [0.666, 0.0, 1.0]

        # reset view to fit data
        self.renderView1.ResetCamera()

        # update the view to ensure updated data information
        self.renderView1.Update()

        # current camera placement for renderView1
        self.renderView1.CameraPosition = [1.25, -3.0, -0.4]
        self.renderView1.CameraViewUp = [0.75, 0.2, 0.6]
        self.renderView1.CameraParallelScale = 0.85

        ##################################################

    # This is the decorator that creates an RPC entry point.  The number of
    # arguments is set by the function definition the decorator is
    # decorating.
    @exportRPC("pvwsdprotocol.change.sides")
    def changeSides(self, N):

        # Properties modified on cone1.  Note the type change. (A string is
        # what is delivered.)
        self.cone1.Resolution = int(N)

        # update the view to ensure updated data information
        self.renderView1.Update()
        return "**** changed number of sides to " + str(N) + " *****"


    @exportRPC("pvwsdprotocol.show.cone")
    def showCone(self):

        print("Showing cone.")
        self.cone1Display = simple.Show(self.cone1, self.renderView1)
        self.renderView1.Update()
        self.coneShown = True
        return "**** executed showCone() ****"

    @exportRPC("pvwsdprotocol.hide.cone")
    def hideCone(self):

        print("Hiding cone.")
        self.cone1Display = simple.Hide(self.cone1, self.renderView1)
        self.renderView1.Update()
        self.coneShown = False
        return "**** executed hideCone() ****"

    @exportRPC("pvwsdprotocol.change.color")
    def changeColor(self, arg1, arg2):
        # We don't do anything with the arg1 and arg2, just pass them to show
        # how it's done.

        if not self.coneShown:
            return "*** Can't change color of invisible object! ***"

        print("Toggling color.")

        if (self.colorToggle):
            print("Changing to pink.")

            # change solid color
            self.cone1Display.DiffuseColor = [1.0, 0.666, 1.0]
            self.renderView1.Update()

        else:
            print("Changing to purple.")

            # change solid color
            self.cone1Display.DiffuseColor = [0.666, 0.0, 1.0]
            self.renderView1.Update()

        self.colorToggle = not self.colorToggle

        return "******** executed change color with: " + str(arg1) + str(arg2) + " *******"

