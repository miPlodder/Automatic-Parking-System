# Automatic Parking System

This project provides user an easy way of booking the parking slots through an application and onspot slot booking based on availability of slots. This project will provide the easy reservation online system for parking.

#### Demo Video [(Link)](https://www.youtube.com/watch?v=SRRTxn5QCrg)

Below are the steps on working of this Parking System,

### Steps-1) 

User can book any vacant slot from Android App, the LED for that slot will be ON and changes will reflected on the firebase console. (Assume Slot-2 is booked)

### Step-2) 

When user presses the OPEN GATE button from the Android App, the gates open and changes are reflected on Firebase Console.

### Step-3)

When car is inside the Parking Spot, the IR sensor senses it's presence, and the gate is closed.

### Step-4)

Now, the car is parked and user is not in car.

### Step-5) 

User now have to exit the parking slot, it's done via Android App. User pays the amount via Android App.

### Step-6)

Gate for that slot opens and car leaves the slot. Now, when the car leaves the slot. IR sensor sense car's absence and closes the gate automatically based on its value changes.

### Step-7)

Now, no slot is booked and other user can book slot 2 also, as its vacant.