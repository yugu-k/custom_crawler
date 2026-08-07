#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
import numpy as np

class KinematicController(Node):
    def __init__(self):
        super().__init__("kinematic_controller")

        self.declare_parameter("wheel_radius", 0.060)
        self.declare_parameter("wheel_separation",0.330)

        self.wheel_radius_ = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_separation_ = self.get_parameter("wheel_separation").get_parameter_value().double_value

        self.get_logger().info("using wheel_radius %f " %self.wheel_radius_)
        self.get_logger().info("using wheel_separation %f " %self.wheel_separation_)

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "simple_velocity_controller/commands", 10)
        self.vel_sub_ = self.create_subscription(TwistStamped, "crawler_controller/cmd_vel", self.velCallback, 10)

        self.speed_conversion_ = np.array([
            [1/self.wheel_radius_,  self.wheel_separation_/(2*self.wheel_radius_)],  
            [1/self.wheel_radius_,  self.wheel_separation_/(2*self.wheel_radius_)],  
            [1/self.wheel_radius_, -self.wheel_separation_/(2*self.wheel_radius_)],  
            [1/self.wheel_radius_, -self.wheel_separation_/(2*self.wheel_radius_)]
        ])

        self.get_logger().info("The conversion matrix is %s" %self.speed_conversion_)

    def velCallback(self, msg):
        robot_speed = np.array([[msg.twist.linear.x],
                                [msg.twist.angular.z]])

        wheel_speed = np.matmul(self.speed_conversion_,robot_speed)
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [wheel_speed[0,0], wheel_speed[2,0], wheel_speed[1,0], wheel_speed[3,0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

def main():
    rclpy.init()
    kinematic_controller = KinematicController()
    rclpy.spin(kinematic_controller)
    kinematic_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()