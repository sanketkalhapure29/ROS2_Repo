#!/usr/bin/env python3
import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


class TrialClient(Node):
    def __init__(self):
        super().__init__("trial_client")
        self.client = self.create_client(AddTwoInts, "add_two_ints")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning("Waiting for add_two_ints server...")

    def send_request(self, first_number, second_number):
        request = AddTwoInts.Request()
        request.a = first_number
        request.b = second_number
        return self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node = TrialClient()

    try:
        while rclpy.ok():
            user_input = input("Enter two integers separated by a space (or q to quit): ")
            if user_input.strip().lower() == "q":
                break

            numbers = user_input.split()
            if len(numbers) != 2:
                print("Please enter exactly two integers.")
                continue

            try:
                first_number, second_number = map(int, numbers)
            except ValueError:
                print("Please enter valid integers.")
                continue

            future = node.send_request(first_number, second_number)
            rclpy.spin_until_future_complete(node, future)

            if future.exception() is not None:
                node.get_logger().error(f"Service call failed: {future.exception()}")
                continue

            response = future.result()
            node.get_logger().info(
                f"{first_number} + {second_number} = {response.sum}"
            )
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
