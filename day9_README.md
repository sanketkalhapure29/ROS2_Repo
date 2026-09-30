# 🤖 ROS 2 Level 2 — Day 9: TF & URDF

> **ROS 2 Learning Journey — Day 9**
>
> Learn how ROS 2 represents robot structure using **TF, URDF, Links, Joints, Materials, Geometry, and Coordinate Frames**.

---

## 📚 Table of Contents

1. [Introduction to ROS 2 Level 2](#1-introduction-to-ros-2-level-2)
2. [Introduction to TF](#2-introduction-to-tf)
3. [What is TF?](#3-what-is-tf)
4. [TF Tree](#4-tf-tree)
5. [What Problem Does TF Solve?](#5-what-problem-does-tf-solve)
6. [What is URDF?](#6-what-is-urdf)
7. [Your First URDF](#7-your-first-urdf)
8. [URDF Syntax Explained](#8-urdf-syntax-explained)
9. [Visualizing URDF](#9-visualizing-urdf)
10. [Materials and Colors](#10-materials-and-colors)
11. [Links and Joints](#11-links-and-joints)
12. [Joint Types](#12-joint-types)
13. [Complete Differential Drive Robot](#13-complete-differential-drive-robot)
14. [URDF Cheat Sheet](#14-urdf-cheat-sheet)
15. [Common Mistakes](#15-common-mistakes)
16. [Learning Workflow](#16-learning-workflow)
17. [TF vs URDF](#17-tf-vs-urdf)
18. [Key Takeaways](#18-key-takeaways)

---

# 1. Introduction to ROS 2 Level 2

After learning ROS 2 fundamentals such as:

- Nodes
- Topics
- Services
- Parameters
- Custom interfaces
- Launch files

the next step is understanding how ROS 2 represents a **physical robot**.

A robot contains:

- A body
- Wheels
- Sensors
- Joints
- Coordinate frames
- Physical dimensions
- Relationships between components

Two important concepts are:

> **TF → Coordinate-frame relationships**

> **URDF → Robot model description**

---

# 2. Introduction to TF

## Topics Covered

1. What is TF?
2. Relationship between TFs and the TF tree
3. What problem are we trying to solve with TF?

---

# 3. What is TF?

**TF** stands for **Transform**.

Robots contain many coordinate frames.

For example:

- `base_link`
- `base_footprint`
- `left_wheel_link`
- `right_wheel_link`
- `camera_link`
- `laser_link`
- `imu_link`

Each frame represents a coordinate system attached to a particular part of the robot.

TF tells ROS 2:

> **Where is one coordinate frame relative to another?**

For example:

```text
base_link
    |
    ├── left_wheel_link
    ├── right_wheel_link
    └── camera_link
```

This allows ROS 2 to understand the robot's spatial structure.

---

# 4. TF Tree

A **TF tree** is a hierarchy showing how coordinate frames are connected.

Example:

```text
                base_link
               /    |     \
              /     |      \
 left_wheel_link  camera  right_wheel_link
```

If the robot has a camera, the camera frame has a known relationship with the robot's base frame.

For example:

```text
base_link → camera_link
```

means that the camera's position and orientation can be described relative to the base frame.

TF relationships are important for:

- Navigation
- Sensor fusion
- LiDAR
- Cameras
- IMUs
- SLAM
- Localization
- Manipulation
- Motion planning

---

# 5. What Problem Does TF Solve?

Imagine a robot with:

```text
base_link
camera_link
laser_link
imu_link
left_wheel_link
right_wheel_link
```

Suppose the LiDAR detects an obstacle.

The LiDAR reports the obstacle using the **LiDAR coordinate frame**.

But the navigation system may need that information relative to the **robot's base frame**.

TF provides the relationship required to transform information between these frames.

### Simple real-world analogy

Think about your body.

Your:

- Hand
- Head
- Feet
- Eyes

all have positions relative to your body.

Robots work similarly.

TF provides the mathematical relationships between the robot's coordinate frames.

---

# 6. What is URDF?

**URDF** stands for:

> **Unified Robot Description Format**

URDF is an XML-based format used to describe the structure of a robot.

It can describe:

- Links
- Joints
- Geometry
- Dimensions
- Materials
- Colors
- Positions
- Orientations
- Relationships between robot components

A simple way to remember:

> **URDF describes the robot model.**

> **TF describes coordinate-frame relationships.**

---

# 7. Your First URDF

Create a file:

```bash
touch my_robot.urdf
```

Open it:

```bash
code my_robot.urdf
```

A basic URDF contains:

```xml
<?xml version="1.0"?>

<robot name="my_robot">

    <link name="base_link">

        <visual>

            <geometry>
                <box size="0.6 0.4 0.2" />
            </geometry>

            <origin xyz="0 0 0.1" rpy="0 0 0" />

        </visual>

    </link>

</robot>
```

This creates a simple rectangular robot body.

---

# 8. URDF Syntax Explained

## 8.1 XML Declaration

```xml
<?xml version="1.0"?>
```

This identifies the file as an XML document.

---

## 8.2 `<robot>`

```xml
<robot name="my_robot">
```

The `<robot>` element is the root of the URDF.

Everything describing the robot goes inside it.

### Syntax

```xml
<robot name="robot_name">
    ...
</robot>
```

---

## 8.3 `<link>`

A **link** represents a physical part of the robot.

Examples:

```text
base_link
left_wheel_link
right_wheel_link
camera_link
laser_link
imu_link
```

Basic syntax:

```xml
<link name="link_name">
    ...
</link>
```

A link can contain information about:

- Visual appearance
- Collision geometry
- Physical properties

---

## 8.4 `<visual>`

The `<visual>` element defines how a link looks.

```xml
<visual>
    ...
</visual>
```

It can contain:

- Geometry
- Origin
- Material

---

## 8.5 `<geometry>`

Geometry defines the shape.

### Box

```xml
<box size="0.6 0.4 0.2" />
```

The values represent:

```text
X dimension
Y dimension
Z dimension
```

So the box is:

```text
0.6 × 0.4 × 0.2 meters
```

### Cylinder

```xml
<cylinder radius="0.1" length="0.2" />
```

### Sphere

```xml
<sphere radius="0.05" />
```

---

## 8.6 `<origin>`

`origin` defines position and orientation.

```xml
<origin xyz="0 0 0.1" rpy="0 0 0" />
```

### `xyz`

Position:

```text
x y z
```

Example:

```text
0 0 0.1
```

means:

```text
X = 0
Y = 0
Z = 0.1
```

### `rpy`

Orientation:

```text
roll pitch yaw
```

For example:

```text
0 0 0
```

means no rotation.

---

# 9. Visualizing URDF

Use the ROS 2 URDF tutorial launch file:

```bash
ros2 launch urdf_tutorial display.launch.py model:=$HOME/my_robot.urdf
```

The general workflow is:

```text
URDF file
    ↓
URDF visualization launch
    ↓
Robot state / visualization
    ↓
RViz
    ↓
Robot Model
```

---

# 10. Materials and Colors

URDF allows us to define materials.

Example:

```xml
<material name="green">
    <color rgba="0 0.5 0 1" />
</material>
```

Apply it to a visual:

```xml
<material name="green" />
```

## Understanding RGBA

RGBA means:

```text
Red
Green
Blue
Alpha
```

Example:

```text
0 0.5 0 1
```

means:

```text
R = 0
G = 0.5
B = 0
A = 1
```

Alpha controls transparency.

```text
1 = fully visible
```

---

# 11. Links and Joints

A real robot has multiple components.

For example:

```text
Base
  |
  ├── Left Wheel
  ├── Right Wheel
  └── Caster Wheel
```

URDF uses **joints** to connect links.

The relationship is:

```text
Parent Link
      ↓
    Joint
      ↓
Child Link
```

## Fixed Joint

A fixed joint does not allow relative movement.

```xml
<joint name="base_second_joint" type="fixed">

    <parent link="base_link" />

    <child link="second_link" />

    <origin xyz="0 0 0.2" rpy="0 0 0" />

</joint>
```

### Important elements

`name` → unique joint name

`type` → joint type

`parent` → parent link

`child` → child link

`origin` → child position/orientation relative to parent

---

# 12. Joint Types

URDF supports several joint types:

- Fixed
- Revolute
- Continuous
- Prismatic
- Floating
- Planar

The main types introduced in this lesson are:

## 12.1 Fixed

No relative movement.

```xml
<joint name="example" type="fixed">
```

Useful for parts rigidly attached to the robot.

---

## 12.2 Revolute

Allows rotation within a limited range.

```xml
<joint name="example_joint" type="revolute">

    <axis xyz="0 0 1" />

    <limit
        lower="-1.57"
        upper="1.57"
        velocity="100"
        effort="100" />

</joint>
```

### Axis

```xml
<axis xyz="0 0 1" />
```

The values represent:

```text
X Y Z
```

Here the rotation axis is the Z-axis.

### Limits

The limit contains:

- `lower`
- `upper`
- `velocity`
- `effort`

For:

```text
-1.57 to +1.57
```

the approximate rotation range is:

```text
-90° to +90°
```

---

## 12.3 Continuous

Allows continuous rotation.

```xml
<joint name="wheel_joint" type="continuous">

    <axis xyz="0 0 1" />

</joint>
```

This type is commonly useful for continuously rotating components such as wheels.

The correct axis depends on the physical orientation of the wheel.

---

# 13. Complete Differential Drive Robot

Now we combine:

- Materials
- Links
- Geometry
- Origins
- Fixed joints
- Continuous joints
- Parent-child relationships

The robot contains:

```text
base_footprint
      |
      ↓
  base_link
   /     \
  /       \
left     right
wheel    wheel

      |
      ↓
   caster
```

## Complete URDF

```xml
<?xml version="1.0"?>
<robot name="my_robot">

    <!-- ================= MATERIALS ================= -->

    <material name="green">
        <color rgba="0 0.5 0 1" />
    </material>

    <material name="blue">
        <color rgba="0 0 0.5 1" />
    </material>

    <!-- ================= BASE FOOTPRINT ================= -->

    <link name="base_footprint" />

    <!-- ================= BASE LINK ================= -->

    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.6 0.4 0.2" />
            </geometry>

            <origin xyz="0 0 0.1" rpy="0 0 0" />

            <material name="green" />
        </visual>
    </link>

    <!-- ================= RIGHT WHEEL ================= -->

    <link name="right_wheel_link">
        <visual>
            <geometry>
                <cylinder radius="0.1" length="0.05" />
            </geometry>

            <origin xyz="0 0 0" rpy="1.5708 0 0" />

            <material name="blue" />
        </visual>
    </link>

    <!-- ================= LEFT WHEEL ================= -->

    <link name="left_wheel_link">
        <visual>
            <geometry>
                <cylinder radius="0.1" length="0.05" />
            </geometry>

            <origin xyz="0 0 0" rpy="1.5708 0 0" />

            <material name="blue" />
        </visual>
    </link>

    <!-- ================= CASTER WHEEL ================= -->

    <link name="caster_wheel_link">
        <visual>
            <geometry>
                <sphere radius="0.05" />
            </geometry>

            <origin xyz="0 0 0" rpy="0 0 0" />

            <material name="blue" />
        </visual>
    </link>

    <!-- ================= BASE JOINT ================= -->

    <joint name="base_joint" type="fixed">
        <parent link="base_footprint" />
        <child link="base_link" />

        <origin xyz="0 0 0.1" rpy="0 0 0" />
    </joint>

    <!-- ================= RIGHT WHEEL JOINT ================= -->

    <joint name="base_right_wheel_joint" type="continuous">
        <parent link="base_link" />
        <child link="right_wheel_link" />

        <origin xyz="-0.15 -0.225 0" rpy="0 0 0" />

        <axis xyz="0 1 0" />
    </joint>

    <!-- ================= LEFT WHEEL JOINT ================= -->

    <joint name="base_left_wheel_joint" type="continuous">
        <parent link="base_link" />
        <child link="left_wheel_link" />

        <origin xyz="-0.15 0.225 0" rpy="0 0 0" />

        <axis xyz="0 1 0" />
    </joint>

    <!-- ================= CASTER JOINT ================= -->

    <joint name="base_caster_wheel_joint" type="fixed">
        <parent link="base_link" />
        <child link="caster_wheel_link" />

        <origin xyz="0.15 0 -0.05" rpy="0 0 0" />
    </joint>

</robot>
```

---

# 14. Understanding the Complete Robot

## `base_footprint`

```xml
<link name="base_footprint" />
```

This is an empty link used as a reference frame for the robot footprint.

It is connected to `base_link` using a fixed joint.

---

## `base_link`

This represents the main body of the robot.

Dimensions:

```text
Length = 0.6 m
Width  = 0.4 m
Height = 0.2 m
```

---

## Left and Right Wheels

The robot contains:

```text
left_wheel_link
right_wheel_link
```

Both use cylinder geometry.

Their visual orientation is adjusted using:

```text
rpy = 1.5708 0 0
```

The wheels are connected to the base using continuous joints.

---

## Caster Wheel

The caster is represented using:

```xml
<sphere radius="0.05" />
```

It is connected to the robot body using a fixed joint in this simplified model.

---

# 15. Understanding the Robot's Joint Tree

```text
base_footprint
      |
    fixed
      |
  base_link
   /       \
continuous continuous
  /             \
left wheel     right wheel

      |
    fixed
      |
 caster wheel
```

The important relationship is:

```text
Parent → Joint → Child
```

This structure forms the link/joint hierarchy of the robot.

---

# 16. URDF Cheat Sheet

| Element | Purpose |
|---|---|
| `<robot>` | Root of the robot description |
| `<link>` | Represents a robot component |
| `<joint>` | Connects two links |
| `<visual>` | Defines visual appearance |
| `<geometry>` | Defines shape |
| `<box>` | Box geometry |
| `<cylinder>` | Cylinder geometry |
| `<sphere>` | Sphere geometry |
| `<origin>` | Position and orientation |
| `<material>` | Defines material |
| `<color>` | Defines color/transparency |
| `<parent>` | Parent link |
| `<child>` | Child link |
| `<axis>` | Joint rotation axis |
| `<limit>` | Joint constraints |

---

# 17. Common Mistakes

## 1. Incorrect XML structure

Make sure opening and closing tags are correct.

```xml
<link>
    ...
</link>
```

---

## 2. Duplicate names

Link and joint names should be unique.

---

## 3. Incorrect parent-child relationship

Every joint should clearly define:

```text
Parent → Joint → Child
```

---

## 4. Wrong wheel axis

If a wheel rotates incorrectly, check:

- Cylinder orientation
- `rpy`
- Joint `axis`

---

## 5. Incorrect dimensions

URDF dimensions are generally given in meters.

For example:

```text
0.6 = 60 cm
0.4 = 40 cm
0.2 = 20 cm
```

---

# 18. Learning Workflow

Learn URDF progressively.

### Step 1 — One link

```text
Robot
 └── base_link
```

### Step 2 — Add geometry

```text
base_link
 └── box
```

### Step 3 — Add material

```text
base_link
 └── colored box
```

### Step 4 — Add another link

```text
base_link
 └── second_link
```

### Step 5 — Connect links

```text
base_link
    |
  joint
    |
second_link
```

### Step 6 — Experiment with joint types

Try fixed, revolute, and continuous joints.

### Step 7 — Build the complete robot

```text
                 base_link
               /     |      \
              /      |       \
       left wheel  caster  right wheel
```

---

# 19. TF vs URDF

| TF | URDF |
|---|---|
| Represents coordinate-frame relationships | Describes robot structure |
| Used for transforms | Used for robot modeling |
| Describes where frames are relative to each other | Defines links and joints |
| Important for navigation and sensor data | Important for robot visualization/modeling |

### Easy way to remember

> **URDF describes the robot.**

> **TF describes the relationships between coordinate frames.**

---

# 20. Real-World Robotics Connection

The concepts learned today are used in real robotic systems.

For example, an autonomous UGV may contain:

```text
                 base_link
                /    |     \
               /     |      \
       left wheel  camera  right wheel
                    |
                  LiDAR
                    |
                   IMU
```

A robotic arm may contain:

```text
base_link
    |
joint_1
    |
link_1
    |
joint_2
    |
link_2
    |
joint_3
    |
...
```

The same concepts scale to more complex robots.

---

# 21. Key Takeaways

After completing Day 9, you should understand:

- What TF is
- Why coordinate frames are needed
- What a TF tree represents
- What problem TF solves
- What URDF means
- How to create a basic URDF
- What a link represents
- What a joint represents
- How visual geometry is defined
- How box, cylinder, and sphere geometry work
- How `origin` works
- How materials and colors work
- How parent-child relationships work
- What fixed, revolute, and continuous joints are
- How to structure a differential-drive robot

---

# 🚀 Final Revision

```text
ROS 2 Level 2
│
├── TF
│   ├── Coordinate Frames
│   ├── Transformations
│   └── TF Tree
│
└── URDF
    ├── Robot
    ├── Links
    ├── Joints
    ├── Visual
    ├── Geometry
    ├── Origin
    ├── Materials
    └── Colors
```

The goal is not to simply copy a URDF.

Try changing:

- Robot dimensions
- Wheel radius
- Wheel positions
- Colors
- Joint types
- Joint axes
- Link positions

Then visualize the result.

> **Understand why every link, joint, transform, and coordinate frame exists.**

---

## 👨‍💻 Author

**Sanket Kalhapure**

Robotics & Automation Engineering  
ROS 2 • Autonomous Robotics • Physical AI

---

## 🔖 Topics

`ROS2` `TF` `URDF` `RViz` `Robot Modeling` `Robotics` `ROS2 Jazzy` `Differential Drive`
