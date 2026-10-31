# First 3D-print experiment: dimensional calibration

The first printed object is an intentionally simple **20 mm cube coupon**, not a functional robot joint. Generate the STL with:

    python -m airobotfactory coupon --output artifacts/cube20.stl

Steps once a 3D printer is available:
1. Inspect STL mesh orientation and dimensions in a slicer. Confirm units are mm and z=0 bottom surface.
2. Record printer model, nozzle, filament material, layer height, orientation, slicer version and intended dimensions.
3. Print at safe vendor-rated temperatures with normal equipment supervision; do not bypass printer protections.
4. Use a caliper to measure x/y/z on at least three independent coupons, recording each individually in examples/print_measurements.csv. Never enter synthetic measurements as real data.
5. Calculate repeatability and systematic scale error. Only after reliable measurements create joints, shaft holes, snap features and gripper fixtures.

Acceptance is recorded evidence rather than a fixed accuracy promise. A failed print is a valid experimental outcome. Model predictions cannot replace printer calibration. Designs for moving mechanisms must add clearance studies and load tests later.
