# neopixel-glasses

http://www.esp8266learning.com/some-neopixel-examples.php

D8 is GPIO15 in microphython. See https://limshankuo.com/d1-wemo-mini/

![](art/test.jpg)

```
import machine, neopixel
np = neopixel.NeoPixel(machine.Pin(15),24)
np[0] = (255,0,0)
np[23] = (0,0,255)
np.write()
```
