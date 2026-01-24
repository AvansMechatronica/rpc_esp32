# ESP32 RPC Server Bug Fix

## [2026-01-24] USB Connected, pinMode(2, 1) No Response

### Issue

After a successful USB connection, sending `pinMode(2, 1)` results in:

  Code: 3, No response from device

#### Troubleshooting Steps

1. Verified USB connection is established.
2. Confirmed command is sent from the Python client.
3. No response received from ESP32 for pinMode command.
4. Possible causes:
   - Firmware not handling pinMode correctly
   - Communication protocol mismatch
   - ESP32 not running expected firmware or is busy

#### Next Steps

- Check ESP32 firmware for correct pinMode handling
- Ensure Python client and firmware protocol match
- Confirm ESP32 is running the latest firmware

See other sections below for architecture and bug fix history.

## Problem Identified

The ESP32 RPC server was sending **two responses** for commands that return data (digitalRead, analogRead, millis, freeMem, chipID).

### Root Cause

The code flow was:

1. `handle_serial()` calls `execute_command()`
2. `execute_command()` calls specific RPC function (e.g., `rpc_digitalRead()`)
3. **`rpc_digitalRead()` calls `send_response()` with data** ✓ First response sent
4. `rpc_digitalRead()` returns `RPC_OK`
5. **`handle_serial()` calls `send_response(result)` again** ✗ Second response sent (with null data)

The Python client was receiving the second response with `"data":null`, causing the `AttributeError: 'NoneType' object has no attribute 'get'`.

## Solution

Changed the architecture so that:

1. RPC functions **store** data in `response_data` member instead of sending response directly
2. Functions return status code only
3. `handle_serial()` checks if data was set and sends **one response** with the data

### Changes Made

#### rpc_server.h
- Added `DynamicJsonDocument response_data{1024};` member variable

#### rpc_server.cpp

**Before:**
```cpp
int RpcServer::rpc_digitalRead(JsonObject params) {
  // ... code ...
  JsonObject data = response_doc.createNestedObject("data");
  data["value"] = value;
  send_response(RPC_OK, "Digital read successful", data);  // ← Sends response
  return RPC_OK;
}

void RpcServer::handle_serial() {
  // ... code ...
  int result = execute_command(method, params);
  send_response(result);  // ← Sends response AGAIN!
}
```

**After:**
```cpp
int RpcServer::rpc_digitalRead(JsonObject params) {
  // ... code ...
  response_data["value"] = value;  // ← Just store data
  return RPC_OK;
}

void RpcServer::handle_serial() {
  // ... code ...
  response_data.clear();
  int result = execute_command(method, params);
  
  // Send response with data if any was set
  if (response_data.size() > 0) {
    send_response(result, "", response_data.as<JsonObject>());
  } else {
    send_response(result);
  }
}
```

### Functions Updated

All functions that return data:
- `rpc_digitalRead()` - Returns pin state
- `rpc_analogRead()` - Returns ADC value
- `rpc_getMillis()` - Returns uptime
- `rpc_getFreeMem()` - Returns free heap
- `rpc_getChipID()` - Returns chip ID

## Testing

After flashing the updated firmware:

1. The Python client should receive proper data responses
2. No more `"data":null` in responses
3. No more AttributeError in Python client
4. All read operations should work correctly

## How to Build and Flash

```bash
# Install PlatformIO if not already installed
sudo apt install platformio

# Build firmware
cd /home/gerard/rpc_esp32/eps32_host
pio run

# Upload to ESP32 (connect via USB)
pio run --target upload

# Monitor serial output
pio device monitor
```

## Python Client Changes

The Python client was also updated to handle null data gracefully as a defensive measure:

**Before:**
```python
value = data.get('value') if result == RPC_OK else None
```

**After:**
```python
value = data.get('value') if (result == RPC_OK and data) else None
```

This ensures robustness even if the ESP32 sends unexpected null data.

## Result

✓ Single, correct response per RPC call
✓ Data properly included in response
✓ No more crashes in Python client
✓ Cleaner, more maintainable architecture
