#include "tcrt5k.h"
#include "lcd.h"

bool last_state = HIGH;

void tcrt( void*pvParameters){
    pinMode(TCRT_PIN, INPUT);
    lcd_init();

    while(1){
        bool current_state = digitalRead(TCRT_PIN);

        if(current_state != last_state){
            if(current_state == LOW){
                if(empty > 0){
                    empty--;
                    lcd_display();
                }
            }
        }

        last_state = current_state;
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}