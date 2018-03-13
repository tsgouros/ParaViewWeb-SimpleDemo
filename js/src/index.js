// This code is released under the Creative Commons zero license.  Go wild, but
// it would be nice to preserve the credit if you find it helpful.
//
// Tom Sgouros
// Center for Computation and Visualization
// Brown University
// March 2018.

import 'normalize.css';

import Workbench from 'paraviewweb/src/Component/Native/Workbench';
import ToggleControl from 'paraviewweb/src/Component/Native/ToggleControl';
import BGColor from 'paraviewweb/src/Component/Native/BackgroundColor';
import Spacer from 'paraviewweb/src/Component/Native/Spacer';
import Composite from 'paraviewweb/src/Component/Native/Composite';
import ReactAdapter from 'paraviewweb/src/Component/React/ReactAdapter';
import WorkbenchController from 'paraviewweb/src/Component/React/WorkbenchController';
import NumberSliderWidget from 'paraviewweb/src/React/Widgets/NumberSliderWidget';
import { debounce } from 'paraviewweb/src/Common/Misc/Debounce';

import RemoteRenderer from 'paraviewweb/src/NativeUI/Canvas/RemoteRenderer';
import SizeHelper from 'paraviewweb/src/Common/Misc/SizeHelper';
import ParaViewWebClient from 'paraviewweb/src/IO/WebSocket/ParaViewWebClient';

import React from 'react';
import ReactDOM from 'react-dom';

import SmartConnect from 'wslink/src/SmartConnect';

// This URL and port number are determined when you invoke the server.
// See python/PVWSDServer.py for instructions.
const config = { sessionURL: 'ws://localhost:1234/ws' };

// We'll use that config object to create a connection to the
// pvpython-run server.
const smartConnect = SmartConnect.newInstance({ config });

// This is just a global object we can use to attach data to, in order to
// access it from other scopes.
var model = {};

// This is a hash of functions that return protocols.  For this example, we
// have only one, called 'pvwsdService'.  You could have more than one, though
// I'm not sure why you'd need that.
const pvwsdProtocols = {
  pvwsdService: (session) => {

    // We return a hash of functions, each of which invokes an RPC call.  The
    // 'session.call' function takes the name of an remote procedure and a list
    // of arguments.
    return {
      changeColor: (arg1, arg2) => {
        // The string here exactly matches a string in the @exportRPC decorator
        // in the PVWSDProtocols.py file.  Note that the RPC names must be
        // lower case only.  This is a limitation of wslink, I believe.
        session.call('pvwsdprotocol.change.color', [ arg1, arg2 ])
          .then((result) => console.log('result: ' + result));
        console.log("******* pressed Change Color *******");
      },

      showCone: () => {
        session.call('pvwsdprotocol.show.cone', [])
          .then((result) => console.log('result' + result));
        console.log("******* pressed Show Cone *******");
      },

      hideCone: () => {
        session.call('pvwsdprotocol.hide.cone', [])
          .then((result) => console.log('result' + result));
        console.log("******* pressed Hide Cone *******");
      },

      changeSides: (N) => {
        session.call('pvwsdprotocol.change.sides', [ N ])
          .then((result) => console.log('result: ' + result));
        console.log("******* adjusted number of sides ********");
      },
    };
  },
};

// Create a callback to be executed when the connection is made.
smartConnect.onConnectionReady((connection) => {
  // The createClient method takes a connection, a list of predefined protocols
  // to use, and a function that returns
  model.pvwClient =
    ParaViewWebClient.createClient(connection,
                                   [
                                     'MouseHandler',   // <--- These are pre-defined.
                                     'ViewPort',
                                     'ViewPortImageDelivery',
                                   ],
                                   pvwsdProtocols);    // <-- These are yours.

  // Now build the HTML element that will display the goods.
  const renderer = new RemoteRenderer(model.pvwClient);
  renderer.setContainer(divRenderer);
  renderer.onImageReady(() => {
    console.log('image ready (for next command)');
  });
  window.renderer = renderer;
  SizeHelper.onSizeChange(() => {
    renderer.resize();
  });
  SizeHelper.startListening();
});

const divTitle = document.createElement('div');
document.body.appendChild(divTitle);
divTitle.innerHTML = '<h1>Hello World!</h1><p>Click a button then click in the main viewing window to see the result.  I advise you to check out the console, too.';

const divRoot = document.createElement('div');
divRoot.id = "root";
document.body.appendChild(divRoot);

// Let's create the controls.
class PVWSDControlPanel extends React.Component {
  constructor(props) {
    super(props);
    // The state of the controls is really just the N on the slider.  There is
    // also a state for the visibility of the cone, but this is tracked on the
    // server.
    this.state = {N: 12};

    this.updateVal = this.updateVal.bind(this);
  }

  updateVal(e) {
    // What changes, and what value?
    const which = e.target.name;
    const newVal = e.target.value;
    const toUpdate = {};
    toUpdate[which] = newVal;

    // Update the new value in the display.
    this.setState(toUpdate);

    console.log(typeof e.target.value);
    // Communicate it to the server.
    model.pvwClient.pvwsdService.changeSides(e.target.value);
  }

  render() {
    const [N] = [this.state.N];

    return (<center>
            <div style={{width: '100%', display: 'table'}}>
            <div style={{display: 'table-cell'}}>
            <button onClick={() => model.pvwClient.pvwsdService.changeColor('pink','purple')}>Change Color</button>
            <button onClick={() => model.pvwClient.pvwsdService.showCone()}>Show Cone</button>
            <button onClick={() => model.pvwClient.pvwsdService.hideCone()}>Hide Cone</button>
            </div>
            <div style={{display: 'table-cell'}}>
            <NumberSliderWidget value={N}
            max="100" min="3" onChange={this.updateVal} name="N"/>
            </div>
            </div>
            </center>
           );
  }
}

// Prepare the rest of the page to be shown.
const divRenderer = document.createElement('div');
document.body.appendChild(divRenderer);

divRenderer.style.position = 'relative';
divRenderer.style.width = '100vw';
divRenderer.style.height = '100vh';
divRenderer.style.overflow = 'hidden';

ReactDOM.render(<PVWSDControlPanel />,
                document.getElementById('root'));

// Let 'er rip.
smartConnect.connect();

