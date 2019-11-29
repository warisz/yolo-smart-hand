//L293D + Serial YOLO hand

char data;

//Motor A
const int motorPin1  = 5; 
const int motorPin2  = 6; 
//Motor B
const int motorPin3  = 10;
const int motorPin4  = 9;   

int trigPin = 11;    // Trigger
int echoPin = 3;    // Echo
int time;
int distance;

//This will run only one time.
void setup(){
    Serial.begin(9600);
    //Set pins as outputs
    pinMode(motorPin1, OUTPUT);
    pinMode(motorPin2, OUTPUT);
    pinMode(motorPin3, OUTPUT);
    pinMode(motorPin4, OUTPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);

}


void loop(){
  if (Serial.available() > 0) {

    data = Serial.read();
      if(data == 'a'){
        //Forwards
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, HIGH);
        
      }else if(data == 'b'){
        //Backwards
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, HIGH);
        digitalWrite(motorPin3, HIGH);
        digitalWrite(motorPin4, LOW);
        
      }else if(data == 'c'){
        //Stop
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, LOW);
      }

    }
    digitalWrite (trigPin, HIGH);
    delayMicroseconds (10);
    digitalWrite (trigPin, LOW);
    time = pulseIn (echoPin, HIGH);
    distance = (time * 0.034) / 2;
    
    Serial.print(distance);
    Serial.println();
  
  delay(250);
}
