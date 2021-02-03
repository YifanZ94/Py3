/*  
 *  How I2C Communication Protocol Works - Arduino I2C Tutorial
 *  
 *   by Dejan, www.HowToMechatronics.com 
 *   
 */
#include <Wire.h>
int ADXLAddress = 0x30; // Device address in which is also included the 8th bit for selecting the mode, read in this case.
#define X_Axis_Register_DATAX0 0x00 // Hexadecima address for the DATAX0 internal register.
#define X_Axis_Register_DATAX1 0x01 // Hexadecima address for the DATAX1 internal register.
#define ORD 0x1a
#define Inter_control_0 0x1b
#define Inter_control_1 0x1C
#define Inter_control_2 0x1d  
 
byte X0,X1;
unsigned int r;
double Gauss;

void setup() {
  Wire.begin(); // Initiate the Wire library
  Serial.begin(9600);
  delay(100);
  
  Wire.beginTransmission(ADXLAddress); // Begin transmission to the Sensor 
  Wire.write(ORD);
  Wire.write(50);
  Wire.endTransmission();
  
  Wire.beginTransmission(ADXLAddress); // Begin transmission to the Sensor 
  Wire.write(Inter_control_0);
  Wire.write(B10000000);
  Wire.endTransmission();

  Wire.beginTransmission(ADXLAddress); // Begin transmission to the Sensor 
  Wire.write(Inter_control_2);
  Wire.write(B00010000);
  Wire.endTransmission();

}

void loop() {

  Wire.beginTransmission(ADXLAddress); 
  Wire.write(X_Axis_Register_DATAX0);
  Wire.write(X_Axis_Register_DATAX1);
  
  Wire.endTransmission(); // Ends the transmission and transmits the data from the two registers
  
  Wire.requestFrom(ADXLAddress,2);// Request the transmitted two bytes from the two registers
  
  //numbyte = Wire.available(); // The number of bytes to be retrieved
  //Serial.print("byte available is ");
  //Serial.println(numbyte);
  
  if(Wire.available()<=2) {  // 
    X0 = Wire.read(); // Reads the data from the register
    X1 = Wire.read(); // every read() only takes one byte  
  }

  r = (X0 << 8) + X1;
  Gauss = (r/(65536.0) - 0.5)*60.0;
  // 2^16 = 65536  30*1024*2 = 61440
  
  Serial.print("X0= ");
  Serial.print(X0);
  Serial.print("   X1= ");
  Serial.println(X1);
  //Serial.print("r = ");
  //Serial.println(r);
  Serial.print("Gauss = ");
  Serial.println(Gauss);
  Serial.println("");
}
