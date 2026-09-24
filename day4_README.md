# ROS 2 Topics: Making Nodes Communicate With Each Other 🤖

Welcome to **Day 4 of my ROS 2 Learning Series**.

Today I learned one of the most important concepts in ROS 2: **Topics**.

ROS 2 nodes need a way to communicate with each other. Topics provide a simple communication mechanism where one node can **publish** data and another node can **subscribe** to that data.

In this example, I created:

* 📢 `RobotNewsStationNode` → Publisher
* 📱 `SmartphoneNode` → Subscriber
* 📡 `/robot_news` → Topic
* 📨 `String` → Message type

---

# 📌 What are ROS 2 Topics?

A **Topic** is a named communication channel in ROS 2.

One node publishes messages to a topic, while another node subscribes to that topic.

```text
Publisher Node
      │
      │ publish()
      ↓
   /robot_news
      │
      │ message
      ↓
Subscriber Node
```

The nodes don't directly call each other's functions.

Instead:

```text
Node → Topic → Node
```

The topic acts as the communication channel.

---

# 🧠 Before Understanding ROS 2: Basic Python Concepts

The ROS 2 code uses some basic Python concepts that are important to understand first.

---

## 1. Class

A **class** is a blueprint for creating objects.

For example:

```python
class SmartphoneNode:
    pass
```

Here, `SmartphoneNode` is a class.

In ROS 2, we create our node as a class:

```python
class SmartphoneNode(Node):
```

This means:

> Create a class called `SmartphoneNode` that inherits functionality from the ROS 2 `Node` class.

Similarly:

```python
class RobotNewsStationNode(Node):
```

creates the publisher node.

---

# 2. Inheritance

Notice:

```python
class SmartphoneNode(Node):
```

The `Node` inside the brackets means that `SmartphoneNode` **inherits from** the ROS 2 `Node` class.

This is called **inheritance**.

Because of inheritance, our class can use ROS 2 functionality such as:

```python
self.create_publisher()
self.create_subscription()
self.create_timer()
self.get_logger()
```

Think of it as:

```text
ROS 2 Node
     │
     │ inheritance
     ↓
SmartphoneNode
```

The same applies to:

```text
ROS 2 Node
     │
     ↓
RobotNewsStationNode
```

---

# 3. `__init__()` — Constructor

Inside our class we have:

```python
def __init__(self):
```

`__init__()` is a special Python function called a **constructor**.

It automatically runs when we create an object.

For example:

```python
node = SmartphoneNode()
```

When Python sees this:

```text
SmartphoneNode()
      ↓
__init__()
```

So everything inside `__init__()` gets executed.

For our ROS 2 node, this is where we:

* Give the node a name
* Create the publisher/subscriber
* Create timers
* Initialize variables

---

# 4. What is `self`?

You will see `self` throughout the code.

For example:

```python
self.robot_name_ = "C3P0"
```

and:

```python
self.publisher_
```

and:

```python
self.create_subscription(...)
```

`self` refers to the **current object**.

For example:

```python
node = SmartphoneNode()
```

The `node` object can be thought of as:

```text
node
 │
 ├── subscriber_
 │
 └── callback_robot_news()
```

When we write:

```python
self.subscriber_
```

we mean:

> The `subscriber_` belonging to this particular node object.

---

# 5. Functions

A function is a block of code designed to perform a particular task.

For example:

```python
def hello():
    print("Hello")
```

Calling:

```python
hello()
```

executes the function.

Our ROS 2 programs contain several functions:

```text
__init__()
publish_news()
callback_robot_news()
main()
```

Each function has a different job.

---

# 📢 1. Publisher Node

The publisher node is responsible for creating and sending news messages.

## `robot_news_station.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class RobotNewsStationNode(Node):

    def __init__(self):
        super().__init__("robot_news_station")

        self.robot_name_ = "C3P0"

        self.publisher_ = self.create_publisher(
            String,
            "robot_news",
            10
        )

        self.timer_ = self.create_timer(
            0.5,
            self.publish_news
        )

        self.get_logger().info(
            "Robot News Station has been started."
        )


    def publish_news(self):

        msg = String()

        msg.data = (
            "Hii, this is "
            + self.robot_name_
            + " from the robot news station"
        )

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = RobotNewsStationNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

# 🔍 Understanding the Publisher Code

## Step 1 — Import ROS 2

```python
import rclpy
```

This gives Python access to the ROS 2 Python API.

---

## Step 2 — Import `Node`

```python
from rclpy.node import Node
```

This allows us to create a ROS 2 node using Python.

---

## Step 3 — Import String

```python
from example_interfaces.msg import String
```

This imports the ROS 2 `String` message type.

We use it to send text messages.

---

# Step 4 — Create the Class

```python
class RobotNewsStationNode(Node):
```

This creates our ROS 2 node class.

It inherits from:

```text
Node
```

Therefore, it can use ROS 2 functions.

---

# Step 5 — Constructor

```python
def __init__(self):
```

This function runs automatically when:

```python
node = RobotNewsStationNode()
```

is executed.

---

# Step 6 — Initialize the ROS 2 Node

```python
super().__init__("robot_news_station")
```

`super()` allows us to call functionality from the parent `Node` class.

This creates the ROS 2 node:

```text
/robot_news_station
```

---

# Step 7 — Create a Variable

```python
self.robot_name_ = "C3P0"
```

This creates a variable belonging to the node object.

Its value is:

```text
C3P0
```

We can later access it using:

```python
self.robot_name_
```

---

# Step 8 — Create the Publisher

```python
self.publisher_ = self.create_publisher(
    String,
    "robot_news",
    10
)
```

This creates a ROS 2 publisher.

It has:

### Message type

```python
String
```

### Topic

```python
"robot_news"
```

### Queue depth

```python
10
```

So:

```text
RobotNewsStationNode
        │
        │ Publisher
        ↓
   /robot_news
```

---

# Step 9 — Create a Timer

```python
self.timer_ = self.create_timer(
    0.5,
    self.publish_news
)
```

This tells ROS 2:

> Call `publish_news()` every 0.5 seconds.

The important thing here is:

```python
self.publish_news
```

We don't use:

```python
self.publish_news()
```

because we are giving ROS 2 the function to call later.

The timer produces:

```text
0.5 sec → publish_news()
0.5 sec → publish_news()
0.5 sec → publish_news()
...
```

---

# Step 10 — `publish_news()` Function

Now we have:

```python
def publish_news(self):
```

This is our own function.

Its job is to:

1. Create a message
2. Put text into the message
3. Publish the message

---

## Create Message

```python
msg = String()
```

Creates a new `String` message.

---

## Add Data

```python
msg.data = (
    "Hii, this is "
    + self.robot_name_
    + " from the robot news station"
)
```

Since:

```python
self.robot_name_ = "C3P0"
```

the final message becomes:

```text
Hii, this is C3P0 from the robot news station
```

---

## Publish

```python
self.publisher_.publish(msg)
```

This sends the message to:

```text
/robot_news
```

So the complete function is:

```text
publish_news()
      │
      ├── Create String message
      │
      ├── Add data
      │
      └── Publish
             ↓
        /robot_news
```

---

# 📱 2. Subscriber Node

The subscriber receives the messages published by the Robot News Station.

## `smartphone.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class SmartphoneNode(Node):

    def __init__(self):

        super().__init__("smartphone")

        self.subscriber_ = self.create_subscription(
            String,
            "robot_news",
            self.callback_robot_news,
            10
        )


    def callback_robot_news(self, msg: String):

        self.get_logger().info(msg.data)


def main(args=None):

    rclpy.init(args=args)

    node = SmartphoneNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

# 🔍 Understanding the Subscriber Code

## Step 1 — Create the Class

```python
class SmartphoneNode(Node):
```

Creates a ROS 2 node called `SmartphoneNode`.

It inherits from the ROS 2 `Node` class.

---

# Step 2 — Constructor

```python
def __init__(self):
```

Runs automatically when:

```python
node = SmartphoneNode()
```

is executed.

---

# Step 3 — Initialize Node

```python
super().__init__("smartphone")
```

The ROS 2 node name becomes:

```text
/smartphone
```

---

# Step 4 — Create Subscriber

```python
self.subscriber_ = self.create_subscription(
    String,
    "robot_news",
    self.callback_robot_news,
    10
)
```

There are four important parts:

```text
String
   ↓
Message type

"robot_news"
   ↓
Topic

self.callback_robot_news
   ↓
Function to execute

10
   ↓
Queue depth
```

So the subscriber means:

> Listen to `/robot_news`. When a `String` message arrives, call `callback_robot_news()`.

---

# 🔔 Step 5 — Callback Function

```python
def callback_robot_news(self, msg: String):
```

This is a **callback function**.

ROS 2 automatically calls it whenever a new message arrives.

The received message is stored in:

```python
msg
```

For example:

```text
msg
 └── data
      └── "Hii, this is C3P0 from the robot news station"
```

---

# Step 6 — Read the Message

```python
self.get_logger().info(msg.data)
```

`msg.data` contains the actual string.

So the terminal displays:

```text
[INFO] [smartphone]: Hii, this is C3P0 from the robot news station
```

---

# 🧠 Understanding the Callback Workflow

The subscriber doesn't continuously call:

```python
callback_robot_news()
```

Instead, ROS 2 waits for a message.

```text
Subscriber
    │
    │ Waiting...
    ↓
Message arrives
    │
    ↓
ROS 2 automatically calls
    │
    ↓
callback_robot_news(msg)
    │
    ↓
msg.data
    │
    ↓
Print message
```

This is the basic idea behind callbacks in ROS 2.

---

# 🚀 The `main()` Function

Both programs contain:

```python
def main(args=None):
```

`main()` is the main entry point of the program.

It performs three important things:

```text
main()
  │
  ├── Initialize ROS 2
  │
  ├── Create Node
  │
  └── Keep Node running
```

---

## 1. Initialize ROS 2

```python
rclpy.init(args=args)
```

This initializes the ROS 2 Python communication system.

---

## 2. Create the Node

Publisher:

```python
node = RobotNewsStationNode()
```

Subscriber:

```python
node = SmartphoneNode()
```

Creating the object automatically calls its:

```python
__init__()
```

---

## 3. Keep the Node Running

```python
rclpy.spin(node)
```

`spin()` keeps the node alive and processes ROS 2 events.

For the publisher:

```text
spin()
  ↓
Timer event
  ↓
publish_news()
```

For the subscriber:

```text
spin()
  ↓
Message arrives
  ↓
callback_robot_news()
```

---

## 4. Shutdown

When the program is stopped:

```python
rclpy.shutdown()
```

shuts down the ROS 2 communication system.

Usually the program is stopped using:

```text
Ctrl + C
```

---

# 🧩 Complete Python Program Flow

The publisher works like this:

```text
main()
  ↓
rclpy.init()
  ↓
RobotNewsStationNode()
  ↓
__init__()
  ↓
Create Publisher
  ↓
Create Timer
  ↓
rclpy.spin()
  ↓
Timer every 0.5 sec
  ↓
publish_news()
  ↓
Create String
  ↓
Add data
  ↓
publish()
  ↓
/robot_news
```

The subscriber works like this:

```text
main()
  ↓
rclpy.init()
  ↓
SmartphoneNode()
  ↓
__init__()
  ↓
Create Subscriber
  ↓
rclpy.spin()
  ↓
Wait for message
  ↓
Message arrives
  ↓
callback_robot_news()
  ↓
msg.data
  ↓
Logger
```

---

# 🔄 Complete ROS 2 Communication

Putting both nodes together:

```text
┌────────────────────────────┐
│   RobotNewsStationNode     │
│                            │
│   class                    │
│       │                    │
│       └── __init__()       │
│              │             │
│              ↓             │
│         Publisher          │
│              │             │
│              ↓             │
│       publish_news()       │
└──────────────┬─────────────┘
               │
               │ publish()
               ↓
        ┌──────────────┐
        │ /robot_news  │
        └──────┬───────┘
               │
               │ String message
               ↓
┌────────────────────────────┐
│       SmartphoneNode       │
│                            │
│   class                    │
│       │                    │
│       └── __init__()       │
│              │             │
│              ↓             │
│         Subscriber         │
│              │             │
│              ↓             │
│   callback_robot_news()    │
│              │             │
│              ↓             │
│          msg.data           │
└────────────────────────────┘
```

---

# 📦 `setup.py` — Creating Executables

Writing Python nodes isn't enough to run them using:

```bash
ros2 run my_py_pkg robot_news_station
```

We need to tell ROS 2 which Python files should become executables.

Open:

```text
my_py_pkg/setup.py
```

Add:

```python
entry_points={
    'console_scripts': [

        "robot_news_station = my_py_pkg.robot_news_station:main",

        "smartphone = my_py_pkg.smartphone:main",

    ],
},
```

---

# 🔍 Understanding `entry_points`

Consider:

```python
"robot_news_station = my_py_pkg.robot_news_station:main",
```

The format is:

```text
executable_name = package.module:function
```

So:

```text
robot_news_station
        ↓
Executable name
```

```text
my_py_pkg.robot_news_station
        ↓
Python module
```

```text
main
        ↓
Function to execute
```

Therefore:

```bash
ros2 run my_py_pkg robot_news_station
```

runs:

```python
main()
```

from:

```text
my_py_pkg/robot_news_station.py
```

Similarly:

```python
"smartphone = my_py_pkg.smartphone:main",
```

allows:

```bash
ros2 run my_py_pkg smartphone
```

---

# 📦 `package.xml` — Declaring Dependencies

Our Python code uses:

```python
from example_interfaces.msg import String
```

Therefore, our package needs the `example_interfaces` package.

Open:

```text
my_py_pkg/package.xml
```

and add:

```xml
<depend>example_interfaces</depend>
```

This tells ROS 2:

> This package depends on `example_interfaces`.

The dependency relationship is:

```text
my_py_pkg
    │
    ↓
example_interfaces
    │
    ↓
String message
```

---

# 📁 Final Package Structure

```text
ros2_ws/
└── src/
    └── my_py_pkg/
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        │
        └── my_py_pkg/
            ├── __init__.py
            ├── robot_news_station.py
            └── smartphone.py
```

---

# 🔎 Useful ROS 2 CLI Commands

## List Nodes

```bash
ros2 node list
```

Expected:

```text
/robot_news_station
/smartphone
```

---

## List Topics

```bash
ros2 topic list
```

You should see:

```text
/robot_news
```

---

## Topic Information

```bash
ros2 topic info /robot_news
```

Example:

```text
Type: example_interfaces/msg/String
Publisher count: 1
Subscription count: 1
```

---

## Check Topic Type

```bash
ros2 topic type /robot_news
```

Output:

```text
example_interfaces/msg/String
```

---

## View Topic Messages

```bash
ros2 topic echo /robot_news
```

Output:

```text
data: Hii, this is C3P0 from the robot news station
---
data: Hii, this is C3P0 from the robot news station
---
```

---

## Check Publishing Frequency

```bash
ros2 topic hz /robot_news
```

Expected approximately:

```text
average rate: 2.0
```

because:

```text
Frequency = 1 / Period
          = 1 / 0.5
          = 2 Hz
```

---

# 🤖 Why Topics Matter in Robotics

Topics are heavily used in real robots.

For example:

### Camera

```text
Camera Node
    ↓
/camera/image_raw
    ↓
Object Detection Node
```

### LiDAR

```text
LiDAR Node
    ↓
/scan
    ↓
SLAM Node
```

### IMU

```text
IMU Node
    ↓
/imu/data
    ↓
Localization Node
```

### Robot Motion

```text
Navigation Node
    ↓
/cmd_vel
    ↓
Motor Controller
    ↓
Motors
```

This modular architecture allows every node to focus on a particular task.

---

# 📊 Publisher vs Subscriber

| Feature       | Publisher            | Subscriber              |
| ------------- | -------------------- | ----------------------- |
| Purpose       | Sends data           | Receives data           |
| API           | `create_publisher()` | `create_subscription()` |
| Topic         | `/robot_news`        | `/robot_news`           |
| Message       | `String`             | `String`                |
| Main function | `publish_news()`     | `callback_robot_news()` |
| Communication | Publishes            | Subscribes              |

---

# 🧠 Key Takeaways

After completing this topic, I learned:

* What a **ROS 2 Topic** is
* How nodes communicate using topics
* What a **Publisher** does
* What a **Subscriber** does
* How `create_publisher()` works
* How `create_subscription()` works
* How ROS 2 callbacks work
* What `__init__()` does
* What `self` means in Python classes
* How Python classes and inheritance are used in ROS 2
* How `rclpy.spin()` keeps a node alive
* How to register Python executables using `setup.py`
* How to declare dependencies using `package.xml`
* How to inspect topics using ROS 2 CLI commands

The most important architecture to remember is:

```text
Node
 ↓
Publisher
 ↓
Topic
 ↓
Subscriber
 ↓
Node
```

Or simply:

> **Node → Publish → Topic → Subscribe → Node**

---

# ▶️ How to Build and Run

Make sure you are using **ROS 2 Jazzy** and your workspace is:

```text
~/ros2_ws
```

## 1. Source ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 2. Go to Workspace

```bash
cd ~/ros2_ws
```

---

## 3. Build the Package

After modifying `setup.py` or `package.xml`:

```bash
colcon build --packages-select my_py_pkg
```

---

## 4. Source the Workspace

```bash
source install/setup.bash
```

---

## 5. Run the Publisher

Open **Terminal 1**:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg robot_news_station
```

You should see:

```text
[INFO] [robot_news_station]: Robot News Station has been started.
```

Keep this terminal running.

---

## 6. Run the Subscriber

Open **Terminal 2**:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_py_pkg smartphone
```

You should see:

```text
[INFO] [smartphone]: Hii, this is C3P0 from the robot news station
[INFO] [smartphone]: Hii, this is C3P0 from the robot news station
[INFO] [smartphone]: Hii, this is C3P0 from the robot news station
```

The message will continue approximately every **0.5 seconds**.

---

## 7. Inspect the Communication

Open **Terminal 3**:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

### List Nodes

```bash
ros2 node list
```

### List Topics

```bash
ros2 topic list
```

### Topic Information

```bash
ros2 topic info /robot_news
```

### Topic Type

```bash
ros2 topic type /robot_news
```

### View Messages

```bash
ros2 topic echo /robot_news
```

### Check Publishing Rate

```bash
ros2 topic hz /robot_news
```

---

# 🚀 Final Result

After running both nodes:

```text
             ROS 2
               │
       ┌───────┴────────┐
       ↓                ↓
RobotNewsStation     Smartphone
       │                ↑
       │                │
       │ publish        │ subscribe
       ↓                │
    /robot_news ────────┘
       │
       ↓
  String Message
```

This simple example demonstrates the basic communication architecture used throughout ROS 2 and provides the foundation for working with real robot sensors, controllers, navigation systems, perception pipelines, and autonomous robots.

---

# 📚 ROS 2 Learning Series

This README is part of my ongoing **ROS 2 Learning Series**, where I am documenting my learning journey through GitHub and LinkedIn.

**Learn → Build → Document → Repeat 🤖**
