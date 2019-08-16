del /Q build
cmd /C "python brainfpga.py"
copy platform\tiny-bx\* build
pushd build
apio build && tinyprog -p hardware.bin
popd