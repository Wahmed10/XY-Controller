import math

class Stepper(QWidget):
    def __init__(self, motor):
        self.motor = motor
        self.stepDirection = stepper.FORWARD
        self.currentPos = 0
        self.num_micro_step = 0
        self.num_single_step = 0

    def forward(self):
        self.stepDirection = stepper.FORWARD
        print("Forward Mode")

    def reverse(self):
        self.stepDirection = stepper.BACKWARD
        print("Reverse Mode")

    def function_before_move(self, steps):
        self.num_micro_step = steps % 16
        self.num_single_step = math.floor(steps / 16)
        if num_single_step > 0:
            self.move(num_single_step, self.stepDirection, stepper.SINGLE)
        if num_micro_step > 0:
            self.move(num_micro_step, self.stepDirection, stepper.MICROSTEP)

    def move(self, steps, direction, style):
        for i in range(steps):
            QTimer.singleShot(10, lambda: self.motor.onestep(direction=direction, style=style))
            if self.stepDirection == stepper.FORWARD:
                self.currentPos += 1
            else:
                self.currentPos -= 1

    def reset(self):
        self.currentPos = 0

    def auto_move(self, target_steps):
        num_micro_target_steps = target_steps % 16
        num_single_target_steps = math.floor(target_steps / 16)

        micro_moving_steps = self.num_micro_step - num_micro_target_steps
        single_moving_steps = self.num_single_step - num_single_target_steps

        newPos = micro_moving_steps + single_moving_steps
        if newPos > self.currentPos:
            self.stepDirection = stepper.FORWARD
        else:
            self.stepDirection = stepper.BACKWARD

        self.move(single_moving_steps, self.stepDirection, stepper.SINGLE)
        self.move(micro_moving_steps, self.stepDirection, stepper.MICROSTEP)
