int PinSinal = 2;
int i=0;
int PWM = 7;
int PinCtrl = 3;
int PinEN1 = 6;
int PinEN2 = 5;
float pot = 60; //Potência do motor em porcentagem
float cycleduty = (pot/100)*255;
float pi = 3.141520;

 long tf, ti=0;
float RPMmedido;

void setup() {
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(PinSinal), contagem, RISING);

}

void loop() {
  digitalWrite(PinEN1, HIGH);
  digitalWrite(PinEN2, LOW);
  analogWrite(PWM,cycleduty);   
}

void contagem() {
  
  tf = micros();
  long delta = tf - ti;

  RPMmedido = (60 / (348*(float(delta) / 1000000.0)));

  ti = tf;
  //Serial.println(i);
  if (i > 20000){
    //Serial.println('12000');
  }
  else{
    i++;
    Serial.print(delta);
    Serial.print(';');
    Serial.print(cycleduty);
    Serial.print(';');
    Serial.println(RPMmedido);
  }


}