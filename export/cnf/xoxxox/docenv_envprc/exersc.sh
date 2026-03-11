tmp=$(mktemp) || exit 1
cat | riscv64-linux-gnu-gcc -nostdlib -static -x assembler -o ${tmp} - && qemu-riscv64 ${tmp}
rm -f ${tmp}
