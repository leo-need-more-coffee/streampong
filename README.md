# streampong  

Pong, visualized in a single HTTP stream. This means you can run and control the game directly from the terminal. All you need is **one command** to watch the game and **one command** to control it.  

---

## Running the Game  

### 1. Watching the Game  
To watch the game, simply run:  
```bash
curl http://$SERVER_IP/
```  
Replace `$SERVER_IP` with the server’s IP address and port (e.g., `localhost:8000`).  

---

### 2. Controlling the Game  
You can control the game using **a single command** that launches a script.  

#### Install `evtest` (if not installed yet):  
```bash
sudo apt-get install evtest
```  

#### Run the control script in one command:  
Copy and paste the following command into the terminal, replacing the values accordingly:  
```bash
KEYBOARD_ID=2 SERVER_IP="localhost:8000" PLAYER_ID=2 KEY_UP="d0" KEY_DOWN="d1" bash -c 'declare -A key_map; key_map["$KEY_UP"]="up"; key_map["$KEY_DOWN"]="down"; while true; do key_code=$(sudo evtest /dev/input/event$KEYBOARD_ID | grep -m 1 "MSC_SCAN" | awk '\''{print $8}'\''); if [ -n "$key_code" ]; then action=${key_map["$key_code"]}; if [ -n "$action" ]; then curl -s "http://$SERVER_IP/move/$PLAYER_ID/$action" > /dev/null; fi; fi; sleep 0.001; done'
```  

---

### What to Replace:  
1. **`KEYBOARD_ID`**: Replace with your keyboard’s ID. To find it, run:  
   ```bash
   sudo evtest
   ```  
   Select the device corresponding to your keyboard and note its number (e.g., `2` for `/dev/input/event2`).  

2. **`SERVER_IP`**: Replace with the server’s IP address and port (e.g., `localhost:8000`).  

3. **`PLAYER_ID`**: Set the player ID you want to control. Usually `1` or `2`.  

4. **`KEY_UP` and `KEY_DOWN`**: Replace with the key codes you want to use for control. For example:  
   - If the "Up" key has the code `d0`, set `KEY_UP="d0"`.  
   - If the "Down" key has the code `d1`, set `KEY_DOWN="d1"`.  

---

### How It Works:  
- The script reads keyboard key presses using the `MSC_SCAN` code from `evtest`.  
- If a specified key is pressed, it sends an HTTP request to the server to control the player with the given `PLAYER_ID`.  
- You can watch the game in real time by running `curl http://$SERVER_IP/`.  

---

## Running the Game and Controls in a Single Command  
You can **watch the game and control it** in one terminal using a single command:  

```bash
( curl http://$SERVER_IP/ & ) | ( KEYBOARD_ID=2 SERVER_IP="localhost:8000" PLAYER_ID=2 KEY_UP="d0" KEY_DOWN="d1" bash -c 'declare -A key_map; key_map["$KEY_UP"]="up"; key_map["$KEY_DOWN"]="down"; while true; do key_code=$(sudo evtest /dev/input/event$KEYBOARD_ID | grep -m 1 "MSC_SCAN" | awk '\''{print $8}'\''); if [ -n "$key_code" ]; then action=${key_map["$key_code"]}; if [ -n "$action" ]; then curl -s "http://$SERVER_IP/move/$PLAYER_ID/$action" > /dev/null; fi; fi; sleep 0.001; done' )
```  

Now you can **watch and control the game simultaneously**, using just **one command** in the terminal! 🚀  

---

## Example Usage  
1. Open the first terminal and start watching the game:  
   ```bash
   curl http://localhost:8000/
   ```  

2. Open a second terminal and start controlling the game:  
   ```bash
   KEYBOARD_ID=2 SERVER_IP="localhost:8000" PLAYER_ID=2 KEY_UP="d0" KEY_DOWN="d1" bash -c 'declare -A key_map; key_map["$KEY_UP"]="up"; key_map["$KEY_DOWN"]="down"; while true; do key_code=$(sudo evtest /dev/input/event$KEYBOARD_ID | grep -m 1 "MSC_SCAN" | awk '\''{print $8}'\''); if [ -n "$key_code" ]; then action=${key_map["$key_code"]}; if [ -n "$action" ]; then curl -s "http://$SERVER_IP/move/$PLAYER_ID/$action" > /dev/null; fi; fi; sleep 0.001; done'
   ```  

3. Or, launch both the game and controls **with a single command** in one terminal:  
   ```bash
   ( curl http://localhost:8000/ & ) | ( KEYBOARD_ID=2 SERVER_IP="localhost:8000" PLAYER_ID=2 KEY_UP="d0" KEY_DOWN="d1" bash -c 'declare -A key_map; key_map["$KEY_UP"]="up"; key_map["$KEY_DOWN"]="down"; while true; do key_code=$(sudo evtest /dev/input/event$KEYBOARD_ID | grep -m 1 "MSC_SCAN" | awk '\''{print $8}'\''); if [ -n "$key_code" ]; then action=${key_map["$key_code"]}; if [ -n "$action" ]; then curl -s "http://$SERVER_IP/move/$PLAYER_ID/$action" > /dev/null; fi; fi; sleep 0.001; done' )
   ```  

Now you can control player `2` using keys `d0` (up) and `d1` (down) while watching the game in real time. 🎮  

---

## Notes  
- If you don’t have permission to read the input device, run the command with `sudo`.  
- If the server is behind a NAT or firewall, make sure the port is open for external connections.


# How to run server
```
pip install aiohttp
python server.py
```