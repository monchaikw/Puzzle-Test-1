import random
import cv2
import mediapipe as mp

redColor = (0,0,255)
blueColor = (255,0,0)
whiteColor = (255,255,255)
boxWidth = 100
boxHeight = 100
padLeft = 17
padBottom = 32
puzzSize = 4
puzzle = [ [1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0] ]

def getSpacePos( puzz ) :
    for count, row in enumerate( puzz ) :
        if 0 in row :
            return count, row.index(0)

def getSwappablePos( puzz ) :
    row,col = getSpacePos( puzz )
    prob = []
    if row > 0 : prob.append( (row-1,col) )             # top
    if row+1 < puzzSize : prob.append( (row+1,col) )    # bottom
    if col > 0 : prob.append( (row,col-1) )             # left
    if col+1 < puzzSize : prob.append( (row,col+1) )    # right
    return prob

def swapPuzzle( puzz, swapPos ) :
    row1,col1 = getSpacePos( puzz )
    row2,col2 = swapPos
    tem              = puzz[row1][col1]
    puzz[row1][col1] = puzz[row2][col2]
    puzz[row2][col2] = tem
    return puzz

def drawPuzzle( x, y ) :
    global puzzleActiveNo, puzzleActiveTime
    for row in range(puzzSize) :
        for col in range(puzzSize) :
            if puzzle[row][col] :
                topBox    = row * boxHeight + 3
                leftBox   = col * boxWidth + 3
                bottomBox = row * boxHeight + boxHeight - 3
                rightBox  = col * boxWidth + boxWidth - 3
                if (row,col) in swappablePos \
                    and x >= leftBox and x <= rightBox \
                    and y >= topBox and y <= bottomBox :
                    drawColor = redColor
                else :
                    drawColor = blueColor
                number = str(puzzle[row][col])
                xNumber = leftBox + padLeft
                if len(number) == 1 : xNumber += 15
                yNumber  = bottomBox - padBottom
                cv2.rectangle(image, (leftBox,topBox), (rightBox,bottomBox), drawColor, 2)
                cv2.putText(image, number, (xNumber-1,yNumber-1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, whiteColor, 3, cv2.FILLED)
                cv2.putText(image, number, (xNumber,yNumber), cv2.FONT_HERSHEY_SIMPLEX, 1.5, drawColor, 3, cv2.FILLED)

for i in range(3000) :
    puzzle = swapPuzzle( puzzle, random.choice(getSwappablePos(puzzle)) )

swappablePos = getSwappablePos( puzzle )

cap = cv2.VideoCapture( 0 )
capWidth  = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
capHeight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:
    _, image = cap.read()
    image = cv2.flip(image, 1)
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None :
        pointer = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        xPointer = int(pointer.x * capWidth)
        yPointer = int(pointer.y * capHeight)
    else :
        xPointer = yPointer = 0
    drawPuzzle( xPointer, yPointer )
    cv2.imshow("Webcam", image)
    key = cv2.waitKey(1) & 0xFF
    if key == 27: break
cap.release()
cv2.destroyAllWindows()
