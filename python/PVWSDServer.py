# This code is released under the Creative Commons zero license.  Go wild, but
# it would be nice to preserve the credit if you find it helpful.
#
# Tom Sgouros
# Center for Computation and Visualization
# Brown University
# March 2018.
#
# This module is a ParaViewWeb server application.
#    Use it like this:
#     $ pvpython PVWSDServer.py -i localhost -p 1234
#
# There should be a README to explain how to start the client.

# import to process args
import os
import sys

# import paraview modules.
from paraview.web import pv_wslink
from paraview.web import protocols as pv_protocols

import PVWSDProtocols

# import RPC annotation
from wslink import register as exportRPC

from paraview import simple
from wslink import server

import json
import argparse

# =============================================================================
# Create custom Pipeline Manager class to handle clients requests
# =============================================================================

class PVWSDServer(pv_wslink.PVServerProtocol):

    authKey = "wslink-secret"
    viewportScale=1.0
    viewportMaxWidth=2560
    viewportMaxHeight=1440


    @staticmethod
    def add_arguments(parser):
      # Not using this argument, but it's here to show how to do it.
      parser.add_argument("--data", default=os.getcwd(),
                            help="path to data directory to list", dest="data")

    @staticmethod
    def configure(args):
      # Same here. Not really using this, but this is how it should look.
      PVWSDServer.authKey   = args.authKey
      PVWSDServer.data      = args.data


    def initialize(self):

      # Register the built-in protocols: MouseHandler, ViewPort and
      # ViewPortImageDelivery.  (You can see these over on the client
      # in the createClient call)
      self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
      self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort(PVWSDServer.viewportScale, PVWSDServer.viewportMaxWidth, PVWSDServer.viewportMaxHeight))
      self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPortImageDelivery())

      # Instantiate an object with the custom protocols...
      PVWSDTest = PVWSDProtocols.PVWSDTest()

      #                                      ... and register them, too.
      self.registerVtkWebProtocol(PVWSDTest)

      # Update authentication key to use
      self.updateSecret(PVWSDServer.authKey)

      # Disable interactor-based render calls
      simple.GetRenderView().EnableRenderOnInteraction = 0
      simple.GetRenderView().Background = [0,0,0]
      simple.GetRenderView().Background2 = [0,0,0]

      # Initialize our scene.
      PVWSDTest.drawCone()

      # Update interaction mode
      pxm = simple.servermanager.ProxyManager()
      interactionProxy = pxm.GetProxy('settings',
                                      'RenderViewInteractionSettings')
      interactionProxy.Camera3DManipulators = ['Rotate',
                                               'Pan',
                                               'Zoom',
                                               'Pan',
                                               'Roll',
                                               'Pan',
                                               'Zoom',
                                               'Rotate',
                                               'Zoom']

      # Custom rendering settings
      renderingSettings = pxm.GetProxy('settings', 'RenderViewSettings')
      renderingSettings.LODThreshold = 102400

# =============================================================================
# Main: Parse args and start server
# =============================================================================

if __name__ == "__main__":
  # Create argument parser
  parser = argparse.ArgumentParser(description="PVWSD")

  # Add arguments with argparse.
  server.add_arguments(parser)
  PVWSDServer.add_arguments(parser)
  args = parser.parse_args()
  PVWSDServer.configure(args)

  # Start server
  server.start_webserver(options=args, protocol=PVWSDServer)
