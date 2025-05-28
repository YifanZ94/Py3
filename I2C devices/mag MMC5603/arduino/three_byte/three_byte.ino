/*  
 *  How I2C Communication Protocol Works - Arduino I2C Tutorial
 *  
 *   by Dejan, www.HowToMechatronics.com 
 *   
 */
#include <Wire.h>
int ADXLAddress = 0x30; // Device address in which is also included the 8th bit for selecting the mode, read in this case.
#define X_Axis_Register_DATAX0 0x00 // Y0--0x02    Z0--0x04
#define X_Axis_Register_DATAX1 0x01 // Y1--0x03    Z1--0x05
#define X_Axis_Register_DATAX2 0x06 // Y2--0x07    Z1--0x08
#define Inter_control_0 0x1b 
byte X0,X1,X2;
unsigned int r;
double Gauss;
int bitShift;

void setup() {
  Wire.begin(); // Initiate the Wire library
  Serial.begin(9600);
  delay(100);
}

void loop() {
  Wire.beginTransmission(ADXLAddress); // Begin transmission to the Sensor 
  //Ask the particular registers for data
  Wire.write(Inter_control_0);
  Wire.write(1);
  Wire.endTransmission();
  
  Wire.beginTransmission(ADXLAddress); 
  Wire.write(X_Axis_Register_DATAX0);
  Wire.write(X_Axis_Register_DATAX1);
  Wire.write(X_Axis_Register_DATAX2);
  Wire.endTransmission(); // Ends the transmission and transmits the data from the two registers
  
  Wire.requestFrom(ADXLAddress,3);// Request the transmitted two bytes from the two registers
  
  //numbyte = Wire.available(); // The number of bytes to be retrieved
  //Serial.print("byte available is ");
  //Serial.println(numbyte);
  
  if(Wire.available()<=3) {  // 
    X0 = Wire.read(); // Reads the data from the register
    X1 = Wire.read(); // every read() only takes one byte  
    X2 = Wire.read();
  }

  bitShift = 2;
  r = (X0 << 16 + X1 << 8 + X2) >> 6;
  // + (X2 >> (8-bitShift))
  Gauss = (r/(4*65536.0) - 0.5)*60.0;
  // 2^16 = 65536  30*1024*2 = 61440
  
  Serial.print("X0= ");
  Serial.print(X0);
  Serial.print("   X1= ");
  Serial.print(X1);
  Serial.print("   X2= ");
  Serial.println(X2);
  Serial.print("r = ");
  Serial.println(r);
  Serial.print("Gauss = ");
  Serial.println(Gauss);
  delay(1000);
}
