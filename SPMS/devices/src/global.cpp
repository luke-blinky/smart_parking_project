#include "global.h"

SemaphoreHandle_t xGateSemaphore = xSemaphoreCreateBinary();

int total_slots = 50;
int empty = 50;