## How it works

This project implements a **6-bit grayscale horizontal image upscaler** using simple linear interpolation.

The module takes two adjacent 6-bit grayscale pixels (`left` and `right`) and computes their average:
  output_pixel = (left_pixel + right_pixel) >> 1


### Pixel Packing

- **Left pixel (6-bit)** → `ui[5:0]`
- **Right pixel (6-bit)** → split across:
  - `uio[3:0]` → lower 4 bits
  - `ui[7:6]` → upper 2 bits

Both pixels are zero-extended to 7 bits before addition to prevent overflow.  
The sum is then right-shifted by 1 to divide by 2.

### Output

- The averaged pixel is driven on `uo[6:0]`
- `uo[7]` is always 0

### Handshake Signals

A ready/valid interface is provided:

- `uio[4]` → `valid_i`
- `uio[5]` → `ready_i`
- `uio[6]` → `ready_o`
- `uio[7]` → `valid_o`

Since the design is purely combinational:
- `valid_o = valid_i`
- `ready_o = ready_i`

This allows the module to be safely inserted into a streaming pipeline with backpressure support.

---

## How to test

1. Provide two 6-bit grayscale pixel values:
   - Place the left pixel on `ui[5:0]`
   - Place the right pixel across `uio[3:0]` and `ui[7:6]`

2. Assert:
   - `valid_i` (`uio[4]`) = 1
   - `ready_i` (`uio[5]`) = 1

3. Wait one clock cycle.

4. Read the output:
   - `uo[6:0]` should equal `(left + right) >> 1`

### Example

If:
- left = 20
- right = 30

Then:
- (20 + 30) >> 1 = 25


So `uo_out` should output `25`.

The provided cocotb testbench verifies multiple test cases including edge values (0 and 63).

---

## External hardware

None.

This design is fully self-contained and does not require any external hardware peripherals.

