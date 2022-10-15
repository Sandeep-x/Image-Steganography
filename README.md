# Image Steganography
Image Steganography refers to the process of hiding data within an image file. The image selected for this purpose is called the cover image and the image obtained after steganography is called the stego image. This application will let you hide any text message in any image file of user's choice with the help of secure key input by user, It also let you retrive your text message from Stego Image with the help of same key used for hiding the message.
<br>
## Features
<ul>
  <li>Select Cover Image</li>
  <li>Input Message and Key</li>
  <li>Create Stego Image</li>
  <li>Retrive Message</li>
 </ul>
 
  ## Technologies
 <ul>
  <li>Python 3.10.5</li>
  <li>OpenCV 4.6.0</li>
  <li>Pillow 9.2.0</li>
  <li>Tkinter</li>
 </ul>
 
  ## Setup
 Clone this repo and use any python interpreter(PyCharm) to run this code.
 Make sure to run the below commands to add the necessary libraries.<br>
 <ul>
  <li><b>pip install pillow </b></li>
  <li><b>pip install opencv-python</b></li>
  <li><b>pip install tk</b></li>
 </ul>
 
 ## Demo
 This is a simple demo to show you how to use the app.



https://user-images.githubusercontent.com/18510244/195977235-21496abf-056f-4a5c-9e19-aea6611c07ca.mp4


Select the radio button for Hiding or Retiving text.
In hiding process, Select the cover image, input the message to hide and provide the key for securely hiding the meaasge. Click on Stego button to hide the message, After Stego image is produced save it in desired folder.
In retrieving process, Select the stego image from which you want to retrieve the message then input the key used in hiding process, click on extract button to get the message.<br>
<b>Note: </b> Wrong key will extract unexpected output (message).
