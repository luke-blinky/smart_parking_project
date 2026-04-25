#include "rc522.h"

MFRC522 rfid(SS_PIN, RST_PIN);

// HARDCODE   
const char* mockDatabaseJSON = R"(
{
  "922B6D06": {
    "role": "university_member",
    "balance": 50000,
    "entry_time": "08:00",
    "exit_time": ""
  },
  "F1234567": {
    "role": "university_member",
    "balance": 15000,
    "entry_time": "09:00",
    "exit_time": ""
  }
}
)";

//Convert byte UID -> string (to compare with JSON) 
//[0xE3, 0xA1, 0xB2, 0xC4]  → "E3A1B2C4"
String getUIDString(byte *uid, byte uidSize) {
  String uidStr = "";
  for (byte i = 0; i < uidSize; i++) {
    if (uid[i] < 0x10) uidStr += "0";
    uidStr += String(uid[i], HEX);
  }
  uidStr.toUpperCase();
  return uidStr;
}

void rfid_reader( void*pvParameters){
    SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, SS_PIN);

    // Parse JSON -> ez for access
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, mockDatabaseJSON);

    while(1){
      rfid.PCD_Init();

      if(rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()){
        String scannedUID = getUIDString(rfid.uid.uidByte, rfid.uid.size);
        Serial.println(scannedUID);
        
        //Check in database
        if (doc.containsKey(scannedUID)) {
          String role = doc[scannedUID]["role"];
          // int balance = doc[scannedUID]["balance"];
                
          if (role == "university_member") {
            Serial.println("UNIVERSITY MEMBER");
            xSemaphoreGive(xGateSemaphore);
            // Serial.printf("=> So du hien tai: %d VND\n", balance);
                    
            // if (balance > 0) {
            //   Serial.println("=> Xac nhan mo cong!");
            //     // TODO: Gửi tín hiệu (Semaphore/Queue) qua cho task Servo
            // } else {
            //   Serial.println("=> So du khong du, tu choi mo cong.");
            // }
          }
        } else {
          Serial.println("=> Loai khach: VISITOR");
          Serial.println("=> Yeu cau cap the khach hoac mua ve.");
        }
        Serial.println("==================================");

        // Delay 1,5s to avoid scan 1 card many times
        rfid.PICC_HaltA();            // Incicate the card to HALT state 
        rfid.PCD_StopCrypto1();       // Stop encrypte
        vTaskDelay(1500 / portTICK_PERIOD_MS); 
      }
    } 
}