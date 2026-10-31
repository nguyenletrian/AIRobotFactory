# Visual testing

## Level 0 — offline web visualization (ready for visual acceptance)

On Windows, open **OpenVisualizer.cmd**, or open visualizer/index.html directly in Edge/Chrome. No installations, server, internet, Edge CDP, worker or physical devices are involved.

- Move the shoulder/elbow angle sliders.
- Enter a Cartesian target (X/Y) and select the elbow branch to exercise inverse kinematics.
- Click/touch the canvas to pick a target. Unreachable targets show an error.
- Use "Chạy quỹ đạo tự động" to preview a continuous motion path.
- Red circular obstacle shows an illustrative 2D segment/circle intersection warning. This is not actual 3D collision physics.

Web viewer and existing Python demo both use 120 mm + 90 mm default links and analytic two-link planar equations. Browser controls are in **degrees and millimeters**. This is a kinematic teaching model, not a load/torque/motor simulator or actual 6-DOF industrial robot.

## Level 1 — optional MuJoCo 3D scene

The repo includes simulations/mujoco/two_link.xml, a simple articulated 2-DOF scene with position actuators, a floor and obstacle. Install official MuJoCo Python package into a dedicated environment, then open the native viewer:

    python -m pip install mujoco
    python -m mujoco.viewer --mjcf=simulations/mujoco/two_link.xml

Official instructions: https://mujoco.readthedocs.io/en/stable/python.html

The XML is structurally checked by tests, **not yet compiled/rendered or dynamically verified with MuJoCo on the owner's machine**. MuJoCo actuator controls are in radians, while browser teaching controls are degrees. The two viewers are separate, not live-synchronized.

## Level 2 — FreeCAD / Blender / 6-axis workcell

FreeCAD will provide parametric mechanical CAD and printable components. Blender will provide presentation-quality assembly animation; MuJoCo will remain the dynamic/collision simulation authority. Later milestones add 6-DOF robot description, link mass/inertias, tool changing, gripper contact, camera observations, and local AI model planning.

## Validation

    python -m unittest discover -s tests -v
    node --test visualizer/kinematics.test.cjs

Each test run must distinguish pure computational verification, GUI/browser acceptance, MuJoCo dynamics and real physical testing. Do not equate one with another. Never permit this teaching viewer to send robot actuation commands.
