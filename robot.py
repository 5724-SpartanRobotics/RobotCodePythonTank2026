import wpilib
import wpilib.drive
import phoenix5


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """Robot initialization function"""
   
        # Power distribution board
        self.pdp = wpilib.PowerDistribution(0, wpilib.PowerDistribution.ModuleType.kCTRE)

        # Motor stuff
        self.leftMotor1 = phoenix5.WPI_VictorSPX(1)
        self.leftMotor2 = phoenix5.WPI_VictorSPX(2)
        self.rightMotor1 = phoenix5.WPI_VictorSPX(3)
        self.rightMotor2 = phoenix5.WPI_VictorSPX(4)

        self.leftMotor1.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.leftMotor2.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightMotor1.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.rightMotor2.setNeutralMode(phoenix5.NeutralMode.Brake)

        self.leftMotor2.follow(self.leftMotor1)
        self.rightMotor2.follow(self.rightMotor1)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotor1, self.rightMotor1)
        self.driverController = wpilib.XboxController(0)

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightMotor1.setInverted(True)

        # --- LED SETUP ---
        self.led_port = 0
        self.led_length = 200 

        self.led = wpilib.AddressableLED(self.led_port)
        self.led.setLength(self.led_length)
        
        # Create a list of LEDData objects for RobotPy
        self.led_data = [wpilib.AddressableLED.LEDData() for _ in range(self.led_length)]
        
        self.led.setData(self.led_data)
        self.led.start()

        # Tracks the shifting offset for the animated rainbow effect
        self.led_first_pixel_hue = 0
    

    def robotPeriodic(self):
        """Runs periodically regardless of mode (Disabled, Autonomous, Teleop)"""
        # Update and write the rainbow animation to the LED strip
        self.update_rainbow_leds()


    def teleopPeriodic(self):
        # Drive with split arcade style
        # That means that the Y axis of the left stick moves forward
        # and backward, and the X of the right stick turns left and right.
        self.robotDrive.arcadeDrive(
            -self.driverController.getLeftY(), -self.driverController.getRightX()
        )
        
        # Add pdp displays in to smart dashboard
        # Get the total current of all channels.
        totalCurrent = self.pdp.getTotalCurrent()
        wpilib.SmartDashboard.putNumber("Total Current", totalCurrent)

        # Get the total power of all channels.
        totalPower = self.pdp.getTotalPower()
        wpilib.SmartDashboard.putNumber("Total Power", totalPower)

        # Get the total energy of all channels.
        totalEnergy = self.pdp.getTotalEnergy()
        wpilib.SmartDashboard.putNumber("Total Energy", totalEnergy)


    def update_rainbow_leds(self):
        """Fills the LED data array with a shifting rainbow pattern."""
        # Loop through all the pixels in the buffer list
        for i in range(len(self.led_data)):
            # Calculate the hue for each pixel based on strip position and shift offset
            # WPILib HSV hue ranges from 0 to 180
            pixel_hue = (self.led_first_pixel_hue + (i * 180 / len(self.led_data))) % 180
            
            # Set the pixel color using HSV (Hue, Saturation, Value/Brightness)
            # Saturation=255 (vibrant), Value=128 (medium brightness to save power)
            self.led_data[i].setHSV(int(pixel_hue), 255, 255)

        # Increment the starting hue to make the rainbow animate/move over time
        self.led_first_pixel_hue += 3
        # Keep it within bounds (0-180)
        self.led_first_pixel_hue %= 180

        # Output the data list to the physical LED strip
        self.led.setData(self.led_data)