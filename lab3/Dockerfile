FROM debian
RUN apt update && apt install -y nasm build-essential gcc-multilib
COPY lab3_combine.cpp .
RUN g++ lab3_combine.cpp -o lab3_combine -static
CMD ./lab3_combine
