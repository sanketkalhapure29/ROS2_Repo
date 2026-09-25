# 🤖 ROS2 Services — Client/Server Communication Between Nodes

Welcome to **Day 5 of my ROS2 learning journey**.

In this topic, I learned how ROS2 nodes can communicate using **Services**.

Unlike Topics, which are mainly used for continuous data communication, Services provide a **Request → Response** communication mechanism.

A simple example is:

> **Client:** Add `3 + 8`
> **Server:** Calculate the result
> **Server:** Return `11`

---

# 📌 Table of Contents

1. [What is a ROS2 Service?](#-what-is-a-ros2-service)
2. [Why Do We Need Services?](#-why-do-we-need-services)
3. [Service Communication Model](#-service-communication-model)
4. [Topics vs Services](#-topics-vs-services)
5. [Example Used in This Project](#-example-used-in-this-project)
6. [Service Interface](#-service-interface)
7. [Understanding the Server](#-understanding-the-server)
8. [Understanding the Client](#-understanding-the-client)
9. [Complete Communication Flow](#-complete-communication-flow)
10. [Package Configuration](#-package-configuration)
11. [Project Structure](#-project-structure)
12. [Build the Package](#-build-the-package)
13. [Run the Service Server](#-run-the-service-server)
14. [Run the Service Client](#-run-the-service-client)
15. [Call the Service from Terminal](#-call-the-service-from-terminal)
16. [Inspect Services Using ROS2 CLI](#-inspect-services-using-ros2-cli)
17. [Visualize Communication Using RQT Graph](#-visualize-communication-using-rqt-graph)
18. [Understanding the RQT Graph](#-understanding-the-rqt-graph)
19. [Service Applications in Robotics](#-service-applications-in-robotics)
20. [Services vs Topics vs Actions](#-services-vs-topics-vs-actions)
21. [Common Mistakes](#-common-mistakes)
22. [Key Takeaways](#-key-takeaways)

---

# 🔹 What is a ROS2 Service?

A **ROS2 Service** is a communication mechanism that allows one node to send a **request** to another node and receive a **response**.

It follows:

```text
CLIENT
   |
   | Request
   ↓
SERVER
   |
   | Response
   ↓
CLIENT
```

For example:

```text
Client
  |
  | a = 3
  | b = 8
  ↓
/add_two_ints
  ↓
Server
  |
  | sum = 11
  ↓
Client
```

The important thing is that the client **asks for something**, and the server **returns the result**.

---

# 🔹 Why Do We Need Services?

Imagine a mobile robot.

You may want to tell the robot:

```text
Reset your odometry.
```

You don't need the robot to continuously publish or receive this command.

Instead:

```text
Robot Controller
      |
      | "Reset odometry"
      ↓
Odometry Node
      |
      | "Reset successful"
      ↓
Robot Controller
```

This is a perfect use case for a **Service**.

Other examples:

* Reset odometry
* Enable motors
* Disable motors
* Start calibration
* Stop calibration
* Save a map
* Trigger sensor calibration
* Change robot configuration
* Request a calculation
* Start a specific operation

---

# 🔹 Service Communication Model

A ROS2 service consists of two main participants:

### 1. Service Server

The **server** provides the service.

It waits for requests and processes them.

```text
SERVER
  |
  | Waits for request
  ↓
Receives request
  |
  ↓
Processes request
  |
  ↓
Returns response
```

### 2. Service Client

The **client** requests the service.

```text
CLIENT
  |
  ↓
Creates request
  |
  ↓
Sends request
  |
  ↓
Waits for response
  |
  ↓
Receives response
```

---

# 🔹 Topics vs Services

Understanding this difference is extremely important in ROS2.

| Feature       | Topic                  | Service                       |
| ------------- | ---------------------- | ----------------------------- |
| Communication | Continuous             | Request/Response              |
| Model         | Publisher → Subscriber | Client → Server               |
| Response      | No direct response     | Yes                           |
| Best for      | Sensor data            | Commands/requests             |
| Example       | LiDAR data             | Reset odometry                |
| Communication | Asynchronous           | Request-response              |
| Typical data  | Camera, IMU, GPS       | Start, stop, reset, calculate |

### Example

A LiDAR continuously publishes:

```text
/lidar_scan
```

This is a **Topic**.

But if we want to request:

```text
Reset LiDAR
```

a **Service** can be used.

---

# 🔹 Example Used in This Project

In this project, we create a service called:

```text
/add_two_ints
```

The client sends:

```text
a = 3
b = 8
```

The server calculates:

```text
3 + 8 = 11
```

and sends:

```text
sum = 11
```

---

# 🔹 Service Interface

We use the service:

```text
example_interfaces/srv/AddTwoInts
```

You can inspect it using:

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

You will see:

```text
int64 a
int64 b
---
int64 sum
```

The `---` separates the:

```text
REQUEST
```

from:

```text
RESPONSE
```

So:

```text
REQUEST
-------
a
b

RESPONSE
--------
sum
```

For our example:

```text
Request:
a = 3
b = 8

Response:
sum = 11
```

---

# 🔹 Understanding the Server

File:

```text
add_two_ints_server.py
```

Complete code:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsServerNode(Node):

    def __init__(self):

        super().__init__("add_two_ints_server")

        self.server_ = self.create_service(
            AddTwoInts,
            "add_two_ints",
            self.callback_add_two_ints
        )

        self.get_logger().info(
            "Add two ints server has been started."
        )


    def callback_add_two_ints(
        self,
        request: AddTwoInts.Request,
        response: AddTwoInts.Response
    ):

        response.sum = request.a + request.b

        self.get_logger().info(
            str(request.a)
            + " + "
            + str(request.b)
            + " = "
            + str(response.sum)
        )

        return response


def main(args=None):

    rclpy.init(args=args)

    node = AddTwoIntsServerNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

# 🧠 Understanding the Server Code

## 1. Import ROS2

```python
import rclpy
```

`rclpy` is the Python client library for ROS2.

It allows Python programs to communicate with ROS2.

---

## 2. Import Node

```python
from rclpy.node import Node
```

Every ROS2 Python node is generally created using the `Node` class.

Our server class inherits from it:

```python
class AddTwoIntsServerNode(Node):
```

This means:

```text
Node
 ↓
AddTwoIntsServerNode
```

Our class gets ROS2 node functionality from the `Node` class.

---

# 🔹 3. Import the Service

```python
from example_interfaces.srv import AddTwoInts
```

This imports the `AddTwoInts` service interface.

It defines:

```text
Request:
a
b

Response:
sum
```

---

# 🔹 4. Create the Node

```python
super().__init__("add_two_ints_server")
```

This creates a ROS2 node named:

```text
add_two_ints_server
```

You can verify it using:

```bash
ros2 node list
```

You should see:

```text
/add_two_ints_server
```

---

# 🔹 5. Create the Service

The most important line in the server is:

```python
self.server_ = self.create_service(
    AddTwoInts,
    "add_two_ints",
    self.callback_add_two_ints
)
```

It has three important parts:

```text
AddTwoInts
     ↓
Service Type

"add_two_ints"
     ↓
Service Name

callback_add_two_ints
     ↓
Function executed when request arrives
```

In simple terms:

> "Create an `add_two_ints` service using the `AddTwoInts` interface and call `callback_add_two_ints()` whenever a client sends a request."

---

# 🔹 6. Callback Function

```python
def callback_add_two_ints(self, request, response):
```

This function is executed when the server receives a request.

The server receives two important objects:

```text
request
response
```

### Request

Contains:

```python
request.a
request.b
```

For example:

```text
a = 3
b = 8
```

### Response

Contains:

```python
response.sum
```

We calculate:

```python
response.sum = request.a + request.b
```

So:

```text
3 + 8 = 11
```

---

# 🔹 7. Return the Response

```python
return response
```

This sends the result back to the client.

Therefore:

```text
Client
  |
  | a=3, b=8
  ↓
Server
  |
  | sum=11
  ↓
Client
```

---

# 🔹 8. Keep the Server Running

```python
rclpy.spin(node)
```

This keeps the node alive and allows ROS2 to process incoming service requests.

Without `spin()`, the program would finish instead of continuously waiting for requests.

---

# 🔹 Understanding the Client

File:

```text
add_two_ints_client.py
```

Complete code:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):

    def __init__(self):

        super().__init__("add_two_ints_client")

        self.client = self.create_client(
            AddTwoInts,
            "add_two_ints"
        )

        while not self.client.wait_for_service(1.0):

            self.get_logger().warning(
                "Waiting for add_two_ints server..."
            )

        request = AddTwoInts.Request()

        request.a = 3
        request.b = 8

        self.future = self.client.call_async(request)

        self.future.add_done_callback(
            lambda completed_future:
            self.log_response(request, completed_future)
        )


    def log_response(self, request, future):

        response = future.result()

        self.get_logger().info(
            str(request.a)
            + " + "
            + str(request.b)
            + " = "
            + str(response.sum)
        )


def main(args=None):

    rclpy.init(args=args)

    node = AddTwoIntsClient()

    rclpy.spin_until_future_complete(
        node,
        node.future
    )

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

# 🧠 Understanding the Client Code

## 1. Create the Client Node

```python
super().__init__("add_two_ints_client")
```

The node is named:

```text
add_two_ints_client
```

---

# 🔹 2. Create the Service Client

```python
self.client = self.create_client(
    AddTwoInts,
    "add_two_ints"
)
```

This creates a client for:

```text
/add_two_ints
```

using:

```text
AddTwoInts
```

service type.

---

# 🔹 3. Wait for the Server

```python
while not self.client.wait_for_service(1.0):
```

The client checks whether the server is available.

If the server is not running:

```text
Waiting for add_two_ints server...
```

will be displayed.

This prevents the client from trying to communicate with a server that does not exist yet.

---

# 🔹 4. Create a Request

```python
request = AddTwoInts.Request()
```

This creates a request object.

The request contains:

```text
a
b
```

We set:

```python
request.a = 3
request.b = 8
```

So our request becomes:

```text
a = 3
b = 8
```

---

# 🔹 5. Send the Request

```python
self.future = self.client.call_async(request)
```

This sends the request to the server.

But there is an important concept here:

## What is a Future?

A `Future` represents a result that will become available later.

Think of it like ordering food:

```text
You place order
      ↓
Kitchen prepares food
      ↓
Food becomes ready
      ↓
You receive food
```

Similarly:

```text
Client sends request
      ↓
Server processes request
      ↓
Response becomes available
      ↓
Client receives response
```

The `Future` represents that pending response.

---

# 🔹 6. Callback After Response

```python
self.future.add_done_callback(
    lambda completed_future:
    self.log_response(request, completed_future)
)
```

This tells ROS2:

> "When the response is ready, call `log_response()`."

---

# 🔹 7. Get the Response

Inside:

```python
def log_response(self, request, future):
```

we use:

```python
response = future.result()
```

This retrieves the response.

Then:

```python
response.sum
```

contains:

```text
11
```

So the output becomes:

```text
3 + 8 = 11
```

---

# 🔹 8. Spin Until the Result Arrives

```python
rclpy.spin_until_future_complete(
    node,
    node.future
)
```

This keeps ROS2 processing events until the Future is completed.

In simple terms:

```text
Send request
    ↓
Wait for response
    ↓
Response arrives
    ↓
Future completed
    ↓
Continue program
```

---

# 🔄 Complete Communication Flow

The complete system works like this:

```text
                ROS 2 SERVICE
                /add_two_ints
                     │
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
     CLIENT NODE          SERVER NODE
add_two_ints_client   add_two_ints_server
          │                     │
          │                     │
          │ Request             │
          │ a = 3               │
          │ b = 8               │
          ├────────────────────►│
          │                     │
          │                     │ Calculate
          │                     │ 3 + 8
          │                     │
          │ Response            │
          │ sum = 11            │
          │◄────────────────────┤
          │                     │
          ▼                     ▼
      Prints 11              Continues
```

---

# 🔹 Package Configuration

For ROS2 to know how to execute these Python files, we need to configure `setup.py`.

## `setup.py`

Inside:

```text
~/ros2_ws/src/my_py_pkg/setup.py
```

Add:

```python
entry_points={
    'console_scripts': [

        "add_two_ints_server = my_py_pkg.add_two_ints_server:main",

        "add_two_ints_client = my_py_pkg.add_two_ints_client:main",

    ],
},
```

---

# 🧠 Understanding `entry_points`

Consider:

```text
"add_two_ints_server = my_py_pkg.add_two_ints_server:main"
```

It means:

```text
add_two_ints_server
        ↓
Executable name

my_py_pkg.add_two_ints_server
        ↓
Python module

main
        ↓
Function to execute
```

Therefore:

```bash
ros2 run my_py_pkg add_two_ints_server
```

will execute:

```text
my_py_pkg/add_two_ints_server.py
```

and call:

```python
main()
```

Similarly:

```bash
ros2 run my_py_pkg add_two_ints_client
```

runs:

```text
my_py_pkg/add_two_ints_client.py
```

---

# 🔹 `package.xml`

Because our Python programs use:

```python
from example_interfaces.srv import AddTwoInts
```

our package needs the `example_interfaces` dependency.

Add:

```xml
<depend>example_interfaces</depend>
```

### Important

The correct syntax is:

```xml
<depend>example_interfaces</depend>
```

NOT:

```xml
<depend> example_interfaces <?depend>
```

---

# 📁 Project Structure

Your package should look approximately like:

```text
ros2_ws/
└── src/
    └── my_py_pkg/
        ├── my_py_pkg/
        │   ├── __init__.py
        │   ├── add_two_ints_server.py
        │   └── add_two_ints_client.py
        │
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```

---

# 🔨 Build the Package

Open a terminal.

First source ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

Go to your workspace:

```bash
cd ~/ros2_ws
```

Build the package:

```bash
colcon build --packages-select my_py_pkg
```

After successful compilation:

```bash
source install/setup.bash
```

---

# ▶️ Execute the Service Server

Open **Terminal 1**.

Source ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

Source your workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Run the server:

```bash
ros2 run my_py_pkg add_two_ints_server
```

You should see:

```text
[INFO] [add_two_ints_server]: Add two ints server has been started.
```

The server is now waiting for requests.

---

# ▶️ Execute the Service Client

Open **Terminal 2**.

Source ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

Source your workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Run:

```bash
ros2 run my_py_pkg add_two_ints_client
```

You should get:

```text
3 + 8 = 11
```

---

# 🧪 Complete Execution Setup

You should have two terminals.

### Terminal 1 — Server

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_server
```

### Terminal 2 — Client

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_client
```

---

# 🔹 Call the Service Directly from Terminal

You don't always need to write a client program.

ROS2 provides a CLI command to call services.

First check the available services:

```bash
ros2 service list
```

You should see:

```text
/add_two_ints
```

Now call it directly:

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 8}"
```

The server should receive:

```text
a = 3
b = 8
```

and calculate:

```text
3 + 8 = 11
```

The terminal will display the response.

This is extremely useful when debugging ROS2 systems.

---

# 🔍 Inspect ROS2 Services

## List all services

```bash
ros2 service list
```

---

## List services with their types

```bash
ros2 service list -t
```

You should see something similar to:

```text
/add_two_ints [example_interfaces/srv/AddTwoInts]
```

---

## Check the type of a service

```bash
ros2 service type /add_two_ints
```

Output:

```text
example_interfaces/srv/AddTwoInts
```

---

## Show the service interface

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

Output:

```text
int64 a
int64 b
---
int64 sum
```

---

# 🔹 Inspect the Nodes

List all running nodes:

```bash
ros2 node list
```

You should see:

```text
/add_two_ints_server
```

When the client is running, you may also see:

```text
/add_two_ints_client
```

---

# 🔹 Get Information About the Server

Run:

```bash
ros2 node info /add_two_ints_server
```

This gives information about the node, including its services and other ROS2 interfaces.

---

# 📊 Visualize the ROS2 Graph

One of the most useful tools for understanding ROS2 communication is:

```text
rqt_graph
```

It provides a graphical representation of ROS2 nodes and their communication connections.

---

# 🔹 Start RQT Graph

With the server running, open another terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Then:

```bash
rqt_graph
```

You can also start it using:

```bash
ros2 run rqt_graph rqt_graph
```

---

# 🔹 What Should I Run Before `rqt_graph`?

For the most useful graph, run the server first:

### Terminal 1

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_server
```

Then run:

### Terminal 2

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_client
```

Then:

### Terminal 3

```bash
source /opt/ros/jazzy/setup.bash

rqt_graph
```

---

# 🧠 Understanding the ROS2 Graph

Conceptually, your system looks like:

```text
┌──────────────────────────┐
│   add_two_ints_client    │
│                          │
│   a = 3                  │
│   b = 8                  │
└────────────┬─────────────┘
             │
             │ Request
             │
             ▼
       /add_two_ints
             │
             │ Response
             │
             ▼
┌──────────────────────────┐
│   add_two_ints_server    │
│                          │
│   sum = a + b            │
│   sum = 11               │
└──────────────────────────┘
```

The exact graphical appearance in `rqt_graph` can vary depending on which nodes are running and which ROS2 interfaces are selected for display.

---

# 🔎 Important Difference: ROS2 Graph vs Service Call

It is important to understand that:

```text
Node
```

and:

```text
Service
```

are different things.

For example:

```text
Node:
add_two_ints_server
```

provides:

```text
Service:
add_two_ints
```

So:

```text
Node
  ↓
provides
  ↓
Service
```

The client node uses that service.

---

# 🤖 Robotics Applications of Services

Services are extremely useful in robotics.

## 1. Reset Odometry

```text
/reset_odometry
```

Client:

```text
Robot Controller
```

Server:

```text
Odometry Node
```

---

## 2. Enable Motors

```text
/enable_motors
```

Client:

```text
Navigation System
```

Server:

```text
Motor Controller
```

---

## 3. Disable Motors

```text
/disable_motors
```

Useful for stopping a robot's motor controller through a request.

---

## 4. Sensor Calibration

For example:

```text
/calibrate_imu
```

Client requests:

```text
Start calibration
```

Server performs calibration and returns a result.

---

## 5. Map Saving

A robot could provide:

```text
/save_map
```

A mapping node can receive the request and save the current map.

---

# 🚙 Example for an Autonomous UGV

Imagine an autonomous UGV.

It may contain:

```text
             UGV
              |
      ┌───────┼────────┐
      │       │        │
      ▼       ▼        ▼
    LiDAR     IMU     GNSS
      │       │        │
      └───────┼────────┘
              │
              ▼
        Localization
              │
              ▼
           Nav2
```

Now imagine we want to reset the robot's localization.

A service could be:

```text
/reset_localization
```

The navigation system sends a request:

```text
RESET
```

The localization node performs the operation and returns:

```text
SUCCESS
```

This is a typical Service use case.

---

# 🔹 Services vs Topics vs Actions

ROS2 provides several communication mechanisms.

| Communication             | Topic      | Service           | Action               |
| ------------------------- | ---------- | ----------------- | -------------------- |
| Model                     | Pub/Sub    | Request/Response  | Goal/Feedback/Result |
| Continuous data           | ✅          | ❌                 | ❌                    |
| Request/response          | ❌          | ✅                 | ✅                    |
| Feedback during operation | ❌          | ❌                 | ✅                    |
| Long-running task         | ❌          | Usually not ideal | ✅                    |
| Example                   | LiDAR data | Reset odometry    | Navigate to goal     |

### Topic

Use when data is continuously flowing.

Example:

```text
/lidar_scan
/camera/image
/imu/data
```

### Service

Use when you need a relatively quick request and response.

Example:

```text
/reset_odometry
/enable_motors
```

### Action

Use when an operation takes time and you want feedback.

Example:

```text
Navigate to a target
```

A navigation action could provide:

```text
Goal
 ↓
"Go to this location"

Feedback
 ↓
"50% completed"

Result
 ↓
"Goal reached"
```

---

# ⚠️ Common Mistakes

## Mistake 1 — Server is not running

If you run:

```bash
ros2 run my_py_pkg add_two_ints_client
```

before starting the server, the client will keep waiting:

```text
Waiting for add_two_ints server...
```

### Solution

Start the server first:

```bash
ros2 run my_py_pkg add_two_ints_server
```

---

# Mistake 2 — Forgetting to source the workspace

If ROS2 cannot find your package:

```text
Package 'my_py_pkg' not found
```

run:

```bash
source ~/ros2_ws/install/setup.bash
```

---

# Mistake 3 — Forgetting to build

After changing `setup.py` or adding files, rebuild:

```bash
cd ~/ros2_ws
colcon build --packages-select my_py_pkg
```

Then:

```bash
source install/setup.bash
```

---

# Mistake 4 — Wrong dependency in `package.xml`

Correct:

```xml
<depend>example_interfaces</depend>
```

---

# Mistake 5 — Wrong executable name

The executable name comes from:

```python
entry_points={
    'console_scripts': [
        "add_two_ints_server = my_py_pkg.add_two_ints_server:main",
        "add_two_ints_client = my_py_pkg.add_two_ints_client:main",
    ],
},
```

Therefore:

```bash
ros2 run my_py_pkg add_two_ints_server
```

and:

```bash
ros2 run my_py_pkg add_two_ints_client
```

must use the names on the **left side**.

---

# 🧪 Useful Command Cheat Sheet

| Purpose               | Command                                                                            |
| --------------------- | ---------------------------------------------------------------------------------- |
| List nodes            | `ros2 node list`                                                                   |
| Node information      | `ros2 node info /add_two_ints_server`                                              |
| List services         | `ros2 service list`                                                                |
| List services + types | `ros2 service list -t`                                                             |
| Service type          | `ros2 service type /add_two_ints`                                                  |
| Show interface        | `ros2 interface show example_interfaces/srv/AddTwoInts`                            |
| Call service          | `ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 8}"` |
| Visualize graph       | `rqt_graph`                                                                        |
| Run server            | `ros2 run my_py_pkg add_two_ints_server`                                           |
| Run client            | `ros2 run my_py_pkg add_two_ints_client`                                           |
| Build package         | `colcon build --packages-select my_py_pkg`                                         |

---

# 🧠 The Entire Concept in One Picture

```text
                 ROS 2
                   │
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
       CLIENT             SERVER
          │                 │
          │                 │
          │  REQUEST        │
          │ a = 3           │
          │ b = 8           │
          ├────────────────►│
          │                 │
          │                 │
          │            Calculate
          │              3 + 8
          │                 │
          │                 │
          │  RESPONSE       │
          │  sum = 11       │
          │◄────────────────┤
          │                 │
          ▼                 ▼
       Future          Callback Function
          │
          ▼
    future.result()
          │
          ▼
       3 + 8 = 11
```

---

# 🎯 What I Learned

Through this ROS2 Services example, I learned:

* What a ROS2 Service is
* Client/Server communication
* Service requests and responses
* ROS2 service interfaces
* `example_interfaces/srv/AddTwoInts`
* Creating a service server
* Creating a service client
* Service callbacks
* `create_service()`
* `create_client()`
* `wait_for_service()`
* `call_async()`
* Futures
* `future.result()`
* `spin()`
* `spin_until_future_complete()`
* ROS2 service CLI commands
* `ros2 service list`
* `ros2 service type`
* `ros2 interface show`
* Calling services directly from the terminal
* Visualizing ROS2 communication using `rqt_graph`
* Difference between Topics, Services and Actions
* How services can be applied to real robotic systems

---

# 🚀 Final Understanding

The easiest way to remember ROS2 Services is:

```text
TOPIC

Publisher ───────────────► Subscriber
        Continuous Data


SERVICE

Client ───── Request ────► Server
Client ◄──── Response ──── Server


ACTION

Client ───── Goal ───────► Server
Client ◄──── Feedback ──── Server
Client ◄──── Result ────── Server
```

For this project:

```text
Client
   │
   │ a = 3
   │ b = 8
   ▼
/add_two_ints
   │
   ▼
Server
   │
   │ 3 + 8
   ▼
sum = 11
   │
   ▼
Client
```

This simple example forms the foundation for using **request/response communication in larger ROS2 robotic systems**.

---

## ⭐ Quick Start

If you only want to run this project:

### Terminal 1

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_server
```

### Terminal 2

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg add_two_ints_client
```

### Terminal 3 — Visualize

```bash
source /opt/ros/jazzy/setup.bash

rqt_graph
```

### Or call the service directly

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 8}"
```

---

# 📚 ROS2 Learning Series

This README is part of my **ROS2 Daily Learning Series**, where I am documenting my journey of learning ROS2 concepts through practical examples.

The goal is to understand not only **how to write ROS2 code**, but also **how these concepts are used in real robotic and autonomous systems**.

**Next:** Continue exploring ROS2 communication, tools, actions, parameters, TF2, URDF/Xacro, simulation, and navigation.
