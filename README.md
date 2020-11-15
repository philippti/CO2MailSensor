<h1> CO2 Sensor with mail-trigger on a Raspberry Pi </h1>

<h2> Implementation of a triggered eMail client for reading CO2 concentration in a room </h2>
<hr/>

This code was written for the "Introduction to Programming" lecture at the DHBW Lörrach.

The programm will monitor a given mailbox for incoming mail. An answer will be sent with <br/>
the readout of the CCS811 TVOC (total volatile organic compounds) and the calculated equivalent <br/> 
CO2 value as well as the temperature. Optional is the use as a warning system in case the concentration <br/> 
of CO2 in the room gets too high. High carbon dioxide levels influence cognitive funcion: <br/>
[https://ehp.niehs.nih.gov/doi/full/10.1289/ehp.1510037] <br/>

A Raspberry Pi model 2 B+ was used to connect to the sensor breakout board via jumper cables. <br/>
The code runs on the pi via a cronjob.



