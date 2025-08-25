from hub import light_matrix, motion_sensor, port
import motor_pair
import runloop
import math
import motor

SPEED = 90

PROGRAM_NUMBER = 1

async def main():
    robot = jones()
    robot.reset_angle()
    front_motor = port.F
    back_motor = port.D
    
    if PROGRAM_NUMBER == 1:
        await pickaxe(robot, front_motor)
    
async def pickaxe(robot, attachment_motor2):
    await robot.drive_forward(43)
    await motor.run_for_degrees(attachment_motor2, 70, 910)
    await wait_for_seconds(1)
    await robot.turn_left(30)
    await robot.drive_backward(17)
    await robot.turn_left(30)
    await motor_pair.move_for_degrees(robot.motor_pair, 300, 0, velocity = 1500)
    await robot.drive_backward(13)
    await robot.turn_left(10)
    await robot.drive_backward(13)
    await robot.turn_left(15)
    await robot.drive_backward(33)
    await robot.turn_left(50)

async def wait_for_seconds(s):
    await runloop.sleep_ms(s*1000)

class jones:
    def __init__(self):
        self.wheel_diameter = 5.5 # cm
        # driving motors
        self.left_motor = port.A
        self.right_motor = port.B
        self.motor_pair = motor_pair.PAIR_1
        motor_pair.pair(self.motor_pair, self.left_motor, self.right_motor)

     def show_state(self):
        print("current angle: {} / angle goal: {}".format(self.get_yaw(), self.angle_goal))

     # drive_forward tells the robot to drive in a
    # straight line "distance" centimeters forwards.
    async def drive_forward(self, distance, speed = SPEED):
        distance_in_degrees = distance * (360.0 / (self.wheel_diameter * math.pi))
        start_position = motor.relative_position(self.right_motor)
        goal_position = start_position + distance_in_degrees
        small_goal = goal_position - 7 * (360.0 / (self.wheel_diameter * math.pi))
        while motor.relative_position(self.right_motor) < small_goal:
            motor_pair.move(self.motor_pair, self.correction(),velocity = speed*10)
        while motor.relative_position(self.right_motor) < goal_position:
            motor_pair.move(self.motor_pair, self.correction(),velocity = 100)
        motor_pair.stop(self.motor_pair)

    async def drive_backward(self, distance, speed = SPEED):
        # convert distance (centimeters) to degrees
        distance_in_degrees = distance * (360.0 / (self.wheel_diameter * math.pi))
        start_position = motor.relative_position(self.right_motor)
        goal_position = start_position - distance_in_degrees
        # plus sign before the seven used to be a minus sign
        small_goal = goal_position + 7 * (360.0 / (self.wheel_diameter * math.pi))
        while motor.relative_position(self.right_motor) > small_goal:
            motor_pair.move(self.motor_pair, -self.correction(),velocity = -speed*10)
        while motor.relative_position(self.right_motor) > goal_position:
            motor_pair.move(self.motor_pair, -self.correction(),velocity = -100)
        motor_pair.stop(self.motor_pair)

    async def turn_left(self, degrees, speed = 25):
        if speed>50:
            speed = 50
        self.angle_goal = self.angle_goal + degrees
        small_goal = self.angle_goal - 20
        motor_pair.move_tank(self.motor_pair, -speed*10, speed*10)
        while self.get_yaw()<small_goal:
            # wait
            True
        motor_pair.move_tank(self.motor_pair, -100, 100)
        while self.get_yaw()<self.angle_goal:
            True
        motor_pair.stop(self.motor_pair)

    async def turn_right(self, degrees, speed = 25):
        if speed>50:
            speed = 50
        self.angle_goal = self.angle_goal - degrees
        small_goal = self.angle_goal + 20
        motor_pair.move_tank(self.motor_pair, speed*10, -speed*10)
        while self.get_yaw()>small_goal:
            # wait
            True
        motor_pair.move_tank(self.motor_pair, 100, -100)
        while self.get_yaw()>self.angle_goal:
            True
        motor_pair.stop(self.motor_pair)
    
    def correction(self):
        correction = self.get_yaw() - self.angle_goal
        correction *= 5
        if correction < -50:
            correction = -50
        if correction > 50:
            correction = 50
        return int(correction)

    # reset_angle tells the robot that it is currently facing
    # the right direction. Call this at the beginning of each
    # program and after the robot squares itself up on an
    # object.
    def reset_angle(self):
        self.angle_goal = 0
        motion_sensor.reset_yaw(0)

    def get_yaw(self):
        yaw, _, _ = motion_sensor.tilt_angles()
        return yaw/10

runloop.run(main())