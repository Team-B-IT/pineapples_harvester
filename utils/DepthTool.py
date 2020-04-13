import utils.image2coord as i2c


class DepthTool():
    def readCord(self, file):
        self.cord = [[]]
        f = open(file, "r")

        id = 0 #index of current row

        for line in f:
            self.cord.append([])
            depthData = line.split(' ')
            for data in depthData:
                if data != "\n":
                    try:
                        convertedData = float(data)
                    except:
                        print((data))
                        pass
                    self.cord[id].append(convertedData)
            id += 1
        #remove last empty row
        self.cord.remove([])

        # height and width of image
        self.height = len(self.cord)
        self.width = len(self.cord[0])
        # print(self.height)
        # print(self.width)

    def getDepthBoundingBox(self, boxPos, gridSize, bias):
        # position of point on grid
        self.gridX = []
        self.gridY = []
        # pos[] = arr[i]
        #get bounding box position
        xLT = int(boxPos[0])# x left top
        yLT = int(boxPos[1]) # y left top
        xRD = int(boxPos[2]) # x right down
        yRD = int(boxPos[3]) # y right down
        # for i in range(yLT, yRD):
        #     print(cord[i][xLT:xRD])
        # devide box by grid size
        dX = xRD - xLT
        dY = yRD - yLT
        stepX = int(dX / gridSize)
        stepY = int(dY / gridSize)

        #save position of each point on grid
        for y in range(yLT, yRD, stepY):
            self.gridY.append(y)
        for x in range(xLT, xRD, stepX):
            self.gridX.append(x)

        self.dimY = len(self.gridY)
        self.dimX = len(self.gridX)
        depth = self.getDepthUsingVoteMap(bias)
        return depth

    def getAverageDepthAroundChosenPoint(self, x, y, bias):
        y = self.gridY[y]
        x = self.gridX[x]
        sum = 0.0
        count = 0
        for thisY in range(self.dimY):
            for thisX in range(self.dimX):
                yy = self.gridY[thisY]
                xx = self.gridX[thisX]
                if abs(self.cord[y][x] - self.cord[yy][xx]) < bias and self.cord[yy][xx] > 0:
                    sum += self.cord[yy][xx]
                    count += 1
        return sum / count

    def getDepthUsingVoteMap(self, bias):
        #vote map
        # print(posX)
        # print(posY)
        voteMap = [[0 for i in range(self.dimX)] for i in range(self.dimY)]
        for thisY in range(self.dimY):
            for thisX in range(self.dimX):
                for otherY in range(self.dimY):
                    for otherX in range(self.dimX):
                        y = min(max(self.gridY[thisY], 0), 719)
                        x = min(max(self.gridX[thisX], 0), 1279)
                        y2 = min(max(self.gridY[otherY], 0), 719)
                        x2 = min(max(self.gridX[otherX], 0), 1279)
                        # print ("({0}, {1}) ({2}, {3})".format(x, y, x2, y2))
                        if abs(self.cord[y][x] - self.cord[y2][x2]) < bias:
                            voteMap[thisY][thisX] += 1

        # print(voteMap)
        FposX = 0
        FposY = 0
        cur = 0
        for thisY in range(self.dimY):
            for thisX in range(self.dimX):
                # print(cord[posY[y]][posX[x]])
                y = self.gridY[thisY]
                x = self.gridX[thisX]
                if voteMap[thisY][thisX] > cur and self.cord[y][x] > 0.0:
                    cur = voteMap[thisY][thisX]
                    FposX = thisX
                    FposY = thisY
        # print(self.gridX[FposX], self.gridY[FposY])
        # return self.cord[self.gridY[FposY]][self.gridX[FposX]]
        #depth = self.getAverageDepthAroundChosenPoint(FposY, FposX, bias)
        depth = self.cord[self.gridY[FposY]][self.gridX[FposX]]
        # print(self.cord[self.gridY[FposY]][self.gridX[FposX]])
        return depth


if __name__ == '__main__':
    DepthTool = DepthTool()
    boxes = [[383,121, 430, 156], [853, 149, 894, 187]]
    f = "1574444192325.txt"
    bias = 0.1
    gridSize = 10
    DepthTool.readCord(f)
    for box in boxes:
        y = box[3]
        x = (box[0] + box[2]) / 2
        depth = DepthTool.getDepthBoundingBox(box, gridSize, bias) * 100
        print(x, y, depth)
        i2c.to_coord(x, y)
        i2c.to_coord_from_depth(x, y, depth)
