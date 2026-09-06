#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
 
 
class AddTwoIntsClient(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("add_two_ints_client") # MODIFY NAME

        self.client = self.create_client(AddTwoInts, "add_two_ints")
        while not self.client.wait_for_service(1.0):
            self.get_logger().warning("Waiting for add_two_ints server...")

        request = AddTwoInts.Request()
        request.a = 3
        request.b = 8

        self.future = self.client.call_async(request)
        self.future.add_done_callback(
            lambda completed_future: self.log_response(request, completed_future)
        )

    def log_response(self, request, future):
        response = future.result()
        self.get_logger().info(
            str(request.a) + " + " + str(request.b) + " = " + str(response.sum)
        )
 
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient() # MODIFY NAME
    rclpy.spin_until_future_complete(node, node.future)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()