# 🤖 ROS2 Daily Learning Series

Documenting my ROS2 learning journey — one concept a day, with code and notes, alongside a daily LinkedIn post.

📅 **Day 1** | Topic: **Introduction to ROS2 & Installation**

---

## 📖 What I Learned Today

### What is ROS2?
ROS2 (Robot Operating System 2) is a set of **open-source robotic middleware and tools** — a collection of software libraries, tools, and communication systems that allow different parts of a robot to work together.

### Why ROS2?
Building a robot involves many different programs and hardware components (sensors, motors, cameras, planners) that all need to communicate and work together reliably. ROS2 provides the framework to make that possible.

---

## ⚙️ Installation (ROS2 Jazzy on Ubuntu)

### 1. Update the system
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Set up locale
```bash
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### 3. Enable Ubuntu Universe repository
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe
```

### 4. Add the ROS2 apt repository
```bash
sudo apt update && sudo apt install curl -y

export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
  | grep -F "tag_name" | awk -F'"' '{print $4}')

curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"

sudo dpkg -i /tmp/ros2-apt-source.deb
```

### 5. Install ROS2 Jazzy Desktop
```bash
sudo apt update
sudo apt install ros-jazzy-desktop -y
```

### 6. Install ROS2 development tools
```bash
sudo apt install ros-dev-tools -y
```

### 7. Source ROS2 Jazzy
```bash
source /opt/ros/jazzy/setup.bash
```

> 💡 To avoid sourcing manually every session, add the line above to the end of your `~/.bashrc` file. Every new terminal will then have ROS2 ready automatically.

---

## 🛠️ Supporting Tools Installed

**VS Code**
```bash
sudo snap install code --classic
```

**Terminator** (multi-pane terminal, useful for running multiple nodes side-by-side)
```bash
sudo apt install terminator
```

---

## ✅ Verifying the Installation

Ran the classic ROS2 talker/listener demo across two terminals to confirm everything was working:

**Terminal 1**
```bash
ros2 run demo_nodes_cpp talker
```

**Terminal 2**
```bash
ros2 run demo_nodes_cpp listener
```

Seeing the talker publish messages and the listener receive them in real time confirmed the installation was successful and gave a first concrete look at ROS2's publish/subscribe communication model.

---

## 🔑 Key Takeaway

ROS2 isn't an operating system — it's middleware that lets independent programs (nodes) on a robot communicate reliably. Getting the install right and verifying it with talker/listener is the foundation everything else in this series builds on.

---

## 🗓️ Progress Tracker

| Day | Topic | Status |
|-----|-------|--------|
| 1 | Introduction to ROS2 & Installation | ✅ Done |
| 2 | First ROS2 Program | 🔜 Coming up |

---

## 🔗 Connect

Following along? I'm posting daily updates on **LinkedIn** — www.linkedin.com/in/sanket-kalhapure-617848318 

`#ROS2 #Robotics #RoboticsEngineering #LearningInPublic #OpenSource`
