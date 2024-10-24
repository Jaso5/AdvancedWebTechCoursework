# Notes

## Site

### What to monitor and display (ordered by importance, grouped by section)

- Camera

```html
<img id="stream" data-v-04dce43b="" src="http://voron24.hacklab/webcam/?action=stream" class="camera-image">

<!-- https://stackoverflow.com/a/70672203 -->
<script>
      let image = document.getElementById('stream');

      async function check() {
        while (true) {
          try {
            await image.decode();
          } catch {
            let src = image.src;
            image.src = ""; // Should set this to an image saying that the camera is down
            image.src = src;
          }

          await new Promise((resolve) => setTimeout(resolve, 5000));
        }
      }

      check();
</script>
```

- Printing time elapsed, predicted time remaining, file currently printing, paused state
  - Paused state: <https://www.klipper3d.org/Status_Reference.html#pause_resume>
  - Everything else: <https://www.klipper3d.org/Status_Reference.html#print_stats>
  - Might be better for info about current file: <https://www.klipper3d.org/Status_Reference.html#virtual_sdcard>
  - Thumbnails can be in the printer fata folder eg: `jacob/cone.N=0.4.gcode` => `jacob/.thumbs/cone.N=0.4-<SIZE>.png` where size is `32x32`, `64x64` or `400x300` (Configured in prusaslicer, these are the sizes I have by default)
    - Gcodes are hosted here: <http://voron24.hacklab/server/files/gcodes/>
- Feedrate, speed+acceleration, stalls?
  - Klipper-side limits: <https://www.klipper3d.org/Status_Reference.html#toolhead>
- Thermals graphed
  - Generic: <https://www.klipper3d.org/Status_Reference.html#temperature_sensor>
  - BME280 (Although relies on the sensor not actually crashing the printer for once): <https://www.klipper3d.org/Status_Reference.html#temperature-sensors>
  - TMC driver temps? We should probably just stick these in a table: <https://www.klipper3d.org/Status_Reference.html#tmc-drivers>, <https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.08.pdf> section 15.1


#### Additional status

- Console log
- Monitor throttling and display a warning?: <https://moonraker.readthedocs.io/en/latest/web_api/#get-moonraker-process-stats>

### Interactibles

- Estop: <https://moonraker.readthedocs.io/en/latest/web_api/#emergency-stop>
  - Might be worth giving a physical button hooked up to the pi? Also def worth adding one to the printer itself...
- light
  - <https://moonraker.readthedocs.io/en/latest/web_api/#run-a-gcode>
  - Gcode: `SET_FAN_SPEED FAN=caselight SPEED=0.5` (Maybe I should stop running my lights as a fan and use the actual lighting object)

### Possible enhancements

- Button for toggling the internal lights
- Gcode viewer
- Object exclude
- Some kind of power savings so when the display is on a different page, we aren't performing requests or updating the camera stream

## Sources

- Display Software: <https://github.com/dylan-thinnes/hacklab-status-screen>
- API:
  - Retrieve Klipper Objects: <https://moonraker.readthedocs.io/en/latest/web_api/#query-printer-object-status>
    - Object listing: <https://www.klipper3d.org/Status_Reference.html>

## Serverside

### Moonraker

- Connect via http, json-RPC or websocket
  - I'd prefer json-RPC, WS might be better for constant polling though?
    - Maybe best to implement a generic interface and I can swap implementations based off testing or something
- Connect, grab printer status as we wish and forward it over to the clientside
- Connect to MQTT for playing noises when a print finishes
  - MQTT: <https://pypi.org/project/paho-mqtt/>
  - Noise maker: <https://wiki.ehlab.uk/squawk>

### Security Concerns

- This will require an API key, and because the display board pi is free to access by any member, I should create a seperate account and API key for it.