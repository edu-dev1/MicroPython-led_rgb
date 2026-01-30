'''Librería para el led rgb'''
from machine import Pin, PWM

class LedRGB:
    __led_rgb_counter = 0
    __led_list = []
    def __init__(self, R:int, G:int, B:int, common_anode:bool = True):
        '''Una clase para el LED RGB.\n
        Los argumentos son los pines de las respectivas salidas del LED `R`, `G`, `B`.\n
        El argumento `common_anode` indica si el led es ánodo común (True) o cátodo común (False).\n
        Funciones extra para los objetos LedRGB:
        >>> \tall_leds_rgb_off()'''

        LedRGB.__led_rgb_counter += 1
        LedRGB.__led_list.append(self)

        self.__r_pin = R
        self.__g_pin = G
        self.__b_pin = B
        
        self.__common_anode = common_anode
        self.__state_on, self.__state_off = (0, 1) if self.__common_anode else (1, 0)
        self.__digital_mode = True
    
    def __str__(self) -> str:
        return 'Led RGB.'
    
    @classmethod
    def __total_leds_rgb__(cls) -> int:
        return cls.__led_rgb_counter
    
    def __get_digital_led(self) -> tuple[Pin, Pin, Pin]:
        self.__digital_mode =  True
        digital_R = Pin(self.__r_pin, Pin.OUT)
        digital_G = Pin(self.__g_pin, Pin.OUT)
        digital_B = Pin(self.__b_pin, Pin.OUT)
        return digital_R, digital_G, digital_B
        
    def __get_analog_led(self) -> tuple[PWM, PWM, PWM]:
        self.__digital_mode = False
        analog_R = PWM(Pin(self.__r_pin), freq = 1000)
        analog_G = PWM(Pin(self.__g_pin), freq = 1000)
        analog_B = PWM(Pin(self.__b_pin), freq = 1000)
        return analog_R, analog_G, analog_B

    def red(self) -> None:
        '''Enciende color rojo el led rgb.'''
        r, g, b = self.__get_digital_led()
        r.value(self.__state_on)
        g.value(self.__state_off)
        b.value(self.__state_off)

    def green(self) -> None:
        '''Enciende color verde el led rgb.'''
        r, g, b = self.__get_digital_led()
        r.value(self.__state_off)
        g.value(self.__state_on)
        b.value(self.__state_off)

    def blue(self) -> None:
        '''Enciende color azul el led rgb.'''
    
        r, g, b = self.__get_digital_led()
        r.value(self.__state_off)
        g.value(self.__state_off)
        b.value(self.__state_on)

    def white(self) -> None:
        '''Enciende color blanco el led rgb.'''
        
        r, g, b = self.__get_digital_led()
        r.value(self.__state_on)
        g.value(self.__state_on)
        b.value(self.__state_on)
    
    def set_color(self, r:int, g:int, b:int) -> None:
        '''Enciende color personalizado.\n
        Args:
            `r`: rango del 0-255 (int)
            `g`: rango del 0-255 (int)
            `b`: rango del 0-255 (int)'''
        if any((color < 0 or color > 255) for color in [r, g, b]):
            raise ValueError("Sólo rangos de color entre 0 a 255.")
        r_pwm, g_pwm, b_pwm = self.__get_analog_led()
        if self.__common_anode:
            r_pwm.duty_u16(65535 - int(r * 65535))
            g_pwm.duty_u16(65535 - int(g * 65535))
            b_pwm.duty_u16(65535 - int(b * 65535))
        else:
            r_pwm.duty_u16(int(r * 65535))
            g_pwm.duty_u16(int(g * 65535))
            b_pwm.duty_u16(int(b * 65535))

    def rgb_off(self) -> None:
        '''Apaga el led rgb.'''
        if self.__digital_mode:
            r, g, b = self.__get_digital_led()
            r.value(self.__state_off)
            g.value(self.__state_off)
            b.value(self.__state_off)
        else:
            r_pwm, g_pwm, b_pwm = self.__get_analog_led()
            __off = 65535 if self.__common_anode else 0
            r_pwm.duty_u16(__off)
            g_pwm.duty_u16(__off)
            b_pwm.duty_u16(int(__off))

def all_leds_rgb_off():
    '''Apaga todos los led's rgb.\n
       Raises:
            RuntimeError: Si no hay objectos LedRGB creados.'''
    for led_rgb in LedRGB.__led_list:
        led_rgb.rgb_off()

if __name__ == '__main__':
    from time import sleep_ms
    r = 2
    g = 1
    b = 0

    led = LedRGB(r, g, b, True)
    colors = {'White':(255, 255, 255), 'Silver':(192, 192, 192), 'Gray':(128, 128, 128), 'Black':(0, 0, 0),
              'Red':(255, 0, 0), 'Maroon':(128, 0, 0), 'Yellow':(255, 255, 0), 'Olive':(128, 128, 0), 'Lime':(0, 255, 0),
              'Green':(0, 128, 0), 'Aqua':(0, 255, 255), 'Teal':(0, 128, 128), 'Blue':(0, 0, 255), 'Navy':(0, 0, 128),
              'Fuchsia':(255, 0, 255), 'Purple':(128, 0, 128)}
    try:
        while True:
            
            led.blue()
            print('Blue\n')
            sleep_ms(1000)

            for name_color, rgb in colors.items():
                led.set_color(rgb[0], rgb[1], rgb[2])
                print(name_color, end = ' ')
                sleep_ms(1000)
            print('\n')

            led.red()
            sleep_ms(500)
            led.green()
            sleep_ms(500)
            led.blue()
            sleep_ms(500)
            led.white()
            sleep_ms(500)

    except KeyboardInterrupt:

        led.rgb_off()
