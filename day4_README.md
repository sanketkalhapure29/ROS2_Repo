# ROS 2 Topics: Making Nodes Communicate With Each Other 🤖

Welcome to **Day 4 of my ROS 2 Learning Series**.

Today I learned one of the most fundamental concepts in ROS 2: **Topics**.

ROS 2 allows different nodes to communicate with each other using topics. In this example, I created a **Robot News Station** that publishes news messages and a **Smartphone** node that subscribes to those messages.

---

## 📌 What are ROS 2 Topics?

A **Topic** is a named communication channel in ROS 2.

One node can **publish** data to a topic, while one or more nodes can **subscribe** to that topic.

The basic communication model is:

```text
Publisher Node
      │
      │ publish()
      ↓
   /topic
      │
      │ message
      ↓
Subscriber Node
```

In this project:

```text
Robot News Station
       │
       │ Publisher
       ↓
  /robot_news
       │
       │ String message
       ↓
   Smartphone
       │
       │ Subscriber
       ↓
     Logger
```

The publisher and subscriber do not directly communicate with each other. The **topic acts as the communication channel between them**.

---

# 🧠 ROS 2 Concepts Used

This example uses four important ROS 2 concepts:

| Concept        | Purpose                                 |
| -------------- | --------------------------------------- |
| **Node**       | A process that performs a specific task |
| **Publisher**  | Sends messages to a topic               |
| **Subscriber** | Receives messages from a topic          |
| **Topic**      | Communication channel between nodes     |

---

# 📁 Package Structure

The package used for this example is:

```text
my_py_pkg/
├── package.xml
├── setup.py
├── setup.cfg
└── my_py_pkg/
    ├── __init__.py
    ├── robot_news_station.py
    └── smartphone.py
```

The two Python files represent two different ROS 2 nodes:

```text
robot_news_station.py
        ↓
Publisher

smartphone.py
        ↓
Subscriber
```

---

# 📢 1. Publisher Node — Robot News Station

The first node publishes a message every **0.5 seconds**.

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

# 🔍 Understanding the Publisher

## Creating the Node

```python
super().__init__("robot_news_station")
```

This creates a ROS 2 node named:

```text
/robot_news_station
```

You can verify it using:

```bash
ros2 node list
```

---

## Creating the Publisher

```python
self.publisher_ = self.create_publisher(
    String,
    "robot_news",
    10
)
```

This creates a publisher.

It has three important parameters:

### Message Type

```python
String
```

The publisher sends `String` messages.

### Topic Name

```python
"robot_news"
```

The topic is:

```text
/robot_news
```

### Queue Depth

```python
10
```

This specifies the queue depth.

---

# ⏱️ Creating the Timer

```python
self.timer_ = self.create_timer(
    0.5,
    self.publish_news
)
```

This tells ROS 2:

> Call `publish_news()` every 0.5 seconds.

Therefore:

```text
0.0 sec → publish_news()
0.5 sec → publish_news()
1.0 sec → publish_news()
1.5 sec → publish_news()
2.0 sec → publish_news()
...
```

Since:

```text
Period = 0.5 seconds
```

the approximate publishing frequency is:

```text
Frequency = 1 / 0.5
          = 2 Hz
```

---

# 📨 Creating the Message

Inside `publish_news()`:

```python
msg = String()
```

creates a new `String` message.

Then:

```python
msg.data = (
    "Hii, this is "
    + self.robot_name_
    + " from the robot news station"
)
```

creates:

```text
Hii, this is C3P0 from the robot news station
```

Finally:

```python
self.publisher_.publish(msg)
```

publishes the message to:

```text
/robot_news
```

---

# 📱 2. Subscriber Node — Smartphone

The second node subscribes to `/robot_news`.

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

# 🔍 Understanding the Subscriber

## Creating the Node

```python
super().__init__("smartphone")
```

This creates a ROS 2 node named:

```text
/smartphone
```

---

## Creating the Subscriber

```python
self.subscriber_ = self.create_subscription(
    String,
    "robot_news",
    self.callback_robot_news,
    10
)
```

The subscriber has four important parameters.

### 1. Message Type

```python
String
```

The subscriber expects `String` messages.

### 2. Topic

```python
"robot_news"
```

It listens to:

```text
/robot_news
```

### 3. Callback

```python
self.callback_robot_news
```

ROS 2 calls this function whenever a message arrives.

### 4. Queue Depth

```python
10
```

The subscriber queue depth is set to 10.

---

# 🔔 What is a Callback?

A **callback** is a function that ROS 2 automatically executes when a particular event occurs.

Here:

```python
def callback_robot_news(self, msg: String):
```

is called whenever a new message is received on `/robot_news`.

Inside the callback:

```python
self.get_logger().info(msg.data)
```

prints the received message.

For example:

```text
[INFO] [smartphone]: Hii, this is C3P0 from the robot news station
```

---

# ⚙️ How `rclpy.spin()` Works

Both nodes contain:

```python
rclpy.spin(node)
```

`spin()` keeps the node alive and allows ROS 2 to process events and callbacks.

For the publisher:

```text
rclpy.spin()
      ↓
Timer reaches 0.5 sec
      ↓
publish_news()
      ↓
Publish message
```

For the subscriber:

```text
rclpy.spin()
      ↓
Wait for message
      ↓
Message arrives
      ↓
callback_robot_news()
      ↓
Print message
```

Without `rclpy.spin(node)`, the node would not remain active waiting for events.

---

# 🔄 Complete Communication Workflow

When both nodes are running, the data flows like this:

```text
┌─────────────────────────────┐
│   RobotNewsStationNode      │
│                             │
│   robot_name = "C3P0"       │
│   Publisher                 │
└──────────────┬──────────────┘
               │
               │ publish()
               ↓
       ┌────────────────┐
       │  /robot_news   │
       │                │
       │ String Message │
       └───────┬────────┘
               │
               │ message
               ↓
┌─────────────────────────────┐
│       SmartphoneNode        │
│                             │
│       Subscriber            │
│                             │
│   callback_robot_news()     │
└──────────────┬──────────────┘
               │
               ↓
          msg.data
               │
               ↓
           Terminal
```

---

# 🛠️ Configuring `setup.py`

To run Python nodes using:

```bash
ros2 run my_py_pkg robot_news_station
```

we need to register them as executable entry points.

Open:

```text
my_py_pkg/setup.py
```

and add:

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

Breaking it down:

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

will execute:

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

allows us to run:

```bash
ros2 run my_py_pkg smartphone
```

---

# 📦 Configuring `package.xml`

Our Python nodes use:

```python
from example_interfaces.msg import String
```

Therefore, the package needs the `example_interfaces` dependency.

Open:

```text
my_py_pkg/package.xml
```

and add:

```xml
<depend>example_interfaces</depend>
```

The correct syntax is:

```xml
<depend>example_interfaces</depend>
```

---

# 🧩 Why is `example_interfaces` Required?

The `String` message comes from:

```text
example_interfaces
```

Our dependency chain is:

```text
my_py_pkg
    │
    │ depends on
    ↓
example_interfaces
    │
    ↓
String
```

Without declaring this dependency, the package does not properly describe what it requires to build/run.

---

# 🔎 Useful ROS 2 CLI Commands

Once the nodes are running, ROS 2 provides several CLI commands to inspect the system.

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

## Get Topic Information

```bash
ros2 topic info /robot_news
```

You should see information similar to:

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

## View Messages Directly

You can inspect the topic without running the Smartphone node:

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

Since the publisher uses a 0.5-second timer, the result should be approximately:

```text
average rate: 2.0
```

---

# 📊 Publisher vs Subscriber

| Feature        | Publisher            | Subscriber              |
| -------------- | -------------------- | ----------------------- |
| Purpose        | Sends data           | Receives data           |
| ROS 2 API      | `create_publisher()` | `create_subscription()` |
| Topic          | `/robot_news`        | `/robot_news`           |
| Message        | `String`             | `String`                |
| Main operation | `publish()`          | Callback                |
| Node           | `robot_news_station` | `smartphone`            |

---

# 🤖 Why Topics Are Important in Robotics

Topics are heavily used in real robotic systems.

For example, a camera node can publish images:

```text
Camera Node
     │
     ↓
/camera/image_raw
     │
     ↓
Object Detection Node
```

A LiDAR can publish laser scan data:

```text
LiDAR Node
     │
     ↓
/scan
     │
     ↓
SLAM / Navigation Node
```

A navigation system can publish velocity commands:

```text
Navigation Node
       │
       ↓
    /cmd_vel
       │
       ↓
Motor Controller
       │
       ↓
    Motors
```

This modular architecture allows each ROS 2 node to focus on a specific task.

---

# 🧠 Key Takeaways

After completing this topic, I learned:

* What a **ROS 2 Topic** is
* How Publisher–Subscriber communication works
* How to create a Publisher using `create_publisher()`
* How to create a Subscriber using `create_subscription()`
* How to create and publish a `String` message
* How subscriber callbacks work
* How `rclpy.spin()` keeps nodes alive
* How to register Python nodes using `setup.py`
* How to declare dependencies using `package.xml`
* How to inspect ROS 2 nodes and topics using the ROS 2 CLI

The core concept is:

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

## 1. Source ROS 2

For ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 2. Go to the Workspace

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

The message will continue to appear approximately every **0.5 seconds**.

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

After running both nodes, the final ROS 2 system looks like:

```text
                 ROS 2
                   │
        ┌──────────┴──────────┐
        │                     │
        ↓                     ↓
robot_news_station        smartphone
        │                     ↑
        │                     │
        │ publish             │ subscribe
        ↓                     │
      /robot_news ────────────┘
        │
        ↓
   String message
```

This simple example demonstrates the basic communication architecture used throughout ROS 2 and provides the foundation for working with real robot sensors, controllers, navigation systems, perception pipelines, and autonomous robots.

---

## 📚 ROS 2 Learning Series

This README is part of my ongoing **ROS 2 Learning Series**, where I am documenting my learning journey through GitHub and LinkedIn.

🔗 **GitHub Repository:**
https://github.com/sanketkalhapure29/ROS2_Fundamentals

**Learn → Build → Document → Repeat 🤖**
