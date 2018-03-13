import os, sys, logging, types, inspect, traceback, logging, re, json, base64
from time import time

# import RPC annotation
from wslink import register as exportRPC

# import paraview modules.
import paraview

from paraview import simple, servermanager
from paraview.web import protocols as pv_protocols

# Needed for:
#    vtkSMPVRepresentationProxy
#    vtkSMTransferFunctionProxy
#    vtkSMTransferFunctionManager
from vtk.vtkPVServerManagerRendering import vtkSMPVRepresentationProxy, vtkSMTransferFunctionProxy, vtkSMTransferFunctionManager

# Needed for:
#    vtkSMProxyManager
from vtk.vtkPVServerManagerCore import vtkSMProxyManager

# Needed for:
#    vtkDataObject
from vtk.vtkCommonDataModel import vtkDataObject


class PVWSDTest(pv_protocols.ParaViewWebProtocol):

    def __init__(self):
        super(PVWSDTest, self).__init__()

        # Set initial conditions.
        self.colorToggle = True
        self.coneShown = True

    def addListener(self, dataChangedInstance):
        self.dataListeners.append(dataChangedInstance)

    def drawCone(self):

        ##################################################
        # create a new Cone object
        self.cone1 = simple.Cone()

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

