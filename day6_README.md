# ROS2 Day 6 — Creating and Using Custom Interfaces

## 📌 Topic: Custom ROS2 Interfaces

On **Day 6** of my ROS2 learning journey, I learned how to create a **custom ROS2 interface** and use it inside a Python ROS2 node.

Until now, I worked with predefined ROS2 interfaces such as:

```text
std_msgs/msg/String
example_interfaces/msg/AddTwoInts
```

Today, I learned how to create my own interface for a robot.

In this project, I created a custom message:

```text
HardwareStatus.msg
```

inside a dedicated interface package:

```text
my_robot_interfaces
```

Then I used this custom message in a Python publisher node to publish the robot's hardware status.

---

# 1. What is a ROS2 Interface?

A **ROS2 interface** defines the structure and data types used for communication between ROS2 nodes.

In simple words:

> **An interface tells ROS2 what data a node is going to send or receive.**

ROS2 mainly provides three types of interfaces:

| Interface | File Extension | Used For |
| --------- | -------------- | -------- |
| Message   | `.msg`         | Topics   |
| Service   | `.srv`         | Services |
| Action    | `.action`      | Actions  |

---

# 2. Types of ROS2 Interfaces

## 2.1 Message — `.msg`

Messages are used with **Topics**.

Example:

```text
float64 temperature
bool are_motors_ready
string debug_message
```

Communication:

```text
Publisher ───────────────► Subscriber
```

Messages are generally used for continuous or streaming data.

Examples:

* LiDAR data
* Camera information
* Robot velocity
* IMU data
* Robot status

---

## 2.2 Service — `.srv`

Services are used for **Request/Response communication**.

Example:

```text
float64 length
float64 width
---
float64 area
```

The part before `---` is the request.

The part after `---` is the response.

Communication:

```text
Client ───── Request ─────► Server
Client ◄──── Response ───── Server
```

Examples:

* Reset odometry
* Enable motors
* Disable motors
* Trigger calibration

---

## 2.3 Action — `.action`

Actions are used for **long-running operations**.

For example:

```text
Navigate the robot to a target location.
```

Actions support:

* Goal
* Feedback
* Result

Communication:

```text
Action Client ───── Goal ─────► Action Server
Action Client ◄── Feedback ─── Action Server
Action Client ◄──── Result ─── Action Server
```

Examples:

* Navigation
* Manipulator movement
* Pick and place
* Autonomous docking

---

# 3. Why Do We Need Custom Interfaces?

ROS2 already provides many predefined interfaces.

For example:

```text
std_msgs/msg/String
std_msgs/msg/Bool
example_interfaces/srv/AddTwoInts
```

But real robots often need to communicate multiple related pieces of information.

For example, a UGV may need to publish:

```text
Motor temperature
Motor status
Battery voltage
GPS status
Emergency stop status
Debug information
```

We could create separate topics for each value.

But this can make the system unnecessarily complicated.

Instead, we can create one custom message:

```text
HardwareStatus
```

containing:

```text
temperature
motor status
debug message
```

This creates a structured and reusable communication interface.

---

# 4. Project Architecture

The project contains two packages:

```text
my_robot_interfaces
        │
        │ defines
        ▼
HardwareStatus.msg
        │
        │ used by
        ▼
my_py_pkg
        │
        ▼
HardwareStatusPublisherNode
        │
        │ publishes
        ▼
/hardware_status
```

The interface package defines **what the data looks like**.

The Python package uses that interface to **send the data**.

---

# 5. Step 1 — Create the Custom Interface Package

Move to the source directory:

```bash
cd ~/ros2_ws/src
```

Create the package:

```bash
ros2 pkg create my_robot_interfaces
```

Move into the package:

```bash
cd my_robot_interfaces
```

Because this package is only being used for interfaces, we don't need the automatically generated C++ source folders.

Remove them if they were created:

```bash
rm -r include
rm -r src
```

> If your package was created with a different build type, make sure the package is configured as an **ament_cmake** package because ROS2 interface generation uses CMake configuration.

---

# 6. Interface Package Structure

Initially:

```text
my_robot_interfaces/
├── CMakeLists.txt
├── package.xml
└── ...
```

We will eventually create:

```text
my_robot_interfaces/
├── CMakeLists.txt
├── package.xml
└── msg/
    └── HardwareStatus.msg
```

---

# 7. Step 2 — Configure `package.xml`

Open:

```text
~/ros2_ws/src/my_robot_interfaces/package.xml
```

Make sure the package contains the required dependencies:

```xml
<buildtool_depend>ament_cmake</buildtool_depend>

<buildtool_depend>rosidl_default_generators</buildtool_depend>

<exec_depend>rosidl_default_runtime</exec_depend>

<member_of_group>rosidl_interface_packages</member_of_group>
```

A minimal package configuration can look like:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd"
schematypens="http://www.w3.org/2001/XMLSchema"?>

<package format="3">

  <name>my_robot_interfaces</name>
  <version>0.0.0</version>
  <description>Custom ROS2 interfaces for my robot</description>
  <maintainer email="your_email@example.com">your_name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <exec_depend>rosidl_default_runtime</exec_depend>

  <member_of_group>rosidl_interface_packages</member_of_group>

</package>
```

---

# 8. Understanding the Dependencies

## `ament_cmake`

```xml
<buildtool_depend>ament_cmake</buildtool_depend>
```

This allows the package to use the ROS2 CMake build system.

---

## `rosidl_default_generators`

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
```

This provides the tools required to generate ROS2 code from our interface definitions.

For example:

```text
HardwareStatus.msg
        ↓
ROSIDL
        ↓
Generated ROS2 interface
        ↓
Python / C++ nodes can use it
```

---

## `rosidl_default_runtime`

```xml
<exec_depend>rosidl_default_runtime</exec_depend>
```

This provides the runtime support required when using the generated interfaces.

---

## `rosidl_interface_packages`

```xml
<member_of_group>rosidl_interface_packages</member_of_group>
```

This tells ROS2 that the package contains interface definitions.

---

# 9. Step 3 — Configure `CMakeLists.txt`

Open:

```text
~/ros2_ws/src/my_robot_interfaces/CMakeLists.txt
```

Use:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
```

---

# 10. Understanding `CMakeLists.txt`

## Find ROS2 dependencies

```cmake
find_package(ament_cmake REQUIRED)
```

Loads the ROS2 CMake build system.

```cmake
find_package(rosidl_default_generators REQUIRED)
```

Loads the tools required for generating interfaces.

---

## Generate the interface

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)
```

This tells ROS2:

> Generate the required ROS2 interface code from `HardwareStatus.msg`.

The flow is:

```text
HardwareStatus.msg
        ↓
rosidl_generate_interfaces()
        ↓
Generated interface
        ↓
Python / C++ can use HardwareStatus
```

---

## Export runtime dependency

```cmake
ament_export_dependencies(rosidl_default_runtime)
```

This makes the runtime dependency available to packages that use the generated interfaces.

---

# 11. Step 4 — Create the `msg` Directory

Move into:

```bash
cd ~/ros2_ws/src/my_robot_interfaces
```

Create the message directory:

```bash
mkdir msg
```

Move inside:

```bash
cd msg
```

Create the message file:

```bash
touch HardwareStatus.msg
```

---

# 12. Step 5 — Define `HardwareStatus.msg`

Open:

```text
~/ros2_ws/src/my_robot_interfaces/msg/HardwareStatus.msg
```

Add:

```text
float64 temperature
bool are_motors_ready
string debug_message
```

---

# 13. Understanding `HardwareStatus.msg`

Our custom message contains three fields.

### Temperature

```text
float64 temperature
```

Stores the hardware temperature.

Example:

```text
25.0
```

---

### Motor Status

```text
bool are_motors_ready
```

A Boolean can contain:

```text
true
```

or:

```text
false
```

For example:

```text
true  → Motors are ready
false → Motors are not ready
```

---

### Debug Message

```text
string debug_message
```

Stores text information.

Example:

```text
"All systems are operational."
```

---

# 14. Visual Representation

Our custom message can be represented as:

```text
HardwareStatus
│
├── temperature        → float64
│
├── are_motors_ready   → bool
│
└── debug_message      → string
```

An actual message could contain:

```text
temperature: 25.0
are_motors_ready: true
debug_message: "All systems are operational."
```

---

# 15. Step 6 — Build the Interface Package

Move to the workspace:

```bash
cd ~/ros2_ws
```

Source ROS2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Build the custom interface package:

```bash
colcon build --packages-select my_robot_interfaces
```

If the build is successful, you should see something similar to:

```text
Starting >>> my_robot_interfaces
Finished <<< my_robot_interfaces
Summary: 1 package finished
```

Now source the workspace:

```bash
source install/setup.bash
```

---

# 16. Verify the Custom Interface

Check whether ROS2 can see the package:

```bash
ros2 pkg list | grep my_robot_interfaces
```

Expected:

```text
my_robot_interfaces
```

Now inspect the interface:

```bash
ros2 interface show my_robot_interfaces/msg/HardwareStatus
```

Expected:

```text
float64 temperature
bool are_motors_ready
string debug_message
```

If this command works, the custom interface has been successfully generated.

---

# 17. Using the Custom Interface in a Python Node

Now we will use our custom message in:

```text
my_py_pkg
```

Move to the Python package:

```bash
cd ~/ros2_ws/src/my_py_pkg/my_py_pkg
```

Create the Python file:

```bash
touch hardware_status_publisher.py
```

Make it executable:

```bash
chmod +x hardware_status_publisher.py
```

---

# 18. Add Interface Dependency to `my_py_pkg`

Open:

```text
~/ros2_ws/src/my_py_pkg/package.xml
```

Add:

```xml
<depend>my_robot_interfaces</depend>
```

This tells ROS2:

> `my_py_pkg` depends on the custom interfaces provided by `my_robot_interfaces`.

---

# 19. Python Publisher Node

Open:

```text
~/ros2_ws/src/my_py_pkg/my_py_pkg/hardware_status_publisher.py
```

Add:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class HardwareStatusPublisherNode(Node):

    def __init__(self):
        super().__init__("hardware_status_publisher")

        self.hw_status_pub = self.create_publisher(
            HardwareStatus,
            "hardware_status",
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_hw_status
        )

        self.get_logger().info(
            "Hardware Status Publisher Node has been started."
        )

    def publish_hw_status(self):

        msg = HardwareStatus()

        msg.temperature = 25.0
        msg.are_motors_ready = True
        msg.debug_message = "All systems are operational."

        self.hw_status_pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = HardwareStatusPublisherNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

# 20. Understanding the Python Code

## Importing the Custom Message

```python
from my_robot_interfaces.msg import HardwareStatus
```

This imports our custom message.

The structure is:

```text
my_robot_interfaces
        ↓
       msg
        ↓
HardwareStatus
```

Now the Python node can create and publish `HardwareStatus` messages.

---

# 21. Creating the Publisher

```python
self.hw_status_pub = self.create_publisher(
    HardwareStatus,
    "hardware_status",
    10
)
```

This creates a ROS2 publisher.

It contains three important parts.

### Message type

```python
HardwareStatus
```

The publisher sends our custom message.

### Topic name

```text
hardware_status
```

The topic will be:

```text
/hardware_status
```

### Queue depth

```text
10
```

This is the publisher's queue depth used as part of the QoS configuration.

---

# 22. Creating the Timer

```python
self.timer = self.create_timer(
    1.0,
    self.publish_hw_status
)
```

This calls:

```text
publish_hw_status()
```

every:

```text
1 second
```

Therefore, our robot hardware status is published continuously.

---

# 23. Creating the Custom Message

Inside the callback:

```python
msg = HardwareStatus()
```

This creates an instance of our custom message.

We can now access its fields.

---

# 24. Filling the Message

Temperature:

```python
msg.temperature = 25.0
```

Motor status:

```python
msg.are_motors_ready = True
```

Debug message:

```python
msg.debug_message = "All systems are operational."
```

The complete message becomes:

```text
temperature: 25.0
are_motors_ready: true
debug_message: "All systems are operational."
```

---

# 25. Publishing the Message

```python
self.hw_status_pub.publish(msg)
```

This publishes the message on:

```text
/hardware_status
```

Communication:

```text
HardwareStatusPublisherNode
            │
            │ HardwareStatus
            ▼
     /hardware_status
            │
            ▼
      Other ROS2 Nodes
```

---

# 26. Step 7 — Add Python Entry Point

Open:

```text
~/ros2_ws/src/my_py_pkg/setup.py
```

Find:

```python
entry_points={
    'console_scripts': [
```

Add:

```python
"hardware_status_publisher = my_py_pkg.hardware_status_publisher:main",
```

For example:

```python
entry_points={
    'console_scripts': [
        "hardware_status_publisher = my_py_pkg.hardware_status_publisher:main",
    ],
},
```

Now ROS2 knows which Python function should execute when we run:

```bash
ros2 run my_py_pkg hardware_status_publisher
```

---

# 27. Final Project Structure

The workspace now looks like:

```text
ros2_ws/
│
└── src/
    │
    ├── my_robot_interfaces/
    │   ├── CMakeLists.txt
    │   ├── package.xml
    │   └── msg/
    │       └── HardwareStatus.msg
    │
    └── my_py_pkg/
        ├── package.xml
        ├── setup.py
        └── my_py_pkg/
            ├── __init__.py
            └── hardware_status_publisher.py
```

---

# 28. Build Both Packages

Because `my_py_pkg` depends on `my_robot_interfaces`, build both packages:

```bash
cd ~/ros2_ws
```

Source ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

Build:

```bash
colcon build --packages-select my_robot_interfaces my_py_pkg
```

Then source the workspace:

```bash
source install/setup.bash
```

---

# 29. Run the Publisher

Run:

```bash
ros2 run my_py_pkg hardware_status_publisher
```

Expected output:

```text
[INFO] [hardware_status_publisher]: Hardware Status Publisher Node has been started.
```

The node will now publish a `HardwareStatus` message every second.

---

# 30. Check the Topic

Open another terminal.

Source the environment:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

List topics:

```bash
ros2 topic list
```

You should see:

```text
/hardware_status
```

---

# 31. Check the Topic Type

Run:

```bash
ros2 topic type /hardware_status
```

Expected:

```text
my_robot_interfaces/msg/HardwareStatus
```

This confirms that `/hardware_status` is using our custom interface.

---

# 32. Display the Published Data

Run:

```bash
ros2 topic echo /hardware_status
```

Expected:

```text
temperature: 25.0
are_motors_ready: true
debug_message: All systems are operational.
---
temperature: 25.0
are_motors_ready: true
debug_message: All systems are operational.
---
```

Every `---` represents a new message.

---

# 33. Inspect the Interface

Run:

```bash
ros2 interface show my_robot_interfaces/msg/HardwareStatus
```

Output:

```text
float64 temperature
bool are_motors_ready
string debug_message
```

---

# 34. Inspect the Node

Run:

```bash
ros2 node list
```

You should see:

```text
/hardware_status_publisher
```

Get information about the node:

```bash
ros2 node info /hardware_status_publisher
```

You should see that the node publishes:

```text
/hardware_status
```

with type:

```text
my_robot_interfaces/msg/HardwareStatus
```

---

# 35. Visualize the Communication Using RQT Graph

Run:

```bash
rqt_graph
```

or:

```bash
ros2 run rqt_graph rqt_graph
```

Conceptually, the graph looks like:

```text
/hardware_status_publisher
            │
            │
            ▼
   /hardware_status
```

The publisher node sends `HardwareStatus` messages to the topic.

---

# 36. Complete Communication Flow

The entire process can be understood as:

```text
             CUSTOM INTERFACE
                    │
                    ▼
       ┌────────────────────────┐
       │ my_robot_interfaces    │
       │                        │
       │ HardwareStatus.msg     │
       │                        │
       │ float64 temperature    │
       │ bool motors_ready      │
       │ string debug_message   │
       └───────────┬────────────┘
                   │
                   │ generated interface
                   ▼
       ┌────────────────────────┐
       │ HardwareStatus         │
       │ Publisher Node         │
       └───────────┬────────────┘
                   │
                   │ publish
                   ▼
           /hardware_status
                   │
                   ▼
             Other Nodes
```

The important concept is:

> **The interface package defines the data structure, while the ROS2 node uses that structure for communication.**

---

# 37. Why Use a Separate Interface Package?

Keeping interfaces in a separate package is useful when multiple ROS2 packages need the same data structures.

For example:

```text
                 my_robot_interfaces
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
         my_py_pkg   my_cpp_pkg   navigation_pkg
```

All of these packages can use:

```text
HardwareStatus.msg
```

without duplicating the interface definition.

This is especially useful in larger robotic systems.

---

# 38. Real Robotics Applications

Custom interfaces are extremely useful in robotics.

## UGV Hardware Status

For an autonomous UGV, we could create:

```text
float64 battery_voltage
float64 motor_temperature
bool motors_ready
bool emergency_stop
bool gps_ready
string system_status
```

and publish it on:

```text
/ugv/hardware_status
```

---

## Sensor Status

A custom interface could contain:

```text
bool lidar_ready
bool camera_ready
bool imu_ready
bool gps_ready
```

This could be used by a system diagnostics node.

---

## Motor Controller Status

For example:

```text
float64 motor_temperature
float64 motor_current
float64 motor_rpm
bool motor_enabled
```

This could provide structured feedback from a motor controller.

---

## Robot Diagnostics

A custom message could combine:

```text
Battery
Motors
Sensors
GPS
Localization
Navigation
Errors
```

into one structured status message.

---

# 39. `.msg` vs `.srv` vs `.action`

| Feature           | `.msg`            | `.srv`           | `.action`            |
| ----------------- | ----------------- | ---------------- | -------------------- |
| Used by           | Topics            | Services         | Actions              |
| Communication     | Publish/Subscribe | Request/Response | Goal/Feedback/Result |
| Continuous data   | ✅                 | ❌                | ❌                    |
| Quick request     | ❌                 | ✅                | ❌                    |
| Long-running task | ❌                 | ❌                | ✅                    |
| Feedback          | ❌                 | ❌                | ✅                    |
| Example           | LiDAR data        | Reset odometry   | Navigate to goal     |

---

# 40. Common Mistakes

## Mistake 1 — Wrong Package Name

Our actual package name is:

```text
my_robot_interfaces
```

Therefore the import must be:

```python
from my_robot_interfaces.msg import HardwareStatus
```

Not:

```python
from my_robot_interface.msg import HardwareStatus
```

---

## Mistake 2 — Wrong Interface Command

Correct:

```bash
ros2 interface show my_robot_interfaces/msg/HardwareStatus
```

---

## Mistake 3 — Forgetting `rosidl_generate_interfaces()`

Your `CMakeLists.txt` must contain:

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)
```

---

## Mistake 4 — Forgetting to Build

After creating or modifying the interface:

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_interfaces
```

Then:

```bash
source install/setup.bash
```

---

## Mistake 5 — Forgetting the Python Dependency

In:

```text
my_py_pkg/package.xml
```

add:

```xml
<depend>my_robot_interfaces</depend>
```

---

## Mistake 6 — Incorrect `CMakeLists.txt`

Make sure:

```cmake
find_package(rosidl_default_generators REQUIRED)
```

is present.

Also make sure:

```cmake
ament_package()
```

is present at the end.

---

# 41. Useful ROS2 Commands

### List packages

```bash
ros2 pkg list
```

### Check custom package

```bash
ros2 pkg list | grep my_robot_interfaces
```

### List interfaces

```bash
ros2 interface list
```

### Inspect custom interface

```bash
ros2 interface show my_robot_interfaces/msg/HardwareStatus
```

### List topics

```bash
ros2 topic list
```

### Check topic type

```bash
ros2 topic type /hardware_status
```

### Display topic data

```bash
ros2 topic echo /hardware_status
```

### List nodes

```bash
ros2 node list
```

### Get node information

```bash
ros2 node info /hardware_status_publisher
```

### Visualize ROS2 graph

```bash
rqt_graph
```

---

# 42. Complete Build and Run Procedure

## Terminal 1

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws

colcon build --packages-select my_robot_interfaces my_py_pkg

source install/setup.bash
```

Run the publisher:

```bash
ros2 run my_py_pkg hardware_status_publisher
```

---

## Terminal 2

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

Check the topic:

```bash
ros2 topic list
```

Check its type:

```bash
ros2 topic type /hardware_status
```

Display the data:

```bash
ros2 topic echo /hardware_status
```

---

## Terminal 3

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

Inspect the custom interface:

```bash
ros2 interface show my_robot_interfaces/msg/HardwareStatus
```

---

# 43. Key Concepts Learned Today

By completing Day 6, I learned:

* What a ROS2 interface is
* Why custom interfaces are required
* Difference between `.msg`, `.srv`, and `.action`
* How to create a dedicated interface package
* How to create a custom `.msg` file
* How to define message fields
* `rosidl_default_generators`
* `rosidl_default_runtime`
* `rosidl_generate_interfaces()`
* `ament_export_dependencies()`
* How ROS2 generates code from interface definitions
* How to use custom messages in Python
* How to declare package dependencies
* How to build an interface package
* How to inspect custom interfaces using ROS2 CLI
* How to publish custom messages
* How to inspect custom topic data
* How custom interfaces can be used in real robotic systems

---

# 🚀 Day 6 Takeaway

Today I moved beyond using only predefined ROS2 interfaces and learned how to **design my own data structure for robot communication**.

The core concept is:

```text
Create Interface
       ↓
Define Data Structure
       ↓
ROSIDL Generates Interface
       ↓
ROS2 Node Imports Interface
       ↓
Node Publishes/Receives Data
```

For today's project:

```text
my_robot_interfaces
        │
        ▼
HardwareStatus.msg
        │
        ▼
HardwareStatusPublisherNode
        │
        ▼
/hardware_status
```

This is an important step toward building larger ROS2 robotic systems where sensors, motor controllers, perception, localization, navigation, and diagnostics need to exchange structured information.

## Day 6

**Custom ROS2 Interfaces — From using predefined messages to designing my own communication data structures for robots.**

---
