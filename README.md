<a name="readme-top"></a>
<br />
<div align="center">
  <h3 align="center">CAN Controller</h3>

  <p align="center">
    Simulate vehicle CAN bus traffic using a game controller
  </p>
</div>

<br>


## Getting Started

#### Requirements
* Python 3.7+
* Linux
* PS4 Controller
* USB2CAN

### Installation

Install Linux can-utils:
```
sudo apt-get install can-utils -y
```

Install Python requirements:
```
python -m pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage
1. Connect USB2CAN & PS4 Controller

```
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
python controller.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
