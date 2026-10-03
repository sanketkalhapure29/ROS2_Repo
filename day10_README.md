# Day 10 — Broadcast TFs with `robot_state_publisher` (ROS 2 Jazzy)

A beginner-friendly guide to publishing a robot's TF frames from a URDF model, launching the tools together, and viewing the result in RViz 2 and `rqt_graph`.

> **Assumptions:** Ubuntu 24.04, ROS 2 Jazzy, workspace `~/ros2_ws`, and a robot file named `my_robot.urdf`. Change the paths if your filenames differ.

## 1. What you will learn

- How URDF describes robot links and joints.
- How `robot_state_publisher` reads the robot description and publishes TF transforms.
- How `joint_state_publisher_gui` provides joint positions for movable joints.
- How RViz 2 visualizes the robot model and TF frames.
- How to organize the URDF, launch file, and RViz config in one package.

### How the pieces work together

1. **URDF** describes links, joints, geometry, and their relationships.
2. **`robot_state_publisher`** uses the robot description and joint positions to publish transforms.
3. **`joint_state_publisher_gui`** lets you change movable-joint positions using sliders and publishes `/joint_states`.
4. **RViz 2** visualizes the robot and TF frames.
5. **`rqt_graph`** shows ROS nodes and topic connections; it does not display the spatial TF tree.

Fixed joints have constant transforms. Movable-joint transforms change when their joint positions change.

## 2. Workspace architecture

```text
~/ros2_ws/
└── src/
    └── my_robot_description/
        ├── CMakeLists.txt
        ├── package.xml
        ├── urdf/
        │   └── my_robot.urdf
        ├── launch/
        │   └── display.launch.xml
        └── rviz/
            └── urdf_config.rviz
```

`build/`, `install/`, and `log/` are generated in the workspace root by `colcon build`.

## 3. Source ROS 2 and install dependencies

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src
sudo apt update
sudo apt install ros-jazzy-robot-state-publisher \
                 ros-jazzy-joint-state-publisher-gui \
                 ros-jazzy-xacro \
                 ros-jazzy-rviz2 \
                 ros-jazzy-rqt-graph \
                 ros-jazzy-tf2-tools
```

## 4. Create the description package

```bash
cd ~/ros2_ws/src
ros2 pkg create my_robot_description
cd ~/ros2_ws/src/my_robot_description
rm -rf include src
mkdir -p urdf launch rviz
```

The `rm -rf include src` command removes the default empty C++ folders created by `ros2 pkg create`. Run it only inside `my_robot_description` if you do not need those folders.

Put your robot model here:

```text
~/ros2_ws/src/my_robot_description/urdf/my_robot.urdf
```

Make sure it is valid URDF/XML. If it uses Xacro features, the `xacro` command must be able to process it.

## 5. Update `CMakeLists.txt`

```bash
nano ~/ros2_ws/src/my_robot_description/CMakeLists.txt
```

Keep the existing project setup and `find_package(ament_cmake REQUIRED)` lines. Add this before `ament_package()`:

```cmake
install(
  DIRECTORY urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)
```

This installs the URDF, launch file, and RViz configuration into the package's share directory. Save in Nano with **Ctrl+O**, Enter, then **Ctrl+X**.

## 6. Check `package.xml` dependencies

```bash
nano ~/ros2_ws/src/my_robot_description/package.xml
```

Inside the `<package> ... </package>` element, add these runtime dependencies if they are not already present. Do not duplicate existing entries:

```xml
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>joint_state_publisher_gui</exec_depend>
<exec_depend>rviz2</exec_depend>
<exec_depend>xacro</exec_depend>
```

## 7. Optional: run `robot_state_publisher` directly

This is a quick test without the launch file. In a terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(xacro ~/ros2_ws/src/my_robot_description/urdf/my_robot.urdf)"
```

This terminal stays occupied while the node runs. Stop it with **Ctrl+C** before starting the full launch setup. This direct command does not start RViz or the joint-state GUI.

## 8. Create `display.launch.xml`

```bash
nano ~/ros2_ws/src/my_robot_description/launch/display.launch.xml
```

Paste and save:

```xml
<launch>
    <let name="urdf_path"
         value="$(find-pkg-share my_robot_description)/urdf/my_robot.urdf" />

    <let name="rviz_config_path"
         value="$(find-pkg-share my_robot_description)/rviz/urdf_config.rviz" />

    <node pkg="robot_state_publisher" exec="robot_state_publisher">
        <param name="robot_description"
               value="$(command 'xacro $(var urdf_path)')" />
    </node>

    <node pkg="joint_state_publisher_gui" exec="joint_state_publisher_gui" />

    <node pkg="rviz2" exec="rviz2" output="screen"
          args="-d $(var rviz_config_path)" />
</launch>
```

### What the launch file does

- `urdf_path`: locates the installed URDF.
- `rviz_config_path`: locates the saved RViz configuration.
- `robot_state_publisher`: receives the URDF processed by `xacro` and publishes TF.
- `joint_state_publisher_gui`: provides sliders for movable joints and publishes their positions on `/joint_states`.
- `rviz2`: opens RViz with the saved configuration.

## 9. Build the workspace

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select my_robot_description
source ~/ros2_ws/install/setup.bash
```

Every new terminal needs the ROS 2 and workspace setup commands:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

After changing the URDF, launch file, or RViz config, rebuild and source the workspace again so the installed resources are updated.

## 10. First launch and configure RViz

```bash
ros2 launch my_robot_description display.launch.xml
```

In RViz:

1. Set **Global Options → Fixed Frame** to a frame that exists in your URDF, commonly `base_link` or `base_footprint`.
2. Click **Add** and add **RobotModel**.
3. Click **Add** and add **TF**.
4. In RobotModel, select `/robot_description` as the **Description Topic** if that option is available in your RViz version. If your version uses a parameter-based description source, select the `robot_description` parameter instead.
5. Check the RViz status panel for errors. Verify the fixed frame, URDF/Xacro, and mesh paths if the model is missing.
6. Move the joint-state GUI sliders to test movable joints.

### Save the RViz configuration

In RViz, choose **File → Save Config As…** and save to:

```text
~/urdf_config.rviz
```

Copy it into the package:

```bash
mkdir -p ~/ros2_ws/src/my_robot_description/rviz
cp ~/urdf_config.rviz ~/ros2_ws/src/my_robot_description/rviz/urdf_config.rviz
```

The launch file already points to this location. Rebuild and source the workspace:

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source ~/ros2_ws/install/setup.bash
```

Launch again:

```bash
ros2 launch my_robot_description display.launch.xml
```

## 11. Inspect nodes, topics, and TF

Keep the launch running. Open a **second terminal** and run:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

### List nodes

```bash
ros2 node list
```

You should see nodes similar to `/robot_state_publisher`, `/joint_state_publisher`, `/joint_state_publisher_gui`, and `/rviz2`. Names can vary slightly by version/setup.

### List topics

```bash
ros2 topic list
```

Useful topics:

- `/joint_states` — positions of movable joints.
- `/tf` — transforms that may change over time.
- `/tf_static` — transforms for fixed relationships.

To inspect joint-state messages:

```bash
ros2 topic echo /joint_states
```

Stop with **Ctrl+C**.

### Generate a TF tree report

```bash
ros2 run tf2_tools view_frames
```

The command prints the generated report filename. Open the resulting PDF to inspect the coordinate-frame hierarchy.

To inspect a transform, replace the example link names with exact frame names from your URDF:

```bash
ros2 run tf2_ros tf2_echo base_link left_wheel_link
```

If `left_wheel_link` is not an actual frame in your model, use the correct name from your URDF.

## 12. Visualize connections with `rqt_graph`

With the launch still running, use the second terminal:

```bash
rqt_graph
```

Or:

```bash
ros2 run rqt_graph rqt_graph
```

Look for nodes such as `robot_state_publisher`, the joint-state publisher, and `rviz2`, plus connections involving `/joint_states`, `/tf`, and `/tf_static`. Filters or graph-view settings can hide some nodes/topics.

**Remember:** `rqt_graph` displays ROS communication connections. To see the spatial TF tree, use the **TF** display in RViz or `ros2 run tf2_tools view_frames`.

## 13. Troubleshooting

### Package or launch file not found

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 pkg prefix my_robot_description
```

### Check whether the URDF is present

```bash
ls -l ~/ros2_ws/src/my_robot_description/urdf/my_robot.urdf
ls -l ~/ros2_ws/install/my_robot_description/share/my_robot_description/urdf/
```

### RViz says the fixed frame does not exist

- Choose a real root frame from the URDF, such as `base_link` or `base_footprint`.
- Make sure `robot_state_publisher` is running.
- Inspect the TF display or use `view_frames` to check frame names.

### Robot model does not appear

- Check the launch terminal for URDF/Xacro errors.
- Add a **RobotModel** display.
- Check the description source/topic setting.
- Ensure the URDF includes valid visual geometry and any mesh paths are correct.

### Sliders do not move the robot

- Confirm the URDF has movable joints (`revolute` or `continuous`, for example).
- Fixed joints do not have sliders.
- Check that `/joint_states` is being published while moving a slider.

### RViz shows old settings

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source ~/ros2_ws/install/setup.bash
ros2 launch my_robot_description display.launch.xml
```

## 14. Quick run checklist

**Terminal 1 — launch visualization**

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch my_robot_description display.launch.xml
```

**Terminal 2 — inspect the graph and topics**

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 node list
ros2 topic list
rqt_graph
```

**Optional — inspect TF frames**

```bash
ros2 run tf2_tools view_frames
```

## 15. Key takeaways

- **URDF** describes the robot's structure.
- **`robot_state_publisher`** uses the URDF and joint positions to publish TF transforms.
- **`joint_state_publisher_gui`** lets you test movable joints without real hardware.
- **RViz 2** visualizes the robot and its frames.
- **`rqt_graph`** shows nodes and topic connections; it is not a TF-tree viewer.
- Install the `urdf`, `launch`, and `rviz` folders so ROS 2 can find them after building the package.
