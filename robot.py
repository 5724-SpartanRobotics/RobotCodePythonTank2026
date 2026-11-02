# TODO: insert robot code here
#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import phoenix5
from phoenix5 import WPI_VictorSPX

class MyRobot(wpilib.TimedRobot):
    """
    This is a demo program showing the use of the DifferentialDrive class.
    Runs the motors with split arcade steering and an Xbox controller.
    """

    def robotInit(self):
        """Robot initialization function"""

        self.leftMotor1 = phoenix5.WPI_VictorSPX(1)
        self.leftMotor2 = phoenix5.WPI_VictorSPX(2)
        self.rightMotor1 = phoenix5.WPI_VictorSPX(3)
        self.rightMotor2 = phoenix5.WPI_VictorSPX(4)

        self.leftMotor2.follow(self.leftMotor1)
        self.rightMotor2.follow(self.rightMotor1)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotor1, self.rightMotor1)
        self.driverController = wpilib.XboxController(0)

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightMotor1.setInverted(True)

    def teleopPeriodic(self):
        # Drive with split arcade style
        # That means that the Y axis of the left stick moves forward
        # and backward, and the X of the right stick turns left and right.
        self.robotDrive.arcadeDrive(
            -self.driverController.getLeftY(), -self.driverController.getRightX()
        )