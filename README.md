<h1> CO2 Sensor with mail-trigger on a Raspberry Pi </h1>

<h2> Implementation of a triggered eMail client for reading CO2 concentration in a room </h2>

This code was written for the "Introduction to Programming" lecture at the DHBW Lörrach.

The programm will monitor a given mailbox for incoming mail. An answer will be sent with 
the readout of the CCS811 TVOC (total volatile organic compounds) and the calculated equivalent <
CO2 value as well as the temperature. Optional is the use as a warning system in case the concentration 
of CO2 in the room gets too high. High carbon dioxide levels influence cognitive funcion:<br/>
[https://ehp.niehs.nih.gov/doi/full/10.1289/ehp.1510037] <br/>

A Raspberry Pi model 2 B+ was used to connect to the sensor breakout board via jumper cables. <br/>
The code runs on the pi via a cronjob.

To run the code a dedicated mail address is needed. The code has to be modified to work with the chosen mail provider. Namely the imap and smpt server have to be matched. The mail address and the password have to be adjusted as well.
If a sensor readout is needed, the setup with the CCS811 a Raspberry Pi and the provided Module from Adafruit should work. If a different sensor is used, the sensor readout module has to be modified to get a sensor readout as tuple.
To only check the functionality of the mail answering module, dummy data for the sensor can be generated using the random python module. Or simply text can be the sent with the mail.


