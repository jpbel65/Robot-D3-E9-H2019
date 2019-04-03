



class PathDrawer:
    def __init__(self, path):
        self.path = path
        self.pixelatedPath = self.convertPathFromCmToPixel()
        self.pixelRatio = self.path.getPixelRatio


    def convertPathFromCmToPixel(self):
        pixelatedPath = []
        for i in self.path:
            pixelatedPath.append((int(i[0]*self.pixelRatio), int(i[1]*self.pixelRatio)))
        return(pixelatedPath)
    # 111 cm de largeur, 231 cm
    # 1235 de long 612 de large 0.18704 0.181372549 5.350649 5.5135135       5.432081257 pixel/cm

    def getPixelatedPath(self):
        return self.pixelatedPath
