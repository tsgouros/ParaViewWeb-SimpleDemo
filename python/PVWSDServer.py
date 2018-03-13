"""
This module is a ParaViewWeb server application.
    Use it like this:
     $ pvpython PVWSDServer.py -i localhost -p 1234
"""

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

try:
    import argparse
except ImportError:
    # since  Python 2.6 and earlier don't have argparse, we simply provide
    # the source for the same as _argparse and we use it instead.
    from vtk.util import _argparse as argparse

# =============================================================================
# Create custom Pipeline Manager class to handle clients requests
# =============================================================================

class PVWSDServer(pv_wslink.PVServerProtocol):

    authKey = "wslink-secret"
    dsHost = None
    dsPort = 11111
    rsHost = None
    rsPort = 11111
    rcPort = -1
    fileToLoad = None
    groupRegex = "[0-9]+\\."
    excludeRegex = "^\\.|~$|^\\$"
    plugins = None
    filterFile = None
    colorPalette = None
    proxies = None
    allReaders = True
    saveDataDir = os.getcwd()
    viewportScale=1.0
    viewportMaxWidth=2560
    viewportMaxHeight=1440
    config = {
        "profiles": {
            "default": {
                "modules_included": [],
                "modules_excluded": [],
                "viewType": 1,
            },
            "secondary": {
                "modules_included": [],
                "modules_excluded": [],
                "viewType": 2,
            },
        },
    }


    @staticmethod
    def add_arguments(parser):
      # Not using this argument, but it's here to show how to do it.
      parser.add_argument("--data", default=os.getcwd(),
                            help="path to data directory to list", dest="data")

    @staticmethod
    def configure(args):
      PVWSDServer.authKey   = args.authKey
      PVWSDServer.data      = args.data


    def initialize(self):

      self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
      self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort(PVWSDServer.viewportScale, PVWSDServer.viewportMaxWidth, PVWSDServer.viewportMaxHeight))
      self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPortImageDelivery())

      PVWSDTest = PVWSDProtocols.PVWSDTest()

      ## Register the PVWSD components
      self.registerVtkWebProtocol(PVWSDTest)

      # Update authentication key to use
      self.updateSecret(PVWSDServer.authKey)

      # Disable interactor-based render calls
      simple.GetRenderView().EnableRenderOnInteraction = 0
      simple.GetRenderView().Background = [0,0,0]
      simple.GetRenderView().Background2 = [0,0,0]

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

  # Add arguments
  server.add_arguments(parser)
  PVWSDServer.add_arguments(parser)
  args = parser.parse_args()
  PVWSDServer.configure(args)

  args.fsEndpoints = 'ds=' + args.data

  # Start server
  server.start_webserver(options=args, protocol=PVWSDServer)
