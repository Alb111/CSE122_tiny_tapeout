/*
 * Copyright (c) 2024 Albert Felix
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  wire [6:0] left_pixel_greyscale_val, right_pixel_greyscale_val;
  wire valid_i, ready_o, ready_i, valid_o;

  // inputs
  assign left_pixel_greyscale_val  = {1'b0, ui_in[5:0]}; 
  assign right_pixel_greyscale_val = {1'b0, uio_in[3:0], ui_in[7:6]}; 
  assign valid_i = uio_in[4];
  assign ready_i = uio_in[5];

  // outputs
  assign uio_out[6] = ready_o;
  assign ready_o = ready_i;
  assign uio_out[7] = valid_o;
  assign valid_o = valid_i;

  assign uo_out = (left_pixel_greyscale_val + right_pixel_greyscale_val) >> 1;
  assign uio_oe  = 8'b11000000;

  // List all unused inputs to prevent warnings
  assign uio_out[5:0] = 6'd0; // unused
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
