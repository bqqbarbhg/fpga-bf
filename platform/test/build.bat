del /Q build
cmd /C "python brainfpga.py"
copy platform\test\* build
pushd build
iverilog -o brain test.v brain.v
vvp brain
popd