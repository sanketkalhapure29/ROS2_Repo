# ROS2 Learning Series — Day 3
## Introduction to ROS2 Tools

Day 3 focused on using ROS2 CLI tools, RQT, RQT Graph, and Turtlesim to inspect and understand a running ROS2 system.

---

## 1. ROS2 CLI — Introspection

ROS2 provides command-line tools to inspect nodes and understand what is running in the ROS2 system.

### List all running nodes

```bash
ros2 node list
```

This displays the names of all currently running ROS2 nodes.

### Get detailed information about a node

```bash
ros2 node info /camera_node
```

This provides information such as:
- Publishers
- Subscribers
- Services
- Actions
- Other node-related interfaces

> Replace `/camera_node` with the name of the node you want to inspect.

---

## 2. Rename a ROS2 Node at Runtime

A node name can be changed when launching it using ROS2 remapping:

```bash
ros2 run my_package my_node --ros-args -r __node:=new_name
```

Here:

- `my_package` → ROS2 package name
- `my_node` → executable/node name
- `__node` → special ROS2 node-name remapping rule
- `new_name` → new runtime name

This is useful when running multiple instances of the same node.

---

## 3. What is RQT?

**RQT** is a graphical user interface framework for ROS/ROS2.

Instead of checking everything through the terminal, RQT provides graphical tools called plugins for monitoring and debugging a ROS2 system.

One of the most useful plugins is:

```bash
rqt_graph
```

### RQT Graph

`rqt_graph` provides a visual representation of:

**Nodes ↔ Topics**

It helps understand which nodes are communicating with each other.

---

## 4. Introduction to Turtlesim

**Turtlesim** is a simple 2D simulator commonly used for learning ROS2 concepts.

It provides an easy way to understand:
- Nodes
- Topics
- Messages
- Publishers
- Subscribers
- ROS2 CLI
- Node communication

### Start Turtlesim

```bash
ros2 run turtlesim turtlesim_node
```

### Control the Turtle

Open another terminal and run:

```bash
ros2 run turtlesim turtle_teleop_key
```

Use the keyboard keys shown in the terminal to control the turtle.

---

## Key Takeaways

- `ros2 node list` → lists running nodes
- `ros2 node info` → gives detailed information about a node
- `--ros-args -r __node:=...` → renames a node at runtime
- **RQT** → graphical ROS2 debugging/visualization framework
- **rqt_graph** → visualizes ROS2 node-topic communication
- **Turtlesim** → simple simulator for learning ROS2 concepts

---

## Day 3 Commands

```bash
# List nodes
ros2 node list

# Inspect a node
ros2 node info /camera_node

# Rename a node
ros2 run my_package my_node --ros-args -r __node:=new_name

# Start Turtlesim
ros2 run turtlesim turtlesim_node

# Control Turtlesim
ros2 run turtlesim turtle_teleop_key

# Launch RQT Graph
rqt_graph
```

---

### Next Step

Continue exploring ROS2 communication by working with **Topics, Publishers, and Subscribers**.
