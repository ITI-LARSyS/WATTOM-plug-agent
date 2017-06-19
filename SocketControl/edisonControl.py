from SocketControl.socketControl import SocketControl
from LEDFeedback.addressableLed import AddressableLedController
from libs.Spark_ADC import Adc
import mraa


class EdisonControl(SocketControl):
    def __init__(self, voltage):
        super().__init__(voltage)
        self.adc = Adc()
        self.voltage = voltage
        self.initialize_adc()
        self.relay = mraa.Gpio(37)
        self.relay.dir(mraa.DIR_OUT)
        self.ledControl = AddressableLedController()

    def change_relay(self, state):
        self.relay.write(state)
        AddressableLedController().change_relay_state(state)

    def initialize_relay(self, state):
        self.relay.write(state)
        # self.ledController.changeRelayState(1)

    def calibrate(self):
        average_voltage = 0
        for i in range(5000):
            average_voltage += self.adc.adc_read()
        average_voltage /= 5000
        return round(average_voltage)

    def initialize_adc(self):
        ain0_operational_status = 0b0
        ain0_input_multiplexer_configuration = 0b100
        ain0_programmable_gain_amplifier_configuration = 0b001
        ain0_device_operating_mode = 0b0
        ain0_data_rate = 0b100
        ain0_comparator_mode = 0b0
        ain0_compulator_polarity = 0b0
        ain0_latching_comparator = 0b0
        ain0_comparator_queue_and_disable = 0b11

        self.adc.set_config_command(
            ain0_operational_status,
            ain0_input_multiplexer_configuration,
            ain0_programmable_gain_amplifier_configuration,
            ain0_device_operating_mode,
            ain0_data_rate,
            ain0_comparator_mode,
            ain0_compulator_polarity,
            ain0_latching_comparator,
            ain0_comparator_queue_and_disable
        )
