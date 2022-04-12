<h1>Image Steganography</h1>
Steganography is the technique of hiding secret data within an ordinary, non-secret file or message in order to avoid detection the secret data is then extracted at its destination.
Image Steganography refers to the process of hiding data within an image file. The image selected for this purpose is called the cover image and the image obtained after steganography is called the stego image.   
  <br>
  <br>
  
 **Least Significant Bit Steganography :**

We can describe a digital image as a finite set of digital values, called pixels. Pixels are 
the smallest individual element of an image, holding values that represent the 
brightness of a given color at any specific point. So we can think of an image as a matrix 
(or a two-dimensional array) of pixels which contains a fixed number of rows and 
columns.
Least Significant Bit (LSB) is a technique in which the last bit of each pixel is modified 
and replaced with the secret message’s data bit.

**Algorithm :**

1. Initializing key as a string of numeric character(range: 0-7), length of key is 8
i.e key=”75143206” (any permutation of the key can be taken as a secret key)

2. **Encoding Algorithm :**  
• Input Image and Secret Message  
• Convert Secret Message to binary list  
• Three pixels are read at a time having a total of 3*3=9 RGB values(9 pixels 
read for greyscale image). The first eight RGB values are used to store one 
character that is converted into an 8-bit binary.  
• A list of 9 RGB values are taken, arr[0-8]  
• Pixel values are chosen from the list arr to store bits of character , pixel 
value is chosen as per the key value.
i.e 1st bit can be stored at arr[3], 2nd bit can be stored at arr[0] (This is 
depend on the secret key to choose the RGB values)  
• The corresponding RGB value and binary data are compared. If the binary 
digit is 1 then the RGB value is converted to odd and, otherwise, even.  
• The ninth value determines if more pixels should be read or not. If there 
is more data to be read, i.e. encoded or decoded, then the ninth pixel 
changes to even. Otherwise, if we want to stop reading pixels further, 
then make it odd.  
• Perform Left shift operation on key  
• Repeat the above process until all characters are encoded to the image.  

3. **Decoding Algorithm :**  
 • Input stego_image(image after messege is hidden)  
 • Again, three pixels are read at a time(9 pixels read for greyscale image). 
The first 8 RGB values give us information about the secret data, and the 
ninth value tells us whether to move forward or not.  
• A list of 9 RGB values are taken, arr[0-8]  
• Pixel values are chosen from the list arr to store bits of character , pixel 
value is chosen as per the key value.
i.e 1st bit can be stored at arr[3], 2nd bit can be stored at arr[0] (This is 
depend on the secret key to choose the RGB values)  
• Corresponding RGB value is checked, if the value is even, then the binary 
bit is 0 otherwise 1.  
• The bits are concatenated to a string, and with every three pixels, we get 
a byte of secret data, which means one character.  
• Now, if the ninth value is even then we keep reading pixels three at a 
time, or otherwise, we stop  


**Steps to Execute the Code in Colab:**

1. Save both the images (greyscale and Colored) in Google Drive, Save them 
under default MyDrive folder.  
Name them as following:  
Greyscale Image: Cover_1.png  
Colored Image: Cover_2.png  
2. Run the code in Colab, It will ask for input (1 or 2)  
1 for choosing Greyscale Image, 2 for the color image.  
3. Enter Secret Messsage  
4. After the execution finishes, extracted date will be printed on the screen 
and both the original image and colored image will also be shown.
