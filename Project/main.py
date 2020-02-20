import cv2
import functions as funcs

imageName=input()#image_name.jpg
img0= cv2.imread(imageName, 0)#read the image
img=funcs.correctRotation(img0)#correct the rotation of the image
img1,circles1=funcs.getAllCircles(img,10,15)#recognize all the MCQ circles in the image
img2,circles2=funcs.getFilledCircles(img,10,15)#recognize all the filled circles in the image
circles1 = funcs.arrangeCircles(circles1)#arrange all circles with respect to the Y-axis then with respect to the X-axis
circles2 = funcs.arrangeCircles(circles2)#arrange the Filled circles with respect to the Y-axis then with respect to the X-axis
gender, semester, program, answers=funcs.scann(circles1,circles2)#scann the circles to compute the answers

#print the output on the console
print(gender)
print(semester)
print(program)
print(answers)
print("The output is saved in output.txt")

text_file = open("output.txt", "w")#make a text file named "output" and open it in "Write mode"
#print the output on the text file
text_file.write("The output of image: "+ imageName +"\n")
text_file.write("\n")
text_file.write("Gender: "+ gender +"\n")
text_file.write("Semester: "+ semester+"\n")
text_file.write("Program: "+ program+"\n")
for i in range(5):
    text_file.write("answer of Q1."+str(i+1)+" is:"+ answers[i]+"\n")
for i in range(5,11):
    text_file.write("answer of Q2."+str(i-4)+" is:"+ answers[i]+"\n")
for i in range(11,14):
    text_file.write("answer of Q3."+str(i-10)+" is:"+ answers[i]+"\n")
for i in range(14,17):
    text_file.write("answer of Q4."+str(i-13)+" is:"+ answers[i]+"\n")
for i in range(17,19):
    text_file.write("answer of Q5."+str(i-16)+" is:"+ answers[i]+"\n")

text_file.close()