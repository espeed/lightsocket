LIBRARY_NAME = rexterCppClient
LIB_SRC_DIR  = ./src/$(LIBRARY_NAME)/
TEST_DIR  = ./src/test/
CXX          = g++
CPPFLAGS     = 
LIBS        := -lzmq -ljson
BUILD_DIR    = ./build/
INCLUDES     = -I/usr/local/include -I./$(LIB_SRC_DIR)
INSTALL_DIR  = /usr/local/

main: $(LIBRARY_NAME).so $(TEST_DIR)main.cpp
	$(CXX) $(INCLUDES) -o $(BUILD_DIR)main  $(TEST_DIR)main.cpp -L$(BUILD_DIR) -l$(LIBRARY_NAME) $(LIBS)

$(LIBRARY_NAME).so: $(LIB_SRC_DIR)/$(LIBRARY_NAME).cpp
	$(CXX) $(INCLUDES) -MMD -std=c++0x -pipe -fPIC -c $(LIB_SRC_DIR)/$(LIBRARY_NAME).cpp -o $(BUILD_DIR)$(LIBRARY_NAME).o $(LIBS)
	$(CXX) -shared  -Wl,-soname,$(BUILD_DIR)$(LIBRARY_NAME).so -o $(BUILD_DIR)$(LIBRARY_NAME).so $(BUILD_DIR)$(LIBRARY_NAME).o
	ln $(BUILD_DIR)$(LIBRARY_NAME).so $(BUILD_DIR)lib$(LIBRARY_NAME).so
	
clean:
	rm $(BUILD_DIR)$(LIBRARY_NAME).o $(BUILD_DIR)$(LIBRARY_NAME).d $(BUILD_DIR)$(LIBRARY_NAME).so $(BUILD_DIR)lib$(LIBRARY_NAME).so $(BUILD_DIR)main
	
install:
	sudo cp $(BUILD_DIR)$(LIBRARY_NAME).so $(BUILD_DIR)lib$(LIBRARY_NAME).so $(INSTALL_DIR)lib/
	sudo cp $(LIB_SRC_DIR)/$(LIBRARY_NAME).h $(INSTALL_DIR)include/