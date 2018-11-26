import face_recognition
import cv2

class Offset: #used to adjust the image relative to the faces in the screen
    def Y_offset(self, left_eye, offset):
        self.left_eye = left_eye
        self.offset = offset
        height_offset =  self.left_eye + offset
        return height_offset
    def X_offset(self, left_eye, offset):
        self.left_eye = left_eye
        width_offset = self.left_eye + offset
        return width_offset
    def draw(self,height, width, frame_height, frame_width, frame, h_offset, w_offset,img):
        self.height = height
        self.width = width
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.frame = frame
        self.h_offset = h_offset
        self.w_offset = w_offset
        self.img = img
        for i in range(0,self.height):
            if self.h_offset + i >= self.frame_height:
                break
            for j in range(0, self.width):
                if self.img[i,j][3] != 0:
                    if self.w_offset + j >= self.frame_width:
                        break
                    else:
                        self.frame[self.h_offset + i,self.w_offset + j] = self.img[i,j]

class Camera: #main class
    def main(self):
        cam = cv2.VideoCapture(0)
        offset = Offset()
        glass = cv2.imread("./santa/Glasses3.png",-1) #use imread 
        beard = cv2.imread("./santa/ber.png",-1)
        hat = cv2.imread("./santa/hat1.png",-1)
        glass = cv2.cvtColor(glass, cv2.COLOR_BGR2BGRA)
        beard = cv2.cvtColor(beard, cv2.COLOR_BGR2BGRA)
        hat = cv2.cvtColor(hat, cv2.COLOR_BGR2BGRA)

        while(cam.isOpened()):
            ret, frame = cam.read()
            fh,fw,fc = frame.shape
            face_locations = face_recognition.face_locations(frame)
            face_landmarks_list = face_recognition.face_landmarks(frame) #this contains the coordinates of the face
            im = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) # you can print(face_landmarks_list) to see the variation of
            #each coordinates as the face moves on the screen

            for elements in face_landmarks_list: #i resized the image using the coordinates of the left and right eye
                glass = cv2.resize(glass, (140+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])),
                (140+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
                beard = cv2.resize(beard, ((120+int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])),
                (200+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
                hat = cv2.resize(hat, (130+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])),
                (150+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
                #because we determine the coordinates using index, the overlayed image will automatically move relative to the
                #face

                height_offset = offset.Y_offset(elements['left_eye'][2][1], -60) #along Y axis
                width_offset = offset.X_offset(elements['left_eye'][0][0], -70) #along  X axis
                height_offset1 = offset.Y_offset(elements['left_eye'][2][1], 60)
                width_offset1 = offset.X_offset(elements['left_eye'][0][0], -60)
                height_offset2 = offset.Y_offset(elements['left_eye'][2][1], -200)
                width_offset2 = offset.X_offset(elements['left_eye'][0][0], -90) #here we can change the values to
                #adjust the desired location of the image
            
            #error handling
            #error occurs when only the half part of the face is scanned, to eliminate this, we use an algorithm such
            #that when the face exceeds the screen, the process will continue
            
                gh,gw,gc = glass.shape
                #graphics.draw(gh, gw, fh, fw, im, height_offset, width_offset, glass)
                for i in range(0,gh):
                    if height_offset + i >= fh:
                        break
                    for j in range(0, gw):
                        if glass[i,j][3] != 0:
                            if width_offset + j >= fw:
                                break
                            else:
                                im[height_offset + i,width_offset + j] = glass[i,j]

                bh,bw,bc = beard.shape
                for i in range(0,bh):
                    if height_offset1 + i >= fh:
                        break
                    for j in range(0, bw):
                        if beard[i,j][3] != 0:
                            if width_offset1 + j >= fw:
                                break
                            else:
                                im[height_offset1 + i,width_offset1 + j] = beard[i,j]

                ch,cw,cc = hat.shape
                for i in range(0,ch):
                    if height_offset2 + i >= fh:
                        break
                    for j in range(0, cw):
                        if hat[i,j][3] != 0:
                            if width_offset2 + j >= fw:
                                break
                            else:
                                im[height_offset2 + i,width_offset2 + j] = hat[i,j]
                

                cv2.imshow("Press esc to exit", im)
                glass = cv2.imread("./santa/Glasses3.png",-1)
                beard = cv2.imread("./santa/ber.png",-1)                
                hat = cv2.imread("./santa/hat1.png",-1)

                if cv2.waitKey(1) == 27:
                    break
        cam.release()
        cv2.destroyAllWindows()

camera = Camera()
camera.main()
#cam.release()
#cv2.destroyAllWindows()

