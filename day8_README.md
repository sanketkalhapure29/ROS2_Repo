# 🐢 ROS 2 Turtlesim — Catch Them All

> **Day 8 of my ROS 2 Learning Journey**

A complete ROS 2 project built using **Python, Turtlesim, Topics, Services, Custom Interfaces, Parameters, Timers, Publishers, Subscribers, Service Clients, Service Servers, and ROS 2 nodes**.

The goal of this project is to build a small autonomous system where one main turtle continuously searches for and catches randomly spawned turtles.

---

# 📌 Table of Contents

* [Project Overview](#-project-overview)
* [Project Goal](#-project-goal)
* [Final Behavior](#-final-behavior)
* [ROS 2 Concepts Used](#-ros-2-concepts-used)
* [System Architecture](#-system-architecture)
* [Node Architecture](#-node-architecture)
* [Communication Architecture](#-communication-architecture)
* [Custom Interfaces](#-custom-interfaces)
* [Spawner Node](#-1-turtle-spawner-node)
* [Controller Node](#-2-turtle-controller-node)
* [How the Controller Finds the Closest Turtle](#-how-the-controller-finds-the-closest-turtle)
* [How the Turtle Moves Toward the Target](#-how-the-turtle-moves-toward-the-target)
* [How a Turtle Gets Caught](#-how-a-turtle-gets-caught)
* [ROS 2 Parameters](#-ros-2-parameters)
* [Package Structure](#-package-structure)
* [Dependencies](#-dependencies)
* [Build the Project](#-build-the-project)
* [Run the Project](#-run-the-project)
* [Useful ROS 2 Commands](#-useful-ros-2-commands)
* [Complete Workflow](#-complete-workflow)
* [Important Concepts Learned](#-important-concepts-learned)
* [Possible Improvements](#-possible-improvements)
* [Key Takeaways](#-key-takeaways)

---

# 🚀 Project Overview

The **Turtlesim Catch Them All** project is a small autonomous robotics simulation.

Instead of manually controlling the turtle, the system automatically:

1. Starts Turtlesim.
2. Randomly spawns new turtles.
3. Keeps track of all currently alive turtles.
4. Selects a turtle to catch.
5. Calculates the distance between the main turtle and the target.
6. Calculates the direction toward the target.
7. Publishes velocity commands.
8. Moves the main turtle toward the target.
9. Calls a custom service when the turtle reaches the target.
10. Removes the caught turtle.
11. Repeats the process.

The project therefore combines many individual ROS 2 concepts into one complete application.

---

# 🎯 Project Goal

The main goal is to create an autonomous turtle that can **find and catch other turtles**.

The project is designed to practice how different ROS 2 components work together.

Instead of learning:

```text
Topics
Services
Parameters
Custom Messages
Nodes
Timers
Publishers
Subscribers
```

individually, this project combines them into one system.

---

# 🎬 Final Behavior

The final simulation looks conceptually like this:

```text
                 🐢 Target Turtle

                       ↑
                       |
                       |
                autonomous movement
                       |
                       |
                 🐢 turtle1
                 Main Turtle
```

New turtles continuously appear at random positions.

The controller determines which turtle should be caught and moves `turtle1` toward it.

Once the target is close enough:

```text
Target detected
      ↓
Move toward target
      ↓
Distance <= 0.5
      ↓
Call catch_turtle service
      ↓
Spawner calls /kill
      ↓
Target turtle disappears
      ↓
Select another turtle
      ↓
Repeat
```

---

# 🧠 ROS 2 Concepts Used

This project combines the following ROS 2 concepts:

### Nodes

Two custom application nodes are used:

```text
turtle_spawner
turtle_controller
```

---

### Topics

Topics are used for continuous data communication.

Examples:

```text
/alive_turtles
/turtle1/pose
/turtle1/cmd_vel
```

---

### Services

Services are used for request/response communication.

Examples:

```text
/spawn
/kill
/catch_turtle
```

---

### Custom Messages

The project uses custom interfaces from:

```text
my_robot_interfaces
```

Including:

```text
Turtle.msg
TurtleArray.msg
```

---

### Custom Service

The project also uses:

```text
CatchTurtle.srv
```

---

### Parameters

The nodes use ROS 2 parameters to change behavior without modifying the source code.

---

### Timers

Timers are used to:

* periodically spawn turtles
* continuously execute the controller loop

---

### Publishers

The nodes publish:

```text
alive_turtles
/turtle1/cmd_vel
```

---

### Subscribers

The controller subscribes to:

```text
/turtle1/pose
alive_turtles
```

---

### Service Clients

The nodes communicate with turtlesim services:

```text
/spawn
/kill
```

---

### Service Server

The spawner provides:

```text
catch_turtle
```

---

# 🏗️ System Architecture

The complete architecture can be represented as:

```text
                         ┌─────────────────────┐
                         │     Turtlesim       │
                         │                     │
                         │     turtle1         │
                         │     turtle2         │
                         │     turtle3         │
                         │       ...           │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                  /spawn                           /kill
                    │                               │
                    ▼                               ▲
          ┌──────────────────┐             ┌────────┴─────────┐
          │ Turtle Spawner   │             │ Catch Turtle     │
          │                  │             │ Service          │
          └────────┬─────────┘             └────────▲─────────┘
                   │                                │
                   │ alive_turtles                  │
                   ▼                                │
          ┌──────────────────┐                      │
          │ Turtle Controller│──────────────────────┘
          │                  │
          └────────┬─────────┘
                   │
                   │ /turtle1/cmd_vel
                   ▼
              🐢 turtle1
```

---

# 🔄 Node Architecture

There are two main custom nodes.

## 1. Turtle Spawner

```text
Node Name:
turtle_spawner
```

Responsibilities:

* Generate random turtle positions.
* Request Turtlesim to spawn turtles.
* Maintain a list of alive turtles.
* Publish information about alive turtles.
* Provide the `catch_turtle` service.
* Remove turtles using the `/kill` service.

---

## 2. Turtle Controller

```text
Node Name:
turtle_controller
```

Responsibilities:

* Receive the current pose of `turtle1`.
* Receive information about alive turtles.
* Select a target turtle.
* Calculate distance to target.
* Calculate target direction.
* Generate velocity commands.
* Move `turtle1`.
* Call the `catch_turtle` service when the target is reached.

---

# 🔌 Communication Architecture

## Topic 1 — `/turtle1/pose`

Turtlesim publishes the current pose of `turtle1`.

Message type:

```text
turtlesim/msg/Pose
```

The controller subscribes to this topic.

It receives:

```text
x
y
theta
```

The controller stores this information as its current robot state.

---

# Topic 2 — `/turtle1/cmd_vel`

The controller publishes:

```text
geometry_msgs/msg/Twist
```

This message controls the movement of `turtle1`.

The controller sets:

```text
linear.x
angular.z
```

to control:

* forward velocity
* rotational velocity

---

# Topic 3 — `alive_turtles`

The spawner publishes information about all currently alive turtles.

Message:

```text
my_robot_interfaces/msg/TurtleArray
```

The controller subscribes to this topic.

The custom message contains multiple:

```text
Turtle
```

objects.

Each turtle contains:

```text
name
x
y
theta
```

---

# 🔧 Custom Interfaces

The project uses the custom package:

```text
my_robot_interfaces
```

The package contains custom messages and services.

---

## `Turtle.msg`

The Turtle message contains:

```text
string name
float64 x
float64 y
float64 theta
```

This represents one turtle and its position/orientation.

---

## `TurtleArray.msg`

This message contains an array of turtles.

Conceptually:

```text
Turtle[] turtles
```

It allows the spawner to publish information about all currently alive turtles.

---

## `CatchTurtle.srv`

The controller sends the name of the turtle it wants to catch.

Conceptually:

```text
string name
---
bool success
```

The request contains the turtle name.

The response tells whether the turtle was successfully caught.

---

# 🐢 1. Turtle Spawner Node

The spawner node is responsible for continuously creating turtles.

The node is named:

```text
turtle_spawner
```

The implementation creates:

```text
alive_turtles
```

publisher:

```text
TurtleArray
```

It also creates clients for:

```text
/spawn
/kill
```

and provides:

```text
catch_turtle
```

service.

The actual implementation creates the `alive_turtles` publisher, `/spawn` client, `/kill` client, and `catch_turtle` service.

---

# 🎲 Random Turtle Generation

Every time the spawning timer executes, a new turtle is generated.

The turtle receives:

```text
name
x
y
theta
```

The position is randomly generated.

Conceptually:

```text
x     → random position
y     → random position
theta → random orientation
```

The implementation uses random values for `x`, `y`, and `theta`.

---

# 📡 Calling the `/spawn` Service

The spawner creates a client for:

```text
/spawn
```

and sends:

```text
x
y
theta
name
```

to Turtlesim.

The response contains the name of the newly created turtle.

The spawner then creates a custom `Turtle` message and stores it in:

```text
alive_turtles_
```

before publishing the updated `TurtleArray`.

---

# 📝 Maintaining the Alive Turtle List

The spawner maintains:

```text
alive_turtles_
```

This list represents all turtles that are currently alive.

When a new turtle is spawned:

```text
New turtle
    ↓
Create Turtle message
    ↓
Add to alive_turtles_
    ↓
Publish TurtleArray
```

When a turtle is caught:

```text
Catch request
    ↓
Call /kill
    ↓
Remove turtle from alive_turtles_
    ↓
Publish updated TurtleArray
```

The removal logic searches for the turtle by name and deletes it from the list.

---

# 🎯 2. Turtle Controller Node

The controller node is named:

```text
turtle_controller
```

It controls the main turtle:

```text
turtle1
```

The controller:

* receives turtle1's pose
* receives alive turtles
* selects a target
* calculates distance
* calculates orientation
* publishes velocity
* catches the target

The controller's publishers, subscribers, service client, and control-loop timer are created in its constructor.

---

# 📍 Receiving Turtle Pose

The controller subscribes to:

```text
/turtle1/pose
```

Message:

```text
turtlesim/msg/Pose
```

The callback stores the latest pose:

```text
self.pose_
```

The controller therefore always knows:

```text
Current X
Current Y
Current orientation
```

The uploaded implementation stores the incoming `Pose` directly in `self.pose_`.

---

# 🎯 Selecting a Target

The controller receives:

```text
alive_turtles
```

through:

```text
TurtleArray
```

If there are alive turtles, the controller selects one.

There are two possible behaviors controlled by a parameter:

```text
catch_closest_turtle_first
```

---

## Option 1 — Closest Turtle

If:

```text
catch_closest_turtle_first = True
```

the controller calculates the distance to every turtle.

For every target:

```text
distance =
sqrt((target_x - current_x)² +
     (target_y - current_y)²)
```

Then it selects the turtle with the smallest distance.

The implementation performs this comparison across the received turtle list.

---

## Option 2 — First Turtle

If the parameter is:

```text
False
```

the controller simply selects:

```text
msg.turtles[0]
```

This provides two different target-selection strategies without changing the source code.

---

# 📐 Distance Calculation

Suppose:

```text
Current position:

x1 = 5
y1 = 5

Target:

x2 = 8
y2 = 9
```

Then:

```text
dx = x2 - x1
dy = y2 - y1
```

and:

```text
distance = sqrt(dx² + dy²)
```

The controller uses exactly this Euclidean distance calculation to determine how far the target turtle is.

---

# 🧭 Calculating the Target Direction

The controller calculates:

```text
goal_theta = atan2(dy, dx)
```

This determines the angle from the main turtle toward the target.

Then:

```text
difference =
goal_theta - current_theta
```

The difference is normalized so that the turtle chooses the appropriate rotational direction.

The controller uses `atan2()` and adjusts the angle into the `[-π, π]` range.

---

# 🎮 Velocity Controller

The controller generates a:

```text
geometry_msgs/msg/Twist
```

message.

When the target is farther than:

```text
0.5
```

the controller calculates:

```text
linear.x = 2 * distance
```

and:

```text
angular.z = 6 * angle_difference
```

This creates a simple proportional control behavior.

Conceptually:

```text
Large distance
      ↓
Higher linear velocity

Large angle error
      ↓
Higher angular velocity
```

The corresponding control logic is implemented in the controller's `control_loop()`.

---

# 🏁 Target Reached

When:

```text
distance <= 0.5
```

the controller considers the target reached.

It sets:

```text
linear.x = 0
angular.z = 0
```

and calls:

```text
catch_turtle
```

with the target's name.

---

# 🪦 Catching the Turtle

The controller does **not directly call `/kill`**.

Instead:

```text
Controller
     |
     | catch_turtle
     ↓
Spawner
     |
     | /kill
     ↓
Turtlesim
```

This is an important ROS2 architecture decision.

The spawner owns the turtle-management functionality, so it is responsible for removing turtles.

The controller only requests:

```text
"Catch this turtle."
```

---

# 🔄 Complete Catching Workflow

```text
Controller reaches target
          ↓
distance <= 0.5
          ↓
Create CatchTurtle request
          ↓
Send turtle name
          ↓
Spawner receives request
          ↓
Spawner calls /kill
          ↓
Turtlesim removes turtle
          ↓
Spawner removes turtle from list
          ↓
Spawner publishes updated alive_turtles
          ↓
Controller selects another target
          ↓
Process repeats
```

The controller sends the catch request asynchronously and checks the service response through a callback.

---

# ⚙️ ROS 2 Parameters

The project uses parameters to make the application configurable.

## Spawner Parameters

### `turtle_name_prefix`

Default:

```text
turtle
```

This controls the name prefix used for generated turtles.

For example:

```text
turtle1
turtle2
turtle3
...
```

### `spawn_frequency`

Default:

```text
1.0
```

This controls how frequently new turtles are spawned.

The spawner declares and reads both parameters during initialization.

---

## Controller Parameter

### `catch_closest_turtle_first`

Default:

```text
true
```

If true:

```text
Catch nearest turtle
```

If false:

```text
Catch first turtle in the list
```

The controller declares and reads this parameter during initialization.

---

# 📁 Package Structure

The package is:

```text
turtlesim_catch_them_all
```

A typical structure is:

```text
turtlesim_catch_them_all/
│
├── package.xml
├── setup.py
├── setup.cfg
│
├── resource/
│   └── turtlesim_catch_them_all
│
└── turtlesim_catch_them_all/
    ├── __init__.py
    ├── turtle_spawner.py
    └── turtle_controller.py
```

The uploaded package is an `ament_python` package and declares dependencies on `rclpy`, `turtlesim`, `geometry_msgs`, and `my_robot_interfaces`.

---

# 🔗 Package Dependencies

The project requires:

```text
rclpy
turtlesim
geometry_msgs
my_robot_interfaces
```

### `rclpy`

Python client library for ROS 2.

Used for:

* Nodes
* Publishers
* Subscribers
* Services
* Timers
* Parameters

---

### `turtlesim`

Provides:

* Turtle simulation
* `/spawn`
* `/kill`
* `/turtle1/pose`
* `/turtle1/cmd_vel`

---

### `geometry_msgs`

Provides:

```text
Twist
```

which is used to control turtle velocity.

---

### `my_robot_interfaces`

Provides the project's custom:

```text
Turtle.msg
TurtleArray.msg
CatchTurtle.srv
```

---

# 🛠️ Build the Project

Go to your workspace:

```bash
cd ~/ros2_ws
```

Build the custom interfaces first:

```bash
colcon build --packages-select my_robot_interfaces
```

Source the workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Then build the project:

```bash
colcon build --packages-select turtlesim_catch_them_all
```

Source again:

```bash
source ~/ros2_ws/install/setup.bash
```

---

# ▶️ Run the Project

You need **three terminals**.

---

## Terminal 1 — Start Turtlesim

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

You should see the Turtlesim window.

---

## Terminal 2 — Start Turtle Spawner

```bash
source ~/ros2_ws/install/setup.bash
ros2 run turtlesim_catch_them_all turtle_spawner
```

The spawner will begin creating turtles.

You should see messages similar to:

```text
New alive turtle: turtle1
New alive turtle: turtle2
New alive turtle: turtle3
```

---

## Terminal 3 — Start Turtle Controller

```bash
source ~/ros2_ws/install/setup.bash
ros2 run turtlesim_catch_them_all turtle_controller
```

The controller will:

```text
Receive turtle positions
        ↓
Select target
        ↓
Calculate distance
        ↓
Calculate angle
        ↓
Move turtle1
        ↓
Catch target
        ↓
Repeat
```

---

# ⚡ Run With Parameters

You can change the spawner frequency without modifying the code.

Example:

```bash
ros2 run turtlesim_catch_them_all turtle_spawner --ros-args -p spawn_frequency:=2.0
```

This makes the spawning frequency:

```text
2 turtles/second
```

You can also change the turtle prefix:

```bash
ros2 run turtlesim_catch_them_all turtle_spawner --ros-args -p turtle_name_prefix:=enemy
```

The generated names will then use:

```text
enemy1
enemy2
enemy3
...
```

---

## Change Target Selection

Closest turtle:

```bash
ros2 run turtlesim_catch_them_all turtle_controller --ros-args -p catch_closest_turtle_first:=true
```

First turtle:

```bash
ros2 run turtlesim_catch_them_all turtle_controller --ros-args -p catch_closest_turtle_first:=false
```

---

# 🔍 Useful ROS 2 Commands

## List Nodes

```bash
ros2 node list
```

Expected nodes include:

```text
/turtlesim
/turtle_spawner
/turtle_controller
```

---

## List Topics

```bash
ros2 topic list
```

Important topics:

```text
/turtle1/pose
/turtle1/cmd_vel
/alive_turtles
```

---

## Inspect Alive Turtles

```bash
ros2 topic echo /alive_turtles
```

This lets you see the custom `TurtleArray` message being published.

---

## Inspect Turtle Pose

```bash
ros2 topic echo /turtle1/pose
```

---

## Inspect Velocity Commands

```bash
ros2 topic echo /turtle1/cmd_vel
```

---

## List Services

```bash
ros2 service list
```

Important services include:

```text
/spawn
/kill
/catch_turtle
```

---

## Inspect Catch Service

```bash
ros2 interface show my_robot_interfaces/srv/CatchTurtle
```

---

## Inspect Turtle Message

```bash
ros2 interface show my_robot_interfaces/msg/Turtle
```

---

## Inspect Turtle Array

```bash
ros2 interface show my_robot_interfaces/msg/TurtleArray
```

---

## Inspect Node

```bash
ros2 node info /turtle_spawner
```

and:

```bash
ros2 node info /turtle_controller
```

These commands are very useful for understanding:

* publishers
* subscribers
* services
* clients

associated with each node.

---

# 🧩 Complete Project Workflow

The complete system works like this:

```text
                 START
                   │
                   ▼
            Start Turtlesim
                   │
                   ▼
          Start Turtle Spawner
                   │
                   ▼
       Generate random coordinates
                   │
                   ▼
             Call /spawn
                   │
                   ▼
             Turtle created
                   │
                   ▼
        Add turtle to alive list
                   │
                   ▼
         Publish alive_turtles
                   │
                   ▼
        Controller receives list
                   │
                   ▼
       Select target turtle
                   │
                   ▼
        Calculate distance
                   │
                   ▼
        Calculate target angle
                   │
                   ▼
       Publish Twist command
                   │
                   ▼
             turtle1 moves
                   │
                   ▼
          Is distance <= 0.5?
             /           \
           NO             YES
           │               │
           │               ▼
           │        Call catch_turtle
           │               │
           │               ▼
           │       Spawner calls /kill
           │               │
           │               ▼
           │       Remove from list
           │               │
           │               ▼
           │      Publish new list
           │               │
           └───────────────┘
                   │
                   ▼
             Select next turtle
                   │
                   ▼
                 REPEAT
```

---

# 🧠 What I Learned From This Project

This project was different from writing individual ROS 2 examples because multiple ROS 2 concepts had to work together.

### 1. Designing before coding

Instead of immediately writing code, the project required thinking about:

```text
What nodes do I need?

Who publishes?

Who subscribes?

Who provides services?

Who calls services?

Where should each functionality live?
```

This is an important step toward designing larger ROS 2 systems.

---

### 2. Node responsibilities

The project demonstrates why functionality should be separated between nodes.

Instead of putting everything into one node:

```text
Spawner
+
Controller
+
Movement
+
Turtle management
```

the system separates responsibilities.

```text
Spawner
    ↓
Turtle management

Controller
    ↓
Movement + target selection
```

This makes the architecture easier to understand and extend.

---

### 3. Topics vs Services

This project uses both.

### Topics

Used for continuous information:

```text
/turtle1/pose
alive_turtles
/turtle1/cmd_vel
```

### Services

Used for specific requests:

```text
/spawn
/kill
catch_turtle
```

This is a practical example of choosing the appropriate ROS 2 communication mechanism.

---

### 4. Custom Interfaces

Instead of using only standard ROS 2 messages, the project uses:

```text
Turtle
TurtleArray
CatchTurtle
```

This demonstrates how custom interfaces can represent application-specific data.

---

### 5. Service chaining

One particularly useful architecture is:

```text
Controller
    ↓
catch_turtle
    ↓
Spawner
    ↓
/kill
    ↓
Turtlesim
```

The controller doesn't need to know how the turtle is actually removed.

It simply requests the operation.

---

### 6. Basic autonomous behavior

The controller implements a simple autonomous behavior:

```text
Sense
 ↓
Decide
 ↓
Act
 ↓
Sense again
 ↓
Decide again
 ↓
Act again
```

This is a simplified version of the same fundamental loop used in many autonomous robotic systems.

---

# 🚀 Possible Improvements

This project can be extended significantly.

## 1. Better Motion Control

The current controller uses proportional control.

A more advanced controller could implement:

```text
PID control
```

for smoother movement.

---

## 2. Collision Avoidance

The turtle currently doesn't intelligently avoid other turtles or obstacles.

A future version could implement:

```text
Obstacle detection
+
Collision avoidance
```

---

## 3. Better Target Selection

Instead of only:

```text
closest turtle
```

you could select based on:

```text
distance
priority
orientation
time alive
```

---

## 4. Visualization

You could visualize:

```text
Current target
Distance
Target direction
Number of alive turtles
```

using RViz or another visualization approach.

---

## 5. Launch File

Instead of opening three terminals manually, create a ROS 2 launch file that starts:

```text
turtlesim
turtle_spawner
turtle_controller
```

with a single command.

For example:

```bash
ros2 launch turtlesim_catch_them_all catch_them_all.launch.py
```

---

## 6. Dynamic Parameters

The parameters could be changed while the system is running.

For example:

```text
spawn_frequency
catch_closest_turtle_first
```

could be modified at runtime.

---

# 📌 Key Takeaways

This project brought together many ROS 2 concepts into one working application:

```text
ROS 2 Nodes
      +
Topics
      +
Services
      +
Custom Messages
      +
Custom Services
      +
Parameters
      +
Timers
      +
Publishers
      +
Subscribers
      +
Service Clients
      +
Service Servers
      +
Turtlesim
      ↓
Complete ROS 2 Application
```

The most important lesson was not simply making the turtle move.

It was learning how to **design a ROS 2 system**, divide responsibilities between nodes, choose appropriate communication mechanisms, create custom interfaces, and connect everything into a scalable application.

---

# 🏁 Final Result

The final project demonstrates a complete ROS 2 workflow:

```text
Random Turtle Generation
          ↓
Custom Message
          ↓
Target Selection
          ↓
Distance Calculation
          ↓
Angle Calculation
          ↓
Velocity Control
          ↓
Target Reached
          ↓
Custom Service
          ↓
Turtle Removal
          ↓
Next Target
```

This was my **Day 8 of learning ROS 2**, and it was a major step from understanding individual ROS 2 concepts to actually combining them into a complete robotic application.

---

## 📚 ROS 2 Concepts Practiced

* Nodes
* Topics
* Publishers
* Subscribers
* Services
* Service Clients
* Service Servers
* Custom Messages
* Custom Services
* Parameters
* Timers
* Turtlesim
* `geometry_msgs/Twist`
* `turtlesim/Pose`
* Asynchronous service calls
* Callbacks
* Distance calculation
* Angle calculation
* Basic proportional control
* ROS 2 package architecture
* Multi-node system design

---

# ⭐ Day 8 Complete

**Project:** Turtlesim Catch Them All
**Platform:** ROS 2 Jazzy
**Language:** Python
**Simulation:** Turtlesim
**Focus:** Complete ROS 2 Application Development

> **From learning individual ROS 2 concepts to integrating them into a complete autonomous application.**
