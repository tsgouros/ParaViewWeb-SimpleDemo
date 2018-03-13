# ParaViewWeb-SimpleDemo
A bare-bones example for people who want to put together a ParaViewWeb
application.

Use this framework to start building a ParaViewWeb application.  It
has a lot of the basics in place -- how to create callable remote
procedures on the python server and how to invoke them from the
client.  It also uses webpack for the client configuration and npm for
its management.

This code is released under the Creative Commons zero license.  Go wild.

```
Tom Sgouros
Center for Computation and Visualization
Brown University
March 2018.
```

# What's going on

The Paraview server is a python-controlled server that runs a paraview
session and is accessible remotely from a web client.  Meanwhile,
there is a web server to serve the client (we just use node.js).  So
there are *three* components here:

 - the paraview server, implemented in Python, and in the python
   subdirectory, which contains a server.py to be the framework, and a
   protocols.py file to contain the communication details between the
   server and the web client.

 - the web server.  This to serve up the web client, and is just
   node.js.  Inside the js directory, you'll find the package.json
   file for explaining what the client pieces are and the
   dependencies, and a config file for webpack, to explain how to
   build and serve the thing.

 - the javascript client.  You'll find this in js/src/index.js.  It's
   pretty rudimentary, but then it's just an example.


# Invitation to newbies

This is undoubtedly a *bad* implementation of the client and server,
since it was put together by someone who is not an expert.  But
hopefully it will serve as a good introduction for other people who
are not experts.  Please feel free to use this code however you wish.
If there is some feature that I have not explained, feel free to offer
a pull request with a better explanation in the comments.

# Invitation to experts

This is undoubtedly a *bad* implementation of the client and server,
since it was put together by someone who is not an expert.  It is
meant for people who are just trying this out and likely to struggle
with the details of the RPC implementation at first.

If there are errors I have made, or features that you see missing here
that cry out to be added, please feel free to fix or add them, and
offer me a pull request with the features added.  But remember, this
is for beginners, so please be liberal with the comments.  Please
remember that anyone can see *what* your code is doing, but nobody can
tell *why* it's doing it.  Any fool can write code only they can use;
the hard thing is to write code that is useful to the rest of us.


# Building and running.
Try this:
```
$ cd python
$ pvpython SimpleDemoServer.py -i localhost -p 1234
```
Over on the client, try this:
```
$ cd js
$ npm install
$ npm run build
$ npm start
```
Then cross your fingers and go to a browser and open localhost:8080.

