PIXELRATIO = 5.432081257


class PathDrawer:
    def __init__(self, path):
        self.path = path
        self.pixelatedPath = self.convertPathFromCmToPixel()


    def convertPathFromCmToPixel(self):
        pixelatedPath = []
        for i in self.path:
            pixelatedPath.append((int(i[0]*PIXELRATIO), int(i[1]*PIXELRATIO)))
        return(pixelatedPath)
    # 111 cm de largeur, 231 cm
    # 1235 de long 612 de large 0.18704 0.181372549 5.350649 5.5135135       5.432081257 pixel/cm

    def getPixelatedPath(self):
        return self.pixelatedPath
