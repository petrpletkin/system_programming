FROM debian
COPY lab2.asm .
RUN apt update && apt install -y nasm build-essential gcc-multilib
RUN nasm -felf32 lab2.asm && gcc -m32 -no-pie lab2.o -o lab2
CMD ./lab2
