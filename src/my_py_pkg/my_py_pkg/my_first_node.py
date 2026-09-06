#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyNode(Node):

    def __init__(self):    #constructor
        super().__init__("py_test")
        self.get_logger().info("Hello World")
        self.create_timer(1.0, self.time_callback)

    def time_callback(self):
        self.get_logger().info("Hello")

def main(args = None):
    rclpy.init(args = args)

    # node = Node("py_test")    #creating a node inside a python file my_first_python.py file
    # node.get_logger().info("Hello World")

    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
