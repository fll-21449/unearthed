async def bulldozer(robot, front_motor):
    await robot.drive_forward(51)
    await robot.turn_right(50)
    await robot.drive_forward(30)
    await motor.run_for_time(front_motor, 15000, 1110)
    return
    await robot.drive_backward(9)
    await robot.turn_right(90)
    await robot.drive_forward(15)
    await robot.turn_left(5)
