package com.example.st.parkingsystem;

import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.support.annotation.NonNull;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.text.SimpleDateFormat;
import java.util.Date;

        import android.content.DialogInterface;
        import android.content.SharedPreferences;
        import android.support.annotation.NonNull;
        import android.support.v7.app.AlertDialog;
        import android.support.v7.app.AppCompatActivity;
        import android.os.Bundle;
        import android.util.Log;
        import android.view.View;
        import android.widget.Button;
        import android.widget.TextView;
        import android.widget.Toast;

        import com.google.firebase.database.DataSnapshot;
        import com.google.firebase.database.DatabaseError;
        import com.google.firebase.database.DatabaseReference;
        import com.google.firebase.database.FirebaseDatabase;
        import com.google.firebase.database.ValueEventListener;

        import java.text.SimpleDateFormat;
        import java.util.Date;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnSlot1, btnSlot2, btnSlot3, btnSlot4;
    Button btnCancel, btnOpenGate, btnExit;

    TextView tvBookingTime, tvSlotBooked, tvBookingDate;

    DatabaseReference mRootRef = FirebaseDatabase.getInstance().getReference();
    DatabaseReference mUserRef = mRootRef.child("User");

    SharedPreferences preferences;
    SharedPreferences.Editor editor;
    Slots slots;

    public static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(com.example.st.parkingsystem.R.layout.activity_main);

        btnSlot1 = findViewById(com.example.st.parkingsystem.R.id.btnSlot1);
        btnSlot2 = findViewById(com.example.st.parkingsystem.R.id.btnSlot2);
        btnSlot3 = findViewById(com.example.st.parkingsystem.R.id.btnSlot3);
        btnSlot4 = findViewById(com.example.st.parkingsystem.R.id.btnSlot4);
        btnCancel = findViewById(com.example.st.parkingsystem.R.id.btnCancel);
        btnExit = findViewById(com.example.st.parkingsystem.R.id.btnExit);
        btnOpenGate = findViewById(com.example.st.parkingsystem.R.id.btnOpenGate);

        tvSlotBooked = findViewById(com.example.st.parkingsystem.R.id.tvSlotBooked);
        tvBookingTime = findViewById(com.example.st.parkingsystem.R.id.tvBookingTime);
        tvBookingDate = findViewById(com.example.st.parkingsystem.R.id.tvBookingDate);

        btnSlot1.setOnClickListener(this);
        btnSlot2.setOnClickListener(this);
        btnSlot3.setOnClickListener(this);
        btnSlot4.setOnClickListener(this);
        btnCancel.setOnClickListener(this);
        btnExit.setOnClickListener(this);
        btnOpenGate.setOnClickListener(this);

        setTitle("Park Sense");

        preferences = getApplicationContext().getSharedPreferences("parking", 0);
        editor = preferences.edit();
        showBookedSlot();

        mUserRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                slots = dataSnapshot.child("1").getValue(Slots.class);
                initializeButtons(slots);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    @Override
    public void onClick(View view) {
        Button btn = findViewById(view.getId());
        boolean upperUI = false;
        String slotId = "";

        switch (btn.getId()) {
            case com.example.st.parkingsystem.R.id.btnSlot1:
                upperUI = true;
                slotId = "Slot 1";
                break;
            case com.example.st.parkingsystem.R.id.btnSlot2:
                upperUI = true;
                slotId = "Slot 2";
                break;
            case com.example.st.parkingsystem.R.id.btnSlot3:
                upperUI = true;
                slotId = "Slot 3";
                break;
            case com.example.st.parkingsystem.R.id.btnSlot4:
                upperUI = true;
                slotId = "Slot 4";
                break;
            case com.example.st.parkingsystem.R.id.btnCancel:
                createPaymentDialog().show();
                break;
            case com.example.st.parkingsystem.R.id.btnExit:
                createPaymentDialog().show();
                break;
            case com.example.st.parkingsystem.R.id.btnOpenGate:
                openGate();
                break;
        }

        if (upperUI) {
            if (preferences.getBoolean("hasBooked", false)) {
                Toast.makeText(this, "You already have booked.", Toast.LENGTH_SHORT).show();
            } else {
                createAlertDialog(btn, slotId).show();
            }
        }

    }

    public void openGate() {
        String slotId = preferences.getString("slotId", "-");

        if (slotId.equals("Slot 1")) {
            slots.slot1.arrived = "1";
        } else if (slotId.equals("Slot 2")) {
            slots.slot2.arrived = "1";
        } else if (slotId.equals("Slot 3")) {
            slots.slot3.arrived = "1";
        } else if (slotId.equals("Slot 4")) {
            slots.slot4.arrived = "1";
        }

        mUserRef.child("1").setValue(slots);
    }

    public AlertDialog createPaymentDialog() {
        String[] endTime = getCurrentTime().split(":");
        String[] startTime = preferences.getString("startTime", "0:0").split(":");

        Integer amount = (Integer.parseInt(endTime[0]) - Integer.parseInt(startTime[0]) + 1) * 20;

        String message = "Total Amount = " + amount;
        AlertDialog.Builder paymentDialogBuilder = new AlertDialog.Builder(this);
        paymentDialogBuilder.setTitle("Payment");
        paymentDialogBuilder.setMessage(message);

        paymentDialogBuilder.setPositiveButton("Pay", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                onPaymentCompleted(preferences.getString("slotId", "-"));
                editor.clear();
                editor.commit();
                showBookedSlot();
            }
        });

        paymentDialogBuilder.setNegativeButton("Cancel", null);
        return paymentDialogBuilder.create();
    }

    public boolean changeEnablibity(String status) {
        if (status.equals("not booked")) {
            return true;
        }
        return false;
    }

    public AlertDialog createAlertDialog(final Button btn, final String slotId) {

        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
        alertDialogBuilder.setTitle("Confirmation");
        alertDialogBuilder.setMessage("Are you sure, you want to book this slot ?");
        alertDialogBuilder.setPositiveButton("Book", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                btn.setEnabled(false);
                btn.setText("booked");

                editor.putBoolean("hasBooked", true);
                editor.putString("slotId", slotId);
                editor.putString("startDate", getCurrentDate());
                editor.putString("startTime", getCurrentTime());
                editor.commit();

                Log.d(TAG, preferences.getBoolean("hasBooked", false) + "");
                Log.d(TAG, preferences.getString("slotId", "no value found"));
                setSlotStatus();
                showBookedSlot();
                mUserRef.child("1").setValue(slots);
                Toast.makeText(MainActivity.this, "Booked Confirmed", Toast.LENGTH_SHORT).show();
            }
        });
        alertDialogBuilder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                Toast.makeText(MainActivity.this, "Booking Cancelled", Toast.LENGTH_SHORT).show();
            }
        });

        return alertDialogBuilder.create();
    }

    public void initializeButtons(Slots slots) {
        btnSlot1.setText(slots.slot1.status);
        btnSlot1.setEnabled(changeEnablibity(slots.slot1.status));
        btnSlot2.setText(slots.slot2.status);
        btnSlot2.setEnabled(changeEnablibity(slots.slot2.status));
        btnSlot3.setText(slots.slot3.status);
        btnSlot3.setEnabled(changeEnablibity(slots.slot3.status));
        btnSlot4.setText(slots.slot4.status);
        btnSlot4.setEnabled(changeEnablibity(slots.slot4.status));

        if (preferences.getBoolean("hasBooked", false)) {
            disableButton();
        }
    }

    // disable buttons of the lower UI
    public void disableButton() {

        String slotId = preferences.getString("slotId", "-");
        if (slotId.equals("Slot 1")) {
            disablingLogic(slots.slot1);
        } else if (slotId.equals("Slot 2")) {
            disablingLogic(slots.slot2);
        } else if (slotId.equals("Slot 3")) {
            disablingLogic(slots.slot3);
        } else if (slotId.equals("Slot 4")) {
            disablingLogic(slots.slot4);
        }
    }

    public void disablingLogic(Slot slot) {
        if (slot.status.equals("booked")) {

            btnCancel.setEnabled(true);
            btnOpenGate.setEnabled(true);
            btnExit.setEnabled(false);

            if (slot.arrived.equals("1")) {
                btnCancel.setEnabled(false);
                btnOpenGate.setEnabled(false);
                btnExit.setEnabled(true);
            }

            if (slot.arrived.equals("2")) {
                btnCancel.setEnabled(false);
                btnOpenGate.setEnabled(false);
                btnExit.setEnabled(true);
            }

            if (slot.exit.equals("1")) {
                btnExit.setEnabled(false);
                btnCancel.setEnabled(false);
                btnOpenGate.setEnabled(false);
            }
        }
    }

    public void setSlotStatus() {
        slots.slot1.status = btnSlot1.getText().toString();
        slots.slot2.status = btnSlot2.getText().toString();
        slots.slot3.status = btnSlot3.getText().toString();
        slots.slot4.status = btnSlot4.getText().toString();
    }

    public void showBookedSlot() {
        if (preferences.getBoolean("hasBooked", false)) {
            tvSlotBooked.setText(preferences.getString("slotId", "-"));
            tvBookingTime.setText(preferences.getString("startTime", "-"));
            tvBookingDate.setText(preferences.getString("startDate", "-"));
        } else {
            tvBookingDate.setText("-");
            tvBookingTime.setText("-");
            tvSlotBooked.setText("-");
        }
    }

    public void onPaymentCompleted(String slotId) {

        Toast.makeText(this, "Payment Completed", Toast.LENGTH_SHORT).show();
        if (slotId.equals("Slot 1")) {
            btnSlot1.setEnabled(true);
            btnSlot1.setText("not booked");
            slots.slot1.status = "not booked";
            slots.slot1.exit = "1";
        } else if (slotId.equals("Slot 2")) {
            btnSlot2.setEnabled(true);
            btnSlot2.setText("not booked");
            slots.slot2.status = "not booked";
            slots.slot2.exit = "1";
        } else if (slotId.equals("Slot 3")) {
            btnSlot3.setEnabled(true);
            btnSlot3.setText("not booked");
            slots.slot3.status = "not booked";
            slots.slot3.exit = "1";
        } else if (slotId.equals("Slot 4")) {
            btnSlot4.setEnabled(true);
            btnSlot4.setText("not booked");
            slots.slot4.status = "not booked";
            slots.slot4.exit = "1";
        }

        btnOpenGate.setEnabled(false);
        btnExit.setEnabled(false);
        btnCancel.setEnabled(false);

        mUserRef.child("1").setValue(slots);
    }

    public String getCurrentDate() {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MMM/yyy");
        String date = sdf.format(new Date());
        return date;
    }

    public String getCurrentTime() {
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm");
        String time = sdf.format(new Date());
        return time;
    }
}