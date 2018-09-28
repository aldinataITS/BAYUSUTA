import cv2

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv

x=0
y=0
w=0
h=0
global x,y,w,h

x+=131
y+=110
w-=224
h-=168

cap = cv2.VideoCapture(1)

flag = 0

while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    rgb = rgb[y:y+h, x:x+w]

    print rgb.shape

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out = cv2.imwrite('test'+str(flag)+'.jpg', frame)
        print flag
        flag += 1
        continue
        #break
    elif cv2.waitKey(1) & 0xFF == 27:
        print("Break")
        break
    
cap.release()
cv2.destroyAllWindows()
