# ROS 2 Level 2 — Day 11: Improve URDF with Xacro

## 📚 What is this lesson about?

In the previous lesson, we learned how to create a robot model using **URDF** and how `robot_state_publisher` uses the robot description to publish TFs.

As a robot becomes more complex, writing a large URDF file can become repetitive and difficult to maintain.

**Xacro** helps us solve this problem.

Xacro allows us to write a cleaner and more reusable robot description by using:

- Properties (variables)
- Macros (functions/templates)
- File inclusion
- Expressions and calculations
- Reusable robot components

At the end of this lesson, we will use Xacro files to generate a normal URDF file.

---

# 🎯 Learning Objectives

By the end of Day 11, you should understand:

1. What Xacro is and why it is useful
2. How to make a URDF compatible with Xacro
3. How to create variables using Xacro properties
4. How to create reusable components using Xacro macros
5. How to include one Xacro file inside another
6. How to use expressions and calculations in Xacro
7. How to convert a Xacro file into a URDF file
8. How to organize a robot description using multiple Xacro files

---

# 1. What is Xacro?

**Xacro** stands for **XML Macros**.

A normal URDF is written using XML. When a robot becomes larger, we may repeatedly write the same dimensions, colors, wheel structures, and other information.

For example, imagine a robot with two wheels.

Without Xacro, we may have to manually write the complete description of the left wheel and then write almost the same description again for the right wheel.

Xacro lets us define the common information once and reuse it.

### Simple idea

Think of it like this:

```text
URDF
 ↓
Everything is written explicitly

Xacro
 ↓
Variables + reusable components + included files
 ↓
Generated URDF
```

So:

> **Xacro is a tool that makes URDF easier to write, reuse, and maintain.**

---

# 2. Why do we need Xacro?

Consider a robot with:

- Base
- Left wheel
- Right wheel
- Caster
- Camera
- LiDAR
- IMU
- Sensors

A large URDF can become difficult to manage.

Xacro helps by allowing us to:

### ✅ Use variables

Instead of writing the same number many times, define it once.

### ✅ Reuse components

Create a wheel once and generate both left and right wheels.

### ✅ Split the robot into files

For example:

```text
my_robot.urdf.xacro
│
├── common_properties.xacro
└── mobile_base.xacro
```

### ✅ Perform calculations

Xacro can calculate values from other properties.

For example:

```text
base_height / 2.0
```

This means we do not have to manually calculate and enter the value every time.

---

# 3. Making URDF Compatible with Xacro

A Xacro file is still XML, but we need to tell Xacro that we want to use its features.

The root element contains the Xacro namespace:

```xml
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
```

### What does this mean?

`robot` is the normal URDF root element.

`xmlns:xacro` tells XML that the `xacro:` prefix refers to the Xacro system.

Because of this, we can use tags such as:

```text
xacro:property
xacro:macro
xacro:include
```

---

# 4. Xacro Properties — Creating Variables

One of the most useful Xacro features is the **property**.

A property is similar to a variable in programming.

### Syntax

```xml
<xacro:property name="property_name" value="value" />
```

### Example from this lesson

In `mobile_base.xacro`:

```xml
<xacro:property name="base_length" value="0.6" />
<xacro:property name="base_width" value="0.4" />
<xacro:property name="base_height" value="0.2" />
<xacro:property name="wheel_radius" value="0.1" />
<xacro:property name="wheel_length" value="0.05" />
```

Now we have reusable values for the robot dimensions.

---

# 5. Using a Xacro Property

To use a property inside another XML value, use:

```text
${property_name}
```

For example:

```xml
<box size="${base_length} ${base_width} ${base_height}" />
```

Instead of writing:

```text
0.6 0.4 0.2
```

we use:

```text
${base_length} ${base_width} ${base_height}
```

This makes the robot much easier to modify.

If you later change:

```text
base_length = 0.6
```

to:

```text
base_length = 0.8
```

the places using `${base_length}` automatically use the new value.

---

# 6. Expressions and Calculations

Xacro can also perform calculations.

For example:

```xml
<origin xyz="0 0 ${base_height / 2.0}" rpy="0 0 0" />
```

Here Xacro calculates:

```text
base_height / 2.0
```

Another example:

```xml
<origin xyz="${base_length / 3.0} 0 ${-wheel_radius / 2.0}" />
```

This is useful because robot dimensions often depend on other dimensions.

Instead of manually calculating every position, we can let Xacro calculate it.

---

# 7. Xacro Macros — Reusable Components

A **macro** is a reusable piece of Xacro.

You can think of a macro like a function in programming.

Instead of writing the same wheel description multiple times, we can create a wheel macro once and call it whenever we need a wheel.

### Basic syntax

```xml
<xacro:macro name="macro_name" params="parameter">
    <!-- reusable robot description -->
</xacro:macro>
```

---

# 8. Wheel Macro from This Lesson

In `mobile_base.xacro`, we created:

```xml
<xacro:macro name="wheel_link" params="prefix">
```

The macro receives a parameter called:

```text
prefix
```

Inside the macro, the prefix is used to create the link name:

```xml
<link name="${prefix}_wheel_link">
```

This allows us to create:

```text
right_wheel_link
```

and:

```text
left_wheel_link
```

using the same macro.

---

# 9. Calling a Macro

Once the macro has been created, we can call it:

```xml
<xacro:wheel_link prefix="right" />
<xacro:wheel_link prefix="left" />
```

The first call produces the right wheel.

The second call produces the left wheel.

### Conceptually

```text
wheel_link macro
       │
       ├── prefix = right
       │       ↓
       │   right_wheel_link
       │
       └── prefix = left
               ↓
           left_wheel_link
```

This is much cleaner than duplicating the complete wheel definition.

---

# 10. Include Another Xacro File

Xacro also allows us to split a robot into multiple files.

The syntax is:

```xml
<xacro:include filename="file_name.xacro" />
```

Our main file is:

```text
my_robot.urdf.xacro
```

It includes:

```text
common_properties.xacro
```

and:

```text
mobile_base.xacro
```

The relevant part is:

```xml
<xacro:include filename="common_properties.xacro" />
<xacro:include filename="mobile_base.xacro" />
```

---

# 11. Understanding Our File Structure

The files used in this lesson are organized like this:

```text
my_robot.urdf.xacro
│
├── common_properties.xacro
│
└── mobile_base.xacro
```

### `my_robot.urdf.xacro`

This is the main Xacro file.

It includes the other files.

### `common_properties.xacro`

This contains common robot materials.

For this lesson, it defines:

- Blue material
- Grey material

### `mobile_base.xacro`

This contains the mobile robot base.

It defines:

- Base dimensions
- Wheel dimensions
- Base footprint
- Base link
- Left wheel
- Right wheel
- Caster wheel
- Wheel macro
- Robot joints

---

# 12. Understanding `common_properties.xacro`

Our material file contains:

```xml
<material name="blue">
    <color rgba="0 0 0.5 1" />
</material>

<material name="grey">
    <color rgba="0.5 0.5 0.5 1" />
</material>
```

The advantage of putting these materials in a separate file is that other robot components can reuse them.

For example:

```text
common_properties.xacro
        │
        ├── blue
        └── grey
```

Then `mobile_base.xacro` can use those materials.

---

# 13. Understanding `mobile_base.xacro`

The mobile base file contains the actual robot structure.

The properties define dimensions:

```text
base_length
base_width
base_height
wheel_radius
wheel_length
```

Then the robot links are created.

### Robot links

```text
base_footprint
base_link
right_wheel_link
left_wheel_link
caster_wheel_link
```

### Robot joints

```text
base_joint
base_right_wheel_joint
base_left_wheel_joint
base_caster_wheel_joint
```

This gives us a simple differential-drive robot with a caster wheel.

---

# 14. Understanding `my_robot.urdf.xacro`

The main file is very small:

```xml
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

    <xacro:include filename="common_properties.xacro" />
    <xacro:include filename="mobile_base.xacro" />

</robot>
```

This is one of the major benefits of Xacro.

Instead of keeping everything inside one huge file, we can create smaller files and combine them.

---

# 15. Xacro Command — Generate URDF

A Xacro file is not the final URDF.

We can use the `xacro` command to process it and generate a URDF.

### Command

```bash
xacro my_robot.urdf.xacro > my_robot.urdf
```

### What happens?

```text
my_robot.urdf.xacro
        │
        │ xacro
        ↓
my_robot.urdf
```

Xacro processes:

- Properties
- Macros
- Includes
- Expressions

and produces a normal URDF file.

---

# 16. Check the Generated URDF

After running:

```bash
xacro my_robot.urdf.xacro > my_robot.urdf
```

you should have:

```text
my_robot.urdf.xacro
my_robot.urdf
```

You can inspect the generated URDF with:

```bash
cat my_robot.urdf
```

The generated file should contain normal URDF elements such as:

```text
robot
link
visual
geometry
joint
material
```

The Xacro-specific logic has been processed.

---

# 17. Complete Learning Workflow

A beginner can follow this workflow:

### Step 1 — Create the Xacro files

```text
common_properties.xacro
mobile_base.xacro
my_robot.urdf.xacro
```

### Step 2 — Add the Xacro namespace

Make sure the root robot element contains:

```text
xmlns:xacro="http://www.ros.org/wiki/xacro"
```

### Step 3 — Create properties

Define dimensions such as:

```text
base_length
base_width
base_height
wheel_radius
wheel_length
```

### Step 4 — Create reusable macros

Create a wheel macro instead of writing the same wheel twice.

### Step 5 — Include files

Include the common properties and mobile base files from the main Xacro file.

### Step 6 — Generate URDF

Run:

```bash
xacro my_robot.urdf.xacro > my_robot.urdf
```

### Step 7 — Use the generated robot description

The generated URDF can then be used wherever a normal URDF is expected.

---

# 18. URDF vs Xacro

| Feature | URDF | Xacro |
|---|---|---|
| XML based | ✅ | ✅ |
| Robot links | ✅ | ✅ |
| Robot joints | ✅ | ✅ |
| Variables | ❌ | ✅ |
| Macros | ❌ | ✅ |
| File inclusion | ❌ | ✅ |
| Calculations | Limited | ✅ |
| Reusable components | Limited | ✅ |
| Easy for large robots | ❌ | ✅ |

### Important

Xacro does **not replace URDF**.

Instead:

```text
Xacro
  ↓
generates
  ↓
URDF
```

So Xacro is a convenient way to create and maintain a URDF.

---

# 19. Common Xacro Syntax Cheat Sheet

### Xacro namespace

```xml
xmlns:xacro="http://www.ros.org/wiki/xacro"
```

### Property

```xml
<xacro:property name="name" value="value" />
```

### Use property

```text
${name}
```

### Macro

```xml
<xacro:macro name="name" params="parameter">
</xacro:macro>
```

### Call macro

```xml
<xacro:name parameter="value" />
```

### Include file

```xml
<xacro:include filename="file.xacro" />
```

### Generate URDF

```bash
xacro robot.urdf.xacro > robot.urdf
```

---

# 20. Common Beginner Mistakes

## ❌ 1. Forgetting the Xacro namespace

If you use Xacro tags without declaring the namespace, Xacro will not understand them.

Make sure the root element includes:

```text
xmlns:xacro="http://www.ros.org/wiki/xacro"
```

---

## ❌ 2. Forgetting `${}` when using a property

If a property is called:

```text
wheel_radius
```

use:

```text
${wheel_radius}
```

when referring to it.

---

## ❌ 3. Wrong file name in `xacro:include`

If the file is:

```text
mobile_base.xacro
```

the include must point to the correct filename.

---

## ❌ 4. Running the wrong command

A Xacro file should be processed using:

```bash
xacro robot.urdf.xacro
```

rather than treating it as an already-generated URDF.

---

## ❌ 5. Defining a macro but never calling it

Creating a macro does not automatically create the robot component.

You must call the macro.

---

# 21. What I Learned in Day 11

By completing this lesson, I learned:

- How to make a URDF compatible with Xacro
- How Xacro properties work like variables
- How to use property values inside URDF elements
- How Xacro expressions can perform calculations
- How to create reusable components using macros
- How macro parameters can generate different components
- How to split a robot description across multiple files
- How to include one Xacro file inside another
- How to convert Xacro into URDF using the `xacro` command
- Why Xacro is useful for maintaining larger robot descriptions

---

# 🧠 Key Takeaway

Think of the relationship like this:

```text
URDF
    ↓
Robot description

Xacro
    ↓
A better way to create and organize the URDF
    ↓
Properties + Macros + Includes + Calculations
    ↓
Generated URDF
```

The goal is not just to write a robot description that works.

The goal is to write a robot description that is:

**Reusable → Maintainable → Modular → Easy to modify**

---

# 🚀 Next Step

After learning:

```text
TF
 ↓
URDF
 ↓
Robot State Publisher
 ↓
Xacro
```

the next step is to continue building a complete robot description and visualize it using ROS 2 tools such as **RViz** and simulation tools.

---

## 📁 Files in This Lesson

```text
common_properties.xacro
mobile_base.xacro
my_robot.urdf.xacro
```

These files demonstrate the main Xacro concepts covered in Day 11.

---

## 📌 ROS 2 Learning Series

**Day 9** — TF & URDF  
**Day 10** — Broadcasting TFs with Robot State Publisher  
**Day 11** — Improving URDF with Xacro

Keep learning one concept at a time and gradually build toward complete robotic systems. 🤖
