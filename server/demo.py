"""
A demo of the SLAM server using Panda3D to display the position and orientation of the camera in realtime.

Adin Ackerman
"""

from threading import Thread
from math import pi

import logging

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from server import SlamServer


class MyApp(ShowBase):
    """
    A simple Panda3D app to demonstrate the SLAM data in real time.

    Adapted from the Panda3D Getting Started tutorial.
    """

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        if self.loader is not None:
            self.scene = self.loader.loadModel("models/environment")
        else:
            raise NotImplementedError("Loader object does not exist.")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.update_camera, "Update Camera")

        self.server = SlamServer(
            host='0.0.0.0', port=8080, loglevel=logging.INFO)
        Thread(target=self.server.run_forever, daemon=True).start()

    def update_camera(self, task):
        """
        Use asyncronously updated transformation values to update camera pose.
        """

        pos = [10*num for num in self.server.pos]  # scale motion
        rot = tuple(map(lambda angle: angle * 180 / pi, self.server.rot))

        if self.camera is not None:
            self.camera.setPos(pos[0], -pos[2], pos[1])
            self.camera.setHpr(rot[1], rot[0], -rot[2])
        else:
            raise Exception("Camera object does not exist.")

        return Task.cont


app = MyApp()
app.run()
