import 'normalize.css';

import Workbench from 'paraviewweb/src/Component/Native/Workbench';
import ToggleControl from 'paraviewweb/src/Component/Native/ToggleControl';
import BGColor from 'paraviewweb/src/Component/Native/BackgroundColor';
import Spacer from 'paraviewweb/src/Component/Native/Spacer';
import Composite from 'paraviewweb/src/Component/Native/Composite';
import ReactAdapter from 'paraviewweb/src/Component/React/ReactAdapter';
import WorkbenchController from 'paraviewweb/src/Component/React/WorkbenchController';
import { debounce } from 'paraviewweb/src/Common/Misc/Debounce';

import RemoteRenderer from 'paraviewweb/src/NativeUI/Canvas/RemoteRenderer';
import SizeHelper from 'paraviewweb/src/Common/Misc/SizeHelper';
import ParaViewWebClient from 'paraviewweb/src/IO/WebSocket/ParaViewWebClient';

import React from 'react';
import ReactDOM from 'react-dom';

import SmartConnect from 'wslink/src/SmartConnect';

const config = { sessionURL: 'ws://localhost:1234/ws' };
const smartConnect = SmartConnect.newInstance({ config });
var model = {};

const pvwsdProtocols = {
  pvwsdService: (session) => {
    return {
      changeColor: (arg1, arg2) => {
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
    };
  },
};

smartConnect.onConnectionReady((connection) => {
  model.pvwClient =
    ParaViewWebClient.createClient(connection,
                                   [
                                     'MouseHandler',
                                     'ViewPort',
                                     'ViewPortImageDelivery',
                                   ],
                                   pvwsdProtocols);
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

document.body.style.padding = '50';
document.body.style.margin = '50';

const divRoot = document.createElement('div');
divRoot.id = "root";
document.body.appendChild(divRoot);

class PVWSDControlPanel extends React.Component {
  render() {
    return (<center>
            <button onClick={() => model.pvwClient.pvwsdService.changeColor('pink','purple')}>Change Color</button>
            <button onClick={() => model.pvwClient.pvwsdService.showCone()}>Show Cone</button>
            <button onClick={() => model.pvwClient.pvwsdService.hideCone()}>Hide Cone</button>
            </center>
           );
  }
}

const divRenderer = document.createElement('div');
document.body.appendChild(divRenderer);

divRenderer.style.position = 'relative';
divRenderer.style.width = '100vw';
divRenderer.style.height = '100vh';
divRenderer.style.overflow = 'hidden';

ReactDOM.render(<PVWSDControlPanel />,
                document.getElementById('root'));

smartConnect.connect();

