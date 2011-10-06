################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/main.cpp \
../src/rexterCppClient.cpp 

OBJS += \
./src/main.o \
./src/rexterCppClient.o 

CPP_DEPS += \
./src/main.d \
./src/rexterCppClient.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/usr/local/include -I/home/hermann-local/src/jsoncpp-src-0.5.0/include -I/home/hermann-local/src/cppzmq -O0 -g3 -Wall -c -fmessage-length=0 -std=c++0x -MMD -std=c++0x -pipe -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


